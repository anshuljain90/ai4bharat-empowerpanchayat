const { S3Client, PutObjectCommand, GetObjectCommand, DeleteObjectCommand } = require('@aws-sdk/client-s3');
const { v4: uuidv4 } = require('uuid');

const s3Client = new S3Client({
  region: process.env.AWS_REGION || 'ap-south-1',
  ...(process.env.AWS_ACCESS_KEY_ID && {
    credentials: {
      accessKeyId: process.env.AWS_ACCESS_KEY_ID,
      secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    }
  })
});

const BUCKET = process.env.S3_BUCKET || 'egramsabha-assets';

function getPrefix(metadata) {
  if (metadata?.type === 'thumbnail') return 'thumbnails';
  if (metadata?.type === 'letterhead') return 'letterheads';
  if (metadata?.type === 'attachment') return 'attachments';
  return 'faces';
}

module.exports = {
  async uploadImage(buffer, filename, metadata = {}) {
    const prefix = getPrefix(metadata);
    const panchayatId = metadata.panchayatId || 'unknown';
    const key = `${prefix}/${panchayatId}/${uuidv4()}_${filename}`;

    await s3Client.send(new PutObjectCommand({
      Bucket: BUCKET,
      Key: key,
      Body: buffer,
      ContentType: metadata.contentType || 'image/jpeg',
      StorageClass: 'INTELLIGENT_TIERING',
      Metadata: {
        userId: metadata.userId?.toString() || '',
        voterId: metadata.voterId || '',
        panchayatId: panchayatId.toString(),
        type: metadata.type || 'profile',
        ...(metadata.originalImageId && { originalImageId: metadata.originalImageId.toString() })
      }
    }));

    // Return the S3 key as the file ID (string instead of ObjectId)
    return key;
  },

  async getImageStream(fileId) {
    const response = await s3Client.send(new GetObjectCommand({
      Bucket: BUCKET,
      Key: fileId,
    }));
    return response.Body;
  },

  async deleteImage(fileId) {
    await s3Client.send(new DeleteObjectCommand({
      Bucket: BUCKET,
      Key: fileId,
    }));
  }
};
