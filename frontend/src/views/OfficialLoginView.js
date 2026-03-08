// File: frontend/src/views/OfficialLoginView.js
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation, Link as RouterLink } from 'react-router-dom';
import {
    Box,
    Container,
    Typography,
    Paper,
    Button,
    TextField,
    Alert,
    CircularProgress,
    Grid,
    useTheme,
    useMediaQuery,
    Link as MuiLink
} from '@mui/material';
import AccountBalanceIcon from '@mui/icons-material/AccountBalance';
import { useAuth } from '../utils/authContext';
import { useLanguage } from '../utils/LanguageContext';
import LanguageSwitcher from '../components/LanguageSwitcher';

const OfficialLoginView = () => {
    const { login, user, error: authError } = useAuth();
    const { strings } = useLanguage();
    const navigate = useNavigate();
    const location = useLocation();
    const theme = useTheme();
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const [formData, setFormData] = useState({
        username: '',
        password: ''
    });
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    // If user is already logged in as an official, redirect to dashboard
    useEffect(() => {
        if (user && ['SECRETARY', 'PRESIDENT', 'WARD_MEMBER', 'COMMITTEE_SECRETARY'].includes(user.role)) {
            const from = location.state?.from?.pathname;
            navigate(from || '/official/dashboard', { replace: true });
        }
    }, [user, navigate, location]);

    // Handle form input changes
    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({
            ...prev,
            [name]: value
        }));
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setLoading(true);

        if (!formData.username || !formData.password) {
            setError(strings.pleaseEnterBoth || 'Please enter both username and password');
            setLoading(false);
            return;
        }

        try {
            // Use the official-specific login function
            const success = await login(formData.username, formData.password, 'OFFICIAL');

            if (!success) {
                setError(strings.loginFailed || 'Login failed. Please try again.');
            }
            // Navigation will be handled by the useEffect hook when user state updates
        } catch (err) {
            setError(err.message || strings.loginFailed || 'Login failed. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <Box
            sx={{
                minHeight: '100vh',
                display: 'flex',
                flexDirection: 'column',
                backgroundImage: 'linear-gradient(rgba(255, 255, 255, 0.8), rgba(255, 255, 255, 0.8)), url("/assets/background-pattern.png")',
                backgroundSize: 'cover',
                backgroundAttachment: 'fixed'
            }}
        >
            {/* Header */}
            <Box
                sx={{
                    bgcolor: 'primary.main',
                    color: 'white',
                    py: 1,
                    px: 3,
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                }}
            >
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <AccountBalanceIcon sx={{ mr: 1 }} />
                    <Typography variant="h6" component="div">
                        {strings.gramSabhaManagement || 'Gram Sabha Management'}
                    </Typography>
                </Box>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    <LanguageSwitcher />
                </Box>
            </Box>

            <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center', py: 4 }}>
                <Container maxWidth="lg">
                    <Grid container spacing={0} sx={{ minHeight: isMobile ? 'auto' : 420, borderRadius: 2, overflow: 'hidden', boxShadow: 3 }}>
                        {/* Left Side - Description */}
                        {!isMobile && (
                            <Grid item md={5}>
                                <Box
                                    sx={{
                                        p: 5,
                                        height: '100%',
                                        bgcolor: 'primary.main',
                                        color: 'white',
                                        display: 'flex',
                                        flexDirection: 'column',
                                        justifyContent: 'center',
                                    }}
                                >
                                    <Typography variant="h4" component="h1" gutterBottom fontWeight="bold">
                                        {strings.officialPortal || 'Official Portal'}
                                    </Typography>
                                    <Typography variant="body1" paragraph sx={{ opacity: 0.9 }}>
                                        {strings.officialPortalDesc || 'This secure portal is designed for Panchayat officials to manage day-to-day operations.'}
                                    </Typography>
                                    <Typography variant="body1" paragraph sx={{ opacity: 0.9 }}>
                                        {strings.useOfficialCredentials || 'Use your official credentials to access the system and manage your panchayat activities.'}
                                    </Typography>
                                    <Box sx={{ mt: 3 }}>
                                        <Typography variant="subtitle1" gutterBottom fontWeight="bold">
                                            {strings.officialFeatures || 'Official Features:'}
                                        </Typography>
                                        <Box component="ul" sx={{ pl: 2, '& li': { mb: 0.5, opacity: 0.9 } }}>
                                            <li>{strings.managePanchayatDetails || 'Manage panchayat details and ward information'}</li>
                                            <li>{strings.trackCitizenIssues || 'Track and respond to citizen issues'}</li>
                                            <li>{strings.organizeGramSabha || 'Organize Gram Sabha meetings'}</li>
                                            <li>{strings.generateReports || 'Generate reports and analytics'}</li>
                                        </Box>
                                    </Box>
                                </Box>
                            </Grid>
                        )}

                        {/* Right Side - Login Form */}
                        <Grid item xs={12} md={7}>
                            <Box sx={{ p: isMobile ? 3 : 5, bgcolor: 'white', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                                <Box sx={{ maxWidth: 400, mx: 'auto', width: '100%' }}>
                                    <Box sx={{ textAlign: 'center', mb: 3 }}>
                                        <Typography variant="h5" component="h2" gutterBottom fontWeight="bold">
                                            {strings.officialLogin || 'Official Login'}
                                        </Typography>
                                        <Typography variant="body2" color="text.secondary">
                                            {strings.loginWithCredentials || 'Login with your official credentials'}
                                        </Typography>
                                    </Box>

                                    {(error || authError) && (
                                        <Alert severity="error" sx={{ mb: 3 }}>
                                            {error || authError}
                                        </Alert>
                                    )}

                                    <Box component="form" onSubmit={handleSubmit} noValidate>
                                        <TextField
                                            margin="normal"
                                            required
                                            fullWidth
                                            id="username"
                                            label={strings.username || 'Username'}
                                            name="username"
                                            autoComplete="username"
                                            autoFocus
                                            value={formData.username}
                                            onChange={handleChange}
                                            disabled={loading}
                                        />
                                        <TextField
                                            margin="normal"
                                            required
                                            fullWidth
                                            name="password"
                                            label={strings.password || 'Password'}
                                            type="password"
                                            id="password"
                                            autoComplete="current-password"
                                            value={formData.password}
                                            onChange={handleChange}
                                            disabled={loading}
                                        />

                                        <Button
                                            type="submit"
                                            fullWidth
                                            variant="contained"
                                            sx={{ mt: 3, mb: 2 }}
                                            disabled={loading}
                                        >
                                            {loading ? (
                                                <CircularProgress size={24} color="inherit" />
                                            ) : (
                                                strings.signIn || 'Sign In'
                                            )}
                                        </Button>

                                        <Grid container justifyContent="center">
                                            <Grid item>
                                                <MuiLink
                                                    component={RouterLink}
                                                    to="/official/forgot-password"
                                                    variant="body2"
                                                    underline="hover"
                                                >
                                                    {strings.forgotPassword || 'Forgot password?'}
                                                </MuiLink>
                                            </Grid>
                                        </Grid>
                                    </Box>
                                </Box>
                            </Box>
                        </Grid>
                    </Grid>
                </Container>
            </Box>

            {/* Footer */}
            <Box
                component="footer"
                sx={{
                    py: 2,
                    px: 3,
                    mt: 'auto',
                    backgroundColor: 'grey.200',
                    textAlign: 'center'
                }}
            >
                <Typography variant="body2" color="text.secondary">
                    &copy; {new Date().getFullYear()} {strings.gramSabhaManagementSystem || 'Gram Sabha Management System'}
                </Typography>
            </Box>
        </Box>
    );
};

export default OfficialLoginView;