"""
ui.py - Beautiful GUI for Global Chat

Features:
- Cream/off-white aesthetic
- Start screen with language selector
- Live translation screen with session history
- Auto-save recordings by date
- Modern, clean design
"""

import customtkinter as ctk
import datetime
import json
from pathlib import Path
from typing import Callable, Optional


# Color scheme
CREAM_BG = "#FAF9F6"
SOFT_BLUE = "#5B9BD5"
DARK_TEXT = "#2C3E50"
LIGHT_GRAY = "#E8E8E8"
WHITE = "#FFFFFF"
RECORDING_RED = "#E74C3C"


class GlobalChatUI:
    def __init__(self):
        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Global Chat")
        self.root.geometry("900x600")
        self.root.configure(fg_color=CREAM_BG)

        # Session data
        self.sessions_dir = Path("sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session_id = None
        self.current_translations = []

        # Callbacks (to be set by main.py)
        self.on_start_callback: Optional[Callable] = None
        self.on_stop_callback: Optional[Callable] = None

        # Start with home screen
        self.show_home_screen()

    def show_home_screen(self):
        """Display the initial start screen."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container
        container = ctk.CTkFrame(self.root, fg_color=CREAM_BG)
        container.pack(fill="both", expand=True)

        # Title with bubble letter style - trying Comic Sans for bubble effect
        title_label = ctk.CTkLabel(
            container,
            text="GLOBAL CHAT",
            font=("Comic Sans MS", 85, "bold"),  # Comic Sans has that bubble look
            text_color=SOFT_BLUE,
        )
        title_label.pack(pady=(100, 50))

        # Start button with shadow effect
        start_btn = ctk.CTkButton(
            container,
            text="🌍  Start Meeting with Globe",
            font=("Comic Sans MS", 20, "bold"),
            fg_color=SOFT_BLUE,
            hover_color="#4A8BC2",
            height=65,
            width=380,
            corner_radius=35,
            command=self.on_start_pressed
        )
        start_btn.pack(pady=25)

        # Language selector with "Subtitles:" label
        lang_frame = ctk.CTkFrame(container, fg_color=CREAM_BG)
        lang_frame.pack(pady=25)

        # "Subtitles:" label
        subtitle_label = ctk.CTkLabel(
            lang_frame,
            text="Subtitles:",
            font=("Comic Sans MS", 18, "bold"),
            text_color=DARK_TEXT
        )
        subtitle_label.pack(side="left", padx=(0, 15))

        # Language dropdown
        self.language_var = ctk.StringVar(value="English")
        language_options = [
            "English", "Spanish", "French", "German", "Italian",
            "Portuguese", "Russian", "Japanese", "Korean", "Chinese",
            "Arabic", "Hindi", "Urdu", "Turkish"
        ]

        self.lang_dropdown = ctk.CTkComboBox(
            lang_frame,
            values=language_options,
            variable=self.language_var,
            font=("Comic Sans MS", 16),
            width=220,
            height=40,
            fg_color=WHITE,
            button_color=SOFT_BLUE,
            border_color=SOFT_BLUE,
            border_width=2,
            corner_radius=20,
            dropdown_font=("Comic Sans MS", 14)
        )
        self.lang_dropdown.pack(side="left")

        # Globe decoration - bigger and more prominent
        globe_label = ctk.CTkLabel(
            container,
            text="🌍",
            font=("Arial", 140)
        )
        globe_label.pack(side="bottom", anchor="se", padx=40, pady=40)

    def show_translation_screen(self):
        """Display the active translation screen."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create new session (use dashes instead of slashes for Windows compatibility)
        self.current_session_id = datetime.datetime.now().strftime("%m-%d-%y_%H%M%S")
        self.current_translations = []

        # Main container with sidebar
        main_container = ctk.CTkFrame(self.root, fg_color=CREAM_BG)
        main_container.pack(fill="both", expand=True)

        # Left sidebar for previous chats
        self.sidebar = ctk.CTkFrame(main_container, width=200, fg_color=LIGHT_GRAY)
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Previous Chat",
            font=("Arial", 16, "bold"),
            text_color=DARK_TEXT
        )
        sidebar_title.pack(pady=20, padx=10)

        # Scrollable frame for chat history
        self.chat_history_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color=LIGHT_GRAY,
            width=180
        )
        self.chat_history_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Load and display previous sessions
        self.load_session_history()

        # Right side - main translation area
        right_container = ctk.CTkFrame(main_container, fg_color=CREAM_BG)
        right_container.pack(side="right", fill="both", expand=True)

        # Top bar with title and recording indicator
        top_bar = ctk.CTkFrame(right_container, fg_color=CREAM_BG, height=60)
        top_bar.pack(fill="x", padx=20, pady=10)
        top_bar.pack_propagate(False)

        title = ctk.CTkLabel(
            top_bar,
            text="GLOBAL CHAT",
            font=("Bahnschrift SemiBold", 32, "bold"),
            text_color=SOFT_BLUE
        )
        title.pack(side="left")

        self.recording_label = ctk.CTkLabel(
            top_bar,
            text="Recording ⏺",
            font=("Arial", 14, "bold"),
            text_color=RECORDING_RED
        )
        self.recording_label.pack(side="right", padx=10)

        # Scrollable translation display area
        self.translation_area = ctk.CTkScrollableFrame(
            right_container,
            fg_color=WHITE,
            corner_radius=15
        )
        self.translation_area.pack(fill="both", expand=True, padx=20, pady=10)

        # Bottom controls
        bottom_frame = ctk.CTkFrame(right_container, fg_color=CREAM_BG, height=80)
        bottom_frame.pack(fill="x", padx=20, pady=10)
        bottom_frame.pack_propagate(False)

        end_btn = ctk.CTkButton(
            bottom_frame,
            text="END CHAT",
            font=("Bahnschrift SemiBold", 18, "bold"),
            fg_color=DARK_TEXT,
            hover_color="#1A252F",
            height=55,
            width=220,
            corner_radius=28,
            command=self.on_end_pressed
        )
        end_btn.pack(side="bottom", pady=15)

    def add_translation(self, original: str, translated: str, detected_lang: str):
        """Add a new translation to the display."""
        timestamp = datetime.datetime.now().strftime("%I:%M %p")

        # Store in current session
        self.current_translations.append({
            "timestamp": timestamp,
            "detected_lang": detected_lang,
            "original": original,
            "translated": translated
        })

        # Create translation card with subtle shadow effect
        card = ctk.CTkFrame(
            self.translation_area,
            fg_color=CREAM_BG,
            corner_radius=15,
            border_width=1,
            border_color=LIGHT_GRAY
        )
        card.pack(fill="x", padx=15, pady=12)

        # Detected language with nicer styling
        lang_label = ctk.CTkLabel(
            card,
            text=f"🗣️  Detected: {detected_lang.title()}",
            font=("Bahnschrift", 13, "bold"),
            text_color=SOFT_BLUE
        )
        lang_label.pack(anchor="w", padx=20, pady=(15, 5))

        # Original text with better styling
        original_label = ctk.CTkLabel(
            card,
            text=f"Original: {original}",
            font=("Bahnschrift", 14),
            text_color=DARK_TEXT,
            wraplength=600,
            justify="left"
        )
        original_label.pack(anchor="w", padx=20, pady=3)

        # Timestamp and translated with better styling
        bottom_frame = ctk.CTkFrame(card, fg_color=CREAM_BG)
        bottom_frame.pack(fill="x", padx=20, pady=(8, 15))

        translated_label = ctk.CTkLabel(
            bottom_frame,
            text=f"●●● ",
            font=("Bahnschrift", 15, "bold"),
            text_color=SOFT_BLUE
        )
        translated_label.pack(side="left")

        # Animate dots then show translation
        self.root.after(500, lambda: self.show_translation(translated_label, translated, timestamp))

        # Auto-scroll to bottom
        self.translation_area._parent_canvas.yview_moveto(1.0)

    def show_translation(self, label, translated: str, timestamp: str):
        """Replace loading dots with actual translation."""
        label.configure(text=f"{translated}  •  {timestamp}")

    def load_session_history(self):
        """Load and display previous session dates."""
        # Clear existing
        for widget in self.chat_history_frame.winfo_children():
            widget.destroy()

        # Get all session files
        session_files = sorted(self.sessions_dir.glob("session_*.json"), reverse=True)

        for session_file in session_files[:10]:  # Show last 10
            # Parse date from filename (format: session_11-28-25_023142.json)
            date_str = session_file.stem.replace("session_", "")
            display_date = date_str.split("_")[0]  # Get the date part (11-28-25)

            btn = ctk.CTkButton(
                self.chat_history_frame,
                text=display_date,
                font=("Arial", 12),
                fg_color=WHITE,
                text_color=DARK_TEXT,
                hover_color=LIGHT_GRAY,
                height=35,
                corner_radius=8,
                command=lambda f=session_file: self.load_session(f)
            )
            btn.pack(fill="x", pady=5)

    def load_session(self, session_file: Path):
        """Load a previous session (placeholder for now)."""
        # TODO: Implement viewing old sessions
        print(f"Loading session: {session_file}")

    def save_current_session(self):
        """Save the current session to a JSON file."""
        if not self.current_translations:
            print("⚠️  No translations to save.")
            return

        try:
            # Ensure sessions directory exists
            self.sessions_dir.mkdir(exist_ok=True)

            filename = self.sessions_dir / f"session_{self.current_session_id}.json"

            session_data = {
                "session_id": self.current_session_id,
                "target_language": self.language_var.get(),
                "translations": self.current_translations,
                "date": datetime.datetime.now().isoformat()
            }

            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Session saved: {filename}")
        except Exception as e:
            print(f"❌ Error saving session: {e}")

    def on_start_pressed(self):
        """Handle start button press."""
        target_lang = self.language_var.get().lower()
        self.show_translation_screen()

        # Call external callback if set
        if self.on_start_callback:
            self.on_start_callback(target_lang)

    def on_end_pressed(self):
        """Handle end chat button press."""
        try:
            # Save session first (don't let errors stop the shutdown)
            self.save_current_session()
        except Exception as e:
            print(f"⚠️  Error saving session: {e}")

        # Call external callback to stop recording
        if self.on_stop_callback:
            try:
                self.on_stop_callback()
            except Exception as e:
                print(f"⚠️  Error stopping recording: {e}")

        # Always return to home screen
        self.show_home_screen()

    def run(self):
        """Start the UI main loop."""
        self.root.mainloop()


# Test the UI standalone
if __name__ == "__main__":
    app = GlobalChatUI()

    # Test with mock translations
    def add_test_data():
        app.show_translation_screen()
        app.root.after(1000, lambda: app.add_translation(
            "Bonjour, comment allez-vous?",
            "Hello, how are you?",
            "French"
        ))
        app.root.after(3000, lambda: app.add_translation(
            "Je vais bien, merci!",
            "I'm doing well, thank you!",
            "French"
        ))

    # Uncomment to test:
    # app.root.after(1000, add_test_data)

    app.run()