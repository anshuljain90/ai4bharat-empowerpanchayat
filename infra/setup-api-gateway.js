/**
 * API Gateway Setup Script for eGramSabha
 *
 * Creates a REST API Gateway that fronts ALL backend traffic:
 * - HTTP_PROXY integration to EC2 Nginx (which routes /api/* and /mom-api/*)
 * - Usage plan with throttling (100 req/sec, 200 burst)
 * - API key for the demo
 * - CloudWatch access/execution logging
 *
 * Architecture:
 *   Browser → API Gateway → Nginx (EC2) → Node.js :5000 (/api/*)
 *                                        → FastAPI :8000 (/mom-api/*)
 *
 * Usage:
 *   node infra/setup-api-gateway.js --ec2-url https://<EC2_IP>
 *
 * Prerequisites:
 *   npm install @aws-sdk/client-api-gateway
 *   AWS credentials configured (env vars or IAM role)
 */

const {
  APIGatewayClient,
  CreateRestApiCommand,
  GetResourcesCommand,
  CreateResourceCommand,
  PutMethodCommand,
  PutIntegrationCommand,
  PutMethodResponseCommand,
  PutIntegrationResponseCommand,
  CreateDeploymentCommand,
  CreateStageCommand,
  CreateUsagePlanCommand,
  CreateUsagePlanKeyCommand,
  CreateApiKeyCommand,
  UpdateStageCommand,
  GetRestApisCommand,
} = require("@aws-sdk/client-api-gateway");

const REGION = process.env.AWS_REGION || "ap-south-1";
const API_NAME = "eGramSabha-MOM-API";
const STAGE_NAME = "prod";

const client = new APIGatewayClient({
  region: REGION,
  ...(process.env.AWS_ACCESS_KEY_ID && {
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    },
  }),
});

async function findExistingApi() {
  const apis = await client.send(new GetRestApisCommand({ limit: 500 }));
  return (apis.items || []).find((a) => a.name === API_NAME);
}

async function createRestApi(ec2Url) {
  // Check if API already exists
  const existing = await findExistingApi();
  if (existing) {
    console.log(`API already exists: ${existing.id} — ${existing.name}`);
    return existing.id;
  }

  const api = await client.send(
    new CreateRestApiCommand({
      name: API_NAME,
      description:
        "eGramSabha MOM API — managed gateway for transcription, MOM generation, agenda, TTS, and analysis endpoints",
      endpointConfiguration: { types: ["REGIONAL"] },
    })
  );
  console.log(`Created REST API: ${api.id}`);
  return api.id;
}

async function getRootResourceId(apiId) {
  const resources = await client.send(
    new GetResourcesCommand({ restApiId: apiId })
  );
  const root = resources.items.find((r) => r.path === "/");
  return root.id;
}

async function createProxyResource(apiId, parentId) {
  const resource = await client.send(
    new CreateResourceCommand({
      restApiId: apiId,
      parentId: parentId,
      pathPart: "{proxy+}",
    })
  );
  console.log(`Created proxy resource: ${resource.id}`);
  return resource.id;
}

async function setupProxyMethod(apiId, resourceId, ec2Url) {
  // ANY method with API key required
  await client.send(
    new PutMethodCommand({
      restApiId: apiId,
      resourceId: resourceId,
      httpMethod: "ANY",
      authorizationType: "NONE",
      apiKeyRequired: true,
      requestParameters: {
        "method.request.path.proxy": true,
      },
    })
  );

  // HTTP_PROXY integration
  await client.send(
    new PutIntegrationCommand({
      restApiId: apiId,
      resourceId: resourceId,
      httpMethod: "ANY",
      type: "HTTP_PROXY",
      integrationHttpMethod: "ANY",
      uri: `${ec2Url}/{proxy}`,
      requestParameters: {
        "integration.request.path.proxy": "method.request.path.proxy",
      },
      connectionType: "INTERNET",
      timeoutInMillis: 29000,
    })
  );

  console.log(`Configured ANY {proxy+} → ${ec2Url}/{proxy}`);
}

async function deployApi(apiId) {
  const deployment = await client.send(
    new CreateDeploymentCommand({
      restApiId: apiId,
      description: "Initial deployment",
    })
  );

  try {
    await client.send(
      new CreateStageCommand({
        restApiId: apiId,
        stageName: STAGE_NAME,
        deploymentId: deployment.id,
        description: "Production stage",
        cacheClusterEnabled: false, // Enable if needed ($0.02/hr for 0.5GB)
        tracingEnabled: true, // X-Ray tracing
      })
    );
  } catch (e) {
    if (e.name === "ConflictException") {
      // Stage already exists, just update deployment
      await client.send(
        new UpdateStageCommand({
          restApiId: apiId,
          stageName: STAGE_NAME,
          patchOperations: [
            { op: "replace", path: "/deploymentId", value: deployment.id },
          ],
        })
      );
    } else {
      throw e;
    }
  }

  // Enable CloudWatch logging on the stage
  try {
    await client.send(
      new UpdateStageCommand({
        restApiId: apiId,
        stageName: STAGE_NAME,
        patchOperations: [
          { op: "replace", path: "/*/*/logging/loglevel", value: "INFO" },
          { op: "replace", path: "/*/*/metrics/enabled", value: "true" },
          {
            op: "replace",
            path: "/*/*/throttling/rateLimit",
            value: "100",
          },
          {
            op: "replace",
            path: "/*/*/throttling/burstLimit",
            value: "200",
          },
        ],
      })
    );
  } catch (e) {
    console.warn("Could not configure stage settings:", e.message);
  }

  console.log(`Deployed to stage: ${STAGE_NAME}`);
  return deployment.id;
}

async function createUsagePlanAndKey(apiId) {
  // Create usage plan
  const plan = await client.send(
    new CreateUsagePlanCommand({
      name: "eGramSabha-Standard",
      description: "Standard usage plan with throttling for panchayat clients",
      throttle: {
        rateLimit: 100, // 100 requests/second
        burstLimit: 200,
      },
      quota: {
        limit: 100000, // 100K requests/day for demo
        period: "DAY",
      },
      apiStages: [{ apiId: apiId, stage: STAGE_NAME }],
    })
  );
  console.log(`Created usage plan: ${plan.id}`);

  // Create API key
  const apiKey = await client.send(
    new CreateApiKeyCommand({
      name: "eGramSabha-Demo-Key",
      description: "Demo API key for hackathon",
      enabled: true,
    })
  );
  console.log(`Created API key: ${apiKey.id} (value: ${apiKey.value})`);

  // Associate key with plan
  await client.send(
    new CreateUsagePlanKeyCommand({
      usagePlanId: plan.id,
      keyId: apiKey.id,
      keyType: "API_KEY",
    })
  );

  return { planId: plan.id, apiKeyId: apiKey.id, apiKeyValue: apiKey.value };
}

async function main() {
  const args = process.argv.slice(2);
  const ec2UrlIdx = args.indexOf("--ec2-url");
  if (ec2UrlIdx === -1 || !args[ec2UrlIdx + 1]) {
    console.error(
      "Usage: node infra/setup-api-gateway.js --ec2-url https://<EC2_IP>"
    );
    console.error(
      "  The EC2 URL should point to Nginx (HTTPS). API Gateway will proxy all paths to Nginx."
    );
    process.exit(1);
  }
  const ec2Url = args[ec2UrlIdx + 1].replace(/\/$/, "");

  console.log("=== eGramSabha API Gateway Setup ===");
  console.log(`Region: ${REGION}`);
  console.log(`Target: ${ec2Url}`);
  console.log("");

  const apiId = await createRestApi(ec2Url);
  const rootId = await getRootResourceId(apiId);
  const proxyResourceId = await createProxyResource(apiId, rootId);
  await setupProxyMethod(apiId, proxyResourceId, ec2Url);
  await deployApi(apiId);
  const { apiKeyValue } = await createUsagePlanAndKey(apiId);

  const invokeUrl = `https://${apiId}.execute-api.${REGION}.amazonaws.com/${STAGE_NAME}`;

  console.log("");
  console.log("=== Setup Complete ===");
  console.log(`API Gateway URL: ${invokeUrl}`);
  console.log(`API Key:         ${apiKeyValue}`);
  console.log("");
  console.log("Set in .env.production:");
  console.log(`  API_GATEWAY_URL=${invokeUrl}`);
  console.log(`  API_GATEWAY_API_KEY=${apiKeyValue}`);
  console.log("");
  console.log("Test:");
  console.log(
    `  curl -H "x-api-key: ${apiKeyValue}" ${invokeUrl}/health`
  );
}

main().catch((err) => {
  console.error("Setup failed:", err);
  process.exit(1);
});
