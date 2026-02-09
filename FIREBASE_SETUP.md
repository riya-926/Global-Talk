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

## Security Notes

- Never commit your `.env` file to version control
- The `.env` file is already in `.gitignore`
- For production, use environment variables on your hosting platform
