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
    onRenameChat: (chatId: string, newName: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({
                                                    isOpen,
                                                    onClose,
                                                    savedChats,
                                                    onLoadChat,
                                                    onDeleteChat,
                                                    onNewChat,
                                                    onRenameChat,
                                                }) => {
    const [sidebarVisible, setSidebarVisible] = React.useState(true);

    const toggleSidebar = () => {
        setSidebarVisible(!sidebarVisible);
    };

    const formatDate = (timestamp: string) => {
        const date = new Date(timestamp);
        return date.toLocaleDateString('en-US', {
            month: 'numeric',
            day: 'numeric',
            year: 'numeric'
        }) + ' ' + date.toLocaleTimeString('en-US', {
            hour: 'numeric',
            minute: '2-digit',
            hour12: true
        });
    };

    return (
        <>
            {/* Hamburger toggle button */}
            <button className="sidebar-toggle" onClick={toggleSidebar}>
                <span></span>
                <span></span>
                <span></span>
            </button>

            <div className={`sidebar-overlay ${isOpen ? 'open' : ''}`} onClick={onClose}></div>
            <aside className={`sidebar ${!sidebarVisible ? 'hidden' : ''} ${isOpen ? 'open' : ''}`}>
                <div className="sidebar-header">
                    <div className="header-content">
                        <span className="icon">🕐</span>
                        <h3>PREVIOUS CHAT</h3>
                    </div>
                    <button className="close-button" onClick={onClose}>✕</button>
                </div>

                <button className="sidebar-home-button" onClick={() => { onNewChat(); onClose(); }}>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                        <path d="m3 9 9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path>
                        <polyline points="9 22 9 12 15 12 15 22"></polyline>
                    </svg>
                    Home
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
                                    <p className="chat-name">{chat.name}</p>
                                    <p className="chat-date">{formatDate(chat.timestamp)}</p>
                                </div>
                                <button
                                    className="delete-btn"
                                    onClick={(e) => {
                                        e.stopPropagation();
                                        onDeleteChat(chat.id);
                                    }}
                                    title="Delete chat"
                                >
                                    ✕
                                </button>
                            </div>
                        ))
                    )}
                </div>
            </aside>
        </>
    );
};