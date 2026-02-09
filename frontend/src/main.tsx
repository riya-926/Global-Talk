import React from 'react'
import ReactDOM from 'react-dom/client'

const root = document.getElementById('root')!

async function loadApp() {
    try {
        const { AuthProvider } = await import('./contexts/AuthContext')
        const { default: App } = await import('./App.tsx')
        const { ErrorBoundary } = await import('./ErrorBoundary')

        ReactDOM.createRoot(root).render(
            <React.StrictMode>
                <ErrorBoundary>
                    <AuthProvider>
                        <App />
                    </AuthProvider>
                </ErrorBoundary>
            </React.StrictMode>,
        )
    } catch (err) {
        root.innerHTML = `
            <div style="padding: 40px; font-family: sans-serif; max-width: 600px; margin: 50px auto;">
                <h2>Failed to load app</h2>
                <pre style="background: #f5f5f5; padding: 16px; overflow: auto;">${err instanceof Error ? err.message : String(err)}</pre>
                <p>Check the browser console (F12) for more details.</p>
            </div>
        `
        console.error('App load error:', err)
    }
}

loadApp()