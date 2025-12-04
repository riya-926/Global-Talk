/**
 * App.tsx
 *
 * Main application component
 * Clean and organized!
 */

import { useState, useEffect, useRef } from 'react';
import { GlobalChatAPI, ContinuousRecorder } from './lib/api';
import { TranscriptLine, SavedChat, ViewType } from './types';
import Sidebar from './components/Sidebar';
import HomeScreen from './components/HomeScreen';
import MeetingScreen from './components/MeetingScreen';
import SaveDialog from './components/SaveDialog';
import './App.css';

export default function App() {
    // View state
    const [view, setView] = useState<ViewType>('home');

    // Recording state
    const [isRecording, setIsRecording] = useState(false);
    const [isProcessing, setIsProcessing] = useState(false);
    const [selectedLanguage, setSelectedLanguage] = useState('English');
    const [transcript, setTranscript] = useState<TranscriptLine[]>([]);

    // Saved chats
    const [savedChats, setSavedChats] = useState<SavedChat[]>([]);
    const [selectedChatId, setSelectedChatId] = useState<string | null>(null);
    const [showSaveDialog, setShowSaveDialog] = useState(false);

    // Refs
    const recorderRef = useRef<ContinuousRecorder | null>(null);
    const apiRef = useRef(new GlobalChatAPI());

    // Load saved chats on mount
    useEffect(() => {
        const saved = localStorage.getItem('savedChats');
        if (saved) {
            setSavedChats(JSON.parse(saved));
        }
    }, []);

    // ==================== HANDLERS ====================

    const handleStartMeeting = async () => {
        try {
            const health = await apiRef.current.healthCheck();
            if (health.status === 'offline') {
                alert('⚠️ Backend server not running!\n\nStart it with:\nuvicorn api_server:app --reload --port 8000');
                return;
            }

            setView('meeting');
            setTranscript([]);

            recorderRef.current = new ContinuousRecorder(async (audioChunk) => {
                setIsProcessing(true);
                try {
                    const result = await apiRef.current.processAudio(
                        audioChunk,
                        selectedLanguage.toLowerCase()
                    );

                    const newLine: TranscriptLine = {
                        id: String(Date.now()),
                        detected_language: result.detected_language.charAt(0).toUpperCase() + result.detected_language.slice(1),
                        original_text: result.original,
                        translation: result.translated,
                        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
                    };

                    setTranscript(prev => [...prev, newLine]);
                } catch (error) {
                    console.error('Error:', error);
                } finally {
                    setIsProcessing(false);
                }
            }, 3000);

            await recorderRef.current.start();
            setIsRecording(true);
        } catch (error) {
            alert('Could not access microphone. Please check permissions.');
        }
    };

    const handleEndMeeting = () => {
        if (recorderRef.current) {
            recorderRef.current.stop();
        }
        setIsRecording(false);
        setShowSaveDialog(true);
    };

    const handleSaveChat = (name: string) => {
        const date = new Date().toLocaleDateString('en-US', {
            month: 'short',
            day: 'numeric',
            year: 'numeric'
        });

        const newChat: SavedChat = {
            id: String(Date.now()),
            name,
            date,
            transcript
        };

        const updated = [newChat, ...savedChats];
        setSavedChats(updated);
        localStorage.setItem('savedChats', JSON.stringify(updated));

        setShowSaveDialog(false);
        setView('home');
    };

    const handleSelectChat = (chatId: string) => {
        setSelectedChatId(chatId);
        const chat = savedChats.find(c => c.id === chatId);
        if (chat) {
            setTranscript(chat.transcript);
            setView('savedChat');
        }
    };

    const handleDeleteChat = (chatId: string) => {
        const updated = savedChats.filter(c => c.id !== chatId);
        setSavedChats(updated);
        localStorage.setItem('savedChats', JSON.stringify(updated));
    };

    const handleClearHistory = () => {
        if (confirm('Clear all chat history?')) {
            setSavedChats([]);
            localStorage.setItem('savedChats', JSON.stringify([]));
        }
    };

    const handleDiscardChat = () => {
        setShowSaveDialog(false);
        setView('home');
    };

    // ==================== RENDER ====================

    const selectedChat = savedChats.find(c => c.id === selectedChatId);

    return (
        <div className="app">
            <Sidebar
                savedChats={savedChats}
                selectedChatId={selectedChatId}
                onSelectChat={handleSelectChat}
                onDeleteChat={handleDeleteChat}
                onClearHistory={handleClearHistory}
            />

            <main className="main-content">
                {view === 'home' && (
                    <HomeScreen
                        selectedLanguage={selectedLanguage}
                        onLanguageChange={setSelectedLanguage}
                        onStartMeeting={handleStartMeeting}
                    />
                )}

                {view === 'meeting' && (
                    <MeetingScreen
                        isRecording={isRecording}
                        isProcessing={isProcessing}
                        transcript={transcript}
                        onEndMeeting={handleEndMeeting}
                    />
                )}

                {view === 'savedChat' && selectedChat && (
                    <div className="saved-chat-view">
                        <div className="saved-header">
                            <button className="back-btn" onClick={() => setView('home')}>
                                ← Back to Home
                            </button>
                            <h2 className="saved-title">{selectedChat.name}</h2>
                            <span className="saved-date">{selectedChat.date}</span>
                        </div>

                        <div className="transcript-area">
                            {selectedChat.transcript.map(line => (
                                <div key={line.id} className="transcript-row">
                                    <div className="original-card">
                                        <p className="card-label">
                                            DETECTED: <span className="lang-name">{line.detected_language}</span>
                                        </p>
                                        <p className="card-text">{line.original_text}</p>
                                    </div>

                                    <div className="translation-card">
                                        <p className="card-label">TRANSLATION:</p>
                                        <p className="card-text">{line.translation}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                )}
            </main>

            <SaveDialog
                isOpen={showSaveDialog}
                onSave={handleSaveChat}
                onDiscard={handleDiscardChat}
            />
        </div>
    );
}