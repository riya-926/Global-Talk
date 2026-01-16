import React from 'react';
import CornerGlobe from './CornerGlobe';
import './HomeScreen.css';

interface HomeProps {
    targetLanguage: string;
    onLanguageChange: (lang: string) => void;
    onStartRecording: () => void;
}

const LANGUAGES = [
    { code: 'ar', name: 'Arabic' },
    { code: 'zh', name: 'Chinese' },
    { code: 'en', name: 'English' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'hi', name: 'Hindi' },
    { code: 'it', name: 'Italian' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ru', name: 'Russian' },
    { code: 'es', name: 'Spanish' },
];

export const Home: React.FC<HomeProps> = ({
                                              targetLanguage,
                                              onLanguageChange,
                                              onStartRecording,
                                          }) => {
    const [sidebarVisible, setSidebarVisible] = React.useState(true);
    const [showHelp, setShowHelp] = React.useState(false);

    const toggleSidebar = () => {
        setSidebarVisible(!sidebarVisible);
        // Add class to body to shift content
        document.body.classList.toggle('sidebar-hidden');
    };

    return (
        <div className="home-screen">
            {/* Hamburger menu button */}
            <button className="sidebar-toggle-btn" onClick={toggleSidebar}>
                <span></span>
                <span></span>
                <span></span>
            </button>

            {/* ADDED: Background blur circles from builder.io */}
            <div className="background-blurs">
                <div className="blur-circle blur-cyan"></div>
                <div className="blur-circle blur-purple"></div>
            </div>

            <div className="home-center">
                <h1 className="title-large">
                    GLOBAL
                    <br />
                    CHAT
                </h1>
                <p className="subtitle">
                    Connect globally, communicate seamlessly across languages
                </p>

                <button className="start-btn" onClick={onStartRecording}>
                    <span className="globe-icon">🌐</span>
                    Start Meeting with Globe
                </button>

                <div className="language-selector">
                    <label>Subtitles</label>
                    <select
                        value={targetLanguage}
                        onChange={(e) => onLanguageChange(e.target.value)}
                    >
                        {LANGUAGES.map((lang) => (
                            <option key={lang.code} value={lang.code}>
                                {lang.name}
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            <CornerGlobe />

            {/* Help button with instructions */}
            <div className="help-btn" onClick={() => setShowHelp(true)}>?</div>

            {/* Help popup */}
            {showHelp && (
                <div className="help-overlay" onClick={() => setShowHelp(false)}>
                    <div className="help-popup" onClick={(e) => e.stopPropagation()}>
                        <button className="help-close" onClick={() => setShowHelp(false)}>✕</button>
                        <h2>How to Use Global Chat</h2>
                        <div className="help-content">
                            <div className="help-step">
                                <span className="step-number">1</span>
                                <p><strong>Select Your Language:</strong> Choose your preferred subtitle language from the dropdown.</p>
                            </div>
                            <div className="help-step">
                                <span className="step-number">2</span>
                                <p><strong>Start Meeting:</strong> Click "Start Meeting with Globe" to begin recording.</p>
                            </div>
                            <div className="help-step">
                                <span className="step-number">3</span>
                                <p><strong>Speak Naturally:</strong> Talk in any language and see real-time translations appear side-by-side.</p>
                            </div>
                            <div className="help-step">
                                <span className="step-number">4</span>
                                <p><strong>Save Your Chat:</strong> Click "End Meeting" and name your conversation to save it for later.</p>
                            </div>
                            <div className="help-step">
                                <span className="step-number">5</span>
                                <p><strong>Access History:</strong> View all saved chats in the sidebar. Click any chat to review the conversation.</p>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};