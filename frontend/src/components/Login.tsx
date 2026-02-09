import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Auth.css';

interface LoginProps {
    onSwitchToSignup: () => void;
    onBackToLanding?: () => void;
}

export const Login: React.FC<LoginProps> = ({ onSwitchToSignup, onBackToLanding }) => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const { login, loginWithGoogle } = useAuth();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!email || !password) {
            setError('Please fill in all fields');
            return;
        }

        try {
            setError('');
            setLoading(true);
            await login(email, password);
        } catch (err: any) {
            setError(err.message || 'Failed to log in');
        } finally {
            setLoading(false);
        }
    };

    const handleGoogleSignIn = async () => {
        try {
            setError('');
            setLoading(true);
            await loginWithGoogle();
        } catch (err: any) {
            setError(err.message || 'Failed to sign in with Google');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            {onBackToLanding && (
                <button type="button" className="auth-back-link" onClick={onBackToLanding}>
                    Back
                </button>
            )}
            <div className="auth-background-blurs">
                <div className="auth-blur-circle auth-blur-cyan"></div>
                <div className="auth-blur-circle auth-blur-purple"></div>
                <div className="auth-blur-circle auth-blur-blue"></div>
                <div className="auth-blur-circle auth-blur-violet"></div>
                <div className="auth-blur-circle auth-blur-indigo"></div>
                <div className="auth-speck auth-speck-1"></div>
                <div className="auth-speck auth-speck-2"></div>
                <div className="auth-speck auth-speck-3"></div>
                <div className="auth-speck auth-speck-4"></div>
                <div className="auth-speck auth-speck-5"></div>
                <div className="auth-speck auth-speck-6"></div>
                <div className="auth-speck auth-speck-7"></div>
                <div className="auth-speck auth-speck-8"></div>
                <div className="auth-speck auth-speck-9"></div>
                <div className="auth-speck auth-speck-10"></div>
            </div>

            <div className="auth-card">
                <div className="auth-header">
                    <h1 className="auth-title">GLOBAL CHAT</h1>
                    <p className="auth-subtitle">Welcome back</p>
                </div>

                {error && <div className="auth-error">{error}</div>}

                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="auth-input-group">
                        <label htmlFor="email">Email</label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="Enter your email"
                            className="auth-input"
                            disabled={loading}
                        />
                    </div>

                    <div className="auth-input-group">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="Enter your password"
                            className="auth-input"
                            disabled={loading}
                        />
                    </div>

                    <button
                        type="submit"
                        className="auth-button auth-button-primary"
                        disabled={loading}
                    >
                        {loading ? 'Signing in...' : 'Sign In'}
                    </button>
                </form>

                <div className="auth-divider">
                    <span>OR</span>
                </div>

                <button
                    onClick={handleGoogleSignIn}
                    className="auth-button auth-button-google"
                    disabled={loading}
                >
                    <svg className="google-icon" viewBox="0 0 24 24">
                        <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                        <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                        <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                        <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                    </svg>
                    Sign in with Google
                </button>

                <div className="auth-footer">
                    <p>
                        Don't have an account?{' '}
                        <button
                            type="button"
                            onClick={onSwitchToSignup}
                            className="auth-link"
                        >
                            Sign up
                        </button>
                    </p>
                </div>
            </div>
        </div>
    );
};
