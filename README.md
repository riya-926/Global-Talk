# Global Chat – Real-Time Meeting Translator

A **web application** that listens to audio during online meetings (Zoom, Teams, Google Meet), automatically detects the spoken language, translates it in real time, and shows live subtitles in the browser. Conversations are saved to your account and stay until you delete them.

---

## Features

- **Continuous audio recording** – Captures speech with no gaps
- **Automatic language detection** – Detects the spoken language
- **Real-time translation** – Translates to your chosen language with live subtitles
- **Saved conversations** – Every recording is auto-saved to your account (Firestore); rename or delete from the sidebar
- **Voice Activity Detection (VAD)** – Skips silence and background noise
- **Account-based history** – Sign in with email/password or Google; your chats are private and synced across devices
- **Responsive UI** – Works in split-screen and narrow windows; hamburger menu opens saved chats

---

## Tech Stack

| Layer    | Stack |
|----------|--------|
| **Frontend** | React 19, TypeScript, Vite |
| **Backend**  | Python 3, FastAPI |
| **Auth & DB**| Firebase Auth, Firestore |
| **APIs**     | OpenAI Whisper (STT), OpenAI GPT (translation) |

---

## Project Structure

```
Global-Talk/
├── api_server.py              # FastAPI server: recording, STT, translation
├── main.py                    # (optional) legacy entry point
├── backend/
│   ├── config.py              # API keys, audio settings, model config
│   ├── audio_manager.py      # Microphone capture, chunked recording
│   ├── vad_module.py          # Voice activity detection (filter noise)
│   ├── stt_module.py          # Whisper speech-to-text
│   ├── stt_wrapper.py         # Wrapper around STT
│   ├── translation_module.py  # GPT-based translation
│   └── translation_wrapper.py # Wrapper around translation
├── frontend/
│   ├── src/
│   │   ├── App.tsx            # Main app, routing, recording state, save flow
│   │   ├── main.tsx
│   │   ├── components/
│   │   │   ├── LandingPage.tsx # Landing + hero
│   │   │   ├── Login.tsx / Signup.tsx
│   │   │   ├── Home.tsx       # Start meeting, language picker
│   │   │   ├── TranslationView.tsx  # Live conversation + RECORDING UI
│   │   │   ├── Sidebar.tsx    # Saved chats list (load, delete, rename)
│   │   │   ├── SaveDialog.tsx # Name/rename after stopping
│   │   │   ├── GlobeLogo.tsx
│   │   │   └── ...
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx
│   │   ├── lib/
│   │   │   ├── firebase.ts    # Firebase init, auth
│   │   │   ├── chats.ts       # Firestore: subscribe, save, delete, rename
│   │   │   └── api.ts         # HTTP client for backend
│   │   └── types/
│   ├── package.json
│   └── vite.config.ts
├── sessions/                  # (legacy) local session JSONs if any
├── recordings/                # Temporary WAV chunks from backend
├── FIREBASE_SETUP.md          # Firebase + Firestore setup
└── README.md
```

---

## Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.10+
- **Firebase project** (Auth + Firestore) – see [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)
- **OpenAI API key** – for Whisper and GPT

---

## Setup

### 1. Clone and install

```bash
git clone <repo-url>
cd Global-Talk
npm install
cd frontend && npm install && cd ..
```

### 2. Backend environment

Create a `.env` in the project root (or set env vars) with:

- `OPENAI_API_KEY` – your OpenAI API key (used by `backend/config.py`)

### 3. Frontend environment (Firebase)

In `frontend/`, create `.env` with your Firebase config:

```env
VITE_FIREBASE_API_KEY=...
VITE_FIREBASE_AUTH_DOMAIN=...
VITE_FIREBASE_PROJECT_ID=...
VITE_FIREBASE_STORAGE_BUCKET=...
VITE_FIREBASE_MESSAGING_SENDER_ID=...
VITE_FIREBASE_APP_ID=...
```

See [FIREBASE_SETUP.md](./FIREBASE_SETUP.md) for Auth and **Firestore** (saved chats), including:

- Creating the Firestore database and **composite index** for the `chats` collection (`userId` Ascending, `timestamp` Descending)
- Security rules so users only read/write their own chats

---

## How to Run

**Option A – Run both together (from repo root):**

```bash
npm start
```

This starts:

- **Backend:** `python api_server.py` (default port 8000)
- **Frontend:** `npm run dev --prefix frontend` (Vite, usually http://localhost:5173)

**Option B – Run separately:**

```bash
# Terminal 1 – backend
python api_server.py

# Terminal 2 – frontend
cd frontend && npm run dev
```

Then open http://localhost:5173 (or the port Vite prints), sign in, choose a language, and click **Start Meeting with Globe**. Speak to see live translations; click **End Meeting** to stop. The conversation is auto-saved to your account; you can rename it in the save dialog or later in the sidebar.

---

## How It Works

1. **Frontend** – User starts a meeting; the app calls the backend to start recording and polls for new messages.
2. **Backend** – Records audio in chunks, runs VAD to drop non-speech, sends speech to Whisper (STT + language detection), then to GPT for translation. Returns messages to the frontend.
3. **Saving** – When the user ends the meeting, the current conversation is auto-saved to Firestore under their `userId`. They can rename it in the dialog or in the sidebar. Chats persist until the user deletes them.
4. **Sidebar** – The “three lines” hamburger (on small/split screen) opens the sidebar with saved chats; load, rename, or delete from there.

### Data flow

```
Microphone → Backend (chunks) → VAD → Whisper (STT + lang) → GPT (translate) → API → Frontend (live UI)
                                                                                        → Firestore (save)
```

---

## Authentication & Saved Chats

- **Sign in** with email/password or Google. You must be signed in to save and see chats.
- **Saved chats** are stored in Firestore in the `chats` collection, keyed by `userId`. They sync across devices and stay until you delete them.
- **Firestore composite index** is required for the “Saved chats” list. If the list is empty and the console shows an index error, create the index (see [FIREBASE_SETUP.md](./FIREBASE_SETUP.md)).

---

## Scripts

| Command | Description |
|--------|-------------|
| `npm start` | Run backend + frontend together |
| `npm run backend` | Run FastAPI server only |
| `npm run frontend` | Run Vite dev server only |
| `cd frontend && npm run build` | Production build |
| `cd frontend && npm run preview` | Preview production build |

---

## Tips for Best Results

- Use a good microphone and reduce background noise.
- Speak clearly; stable internet is required for Whisper and GPT.
- On split-screen or narrow windows, use the hamburger menu (☰) to open saved chats.

---

## License

This project is for educational use. Comply with OpenAI’s usage policies and Firebase terms.

---

## Acknowledgments

- **OpenAI Whisper** – Speech-to-text and language detection  
- **OpenAI GPT** – Translation  
- **Firebase** – Auth and Firestore  
- **React + Vite** – Frontend  
- **FastAPI** – Backend API  
