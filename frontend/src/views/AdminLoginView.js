// File: frontend/src/views/AdminLoginView.js (Updated)
import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
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
import GroupIcon from '@mui/icons-material/Group';
import PersonIcon from '@mui/icons-material/Person';
import { useAuth } from '../utils/authContext';
import { Link } from 'react-router-dom';

const AdminLoginView = () => {
    const { login, user, error: authError } = useAuth();
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

    // If user is already logged in, redirect to appropriate dashboard
    useEffect(() => {
        if (user) {
            const from = location.state?.from?.pathname;
            if (from) {
                navigate(from, { replace: true });
            } else {
                // Navigate based on role
                if (user.role === 'ADMIN') {
                    navigate('/admin', { replace: true });
                } else {
                    navigate('/official/dashboard', { replace: true });
                }
            }
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
            setError('Please enter both username and password');
            setLoading(false);
            return;
        }

        try {
            // Use the adminLogin function from your updated auth context
            await login(formData.username, formData.password, 'ADMIN');

            // Navigation will be handled by the useEffect hook when user state updates
        } catch (err) {
            setError(err.message || 'Login failed. Please try again.');
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
                    bgcolor: 'primary.dark',
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
                        Gram Sabha Management
                    </Typography>
                </Box>
                <Box>
                    <Button
                        component={Link}
                        to="/login/official"
                        variant="outlined"
                        color="inherit"
                        size="small"
                        startIcon={<GroupIcon />}
                        sx={{
                            mr: 1,
                            borderColor: 'rgba(255,255,255,0.5)',
                            '&:hover': {
                                borderColor: 'white',
                                backgroundColor: 'rgba(255,255,255,0.1)'
                            }
                        }}
                    >
                        Official Portal
                    </Button>
                    <Button
                        component={Link}
                        to="/"
                        variant="outlined"
                        color="inherit"
                        size="small"
                        startIcon={<PersonIcon />}
                        sx={{
                            borderColor: 'rgba(255,255,255,0.5)',
                            '&:hover': {
                                borderColor: 'white',
                                backgroundColor: 'rgba(255,255,255,0.1)'
                            }
                        }}
                    >
                        Citizen Portal
                    </Button>
                </Box>
            </Box>

            <Container maxWidth="lg" sx={{ flexGrow: 1, display: 'flex', py: 4 }}>
                <Grid container spacing={4} alignItems="center" justifyContent="center">
                    {/* Left Side - Description */}
                    {!isMobile && (
                        <Grid item xs={12} md={6}>
                            <Paper
                                elevation={2}
                                sx={{
                                    p: 4,
                                    height: '100%',
                                    bgcolor: 'primary.dark',
                                    color: 'white'
                                }}
                            >
                                <Typography variant="h4" component="h1" gutterBottom>
                                    System Administration
                                </Typography>
                                <Typography variant="body1" paragraph>
                                    This secure portal is designed for system administrators to manage the entire Gram Sabha Management platform.
                                </Typography>
                                <Typography variant="body1" paragraph>
                                    Use your admin credentials to access system-wide configurations and management tools.
                                </Typography>
                                <Box sx={{ mt: 4 }}>
                                    <Typography variant="subtitle1" gutterBottom fontWeight="bold">
                                        Admin Features:
                                    </Typography>
                                    <ul>
                                        <li>Manage panchayats and officials</li>
                                        <li>System-wide configurations and settings</li>
                                        <li>User management and security controls</li>
                                        <li>Advanced analytics and reporting</li>
                                    </ul>
                                </Box>
                            </Paper>
                        </Grid>
                    )}

                    {/* Right Side - Login Form */}
                    <Grid item xs={12} md={6}>
                        <Paper elevation={3} sx={{ p: 4, borderRadius: 2 }}>
                            <Box sx={{ textAlign: 'center', mb: 3 }}>
                                <Typography variant="h5" component="h2" gutterBottom>
                                    Administrator Login
                                </Typography>
                                <Typography variant="body2" color="text.secondary">
                                    Login with your admin credentials
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
                                    label="Username"
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
                                    label="Password"
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
                                    color="primary"
                                    sx={{ mt: 3, mb: 2, bgcolor: 'primary.dark' }}
                                    disabled={loading}
                                >
                                    {loading ? (
                                        <CircularProgress size={24} color="inherit" />
                                    ) : (
                                        'Sign In'
                                    )}
                                </Button>

                                <Grid container justifyContent="center">
                                    <Grid item>
                                        <MuiLink
                                            component={Link}
                                            to="/forgot-password"
                                            variant="body2"
                                            underline="hover"
                                        >
                                            Forgot password?
                                        </MuiLink>
                                    </Grid>
                                </Grid>
                            </Box>
                        </Paper>
                    </Grid>
                </Grid>
            </Container>

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
                    &copy; {new Date().getFullYear()} Gram Sabha Management System
                </Typography>
            </Box>
        </Box>
    );
};

export default AdminLoginView;