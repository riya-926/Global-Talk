import { useState } from 'react';
import './SaveDialog.css';

interface SaveDialogProps {
    isOpen: boolean;
    onSave: (name: string) => void;
    onDiscard: () => void;
}

export default function SaveDialog({ isOpen, onSave, onDiscard }: SaveDialogProps) {
    const [chatName, setChatName] = useState('');

    if (!isOpen) return null;

    const handleSave = () => {
        onSave(chatName.trim() || 'Untitled Chat');
        setChatName('');
    };

    return (
        <div className="modal-overlay" onClick={onDiscard}>
            <div className="modal" onClick={(e) => e.stopPropagation()}>
                <h3>Save Conversation</h3>
                <p>Enter a name for this chat</p>
                <input
                    type="text"
                    placeholder="e.g., Travel Planning Discussion"
                    value={chatName}
                    onChange={(e) => setChatName(e.target.value)}
                    onKeyDown={(e) => e.key === 'Enter' && handleSave()}
                    autoFocus
                />
                <div className="modal-buttons">
                    <button onClick={onDiscard}>Discard</button>
                    <button className="primary" onClick={handleSave}>
                        Save Chat
                    </button>
                </div>
            </div>
        </div>
    );
}