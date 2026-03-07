const winston = require('winston');

const transports = [
  new winston.transports.Console({
    format: winston.format.combine(
      winston.format.colorize(),
      winston.format.simple()
    )
  })
];

// Add CloudWatch transport if configured
if (process.env.AWS_REGION || process.env.AWS_ACCESS_KEY_ID) {
  try {
    const WinstonCloudWatch = require('winston-cloudwatch');
    const cwTransport = new WinstonCloudWatch({
      logGroupName: process.env.CLOUDWATCH_LOG_GROUP || '/egramsabha/backend',
      logStreamName: `${process.env.HOSTNAME || 'backend'}-${new Date().toISOString().split('T')[0]}`,
      awsRegion: process.env.AWS_REGION || 'ap-south-1',
      ...(process.env.AWS_ACCESS_KEY_ID && {
        awsAccessKeyId: process.env.AWS_ACCESS_KEY_ID,
        awsSecretKey: process.env.AWS_SECRET_ACCESS_KEY,
      }),
      jsonMessage: true,
      retentionInDays: 30,
      messageFormatter: ({ level, message, ...meta }) => {
        return JSON.stringify({ level, message, timestamp: new Date().toISOString(), ...meta });
      }
    });
    let cwErrorLogged = false;
    cwTransport.on('error', (err) => {
      if (!cwErrorLogged) {
        cwErrorLogged = true;
        console.warn(`[Logger] CloudWatch disabled: ${err.message}`);
        cwTransport.enabled = false;
      }
    });
    transports.push(cwTransport);
    console.log('[Logger] CloudWatch transport enabled');
  } catch (error) {
    console.warn('[Logger] CloudWatch transport not available:', error.message);
  }
}

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || 'info',
  format: winston.format.combine(
    winston.format.timestamp(),
    winston.format.errors({ stack: true }),
    winston.format.json()
  ),
  defaultMeta: { service: 'egramsabha-backend' },
  transports
});

// Morgan stream for HTTP request logging
logger.stream = {
  write: (message) => logger.info(message.trim())
};

module.exports = logger;
