const { SNSClient, PublishCommand } = require('@aws-sdk/client-sns');
const logger = require('../utils/logger');

const SNS_ENABLED = process.env.SNS_ENABLED === 'true';

let snsClient = null;

if (SNS_ENABLED) {
  snsClient = new SNSClient({
    region: process.env.AWS_REGION || 'ap-south-1',
    ...(process.env.AWS_ACCESS_KEY_ID && {
      credentials: {
        accessKeyId: process.env.AWS_ACCESS_KEY_ID,
        secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
      }
    })
  });
}

async function sendSMS(phoneNumber, message) {
  if (!snsClient) {
    logger.info(`[SNS] Disabled. Would send to ${phoneNumber}: ${message}`);
    return null;
  }

  // Ensure Indian phone number format (+91...)
  let formattedNumber = phoneNumber.replace(/\s+/g, '');
  if (!formattedNumber.startsWith('+')) {
    if (formattedNumber.startsWith('91')) {
      formattedNumber = '+' + formattedNumber;
    } else {
      formattedNumber = '+91' + formattedNumber;
    }
  }

  try {
    const response = await snsClient.send(new PublishCommand({
      PhoneNumber: formattedNumber,
      Message: message,
      MessageAttributes: {
        'AWS.SNS.SMS.SMSType': {
          DataType: 'String',
          StringValue: 'Transactional',
        },
        'AWS.SNS.SMS.SenderID': {
          DataType: 'String',
          StringValue: 'eGramSbha',
        },
      },
    }));

    logger.info(`[SNS] SMS sent to ${formattedNumber}: ${response.MessageId}`);
    return response.MessageId;
  } catch (error) {
    logger.error(`[SNS] Failed to send SMS to ${formattedNumber}: ${error.message}`);
    throw error;
  }
}

async function notifyGramSabhaScheduled(panchayatName, dateStr, citizens) {
  if (!SNS_ENABLED) return;

  const message = `eGramSabha: Gram Sabha meeting scheduled for ${panchayatName} on ${dateStr}. Please join to raise your voice. - eGramSabha Platform`;

  const results = [];
  for (const citizen of citizens) {
    if (citizen.mobileNumber) {
      try {
        const messageId = await sendSMS(citizen.mobileNumber, message);
        results.push({ userId: citizen._id, status: 'sent', messageId });
      } catch {
        results.push({ userId: citizen._id, status: 'failed' });
      }
    }
  }
  return results;
}

async function notifyIssueStatusChange(phoneNumber, issueText, newStatus) {
  if (!SNS_ENABLED || !phoneNumber) return;

  const statusMessages = {
    PICKED_IN_AGENDA: 'has been picked for the next Gram Sabha agenda',
    DISCUSSED_IN_GRAM_SABHA: 'was discussed in the Gram Sabha',
    RESOLVED: 'has been resolved',
    TRANSFERRED: 'has been transferred to the relevant department',
  };

  const statusMsg = statusMessages[newStatus] || `status updated to ${newStatus}`;
  const message = `eGramSabha: Your issue "${issueText?.substring(0, 50)}..." ${statusMsg}. - eGramSabha Platform`;

  return sendSMS(phoneNumber, message);
}

function isEnabled() {
  return SNS_ENABLED && snsClient !== null;
}

module.exports = { sendSMS, notifyGramSabhaScheduled, notifyIssueStatusChange, isEnabled };
