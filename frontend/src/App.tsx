import { useState, useEffect } from 'react';
import { Home } from './components/Home';
import { TranslationView } from './components/TranslationView';
import { Sidebar } from './components/Sidebar';
import { SaveDialog } from './components/SaveDialog';
import { Login } from './components/Login';
import { Signup } from './components/Signup';
import CornerGlobe from './components/CornerGlobe';
import { api } from './lib/api';
import { useAuth } from './contexts/AuthContext';
import type { SavedChat, TranslationMessage } from './types';
import './App.css';

function AppContent() {
    const { currentUser, logout } = useAuth();
    const [isRecording, setIsRecording] = useState(false);
    const [targetLanguage, setTargetLanguage] = useState('en');
    const [messages, setMessages] = useState<TranslationMessage[]>([]);
    const [savedChats, setSavedChats] = useState<SavedChat[]>([]);
    const [currentChatId, setCurrentChatId] = useState<string | null>(null);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [showSaveDialog, setShowSaveDialog] = useState(false);
    const [showAuth, setShowAuth] = useState<'login' | 'signup' | null>(null);

    // Load saved chats from localStorage
    useEffect(() => {
        const saved = localStorage.getItem('globalChats');
        if (saved) {
            setSavedChats(JSON.parse(saved));
        }
    }, []);

    // Save chats to localStorage whenever they change
    useEffect(() => {
        if (savedChats.length > 0) {
            localStorage.setItem('globalChats', JSON.stringify(savedChats));
        }
    }, [savedChats]);

    // Poll for new messages when recording
    useEffect(() => {
        if (!isRecording) return;

        const interval = setInterval(async () => {
            try {
                const newMessages = await api.getMessages();
                if (newMessages.length > messages.length) {
                    setMessages(newMessages);
                }
            } catch (error) {
                console.error('Error fetching messages:', error);
            }
        }, 1000);

        return () => clearInterval(interval);
    }, [isRecording, messages.length]);

    const handleStartRecording = async () => {
        try {
            await api.startRecording(targetLanguage);
            setIsRecording(true);
            setMessages([]);
            setCurrentChatId(Date.now().toString());
        } catch (error) {
            console.error('Error starting recording:', error);
            alert('Failed to start recording. Make sure the backend is running.');
        }
    };

    const handleStopRecording = async () => {
        try {
            await api.stopRecording();
            setIsRecording(false);

            // Always show save dialog when stopping
            setShowSaveDialog(true);
        } catch (error) {
            console.error('Error stopping recording:', error);
        }
    };

    const handleSaveChat = (chatName: string) => {
        if (currentChatId) {
            const newChat: SavedChat = {
                id: currentChatId,
                name: chatName,
                timestamp: new Date().toISOString(),
                messages: messages,
                targetLanguage: targetLanguage
            };
            setSavedChats(prev => [newChat, ...prev]);
        }
        setShowSaveDialog(false);
        setMessages([]);
        setCurrentChatId(null);
    };

    const handleDiscardChat = () => {
        setShowSaveDialog(false);
        setMessages([]);
        setCurrentChatId(null);
    };

    const handleLoadChat = (chat: SavedChat) => {
        setMessages(chat.messages);
        setTargetLanguage(chat.targetLanguage);
        setCurrentChatId(chat.id);
        setSidebarOpen(false);
    };

    const handleDeleteChat = (chatId: string) => {
        setSavedChats(prev => prev.filter(chat => chat.id !== chatId));
        if (currentChatId === chatId) {
            setMessages([]);
            setCurrentChatId(null);
        }
    };

    const handleRenameChat = (chatId: string, newName: string) => {
        setSavedChats(prev => prev.map(chat =>
            chat.id === chatId ? { ...chat, name: newName } : chat
        ));
    };

    const handleNewChat = () => {
        setMessages([]);
        setCurrentChatId(null);
        setIsRecording(false);
    };

    // ONLY show globe on homepage (not recording and no messages)
    const showGlobe = !isRecording && messages.length === 0;

    // Show auth if not logged in
    if (!currentUser) {
        return (
            <>
                {showAuth === 'login' || showAuth === null ? (
                    <Login onSwitchToSignup={() => setShowAuth('signup')} />
                ) : (
                    <Signup onSwitchToLogin={() => setShowAuth('login')} />
                )}
            </>
        );
    }

    return (
        <div className="app">
            {/* Logout button */}
            <button
                onClick={logout}
                className="logout-button"
                title="Logout"
            >
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                    <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path>
                    <polyline points="16 17 21 12 16 7"></polyline>
                    <line x1="21" y1="12" x2="9" y2="12"></line>
                </svg>
            </button>

            {/* Globe ONLY shows on homepage */}
            {showGlobe && <CornerGlobe />}

            {/* Hamburger menu button for small screens */}
            <button
                className="hamburger-menu"
                onClick={() => setSidebarOpen(!sidebarOpen)}
                style={{
                    display: window.innerWidth <= 900 ? 'flex' : 'none'
                }}
            >
                ☰
            </button>

            <Sidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                savedChats={savedChats}
                onLoadChat={handleLoadChat}
                onDeleteChat={handleDeleteChat}
                onNewChat={handleNewChat}
                onRenameChat={handleRenameChat}
            />

            <div className="main-content">
                {!isRecording && messages.length === 0 ? (
                    <Home
                        targetLanguage={targetLanguage}
                        onLanguageChange={setTargetLanguage}
                        onStartRecording={handleStartRecording}
                    />
                ) : (
                    <TranslationView
                        messages={messages}
                        isRecording={isRecording}
                        onStopRecording={handleStopRecording}
                    />
                )}
            </div>

            {showSaveDialog && (
                <SaveDialog
                    onSave={handleSaveChat}
                    onDiscard={handleDiscardChat}
                />
            )}
        </div>
    );
}

function App() {
    return <AppContent />;
}

export default App;