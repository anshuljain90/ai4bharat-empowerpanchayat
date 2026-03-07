const backend = process.env.STORAGE_BACKEND || 'gridfs';

if (backend === 's3') {
  module.exports = require('./s3Service');
} else if (backend === 'gridfs') {
  module.exports = require('./gridfsService');
} else {
  throw new Error(`Unknown STORAGE_BACKEND: ${backend}`);
}