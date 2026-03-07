/**
 * CloudFront Distribution Setup for eGramSabha
 *
 * Creates a CloudFront distribution in front of the S3 assets bucket
 * for low-latency delivery of face images, TTS audio cache, and
 * static attachments across India's 13 edge locations.
 *
 * Usage:
 *   node infra/setup-cloudfront.js
 *
 * Prerequisites:
 *   npm install @aws-sdk/client-cloudfront
 *   S3 bucket (egramsabha-assets) must already exist
 */

const {
  CloudFrontClient,
  CreateDistributionCommand,
  ListDistributionsCommand,
} = require("@aws-sdk/client-cloudfront");

const REGION = process.env.AWS_REGION || "ap-south-1";
const S3_BUCKET = process.env.S3_BUCKET || "egramsabha-assets";
const S3_ORIGIN = `${S3_BUCKET}.s3.${REGION}.amazonaws.com`;

const client = new CloudFrontClient({
  region: "us-east-1", // CloudFront is a global service, managed from us-east-1
  ...(process.env.AWS_ACCESS_KEY_ID && {
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    },
  }),
});

async function findExistingDistribution() {
  const result = await client.send(new ListDistributionsCommand({}));
  const items = result.DistributionList?.Items || [];
  return items.find((d) =>
    d.Origins?.Items?.some((o) => o.DomainName === S3_ORIGIN)
  );
}

async function createDistribution() {
  const existing = await findExistingDistribution();
  if (existing) {
    console.log(`Distribution already exists: ${existing.Id}`);
    console.log(`Domain: ${existing.DomainName}`);
    return existing;
  }

  const callerRef = `egramsabha-${Date.now()}`;

  const result = await client.send(
    new CreateDistributionCommand({
      DistributionConfig: {
        CallerReference: callerRef,
        Comment: "eGramSabha - S3 assets CDN (faces, TTS cache, attachments)",
        Enabled: true,
        Origins: {
          Quantity: 1,
          Items: [
            {
              Id: "S3-egramsabha-assets",
              DomainName: S3_ORIGIN,
              S3OriginConfig: {
                OriginAccessIdentity: "",
              },
            },
          ],
        },
        DefaultCacheBehavior: {
          TargetOriginId: "S3-egramsabha-assets",
          ViewerProtocolPolicy: "redirect-to-https",
          AllowedMethods: {
            Quantity: 2,
            Items: ["GET", "HEAD"],
          },
          CachedMethods: {
            Quantity: 2,
            Items: ["GET", "HEAD"],
          },
          ForwardedValues: {
            QueryString: false,
            Cookies: { Forward: "none" },
          },
          MinTTL: 0,
          DefaultTTL: 86400, // 1 day
          MaxTTL: 31536000, // 1 year
          Compress: true,
        },
        PriceClass: "PriceClass_200", // Includes India edge locations
        HttpVersion: "http2",
        IsIPV6Enabled: true,
      },
    })
  );

  console.log(`Created distribution: ${result.Distribution.Id}`);
  console.log(`Domain: ${result.Distribution.DomainName}`);
  console.log(`Status: ${result.Distribution.Status}`);
  return result.Distribution;
}

async function main() {
  console.log("=== eGramSabha CloudFront Setup ===");
  console.log(`S3 Origin: ${S3_ORIGIN}`);
  console.log("");

  const dist = await createDistribution();
  const domain = dist.DomainName || dist.domainName;

  console.log("");
  console.log("=== Setup Complete ===");
  console.log(`CloudFront Domain: https://${domain}`);
  console.log("");
  console.log("TTS cache URL example:");
  console.log(`  https://${domain}/tts-cache/hi/<hash>.mp3`);
  console.log("Face image URL example:");
  console.log(`  https://${domain}/faces/<panchayatId>/<uuid>_image.jpg`);
}

main().catch((err) => {
  console.error("Setup failed:", err);
  process.exit(1);
});
