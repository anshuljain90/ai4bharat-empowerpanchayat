/**
 * Database configuration for MongoDB / Amazon DocumentDB.
 *
 * DocumentDB requires:
 *  - TLS connection with the AWS global-bundle.pem CA certificate
 *  - retryWrites=false (DocumentDB does not support retryable writes)
 *  - No $text indexes (removed from Panchayat model)
 *  - No GridFS (migrated to S3)
 *
 * Usage:
 *   const { getMongooseOptions, getConnectionUri } = require('./config/database');
 *   mongoose.connect(getConnectionUri(), getMongooseOptions());
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const logger = require('../utils/logger');

const CA_BUNDLE_URL = 'https://truststore.pki.rds.amazonaws.com/global/global-bundle.pem';
const CA_BUNDLE_PATH = path.join(__dirname, '..', 'certs', 'global-bundle.pem');

/**
 * Download the AWS RDS/DocumentDB CA bundle if not present.
 */
async function ensureCACertificate() {
  if (fs.existsSync(CA_BUNDLE_PATH)) {
    return CA_BUNDLE_PATH;
  }

  const certsDir = path.dirname(CA_BUNDLE_PATH);
  if (!fs.existsSync(certsDir)) {
    fs.mkdirSync(certsDir, { recursive: true });
  }

  return new Promise((resolve, reject) => {
    logger.info('[DB] Downloading AWS DocumentDB CA bundle...');
    const file = fs.createWriteStream(CA_BUNDLE_PATH);
    https.get(CA_BUNDLE_URL, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        logger.info('[DB] CA bundle downloaded successfully');
        resolve(CA_BUNDLE_PATH);
      });
    }).on('error', (err) => {
      fs.unlink(CA_BUNDLE_PATH, () => {});
      reject(err);
    });
  });
}

/**
 * Detect whether MONGODB_URI points to DocumentDB.
 */
function isDocumentDB(uri) {
  if (!uri) return false;
  return uri.includes('.docdb.amazonaws.com') ||
         uri.includes('docdb') ||
         process.env.USE_DOCUMENTDB === 'true';
}

/**
 * Get the connection URI, ensuring DocumentDB params are set.
 */
function getConnectionUri() {
  const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017/voter_registration';

  if (isDocumentDB(uri)) {
    // Ensure retryWrites=false for DocumentDB
    const url = new URL(uri);
    url.searchParams.set('retryWrites', 'false');
    if (!url.searchParams.has('tls')) {
      url.searchParams.set('tls', 'true');
    }
    logger.info('[DB] DocumentDB connection detected');
    return url.toString();
  }

  return uri;
}

/**
 * Get Mongoose connection options, including TLS for DocumentDB.
 */
async function getMongooseOptions() {
  const uri = process.env.MONGODB_URI || '';
  const options = {};

  if (isDocumentDB(uri)) {
    const caPath = await ensureCACertificate();
    options.tls = true;
    options.tlsCAFile = caPath;
    options.retryWrites = false;
    // DocumentDB does not support directConnection in replica sets
    logger.info('[DB] TLS enabled with AWS CA bundle for DocumentDB');
  }

  return options;
}

module.exports = { getMongooseOptions, getConnectionUri, isDocumentDB, ensureCACertificate };
