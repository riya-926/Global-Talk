import React from 'react';
import './LandingPage.css';

interface LandingPageProps {
    onGetStarted: () => void;
}

export const LandingPage: React.FC<LandingPageProps> = ({ onGetStarted }) => {
    return (
        <div className="landing-page">
            {/* Background effects */}
            <div className="landing-bg-gradient" />
            <div className="landing-glow-line" />
            <div className="landing-blur-circles">
                <div className="landing-blur landing-blur-1" />
                <div className="landing-blur landing-blur-2" />
            </div>

            {/* Header */}
            <header className="landing-header">
                <div className="landing-logo">
                    <div className="landing-logo-icon">
                        <span /><span /><span /><span />
                    </div>
                    <span className="landing-logo-text">Global Chat</span>
                </div>
            </header>

            {/* Hero Section */}
            <section className="landing-hero">
                <div className="landing-hero-content">
                    <span className="landing-pill">Real-Time Meeting Translator</span>
                    <h1 className="landing-hero-title">Break Language Barriers in Every Meeting.</h1>
                    <p className="landing-hero-desc">
                        A lightweight desktop application that listens to audio during online meetings,
                        automatically detects languages, and provides instant translations with beautiful live subtitles.
                    </p>
                    <div className="landing-hero-buttons">
                        <button className="landing-btn landing-btn-primary" onClick={onGetStarted}>
                            Get Started Free
                        </button>
                    </div>
                    <div className="landing-features-inline">
                        <span className="landing-feature-dot">Works with Zoom, Teams, Meet</span>
                        <span className="landing-feature-dot">100+ Languages</span>
                    </div>
                </div>
                <div className="landing-hero-visual" aria-hidden="true" />
            </section>

            {/* Features Section */}
            <section className="landing-features">
                <h2 className="landing-section-title">Powerful Features for Seamless Communication</h2>
                <p className="landing-section-subtitle">Everything you need for real-time meeting translation</p>
                <div className="landing-features-grid">
                    {[
                        { icon: 'mic', title: 'Continuous Audio Recording', desc: 'No gaps, captures everything spoken during your meetings' },
                        { icon: 'lang', title: 'Automatic Language Detection', desc: 'Instantly detects what language is being spoken' },
                        { icon: 'translate', title: 'Real-Time Translation', desc: 'Translates to your chosen language instantly' },
                        { icon: 'save', title: 'Session Saving', desc: 'Auto-saves all translations by date for easy access' },
                        { icon: 'filter', title: 'Smart Filtering', desc: 'Voice Activity Detection skips silence and background noise' },
                        { icon: 'history', title: 'Session History', desc: 'Review past conversations and translations anytime' },
                    ].map((f) => (
                        <div key={f.title} className="landing-feature-card">
                            <div className="landing-feature-icon">
                                <FeatureIcon type={f.icon} />
                            </div>
                            <h3>{f.title}</h3>
                            <p>{f.desc}</p>
                        </div>
                    ))}
                </div>
            </section>

            {/* How It Works */}
            <section className="landing-how">
                <h2 className="landing-section-title">How It Works</h2>
                <p className="landing-section-subtitle">Simple, fast, and effective</p>
                <div className="landing-steps">
                    <div className="landing-step">
                        <div className="landing-step-num landing-step-1">1</div>
                        <h3>Start Your Meeting</h3>
                        <p>Launch Global Chat alongside Zoom, Teams, or Google Meet</p>
                    </div>
                    <div className="landing-step">
                        <div className="landing-step-num landing-step-2">2</div>
                        <h3>Auto-Detection</h3>
                        <p>The app automatically detects and captures spoken audio</p>
                    </div>
                    <div className="landing-step">
                        <div className="landing-step-num landing-step-3">3</div>
                        <h3>Live Translations</h3>
                        <p>See real-time translations displayed as beautiful subtitles</p>
                    </div>
                </div>
            </section>

            {/* CTA Section */}
            <section className="landing-cta">
                <div className="landing-cta-card">
                    <h2>Ready to Transform Your Meetings?</h2>
                    <p>Join thousands of users breaking language barriers every day</p>
                    <button className="landing-btn landing-btn-cta" onClick={onGetStarted}>
                        Get Started Now
                    </button>
                </div>
            </section>

            {/* Footer */}
            <footer className="landing-footer">
                <div className="landing-footer-logo">
                    <div className="landing-logo-icon landing-logo-icon-sm">
                        <span /><span /><span /><span />
                    </div>
                    <span>Global Chat</span>
                </div>
                <span className="landing-footer-copy">© 2026 Global Chat. All rights reserved.</span>
            </footer>
        </div>
    );
};

function FeatureIcon({ type }: { type: string }) {
    const baseClass = 'landing-icon-svg';
    switch (type) {
        case 'mic':
            return (
                <svg className={baseClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z" />
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2" />
                    <line x1="12" y1="19" x2="12" y2="23" />
                    <line x1="8" y1="23" x2="16" y2="23" />
                </svg>
            );
        case 'lang':
            return (
                <svg className={baseClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <line x1="2" y1="12" x2="22" y2="12" />
                    <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z" />
                </svg>
            );
        case 'translate':
            return (
                <svg className={baseClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="12 2 15 8 22 9 17 14 18 21 12 18 6 21 7 14 2 9 9 8" />
                </svg>
            );
        case 'save':
            return (
                <svg className={baseClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                </svg>
            );
        case 'filter':
            return (
                <svg className={baseClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <polygon points="22 3 2 3 10 12.46 10 19 14 21 14 12.46 22 3" />
                </svg>
            );
        case 'history':
            return (
                <svg className={baseClass} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <circle cx="12" cy="12" r="10" />
                    <polyline points="12 6 12 12 16 14" />
                    <path d="M12 2a10 10 0 0 1 10 10" />
                </svg>
            );
        default:
            return null;
    }
}
