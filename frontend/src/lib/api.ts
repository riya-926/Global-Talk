import type { TranslationMessage } from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export const api = {
    async startRecording(targetLanguage: string): Promise<void> {
        const response = await fetch(`${API_BASE_URL}/start-recording`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target_language: targetLanguage }),
        });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Failed to start recording' }));
            throw new Error(error.error || 'Failed to start recording');
        }
    },

    async stopRecording(): Promise<void> {
        const response = await fetch(`${API_BASE_URL}/stop-recording`, { method: 'POST' });
        if (!response.ok) {
            const error = await response.json().catch(() => ({ error: 'Failed to stop recording' }));
            throw new Error(error.error || 'Failed to stop recording');
        }
    },

    async getMessages(): Promise<TranslationMessage[]> {
        const response = await fetch(`${API_BASE_URL}/messages`);
        if (!response.ok) throw new Error('Failed to fetch messages');
        return response.json();
    },

    async healthCheck(): Promise<{ status: string; is_recording: boolean; message_count: number }> {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (!response.ok) throw new Error('Health check failed');
        return response.json();
    },
};
