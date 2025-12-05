import React from 'react';
import './HomeScreen.css';

interface HomeProps {
    targetLanguage: string;
    onLanguageChange: (lang: string) => void;
    onStartRecording: () => void;
}

const LANGUAGES = [
    { code: 'en', name: 'English' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'de', name: 'German' },
    { code: 'it', name: 'Italian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'ru', name: 'Russian' },
    { code: 'ja', name: 'Japanese' },
    { code: 'ko', name: 'Korean' },
    { code: 'zh', name: 'Chinese' },
    { code: 'ar', name: 'Arabic' },
    { code: 'hi', name: 'Hindi' },
];

export const Home: React.FC<HomeProps> = ({
                                              targetLanguage,
                                              onLanguageChange,
                                              onStartRecording,
                                          }) => {
    return (
        <div className="home-screen">
            <div className="home-center">
                <h1 className="title-large">
                    GLOBAL<br/>CHAT
                </h1>
                <p className="subtitle">
                    Connect globally, communicate seamlessly across languages
                </p>

                <button className="start-btn" onClick={onStartRecording}>
                    <span className="globe-emoji">🌍</span>
                    Start Meeting with Globe
                </button>

                <div className="language-selector">
                    <label>Translate to:</label>
                    <select
                        value={targetLanguage}
                        onChange={(e) => onLanguageChange(e.target.value)}
                    >
                        {LANGUAGES.map(lang => (
                            <option key={lang.code} value={lang.code}>{lang.name}</option>
                        ))}
                    </select>
                </div>
            </div>

            <div className="floating-globe">🌍</div>
            <div className="help-btn">?</div>
        </div>
    );
};