import { useState, useEffect } from 'react';
import { Home } from './components/Home';
import { TranslationView } from './components/TranslationView';
import { Sidebar } from './components/Sidebar';
import { SaveDialog } from './components/SaveDialog';
import CornerGlobe from './components/CornerGlobe';
import { api } from './lib/api';
import type { SavedChat, TranslationMessage } from './types';
import './App.css';

function App() {
    const [isRecording, setIsRecording] = useState(false);
    const [targetLanguage, setTargetLanguage] = useState('en');
    const [messages, setMessages] = useState<TranslationMessage[]>([]);
    const [savedChats, setSavedChats] = useState<SavedChat[]>([]);
    const [currentChatId, setCurrentChatId] = useState<string | null>(null);
    const [sidebarOpen, setSidebarOpen] = useState(true);
    const [showSaveDialog, setShowSaveDialog] = useState(false);

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

    return (
        <div className="app">
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

export default App;