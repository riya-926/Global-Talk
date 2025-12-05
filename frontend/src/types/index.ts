export interface TranslationMessage {
    originalText: string;
    translatedText: string;
    detectedLanguage: string;
    targetLanguage: string;
    timestamp: string;
}

export interface SavedChat {
    id: string;
    timestamp: string;
    messages: TranslationMessage[];
    targetLanguage: string;
}