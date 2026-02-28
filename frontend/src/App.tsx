import { useState, useEffect, useRef } from 'react';
import { Home } from './components/Home';
import { TranslationView } from './components/TranslationView';
import { Sidebar } from './components/Sidebar';
import { SaveDialog } from './components/SaveDialog';
import { LandingPage } from './components/LandingPage';
import { Login } from './components/Login';
import { Signup } from './components/Signup';
import CornerGlobe from './components/CornerGlobe';
import { api } from './lib/api';
import { useAuth } from './contexts/AuthContext';
import { subscribeToUserChats, saveChat, deleteChat, renameChat } from './lib/chats';
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
    const [saveDialogDefaultName, setSaveDialogDefaultName] = useState('');
    const [showAuth, setShowAuth] = useState<'login' | 'signup' | null>(null);
    const lastSavedChatIdRef = useRef<string | null>(null);

    // Subscribe to current user's chats from Firestore (real-time, synced across devices)
    useEffect(() => {
        if (!currentUser) {
            setSavedChats([]);
            return;
        }
        const uid = currentUser.uid;

        // One-time migration: move any chats from localStorage to Firestore
        const storageKey = `globalChats_${uid}`;
        const stored = localStorage.getItem(storageKey);
        if (stored) {
            try {
                const parsed = JSON.parse(stored) as SavedChat[];
                if (Array.isArray(parsed) && parsed.length > 0) {
                    Promise.all(
                        parsed.map((chat) =>
                            saveChat(uid, {
                                name: chat.name,
                                timestamp: chat.timestamp,
                                messages: chat.messages,
                                targetLanguage: chat.targetLanguage
                            })
                        )
                    ).then(() => localStorage.removeItem(storageKey));
                }
            } catch {
                localStorage.removeItem(storageKey);
            }
        }

        const unsubscribe = subscribeToUserChats(uid, setSavedChats);
        return () => unsubscribe();
    }, [currentUser?.uid]);

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

            // Auto-save to user's account so the conversation is never lost
            if (currentUser && messages.length > 0) {
                const defaultName = `Conversation ${new Date().toLocaleDateString()} ${new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
                setSaveDialogDefaultName(defaultName);
                lastSavedChatIdRef.current = null;
                try {
                    const docId = await saveChat(currentUser.uid, {
                        name: defaultName,
                        timestamp: new Date().toISOString(),
                        messages,
                        targetLanguage
                    });
                    setCurrentChatId(docId);
                    lastSavedChatIdRef.current = docId;
                    setSavedChats((prev) => {
                        const next: SavedChat[] = [{
                            id: docId,
                            name: defaultName,
                            timestamp: new Date().toISOString(),
                            messages,
                            targetLanguage
                        }, ...prev];
                        return next;
                    });
                } catch (err) {
                    console.error('Failed to auto-save chat:', err);
                    setSaveDialogDefaultName('');
                    alert('Could not save conversation. Please try saving again from the dialog.');
                }
            } else {
                setSaveDialogDefaultName('');
            }
            setShowSaveDialog(true);
        } catch (error) {
            console.error('Error stopping recording:', error);
        }
    };

    const handleSaveChat = async (chatName: string) => {
        if (!currentUser) {
            setShowSaveDialog(false);
            setMessages([]);
            setCurrentChatId(null);
            return;
        }
        const name = chatName.trim() || 'Untitled Chat';
        const chatIdToRename = lastSavedChatIdRef.current ?? currentChatId;
        try {
            if (chatIdToRename) {
                await renameChat(chatIdToRename, name);
                setSavedChats((prev) =>
                    prev.map((c) => (c.id === chatIdToRename ? { ...c, name } : c))
                );
            } else if (messages.length > 0) {
                const docId = await saveChat(currentUser.uid, {
                    name,
                    timestamp: new Date().toISOString(),
                    messages,
                    targetLanguage
                });
                setSavedChats((prev) => [{
                    id: docId,
                    name,
                    timestamp: new Date().toISOString(),
                    messages,
                    targetLanguage
                }, ...prev]);
            }
        } catch (err) {
            console.error('Failed to save chat:', err);
            alert('Failed to save conversation. Check your connection and try again.');
            return;
        }
        lastSavedChatIdRef.current = null;
        setShowSaveDialog(false);
        setMessages([]);
        setCurrentChatId(null);
    };

    const handleDiscardChat = () => {
        lastSavedChatIdRef.current = null;
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

    const handleDeleteChat = async (chatId: string) => {
        if (currentChatId === chatId) {
            setMessages([]);
            setCurrentChatId(null);
        }
        try {
            await deleteChat(chatId);
        } catch (err) {
            console.error('Failed to delete chat:', err);
        }
    };

    const handleRenameChat = async (chatId: string, newName: string) => {
        try {
            await renameChat(chatId, newName);
        } catch (err) {
            console.error('Failed to rename chat:', err);
        }
    };

    const handleNewChat = () => {
        setMessages([]);
        setCurrentChatId(null);
        setIsRecording(false);
    };

    // ONLY show globe on homepage (not recording and no messages)
    const showGlobe = !isRecording && messages.length === 0;
    const isHomepage = showGlobe;

    // Show landing, login, or signup if not logged in
    if (!currentUser) {
        if (showAuth === null) {
            return <LandingPage onGetStarted={() => setShowAuth('login')} />;
        }
        return (
            <>
                {showAuth === 'login' ? (
                    <Login
                        onSwitchToSignup={() => setShowAuth('signup')}
                        onBackToLanding={() => setShowAuth(null)}
                    />
                ) : (
                    <Signup
                        onSwitchToLogin={() => setShowAuth('login')}
                        onBackToLanding={() => setShowAuth(null)}
                    />
                )}
            </>
        );
    }

    return (
        <div className="app">
            {/* Logout button - only on homepage */}
            {isHomepage && (
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
            )}

            {/* Globe ONLY shows on homepage - hidden on narrow/split-screen */}
            {showGlobe && (
                <div className="corner-globe-container">
                    <CornerGlobe />
                </div>
            )}

            {/* Hamburger menu button for small screens */}
            <button
                className="hamburger-menu"
                onClick={() => {
                    const next = !sidebarOpen;
                    setSidebarOpen(next);
                    if (next) document.body.classList.remove('sidebar-hidden');
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
                userName={currentUser?.displayName || currentUser?.email?.split('@')[0] || 'User'}
            />

            <div className="main-content">
                {!isRecording && messages.length === 0 ? (
                    <Home
                        targetLanguage={targetLanguage}
                        onLanguageChange={setTargetLanguage}
                        onStartRecording={handleStartRecording}
                        onToggleSidebar={() => {
                            setSidebarOpen((prev) => {
                                const next = !prev;
                                if (next) document.body.classList.remove('sidebar-hidden');
                                return next;
                            });
                        }}
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
                    defaultName={saveDialogDefaultName}
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