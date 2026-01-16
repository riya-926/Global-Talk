import React, { useState } from 'react';
import './SaveDialog.css';

interface SaveDialogProps {
    onSave: (name: string) => void;
    onDiscard: () => void;
}

export const SaveDialog: React.FC<SaveDialogProps> = ({ onSave, onDiscard }) => {
    const [chatName, setChatName] = useState('');

    const handleSave = () => {
        onSave(chatName.trim() || 'Untitled Chat');
    };

    return (
        <div className="save-dialog-overlay">
            <div className="save-dialog">
                <h2 className="save-dialog-title">Save Conversation</h2>
                <p className="save-dialog-subtitle">
                    Enter a name for this chat to save it in your conversation history.
                </p>

                <input
                    type="text"
                    className="save-dialog-input"
                    placeholder="e.g., Travel Planning Discussion"
                    value={chatName}
                    onChange={(e) => setChatName(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && handleSave()}
                    autoFocus
                />

                <div className="save-dialog-buttons">
                    <button className="discard-btn" onClick={onDiscard}>
                        Discard
                    </button>
                    <button className="save-btn" onClick={handleSave}>
                        Save Chat
                    </button>
                </div>
            </div>
        </div>
    );
};