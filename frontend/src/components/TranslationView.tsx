import React from 'react';
import type { TranslationMessage } from '../types';
import './MeetingScreen.css';

interface TranslationViewProps {
    messages: TranslationMessage[];
    isRecording: boolean;
    onStopRecording: () => void;
}

export const TranslationView: React.FC<TranslationViewProps> = ({
                                                                    messages,
                                                                    isRecording,
                                                                    onStopRecording,
                                                                }) => {
    return (
        <div className="meeting-screen">
            <header className="meeting-header">
                <div className="header-title">
                    <h2>GLOBAL<br/>CHAT</h2>
                </div>

                {isRecording && (
                    <div className="recording-badge">
                        <span className="mic-icon">🎤</span>
                        <span>RECORDING</span>
                        <span className="pulse-dot"></span>
                    </div>
                )}

                <button className="end-btn" onClick={onStopRecording}>
                    × End Meeting
                </button>
            </header>

            <div className="meeting-content">
                <h1 className="meeting-title">Live Conversation</h1>

                <div className="transcript-area">
                    {messages.length === 0 ? (
                        <div className="empty-state">
                            🎤 Start speaking to see translations appear here...
                        </div>
                    ) : (
                        messages.map((msg, index) => (
                            <div key={index} className="transcript-row">
                                <div className="original-card">
                                    <p className="card-label">
                                        DETECTED: <span className="lang-name">{msg.detectedLanguage}</span>
                                    </p>
                                    <p className="card-text">{msg.originalText}</p>
                                </div>

                                <div className="translation-card">
                                    <p className="card-label">TRANSLATION:</p>
                                    <p className="card-text">{msg.translatedText}</p>
                                </div>
                            </div>
                        ))
                    )}
                </div>
            </div>
        </div>
    );
};