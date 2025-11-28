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

        # Title
        title_label = ctk.CTkLabel(
            container,
            text="GLOBAL CHAT",
            font=("Arial", 72, "bold"),
            text_color=SOFT_BLUE
        )
        title_label.pack(pady=(80, 40))

        # Start button
        start_btn = ctk.CTkButton(
            container,
            text="🌍 Start Meeting with Globe",
            font=("Arial", 18),
            fg_color=SOFT_BLUE,
            hover_color="#4A8BC2",
            height=60,
            width=350,
            corner_radius=30,
            command=self.on_start_pressed
        )
        start_btn.pack(pady=20)

        # Language selector frame
        lang_frame = ctk.CTkFrame(container, fg_color=CREAM_BG)
        lang_frame.pack(pady=20)

        lang_label = ctk.CTkLabel(
            lang_frame,
            text="Record Subtitle: Select Language 🌍",
            font=("Arial", 14),
            text_color=DARK_TEXT
        )
        lang_label.pack(side="left", padx=10)

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
            font=("Arial", 14),
            width=200,
            fg_color=WHITE,
            button_color=SOFT_BLUE,
            border_color=LIGHT_GRAY
        )
        self.lang_dropdown.pack(side="left", padx=10)

        # Globe decoration (emoji as placeholder)
        globe_label = ctk.CTkLabel(
            container,
            text="🌍",
            font=("Arial", 120)
        )
        globe_label.pack(side="bottom", anchor="se", padx=30, pady=30)

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
            font=("Arial", 28, "bold"),
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
            font=("Arial", 16, "bold"),
            fg_color=DARK_TEXT,
            hover_color="#1A252F",
            height=50,
            width=200,
            corner_radius=25,
            command=self.on_end_pressed
        )
        end_btn.pack(side="bottom", pady=10)

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

        # Create translation card
        card = ctk.CTkFrame(
            self.translation_area,
            fg_color=CREAM_BG,
            corner_radius=10
        )
        card.pack(fill="x", padx=10, pady=10)

        # Detected language
        lang_label = ctk.CTkLabel(
            card,
            text=f"Detected: {detected_lang}",
            font=("Arial", 12, "bold"),
            text_color=SOFT_BLUE
        )
        lang_label.pack(anchor="w", padx=15, pady=(10, 5))

        # Original text
        original_label = ctk.CTkLabel(
            card,
            text=f"Original: {original}",
            font=("Arial", 13),
            text_color=DARK_TEXT,
            wraplength=550,
            justify="left"
        )
        original_label.pack(anchor="w", padx=15, pady=2)

        # Timestamp and translated on same line
        bottom_frame = ctk.CTkFrame(card, fg_color=CREAM_BG)
        bottom_frame.pack(fill="x", padx=15, pady=(5, 10))

        translated_label = ctk.CTkLabel(
            bottom_frame,
            text=f"●●● ",
            font=("Arial", 14),
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
            # Parse date from filename
            date_str = session_file.stem.replace("session_", "")
            display_date = date_str.split("_")[0]  # Just the date part

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
            return

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

    def on_start_pressed(self):
        """Handle start button press."""
        target_lang = self.language_var.get().lower()
        self.show_translation_screen()

        # Call external callback if set
        if self.on_start_callback:
            self.on_start_callback(target_lang)

    def on_end_pressed(self):
        """Handle end chat button press."""
        # Save session
        self.save_current_session()

        # Call external callback if set
        if self.on_stop_callback:
            self.on_stop_callback()

        # Return to home screen
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