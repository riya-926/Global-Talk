/**
 * components/Sidebar.css
 *
 * Sidebar styling - matches your design exactly
 */

.sidebar {
    width: 300px;
    background: rgba(10, 22, 40, 0.8);
    border-right: 1px solid rgba(59, 130, 246, 0.2);
    display: flex;
    flex-direction: column;
    backdrop-filter: blur(10px);
}

.sidebar-header {
    padding: 24px 20px;
    border-bottom: 1px solid rgba(59, 130, 246, 0.2);
    display: flex;
    align-items: center;
    gap: 10px;
}

.sidebar-header .icon {
    font-size: 18px;
}

.sidebar-header h3 {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    color: rgba(255, 255, 255, 0.7);
}

.chat-list {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
}

.chat-item {
    display: flex;
    align-items: start;
    gap: 12px;
    padding: 14px;
    border-radius: 10px;
    cursor: pointer;
    transition: all 0.2s;
    position: relative;
    border: 1px solid transparent;
    margin-bottom: 8px;
}

.chat-item:hover {
    background: rgba(59, 130, 246, 0.1);
    border-color: rgba(59, 130, 246, 0.3);
}

.chat-item.active {
    background: rgba(59, 130, 246, 0.2);
    border-color: rgba(59, 130, 246, 0.5);
}

.chat-icon {
    font-size: 18px;
    flex-shrink: 0;
}

.chat-info {
    flex: 1;
    min-width: 0;
}

.chat-title {
    font-size: 14px;
    font-weight: 500;
    color: white;
    margin-bottom: 4px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.chat-date {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.5);
}

.delete-btn {
    opacity: 0;
    background: none;
    border: none;
    color: rgba(255, 255, 255, 0.5);
    font-size: 24px;
    cursor: pointer;
    padding: 0 8px;
    transition: all 0.2s;
    line-height: 1;
}

.chat-item:hover .delete-btn {
    opacity: 1;
}

.delete-btn:hover {
    color: #ef4444;
}

.clear-btn {
    margin: 16px;
    padding: 12px;
    background: rgba(255, 255, 255, 0.05);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: white;
    font-size: 14px;
    cursor: pointer;
    transition: all 0.2s;
}

.clear-btn:hover {
    background: rgba(255, 255, 255, 0.1);
}