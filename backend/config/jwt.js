// File: backend/config/jwt.js (Updated with multi-user token support)
const jwt = require('jsonwebtoken');
const crypto = require('crypto');
const { getSecret } = require('./secrets');

// JWT Secret keys resolved lazily via Secrets Manager with env var fallback.
// These are functions, NOT constants — called at sign/verify time so that
// secrets loaded asynchronously by loadSecrets() are picked up.
const getAdminSecret = () => getSecret('JWT_ADMIN_SECRET') || 'admin-secret-key';
const getOfficialSecret = () => getSecret('JWT_OFFICIAL_SECRET') || 'official-secret-key';
const getCitizenSecret = () => getSecret('JWT_CITIZEN_SECRET') || 'citizen-secret-key';
const getRefreshSecret = () => getSecret('JWT_REFRESH_SECRET') || 'refresh-secret-key';

// Token expiration times
const JWT_ADMIN_EXPIRES_IN = '12h';
const JWT_OFFICIAL_EXPIRES_IN = '24h';
const JWT_CITIZEN_EXPIRES_IN = '72h';
const JWT_REFRESH_EXPIRES_IN = '7d';

function _resolveSecret(userType) {
    switch (userType) {
        case 'ADMIN':    return getAdminSecret();
        case 'OFFICIAL': return getOfficialSecret();
        case 'CITIZEN':  return getCitizenSecret();
        default:         return getOfficialSecret();
    }
}

function _resolveExpiry(userType) {
    switch (userType) {
        case 'ADMIN':    return JWT_ADMIN_EXPIRES_IN;
        case 'OFFICIAL': return JWT_OFFICIAL_EXPIRES_IN;
        case 'CITIZEN':  return JWT_CITIZEN_EXPIRES_IN;
        default:         return JWT_OFFICIAL_EXPIRES_IN;
    }
}

// Generate token based on user type
const generateToken = (payload, userType) => {
    const secret = _resolveSecret(userType);
    const expiresIn = _resolveExpiry(userType);
    return jwt.sign(payload, secret, { expiresIn });
};

// Verify token based on user type
const verifyToken = (token, userType) => {
    if (userType) {
        return jwt.verify(token, _resolveSecret(userType));
    }

    // Try all secrets if type not specified
    const secretGetters = [getAdminSecret, getOfficialSecret, getCitizenSecret];
    for (let i = 0; i < secretGetters.length; i++) {
        try {
            return jwt.verify(token, secretGetters[i]());
        } catch (e) {
            if (i === secretGetters.length - 1) throw new Error('Invalid token for any user type');
        }
    }
};

// Generate refresh token (common for all users)
const generateRefreshToken = (payload) => {
    return jwt.sign(payload, getRefreshSecret(), { expiresIn: JWT_REFRESH_EXPIRES_IN });
};

// Verify refresh token
const verifyRefreshToken = (token) => {
    return jwt.verify(token, getRefreshSecret());
};

// Legacy functions for backward compatibility
const JWT_EXPIRES_IN = '24h';

const generateLegacyToken = (payload) => {
    const secret = getSecret('JWT_SECRET') || getOfficialSecret();
    return jwt.sign(payload, secret, { expiresIn: JWT_EXPIRES_IN });
};

const verifyLegacyToken = (token) => {
    const secret = getSecret('JWT_SECRET') || getOfficialSecret();
    return jwt.verify(token, secret);
};

module.exports = {
    generateToken,
    verifyToken,
    generateRefreshToken,
    verifyRefreshToken,

    // Legacy — lazy getters (backward compat for code that reads these)
    get JWT_SECRET() { return getSecret('JWT_SECRET') || getOfficialSecret(); },
    get JWT_REFRESH_SECRET() { return getRefreshSecret(); },
    JWT_EXPIRES_IN,
    JWT_REFRESH_EXPIRES_IN,
    generateLegacyToken,
    verifyLegacyToken
};
