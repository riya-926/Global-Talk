import React from 'react';
import type { SavedChat } from '../types';
import './Sidebar.css';

interface SidebarProps {
    isOpen: boolean;
    onClose: () => void;
    savedChats: SavedChat[];
    onLoadChat: (chat: SavedChat) => void;
    onDeleteChat: (chatId: string) => void;
    onNewChat: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
                                                    isOpen,
                                                    onClose,
                                                    savedChats,
                                                    onLoadChat,
                                                    onDeleteChat,
                                                    onNewChat,
                                                }) => {
    const formatDate = (timestamp: string) => {
        const date = new Date(timestamp);
        return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
    };

    return (
        <>
            <div className={`sidebar-overlay ${isOpen ? 'open' : ''}`} onClick={onClose}></div>
            <aside className={`sidebar ${isOpen ? 'open' : ''}`}>
                <div className="sidebar-header">
                    <div className="header-content">
                        <span className="icon">🕐</span>
                        <h3>PREVIOUS CHAT</h3>
                    </div>
                    <button className="close-button" onClick={onClose}>✕</button>
                </div>

                <button className="new-chat-button" onClick={onNewChat}>
                    ➕ New Chat
                </button>

                <div className="chat-list">
                    {savedChats.length === 0 ? (
                        <p className="empty-chats">No saved chats yet</p>
                    ) : (
                        savedChats.map(chat => (
                            <div
                                key={chat.id}
                                className="chat-item"
                                onClick={() => onLoadChat(chat)}
                            >
                                <span className="chat-icon">💬</span>
                                <div className="chat-info">
                                    <p className="chat-date">{formatDate(chat.timestamp)}</p>
                                    <p className="chat-preview">
                                        {chat.messages.length} messages · {chat.targetLanguage}
                                    </p>
                                </div>
                                <button
                                    className="delete-btn"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onDeleteChat(chat.id);
                                    }}
                                >
                                    🗑️
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </aside>
        </>
    );
};