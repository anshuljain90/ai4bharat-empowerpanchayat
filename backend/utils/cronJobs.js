const cron = require('node-cron');
const axios = require('axios');
const { updateAllMeetingStatuses } = require('./meetingUtils');
const Issue = require('../models/Issue');
const transcriptionService = require('../services/transcriptionService');
const { initiateSummaryGeneration, fetchSummaryResults, retryFailedSummaryRequests } = require('./summaryCronJobs');
const { agendaTranslationCron } = require('./agendaTranslationCron');
const logger = require('./logger');

const VIDEO_MOM_URL = process.env.VIDEO_MOM_BACKEND_URL || 'http://video-mom-backend:8000';

// Check transcription status every 5 minutes
const checkTranscriptionStatus = cron.schedule('*/1 * * * *', async () => {
    try {
        // Find all issues with processing transcription
        const processingIssues = await Issue.find({
            'transcription.status': 'PROCESSING',
            'transcription.requestId': { $exists: true, $ne: null }
        });

        for (const issue of processingIssues) {
            try {
                const statusResult = await transcriptionService.checkTranscriptionStatus(issue.transcription.requestId);
                
                if (statusResult.status === 'completed' && statusResult.transcription) {
                    // Update issue with completed transcription
                    issue.transcription.status = 'COMPLETED';
                    issue.transcription.text = statusResult.transcription;
                    issue.transcription.originalTranscription = statusResult.originalTranscription;
                    issue.transcription.enhancedEnglishTranscription = statusResult.enhancedEnglishTranscription;
                    issue.transcription.enhancedHindiTranscription = statusResult.enhancedHindiTranscription;
                    issue.transcription.processingMode = statusResult.processingMode;
                    issue.transcription.transcriptionProvider = statusResult.transcriptionProvider;
                    issue.transcription.providerInfo = statusResult.providerInfo;
                    issue.transcription.llmEnhancementStatus = statusResult.llmEnhancementStatus;
                    issue.transcription.completedAt = new Date();
                    issue.transcription.lastError = null;
                    await issue.save();

                    // Trigger Comprehend analysis on completed transcription
                    try {
                        const analysisText = statusResult.enhancedEnglishTranscription || statusResult.transcription;
                        if (analysisText && analysisText.trim()) {
                            const comprehendRes = await axios.post(`${VIDEO_MOM_URL}/analyze/issue`, {
                                text: analysisText,
                                language: 'en'
                            });
                            if (comprehendRes.data && comprehendRes.data.sentiment) {
                                issue.sentiment = comprehendRes.data.sentiment;
                                issue.keyPhrases = comprehendRes.data.keyPhrases || [];
                                if (comprehendRes.data.suggestedPriority === 'URGENT' && issue.priority !== 'URGENT') {
                                    issue.priority = 'URGENT';
                                }
                                await issue.save();
                            }
                        }
                    } catch (comprehendErr) {
                        // Non-blocking — analysis failure shouldn't affect transcription flow
                    }

                } else if (statusResult.status === 'failed') {
                    // Update issue with failed status
                    issue.transcription.status = 'FAILED';
                    issue.transcription.lastError = statusResult.error || 'Transcription failed';
                    await issue.save();
                    
                }
                
            } catch (error) {
            }
        }
        
    } catch (error) {
    }
});

// Retry failed transcriptions every 15 minutes
const retryFailedTranscriptions = cron.schedule('*/1 * * * *', async () => {
    try {
        // Find all issues with failed transcription and retry count < 3
        const failedIssues = await Issue.find({
            'transcription.status': 'FAILED',
            'transcription.retryCount': { $lt: 3 },
            'transcription.requestId': { $exists: true, $ne: null }
        });

        for (const issue of failedIssues) {
            try {
                // Get audio attachment
                const audioAttachment = issue.attachments.find(att => 
                    att.mimeType.startsWith('audio/')
                );

                if (!audioAttachment) {
                    continue;
                }

                // Get language from panchayat
                const language = await transcriptionService.getPanchayatLanguage(issue.panchayatId);
                
                // Retry transcription
                const transcriptionResponse = await transcriptionService.initiateTranscription(
                    audioAttachment.attachment,
                    language,
                    issue._id
                );
                
                // Update issue
                issue.transcription.requestId = transcriptionResponse.request_id;
                issue.transcription.status = 'PROCESSING';
                issue.transcription.language = language;
                issue.transcription.requestedAt = new Date();
                issue.transcription.lastError = null;
                await issue.save();
                
            } catch (error) {
                // Update issue with new error
                issue.transcription.retryCount += 1;
                issue.transcription.lastError = error.message;
                await issue.save();
            }
        }
        
    } catch (error) {
    }
});

// Retry transcription initiation for issues that failed to get requestId
const retryTranscriptionInitiation = cron.schedule('*/1 * * * *', async () => {
    try {
        // Find all issues with audio attachments but no transcription.requestId (failed initial attempts)
        const issuesWithAudio = await Issue.find({
            'attachments': {
                $elemMatch: {
                    'mimeType': { $regex: /^audio\// }
                }
            },
            $or: [
                { 'transcription.requestId': { $exists: false } },
                { 'transcription.requestId': null },
                { 'transcription.status': { $exists: false } },
                { 'transcription.status': null }
            ]
        });

        for (const issue of issuesWithAudio) {
            try {
                // Get audio attachment
                const audioAttachment = issue.attachments.find(att => 
                    att.mimeType.startsWith('audio/')
                );

                if (!audioAttachment) {
                    continue;
                }

                // Get language from panchayat
                const language = await transcriptionService.getPanchayatLanguage(issue.panchayatId);
                
                // Initialize transcription
                const transcriptionResponse = await transcriptionService.initiateTranscription(
                    audioAttachment.attachment,
                    language,
                    issue._id
                );
                
                // Update issue with transcription data
                if (!issue.transcription) {
                    issue.transcription = {};
                }
                issue.transcription.requestId = transcriptionResponse.request_id;
                issue.transcription.status = 'PROCESSING';
                issue.transcription.language = language;
                issue.transcription.requestedAt = new Date();
                issue.transcription.retryCount = 0;
                issue.transcription.lastError = null;
                await issue.save();
                
            } catch (error) {
                // Initialize transcription object if it doesn't exist
                if (!issue.transcription) {
                    issue.transcription = {};
                }
                
                // Update issue with error
                issue.transcription.status = 'FAILED';
                issue.transcription.retryCount = (issue.transcription.retryCount || 0) + 1;
                issue.transcription.lastError = error.message;
                await issue.save();
            }
        }
        
    } catch (error) {
    }
});

// Start the cron jobs
const startCronJobs = () => {
    agendaTranslationCron.start();
    checkTranscriptionStatus.start();
    retryFailedTranscriptions.start();
    retryTranscriptionInitiation.start();
    initiateSummaryGeneration.start();
    fetchSummaryResults.start();
    retryFailedSummaryRequests.start();
};

// Stop the cron jobs
const stopCronJobs = () => {
    agendaTranslationCron.stop();
    checkTranscriptionStatus.stop();
    retryFailedTranscriptions.stop();
    retryTranscriptionInitiation.stop();
    initiateSummaryGeneration.stop();
    fetchSummaryResults.stop();
    retryFailedSummaryRequests.stop();
};

module.exports = {
    startCronJobs,
    stopCronJobs,
    checkTranscriptionStatus,
    retryFailedTranscriptions,
    retryTranscriptionInitiation,
    initiateSummaryGeneration,
    fetchSummaryResults,
    retryFailedSummaryRequests
};
