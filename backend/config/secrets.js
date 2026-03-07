const { SecretsManagerClient, GetSecretValueCommand } = require('@aws-sdk/client-secrets-manager');

let secretsCache = null;

const SECRET_NAME = process.env.SECRETS_MANAGER_SECRET_NAME || 'egramsabha/prod';

async function loadSecrets() {
  // Skip if no AWS region configured or running in local dev
  if (!process.env.AWS_REGION && !process.env.AWS_ACCESS_KEY_ID) {
    console.log('[Secrets] No AWS credentials configured, using environment variables');
    return;
  }

  try {
    const client = new SecretsManagerClient({
      region: process.env.AWS_REGION || 'ap-south-1',
      ...(process.env.AWS_ACCESS_KEY_ID && {
        credentials: {
          accessKeyId: process.env.AWS_ACCESS_KEY_ID,
          secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
        }
      })
    });

    const response = await client.send(new GetSecretValueCommand({
      SecretId: SECRET_NAME,
    }));

    secretsCache = JSON.parse(response.SecretString);
    console.log('[Secrets] Loaded secrets from AWS Secrets Manager');
  } catch (error) {
    console.warn(`[Secrets] Failed to load from Secrets Manager (${error.message}), falling back to env vars`);
  }
}

function getSecret(key) {
  if (secretsCache && secretsCache[key]) {
    return secretsCache[key];
  }
  return process.env[key];
}

module.exports = { loadSecrets, getSecret };
