# Firebase Authentication Setup Guide

This project now includes Firebase authentication with email/password and Google sign-in. Follow these steps to set it up:

## Step 1: Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Click "Add project" or select an existing project
3. Follow the setup wizard

## Step 2: Enable Authentication

1. In your Firebase project, go to **Authentication** > **Sign-in method**
2. Enable **Email/Password** authentication
3. Enable **Google** authentication:
   - Click on Google
   - Toggle "Enable"
   - Add your project's support email
   - Click "Save"

## Step 3: Get Your Firebase Config

1. Go to **Project Settings** (gear icon)
2. Scroll down to "Your apps"
3. Click the web icon (`</>`) to add a web app
4. Register your app (you can name it "Global Chat")
5. Copy the Firebase configuration object

## Step 4: Configure Environment Variables

1. Create a `.env` file in the `frontend` directory
2. Add your Firebase configuration:

```env
VITE_FIREBASE_API_KEY=your-api-key-here
VITE_FIREBASE_AUTH_DOMAIN=your-project.firebaseapp.com
VITE_FIREBASE_PROJECT_ID=your-project-id
VITE_FIREBASE_STORAGE_BUCKET=your-project.appspot.com
VITE_FIREBASE_MESSAGING_SENDER_ID=your-sender-id
VITE_FIREBASE_APP_ID=your-app-id
```

Replace the placeholder values with your actual Firebase config values.

## Step 5: Update Authorized Domains (for Google Sign-in)

1. In Firebase Console, go to **Authentication** > **Settings**
2. Under "Authorized domains", make sure `localhost` is listed
3. For production, add your domain

## Step 6: Test the Setup

1. Start your frontend: `cd frontend && npm run dev`
2. You should see the login page
3. Try creating an account or signing in with Google

## Troubleshooting

- **"Firebase: Error (auth/unauthorized-domain)"**: Make sure `localhost` is in your authorized domains
- **"Firebase: Error (auth/api-key-not-valid)"**: Double-check your API key in the `.env` file
- **Google sign-in not working**: Ensure Google authentication is enabled in Firebase Console

## Firestore: Saved Chats (sync across devices)

Saved conversations are stored in Firestore so each user only sees their own chats, and they sync across devices.

### Step 1: Create a Firestore database

1. In Firebase Console, go to **Build** > **Firestore Database**
2. Click **Create database**
3. Choose **Start in test mode** (we'll add security rules next), then pick a location

### Step 2: Security rules

1. In Firestore, open the **Rules** tab
2. Replace the rules with:

```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /chats/{chatId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
      allow create: if request.auth != null && request.resource.data.userId == request.auth.uid;
    }
  }
}
```

3. Click **Publish**

This lets users read/write only documents where `userId` matches their own UID.

### Step 3: Composite index (required for listing chats)

Without this index, the "Saved chats" list will stay empty and the console will show a Firestore error.

1. In Firebase Console go to **Firestore** > **Indexes** > **Composite** > **Create index**
2. Collection ID: `chats`
3. Add fields: `userId` (Ascending), `timestamp` (Descending)
4. Create the index (it may take a few minutes to build)

Alternatively, run the app and open the sidebar once; if the console shows a Firestore error with a **link to create an index**, open that link and create the index.

### Migration from localStorage

If a user had chats stored locally before, the app will move them into Firestore once when they next log in. After that, only Firestore is used.

## Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- For production, use environment variables on your hosting platform
