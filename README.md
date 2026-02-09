# Global Chat - Real-Time Meeting Translator

A lightweight desktop application that listens to audio during online meetings (Zoom, Teams, Google Meet), automatically detects the spoken language, translates it in real-time, and displays live subtitles on screen.

---

## Features

-  **Continuous audio recording** - No gaps, captures everything spoken
-  **Automatic language detection** - Detects what language is being spoken
-  **Real-time translation** - Translates to your chosen language instantly
-  **Beautiful UI** - Clean, modern interface with subtitle display
-  **Session saving** - Auto-saves all translations by date
-  **Smart filtering** - Voice Activity Detection skips silence and noise
-  **Session history** - Review past conversations anytime

---

##  Project Structure

```
Global-Talk/
│
├── backend/
│   ├── config.py              # Configuration settings (API keys, audio params)
│   ├── audio_manager.py       # Handles microphone access and audio recording
│   ├── stt_module.py          # Speech-to-Text using OpenAI Whisper
│   └── translation_module.py  # Translation using OpenAI GPT-4o-mini
│
├── frontend/
│   └── ui.py                  # Beautiful GUI interface (CustomTkinter)
│
├── main.py                    # Main app - connects backend + frontend
├── sessions/                  # Auto-saved translation sessions (JSON files)
└── README.md                  # This file
```

---

## File Descriptions

### **Backend Files**

#### `backend/config.py`
Configuration file storing all settings: API keys, audio chunk duration (3 seconds), sample rate (16kHz), target language defaults, and model names for Whisper and GPT.

#### `backend/audio_manager.py`
Manages microphone access using `sounddevice` library - records audio chunks, lists available input devices, and returns numpy arrays ready for speech-to-text processing.

#### `backend/stt_module.py`
Speech-to-Text module using OpenAI Whisper API - converts audio numpy arrays to WAV format, sends to Whisper, and returns both transcript text and detected language code.

#### `backend/translation_module.py`
Translation module using OpenAI GPT-4o-mini - takes transcript text with source/target languages and returns translated text while preserving numbers, dates, and formatting.

---

### **Frontend Files**

#### `frontend/ui.py`
Beautiful GUI built with CustomTkinter - displays home screen with language selector, live translation screen with subtitle cards, session history sidebar, and handles all user interactions.




---



## How It Works

### Architecture Overview:

1. **Audio Recording Thread**
    - Continuously records audio in 100ms blocks using `sounddevice`
    - Buffers audio and creates 3-second chunks
    - Puts chunks into a queue for processing

2. **Processing Worker Thread**
    - Gets audio chunks from queue
    - Checks Voice Activity Detection (VAD) to skip silence
    - Sends to Whisper API for transcription + language detection
    - Sends transcript to GPT for translation
    - Puts results in output queue

3. **Main UI Thread**
    - Displays the interface
    - Checks output queue every 100ms
    - Updates UI with new translation cards
    - Handles user interactions (start/stop)

### Data Flow:
```
Microphone → Audio Buffer → Queue → VAD Filter → Whisper API → GPT API → UI Display
```



---


## Authentication

Global Chat now includes Firebase authentication:
- **Email/Password** sign up and login
- **Google Sign-in** for quick access
- Secure user sessions

See [FIREBASE_SETUP.md](./FIREBASE_SETUP.md) for setup instructions.

## Recent Improvements

- ✅ **Enhanced Voice Activity Detection (VAD)**: Improved filtering for meeting environments - filters out background noise and only processes actual speech
- ✅ **Fixed Globe Animation**: Globe now rotates consistently without interruption
- ✅ **Firebase Authentication**: Secure login and signup with Google sign-in support

## Future Enhancements

- Add support for system audio capture (not just microphone)
- Export sessions as subtitle files (.srt format)
- Add real-time voice activity visualization
- Support for custom translation models
- Dark mode theme option
- Floating subtitle overlay mode
- Multi-speaker detection

---

## License

This project is for educational purposes. Make sure to comply with OpenAI's usage policies.

---

## Acknowledgments

- **OpenAI Whisper** - State-of-the-art speech recognition
- **OpenAI GPT-4o-mini** - Fast, accurate translation
- **CustomTkinter** - Modern Python UI framework

---

## Tips for Best Results

- **Use a good microphone** - Better audio = better transcription
- **Reduce background noise** - Close windows, mute notifications
- **Speak clearly** - Better enunciation = higher accuracy
- **Adjust chunk duration** - Shorter (2s) for faster response, longer (4s) for better accuracy
- **Internet connection** - Requires stable connection for API calls

---

**Made with ❤️ for breaking down language barriers in real-time meetings!** 