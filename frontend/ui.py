"""
ui.py - Dreamy & Sleek UI for Global Chat

Features:
- Animated gradient background
- Soft floating animations
- Gentle glow effects with TRUE transparency
- Professional, minimal design
- Smooth transitions
"""

import customtkinter as ctk
from customtkinter import CTkInputDialog
import datetime
import json
from pathlib import Path
from typing import Callable, Optional
import math
from PIL import Image, ImageDraw


# Dreamy & Sleek Color Palette
BG_START = "#E8EAF6"      # Soft lavender
BG_END = "#F5F7FA"        # Soft white-blue
GLASS_BG = "#FFFFFF"      # Pure white
ACCENT_PRIMARY = "#7C3AED"  # Dreamy purple
ACCENT_LIGHT = "#A78BFA"    # Light purple
ACCENT_HOVER = "#6D28D9"    # Deep purple
TEXT_PRIMARY = "#1F2937"    # Almost black
TEXT_SECONDARY = "#6B7280"  # Soft gray
RECORDING_RED = "#EF4444"   # Soft red
GLOW_COLOR = "#DDD6FE"      # Soft purple glow


class GlobalChatUI:
    def __init__(self):
        # Set appearance
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        # Create main window
        self.root = ctk.CTk()
        self.root.title("Global Chat")
        self.root.geometry("900x580")
        self.root.configure(fg_color=BG_START)
        # keep UI from stretching ugly in fullscreen
        self.root.resizable(False, False)

        # Session data
        self.sessions_dir = Path("sessions")
        self.sessions_dir.mkdir(exist_ok=True)
        self.current_session_id: Optional[str] = None
        self.current_translations: list[dict] = []
        self.current_session_title: Optional[str] = None

        # Callbacks (set from main.py)
        self.on_start_callback: Optional[Callable] = None
        self.on_stop_callback: Optional[Callable] = None

        # Animation state
        self.bg_phase = 0
        self.float_offset = 0

        # Create transparent shadow images
        self.create_shadow_images()

        # Start with home screen
        self.show_home_screen()

    # ------------------------------------------------------------------
    # Visual helpers
    # ------------------------------------------------------------------
    def create_shadow_images(self):
        """Create transparent shadow/glow images using PIL."""
        # Soft shadow for cards
        shadow_size = (520, 270)
        self.card_shadow = Image.new("RGBA", shadow_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.card_shadow)
        for i in range(8):
            opacity = int(20 - i * 2.5)
            draw.rounded_rectangle(
                [i, i, shadow_size[0] - i, shadow_size[1] - i],
                radius=30 - i,
                fill=(0, 0, 0, opacity),
            )

        # Soft glow for button
        glow_size = (360, 85)
        self.button_glow = Image.new("RGBA", glow_size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(self.button_glow)
        for i in range(10):
            opacity = int(15 - i * 1.5)
            draw.rounded_rectangle(
                [i, i, glow_size[0] - i, glow_size[1] - i],
                radius=25 - i,
                fill=(91, 155, 213, opacity),  # bluish glow
            )

    def animate_background(self):
        """Subtle background gradient animation."""
        if not hasattr(self, "main_container") or not self.main_container.winfo_exists():
            return

        try:
            self.bg_phase = (self.bg_phase + 0.02) % (2 * math.pi)
            shift = int(8 * math.sin(self.bg_phase))

            r1, g1, b1 = 232, 234, 246
            new_r = max(0, min(255, r1 + shift))
            new_g = max(0, min(255, g1 + shift))
            new_b = max(0, min(255, b1 + shift))
            new_color = f"#{new_r:02x}{new_g:02x}{new_b:02x}"

            self.main_container.configure(fg_color=new_color)
            self.root.after(50, self.animate_background)
        except Exception:
            return

    def float_animation(self, widget):
        """Gentle floating animation for an element."""
        if not widget.winfo_exists():
            return

        try:
            self.float_offset = (self.float_offset + 0.05) % (2 * math.pi)
            offset = int(8 * math.sin(self.float_offset))

            current_y = widget.winfo_y()
            base_y = getattr(widget, "_base_y", current_y)
            widget.place(x=widget.winfo_x(), y=base_y + offset)

            self.root.after(50, lambda: self.float_animation(widget))
        except Exception:
            return

    # ------------------------------------------------------------------
    # HOME SCREEN
    # ------------------------------------------------------------------
    def show_home_screen(self):
        """Display dreamy home screen with tighter layout and Previous Chats."""
        # Clear window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Main container with animated gradient
        self.main_container = ctk.CTkFrame(self.root, fg_color=BG_START)
        self.main_container.pack(fill="both", expand=True)

        # Start background animation
        self.animate_background()

        # Centered content cluster
        content = ctk.CTkFrame(self.main_container, fg_color="transparent")
        content.pack(expand=True)

        # Title
        title_label = ctk.CTkLabel(
            content,
            text="GLOBAL CHAT",
            font=("Segoe UI", 60, "bold"),
            text_color=ACCENT_PRIMARY,
        )
        title_label.pack(pady=(0, 10))

        # Tagline
        tagline = ctk.CTkLabel(
            content,
            text="Real-time subtitles for any language.",
            font=("Segoe UI", 16),
            text_color=TEXT_SECONDARY,
        )
        tagline.pack(pady=(0, 18))

        # Card wrapper (shadow + glass)
        card_frame = ctk.CTkFrame(content, fg_color="transparent", width=520, height=260)
        card_frame.pack(pady=5)
        card_frame.pack_propagate(False)

        shadow_img = ctk.CTkImage(
            light_image=self.card_shadow,
            dark_image=self.card_shadow,
            size=(520, 270),
        )
        shadow_label = ctk.CTkLabel(card_frame, image=shadow_img, text="")
        shadow_label.place(x=0, y=0)

        glass_card = ctk.CTkFrame(
            card_frame,
            fg_color=GLASS_BG,
            corner_radius=30,
            border_width=1,
            border_color="#E5E7EB",
            width=500,
            height=240,
        )
        glass_card.place(x=10, y=10)
        glass_card.pack_propagate(False)

        # Start button with glow
        btn_container = ctk.CTkFrame(
            glass_card, fg_color="transparent", width=360, height=80
        )
        btn_container.pack(pady=(30, 10))
        btn_container.pack_propagate(False)

        glow_img = ctk.CTkImage(
            light_image=self.button_glow,
            dark_image=self.button_glow,
            size=(360, 85),
        )
        glow_label = ctk.CTkLabel(btn_container, image=glow_img, text="")
        glow_label.place(x=0, y=0)

        start_btn = ctk.CTkButton(
            btn_container,
            text="🌍  Start Meeting",
            font=("Segoe UI", 18, "bold"),
            fg_color=ACCENT_PRIMARY,
            hover_color=ACCENT_HOVER,
            text_color="white",
            height=60,
            width=340,
            corner_radius=20,
            border_width=0,
            command=self.on_start_pressed,
        )
        start_btn.place(x=10, y=10)

        # Helper text
        helper_text = ctk.CTkLabel(
            glass_card,
            text="Choose your subtitle language and hit Start.",
            font=("Segoe UI", 12),
            text_color=TEXT_SECONDARY,
        )
        helper_text.pack(pady=(0, 8))

        # Subtitles row
        subtitle_frame = ctk.CTkFrame(glass_card, fg_color="transparent")
        subtitle_frame.pack(pady=(0, 10))

        subtitle_label = ctk.CTkLabel(
            subtitle_frame,
            text="Subtitles",
            font=("Segoe UI", 14),
            text_color=TEXT_SECONDARY,
        )
        subtitle_label.pack(side="left", padx=(0, 10))

        self.language_var = ctk.StringVar(value="English")
        language_options = [
            "English",
            "Spanish",
            "French",
            "German",
            "Italian",
            "Portuguese",
            "Russian",
            "Japanese",
            "Korean",
            "Chinese",
            "Arabic",
            "Hindi",
            "Urdu",
            "Turkish",
        ]

        self.lang_dropdown = ctk.CTkComboBox(
            subtitle_frame,
            values=language_options,
            variable=self.language_var,
            font=("Segoe UI", 14),
            width=190,
            height=40,
            fg_color="white",
            button_color=ACCENT_PRIMARY,
            border_color="#D1D5DB",
            border_width=1,
            corner_radius=12,
            dropdown_font=("Segoe UI", 13),
        )
        self.lang_dropdown.pack(side="left")

        # ===== Previous Chats section on home =====
        prev_label = ctk.CTkLabel(
            content,
            text="Previous Chats",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_PRIMARY,
        )
        prev_label.pack(anchor="w", pady=(18, 4), padx=40)

        self.home_prev_frame = ctk.CTkScrollableFrame(
            content,
            fg_color="transparent",
            width=520,
            height=120,
        )
        self.home_prev_frame.pack(pady=(0, 10), padx=40, fill="x")
        self.home_prev_frame.pack_propagate(False)

        self.load_recent_sessions_for_home()

        # Footer + globe
        footer = ctk.CTkLabel(
            self.main_container,
            text="Powered by OpenAI Whisper & GPT",
            font=("Segoe UI", 10),
            text_color=TEXT_SECONDARY,
        )
        footer.place(relx=0.97, rely=0.96, anchor="se")

        globe_label = ctk.CTkLabel(
            self.main_container,
            text="🌍",
            font=("Segoe UI", 70),
        )
        globe_label.place(relx=0.9, rely=0.88, anchor="center")
        globe_label._base_y = int(0.88 * 580)
        self.root.after(100, lambda: self.float_animation(globe_label))

    # ------------------------------------------------------------------
    # TRANSLATION SCREEN
    # ------------------------------------------------------------------
    def show_translation_screen(self):
        """Display dreamy translation screen."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.current_session_id = datetime.datetime.now().strftime("%m-%d-%y_%H%M%S")
        self.current_translations = []
        self.current_session_title = None

        self.main_container = ctk.CTkFrame(self.root, fg_color=BG_START)
        self.main_container.pack(fill="both", expand=True)

        self.animate_background()

        # Sidebar
        self.sidebar = ctk.CTkFrame(
            self.main_container,
            width=220,
            fg_color=GLASS_BG,
            border_width=0,
            corner_radius=0,
        )
        self.sidebar.pack(side="left", fill="y", padx=0, pady=0)
        self.sidebar.pack_propagate(False)

        sidebar_title = ctk.CTkLabel(
            self.sidebar,
            text="Previous Sessions",
            font=("Segoe UI", 14, "bold"),
            text_color=TEXT_PRIMARY,
        )
        sidebar_title.pack(pady=25, padx=15)

        self.chat_history_frame = ctk.CTkScrollableFrame(
            self.sidebar,
            fg_color="transparent",
            width=190,
        )
        self.chat_history_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.load_session_history()

        # Right container
        right_container = ctk.CTkFrame(self.main_container, fg_color="transparent")
        right_container.pack(side="right", fill="both", expand=True)

        # Top bar
        top_bar = ctk.CTkFrame(
            right_container,
            fg_color=GLASS_BG,
            height=80,
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB",
        )
        top_bar.pack(fill="x", padx=20, pady=20)
        top_bar.pack_propagate(False)

        title = ctk.CTkLabel(
            top_bar,
            text="GLOBAL CHAT",
            font=("Segoe UI", 26, "bold"),
            text_color=ACCENT_PRIMARY,
        )
        title.pack(side="left", padx=25)

        rec_frame = ctk.CTkFrame(top_bar, fg_color="transparent")
        rec_frame.pack(side="right", padx=25)

        self.recording_dot = ctk.CTkLabel(
            rec_frame,
            text="●",
            font=("Segoe UI", 14),
            text_color=RECORDING_RED,
        )
        self.recording_dot.pack(side="left", padx=(0, 8))

        self.recording_label = ctk.CTkLabel(
            rec_frame,
            text="Recording",
            font=("Segoe UI", 13),
            text_color=TEXT_PRIMARY,
        )
        self.recording_label.pack(side="left")

        self.pulse_recording_dot()

        # Translation area
        translation_container = ctk.CTkFrame(
            right_container,
            fg_color=GLASS_BG,
            corner_radius=20,
            border_width=1,
            border_color="#E5E7EB",
        )
        translation_container.pack(fill="both", expand=True, padx=20, pady=(0, 15))

        self.translation_area = ctk.CTkScrollableFrame(
            translation_container,
            fg_color="transparent",
        )
        self.translation_area.pack(fill="both", expand=True, padx=5, pady=5)

        # Bottom controls
        bottom_frame = ctk.CTkFrame(right_container, fg_color="transparent", height=80)
        bottom_frame.pack(fill="x", padx=20, pady=(0, 20))
        bottom_frame.pack_propagate(False)

        end_btn = ctk.CTkButton(
            bottom_frame,
            text="End Chat",
            font=("Segoe UI", 16, "bold"),
            fg_color=TEXT_PRIMARY,
            hover_color="#111827",
            text_color="white",
            height=55,
            width=180,
            corner_radius=18,
            command=self.on_end_pressed,
        )
        end_btn.pack(pady=12)

    # ------------------------------------------------------------------
    # Animations & cards
    # ------------------------------------------------------------------
    def pulse_recording_dot(self):
        """Gentle pulse animation for recording dot."""
        if not hasattr(self, "recording_dot") or not self.recording_dot.winfo_exists():
            return

        try:
            current = self.recording_dot.cget("text_color")
            if current == RECORDING_RED:
                self.recording_dot.configure(text_color="#FCA5A5")
            else:
                self.recording_dot.configure(text_color=RECORDING_RED)
            self.root.after(800, self.pulse_recording_dot)
        except Exception:
            return

    def add_translation(self, original: str, translated: str, detected_lang: str):
        """Add a translation card to the scroll area."""
        timestamp = datetime.datetime.now().strftime("%I:%M %p")

        self.current_translations.append(
            {
                "timestamp": timestamp,
                "detected_lang": detected_lang,
                "original": original,
                "translated": translated,
            }
        )

        card = ctk.CTkFrame(
            self.translation_area,
            fg_color="white",
            corner_radius=16,
            border_width=1,
            border_color="#E5E7EB",
        )
        card.pack(fill="x", padx=15, pady=10)

        lang_badge = ctk.CTkFrame(
            card,
            fg_color=ACCENT_LIGHT,
            corner_radius=10,
            height=26,
        )
        lang_badge.pack(anchor="w", padx=20, pady=(16, 8))

        lang_label = ctk.CTkLabel(
            lang_badge,
            text=f"  {detected_lang.title()}  ",
            font=("Segoe UI", 10, "bold"),
            text_color="white",
        )
        lang_label.pack(padx=10, pady=2)

        original_label = ctk.CTkLabel(
            card,
            text=original,
            font=("Segoe UI", 13),
            text_color=TEXT_SECONDARY,
            wraplength=650,
            justify="left",
            anchor="w",
        )
        original_label.pack(anchor="w", padx=20, pady=(4, 8))

        translated_label = ctk.CTkLabel(
            card,
            text="...",
            font=("Segoe UI", 16, "bold"),
            text_color=TEXT_PRIMARY,
            wraplength=650,
            justify="left",
            anchor="w",
        )
        translated_label.pack(anchor="w", padx=20, pady=(0, 8))

        time_label = ctk.CTkLabel(
            card,
            text=timestamp,
            font=("Segoe UI", 10),
            text_color=TEXT_SECONDARY,
        )
        time_label.pack(anchor="e", padx=20, pady=(0, 14))

        self.root.after(300, lambda: translated_label.configure(text=translated))
        self.translation_area._parent_canvas.yview_moveto(1.0)

    # ------------------------------------------------------------------
    # Session history & saving
    # ------------------------------------------------------------------
    def load_recent_sessions_for_home(self, max_sessions: int = 6):
        """Show recent sessions in the home screen 'Previous Chats' section."""
        # Clear existing
        for widget in self.home_prev_frame.winfo_children():
            widget.destroy()

        if not self.sessions_dir.exists():
            empty_label = ctk.CTkLabel(
                self.home_prev_frame,
                text="No chats yet. Your sessions will appear here.",
                font=("Segoe UI", 11),
                text_color=TEXT_SECONDARY,
            )
            empty_label.pack(anchor="w", padx=4, pady=4)
            return

        # Find all session_*.json in all date folders
        session_files: list[Path] = []
        for date_dir in self.sessions_dir.iterdir():
            if date_dir.is_dir():
                session_files.extend(sorted(date_dir.glob("session_*.json")))

        if not session_files:
            empty_label = ctk.CTkLabel(
                self.home_prev_frame,
                text="No chats yet. Your sessions will appear here.",
                font=("Segoe UI", 11),
                text_color=TEXT_SECONDARY,
            )
            empty_label.pack(anchor="w", padx=4, pady=4)
            return

        # Sort by last modified (newest first)
        session_files = sorted(session_files, key=lambda f: f.stat().st_mtime, reverse=True)

        for session_file in session_files[:max_sessions]:
            # Load JSON
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                title = data.get("title")
                date_iso = data.get("date")
                if date_iso:
                    try:
                        dt = datetime.datetime.fromisoformat(date_iso)
                        date_str = dt.strftime("%b %d, %Y • %I:%M %p").lstrip("0")
                    except Exception:
                        date_str = date_iso
                else:
                    date_str = session_file.parent.name
            except Exception:
                title = None
                date_str = session_file.parent.name

            if not title:
                # fallback from filename
                time_part = session_file.stem.replace("session_", "")
                title = f"Session {time_part[:2]}:{time_part[2:4]}"

            btn = ctk.CTkButton(
                self.home_prev_frame,
                text=f"{title}\n{date_str}",
                font=("Segoe UI", 11),
                fg_color="white",
                text_color=TEXT_PRIMARY,
                hover_color="#F3F4F6",
                height=46,
                corner_radius=10,
                border_width=1,
                border_color="#E5E7EB",
                anchor="w",
                command=lambda f=session_file: self.open_session_from_home(f),
            )
            btn.pack(fill="x", padx=4, pady=3)

    def load_session_history(self):
        """Load previous sessions, grouped by date, showing custom titles in sidebar."""
        for widget in self.chat_history_frame.winfo_children():
            widget.destroy()

        if not self.sessions_dir.exists():
            return

        # Date folders: sessions/YYYY-MM-DD
        date_dirs = sorted(
            [p for p in self.sessions_dir.iterdir() if p.is_dir()],
            reverse=True,
        )

        for date_dir in date_dirs:
            date_str = date_dir.name
            try:
                dt = datetime.datetime.strptime(date_str, "%Y-%m-%d")
                pretty_date = dt.strftime("%b %d, %Y")
            except ValueError:
                pretty_date = date_str

            header = ctk.CTkLabel(
                self.chat_history_frame,
                text=pretty_date,
                font=("Segoe UI", 12, "bold"),
                text_color=TEXT_PRIMARY,
            )
            header.pack(anchor="w", padx=6, pady=(10, 2))

            session_files = sorted(date_dir.glob("session_*.json"), reverse=True)

            for session_file in session_files:
                # Read JSON to get stored title
                title = None
                try:
                    with open(session_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    title = data.get("title")
                except Exception:
                    pass

                time_part = session_file.stem.replace("session_", "")  # "HHMMSS"
                fallback_time = time_part[:2] + ":" + time_part[2:4]
                display_text = title or fallback_time

                btn = ctk.CTkButton(
                    self.chat_history_frame,
                    text=display_text,
                    font=("Segoe UI", 11),
                    fg_color="white",
                    text_color=TEXT_PRIMARY,
                    hover_color="#F3F4F6",
                    height=32,
                    corner_radius=10,
                    border_width=1,
                    border_color="#E5E7EB",
                    anchor="w",
                    command=lambda f=session_file: self.load_session(f, render=True),
                )
                btn.pack(fill="x", padx=10, pady=2)

    def load_session(self, session_file: Path, render: bool = False):
        """Load a previous session; optionally render messages."""
        print(f"Loading session: {session_file}")

        try:
            with open(session_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Error reading session file: {e}")
            return

        self.current_session_id = data.get("session_id")
        self.current_session_title = data.get("title")
        translations = data.get("translations", [])

        if not render:
            return

        if not hasattr(self, "translation_area"):
            print("⚠️ No translation area to render into.")
            return

        # Clear current UI cards
        for widget in self.translation_area.winfo_children():
            widget.destroy()

        self.current_translations = translations

        # Rebuild cards from stored data
        for item in translations:
            original = item.get("original", "")
            translated = item.get("translated", "")
            detected_lang = item.get("detected_lang", "unknown")

            card = ctk.CTkFrame(
                self.translation_area,
                fg_color="white",
                corner_radius=16,
                border_width=1,
                border_color="#E5E7EB",
            )
            card.pack(fill="x", padx=15, pady=10)

            lang_badge = ctk.CTkFrame(
                card,
                fg_color=ACCENT_LIGHT,
                corner_radius=10,
                height=26,
            )
            lang_badge.pack(anchor="w", padx=20, pady=(16, 8))

            lang_label = ctk.CTkLabel(
                lang_badge,
                text=f"  {detected_lang.title()}  ",
                font=("Segoe UI", 10, "bold"),
                text_color="white",
            )
            lang_label.pack(padx=10, pady=2)

            original_label = ctk.CTkLabel(
                card,
                text=original,
                font=("Segoe UI", 13),
                text_color=TEXT_SECONDARY,
                wraplength=650,
                justify="left",
                anchor="w",
            )
            original_label.pack(anchor="w", padx=20, pady=(4, 8))

            translated_label = ctk.CTkLabel(
                card,
                text=translated,
                font=("Segoe UI", 16, "bold"),
                text_color=TEXT_PRIMARY,
                wraplength=650,
                justify="left",
                anchor="w",
            )
            translated_label.pack(anchor="w", padx=20, pady=(0, 8))

            ts = item.get("timestamp")
            time_label = ctk.CTkLabel(
                card,
                text=ts if ts else "",
                font=("Segoe UI", 10),
                text_color=TEXT_SECONDARY,
            )
            time_label.pack(anchor="e", padx=20, pady=(0, 14))

        self.translation_area._parent_canvas.yview_moveto(1.0)

    def save_current_session(self):
        """Save current session into a date-based folder, with optional title."""
        if not self.current_translations:
            return

        try:
            now = datetime.datetime.now()
            date_str = now.strftime("%Y-%m-%d")   # e.g. 2025-02-26
            time_str = now.strftime("%H%M%S")     # e.g. 231530

            # Directory for that date
            date_dir = self.sessions_dir / date_str
            date_dir.mkdir(parents=True, exist_ok=True)

            # File path
            filename = date_dir / f"session_{time_str}.json"

            # Final title: user input or fallback
            fallback_title = time_str[:2] + ":" + time_str[2:4]
            title = self.current_session_title or fallback_title

            self.current_session_id = f"{date_str}_{time_str}"

            session_data = {
                "session_id": self.current_session_id,
                "title": title,
                "target_language": self.language_var.get()
                if hasattr(self, "language_var")
                else None,
                "translations": self.current_translations,
                "date": now.isoformat(),
            }

            with open(filename, "w", encoding="utf-8") as f:
                json.dump(session_data, f, indent=2, ensure_ascii=False)

            print(f"✅ Saved session: {filename}")
        except Exception as e:
            print(f"❌ Error saving session: {e}")

    # ------------------------------------------------------------------
    # Buttons / callbacks
    # ------------------------------------------------------------------
    def open_session_from_home(self, session_file: Path):
        """When clicked from home 'Previous Chats' – go to translation screen and render."""
        self.show_translation_screen()
        self.load_session(session_file, render=True)

    def on_start_pressed(self):
        """Handle Start Meeting from home screen."""
        target_lang = self.language_var.get().lower()
        self.show_translation_screen()
        if self.on_start_callback:
            self.on_start_callback(target_lang)

    def on_end_pressed(self):
        """End the current chat and ask user to name the session."""
        # Only prompt if there is content
        if self.current_translations:
            now = datetime.datetime.now()
            default_name = now.strftime("%I:%M %p session").lstrip("0")

            dialog = CTkInputDialog(
                text="Name this session (optional):", title="Save Session"
            )
            user_input = dialog.get_input()

            if user_input is None:
                self.current_session_title = default_name
            else:
                name = user_input.strip()
                self.current_session_title = name if name else default_name
        else:
            self.current_session_title = None

        # Save session
        try:
            self.save_current_session()
        except Exception as e:
            print(f"⚠️ Error saving session: {e}")

        # Stop backend
        if self.on_stop_callback:
            try:
                self.on_stop_callback()
            except Exception as e:
                print(f"⚠️ Error stopping backend: {e}")

        # Back to home
        self.show_home_screen()

    # ------------------------------------------------------------------
    # Run
    # ------------------------------------------------------------------
    def run(self):
        """Start the Tk mainloop."""
        self.root.mainloop()


if __name__ == "__main__":
    app = GlobalChatUI()
    app.run()
