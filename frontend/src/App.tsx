import { useState, useEffect } from 'react';
import { Home } from './components/Home';
import { TranslationView } from './components/TranslationView';
import { Sidebar } from './components/Sidebar';
import { api } from './lib/api';
import type { SavedChat, TranslationMessage } from './types';
import './App.css';

function App() {
    const [isRecording, setIsRecording] = useState(false);
    const [targetLanguage, setTargetLanguage] = useState('es');
    const [messages, setMessages] = useState<TranslationMessage[]>([]);
    const [savedChats, setSavedChats] = useState<SavedChat[]>([]);
    const [currentChatId, setCurrentChatId] = useState<string | null>(null);
    const [sidebarOpen, setSidebarOpen] = useState(false);

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

            // Save the conversation
            if (messages.length > 0 && currentChatId) {
                const newChat: SavedChat = {
                    id: currentChatId,
                    timestamp: new Date().toISOString(),
                    messages: messages,
                    targetLanguage: targetLanguage
                };
                setSavedChats(prev => [newChat, ...prev]);
            }
        } catch (error) {
            console.error('Error stopping recording:', error);
        }
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

    const handleNewChat = () => {
        setMessages([]);
        setCurrentChatId(null);
        setIsRecording(false);
    };

    return (
        <div className="app">
            <Sidebar
                isOpen={sidebarOpen}
                onClose={() => setSidebarOpen(false)}
                savedChats={savedChats}
                onLoadChat={handleLoadChat}
                onDeleteChat={handleDeleteChat}
                onNewChat={handleNewChat}
            />

            <div className="main-content">
                <header className="app-header">
                    <button
                        className="menu-button"
                        onClick={() => setSidebarOpen(!sidebarOpen)}
                    >
                        ☰
                    </button>
                    <h1>🌍 Global Chat</h1>
                    <div className="header-spacer"></div>
                </header>

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
        </div>
    );
}

export default App;