const { RekognitionClient, CreateCollectionCommand, IndexFacesCommand, SearchFacesByImageCommand, DeleteFacesCommand } = require('@aws-sdk/client-rekognition');
const logger = require('../utils/logger');

const PROVIDER = process.env.FACE_VERIFICATION_PROVIDER || 'local';

let rekognitionClient = null;

if (PROVIDER === 'rekognition') {
  rekognitionClient = new RekognitionClient({
    region: process.env.AWS_REGION || 'ap-south-1',
    ...(process.env.AWS_ACCESS_KEY_ID && {
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
      }
    })
  });
}

function collectionId(panchayatId) {
  return `egramsabha-${panchayatId}`;
}

async function ensureCollection(panchayatId) {
  try {
    await rekognitionClient.send(new CreateCollectionCommand({
      CollectionId: collectionId(panchayatId),
    }));
    logger.info(`[Rekognition] Created collection for panchayat ${panchayatId}`);
  } catch (err) {
    if (err.name === 'ResourceAlreadyExistsException') {
      // Collection already exists
      return;
    }
    throw err;
  }
}

async function indexFace(imageBuffer, panchayatId, userId) {
  if (!rekognitionClient) return null;

  await ensureCollection(panchayatId);

  const response = await rekognitionClient.send(new IndexFacesCommand({
    CollectionId: collectionId(panchayatId),
    Image: { Bytes: imageBuffer },
    ExternalImageId: userId.toString(),
    MaxFaces: 1,
    DetectionAttributes: ['DEFAULT'],
  }));

  const faceRecords = response.FaceRecords || [];
  if (faceRecords.length === 0) {
    logger.warn(`[Rekognition] No face detected for user ${userId}`);
    return null;
  }

  const faceId = faceRecords[0].Face.FaceId;
  logger.info(`[Rekognition] Indexed face ${faceId} for user ${userId}`);
  return faceId;
}

async function searchFace(imageBuffer, panchayatId, similarityThreshold = 90) {
  if (!rekognitionClient) return null;

  try {
    const response = await rekognitionClient.send(new SearchFacesByImageCommand({
      CollectionId: collectionId(panchayatId),
      Image: { Bytes: imageBuffer },
      MaxFaces: 1,
      FaceMatchThreshold: similarityThreshold,
    }));

    const matches = response.FaceMatches || [];
    if (matches.length === 0) {
      return null;
    }

    return {
      faceId: matches[0].Face.FaceId,
      externalImageId: matches[0].Face.ExternalImageId,
      similarity: matches[0].Similarity,
    };
  } catch (err) {
    if (err.name === 'ResourceNotFoundException') {
      logger.warn(`[Rekognition] Collection not found for panchayat ${panchayatId}`);
      return null;
    }
    throw err;
  }
}

async function deleteFace(panchayatId, faceId) {
  if (!rekognitionClient || !faceId) return;

  try {
    await rekognitionClient.send(new DeleteFacesCommand({
      CollectionId: collectionId(panchayatId),
      FaceIds: [faceId],
    }));
    logger.info(`[Rekognition] Deleted face ${faceId}`);
  } catch (err) {
    logger.error(`[Rekognition] Delete error: ${err.message}`);
  }
}

function isEnabled() {
  return PROVIDER === 'rekognition' && rekognitionClient !== null;
}

module.exports = { indexFace, searchFace, deleteFace, isEnabled };
