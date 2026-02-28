# Global Chat – Real-Time Meeting Translator

A **web application** that listens to audio during online meetings (Zoom, Teams, Google Meet), automatically detects the spoken language, translates it in real time, and shows live subtitles in the browser. Conversations are saved to your account and stay until you delete them.

---

## Features

- **Continuous audio recording** – Captures speech with no gaps
- **Automatic language detection** – Detects the spoken language
- **Real-time translation** – Translates to your chosen language with live subtitles
- **Saved conversations** – Every recording is auto-saved to your account; rename or delete from the sidebar
- **Voice Activity Detection (VAD)** – Skips silence and background noise
- **Account-based history** – Sign in with email/password or Google; your chats are private and synced across devices
- **Responsive UI** – Works in split-screen and narrow windows; hamburger menu opens saved chats

---

## Tech Stack

| Layer    | Stack |
|----------|--------|
| **Frontend** | React 19, TypeScript, Vite |
| **Backend**  | Python 3, FastAPI |
| **Auth & data** | Secure sign-in and cloud-synced chat history |
| **APIs**     | Speech-to-text and translation services |

---

## Project Structure

```
Global-Talk/
├── api_server.py              # API server: recording, STT, translation
├── main.py                    # (optional) legacy entry point
├── backend/
│   ├── config.py              # Settings and model config
│   ├── audio_manager.py       # Microphone capture, chunked recording
│   ├── vad_module.py          # Voice activity detection (filter noise)
│   ├── stt_module.py          # Speech-to-text
│   ├── stt_wrapper.py         # STT wrapper
│   ├── translation_module.py  # Translation
│   └── translation_wrapper.py # Translation wrapper
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main app, routing, recording state, save flow
│   │   ├── main.tsx
│   │   ├── components/        # Landing, auth, home, translation view, sidebar, etc.
│   │   ├── contexts/          # Auth context
│   │   ├── lib/               # API client and services
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
├── sessions/                  # Local session data (if used)
├── recordings/                # Temporary audio chunks from backend
└── README.md
```

---

## Access

Use the app by visiting the link (when available). Sign in, choose your subtitle language, and click **Start Meeting with Globe** to begin. Speak to see live translations; click **End Meeting** to stop. Conversations are auto-saved to your account—rename or manage them from the sidebar.

---

## How It Works

1. **Frontend** – User starts a meeting; the app calls the backend to start recording and polls for new messages.
2. **Backend** – Records audio in chunks, runs VAD to drop non-speech, sends speech to speech-to-text, then to translation. Returns messages to the frontend.
3. **Saving** – When the user ends the meeting, the current conversation is auto-saved under their account. They can rename it in the dialog or in the sidebar. Chats persist until the user deletes them.
4. **Sidebar** – The “three lines” hamburger (on small/split screen) opens the sidebar with saved chats; load, rename, or delete from there.

### Data flow

```
Microphone → Backend (chunks) → VAD → Speech-to-text → Translation → API → Frontend (live UI + saved chats)
```

---

## Scripts

| Command | Description |
|--------|-------------|
| `npm start` | Run backend + frontend together |
| `npm run backend` | Run API server only |
| `npm run frontend` | Run frontend dev server only |
| `cd frontend && npm run build` | Production build |
| `cd frontend && npm run preview` | Preview production build |

---

## Tips for Best Results

- Use a good microphone and reduce background noise.
- Speak clearly; stable internet is required for transcription and translation.
- On split-screen or narrow windows, use the hamburger menu (☰) to open saved chats.

---

## License

This project is for educational purposes. Use in compliance with applicable API and service terms.

---

## Acknowledgments

- Speech-to-text and translation services
- React + Vite for the frontend
- FastAPI for the backend API
