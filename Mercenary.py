import time
import os
import sys
import threading
import multiprocessing
from PIL import Image, ImageTk
import tkinter as tk
import pygame
from winotify import Notification

# === CONFIG ===
FILE_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Path of Exile\\logs\\client.txt"  # <-- Your full log path
TARGET_LINES = {
    "A Reflecting Mist has manifested nearby.",
    "The Nameless Seer has appeared nearby.",
}

MERCENARY_LINES = {
    "Take your trinket, then. My freedom's worth more",
}

# ✅ Feature toggles
ENABLE_TOAST = True
ENABLE_SOUND = True
ENABLE_ICON = True

# 🔔 Sound file path (MP3 or WAV)
SOUND_PATH = "resources\\alert.mp3"  # Put a short sound file here

app = None  # Will be assigned after GUI setup

class FloatingToggle:
    def __init__(self, root, icon_on_path, icon_off_path, callback=None, pos_file="resources\\position.txt"):
        self.root = root
        self.state = True
        self.callback = callback
        self.pos_file = pos_file

        # Load icons
        self.icon_on = ImageTk.PhotoImage(Image.open(icon_on_path))
        self.icon_off = ImageTk.PhotoImage(Image.open(icon_off_path))

        # Create button
        self.button = tk.Label(root, image=self.icon_on, bg="white", bd=0)
        self.button.pack()

        # Drag and toggle logic
        self.button.bind("<ButtonPress-1>", self.start_move)
        self.button.bind("<B1-Motion>", self.do_move)
        self.button.bind("<ButtonRelease-1>", self.on_release)
        self.button.bind("<ButtonRelease-3>", self.close_app)  # Right-click to exit

        # Transparent window setup
        root.overrideredirect(True)
        root.attributes("-topmost", True)
        root.wm_attributes("-transparentcolor", "white")

        # Load last position
        self.load_position()

    def toggle(self):
        self.set_state(not self.state)

    def set_state(self, new_state: bool):
        self.state = new_state
        self.button.configure(image=self.icon_on if self.state else self.icon_off)
        if self.callback:
            self.callback(self.state)

    def start_move(self, event):
        self._drag_start_x = event.x
        self._drag_start_y = event.y
        self._moved = False

    def do_move(self, event):
        x = event.x_root - self._drag_start_x
        y = event.y_root - self._drag_start_y
        self.root.geometry(f"+{x}+{y}")
        self._moved = True

    def on_release(self, event):
        if not self._moved:
            self.toggle()
        self.save_position()

    def save_position(self):
        pos = self.root.geometry()
        with open(self.pos_file, "w") as f:
            f.write(pos)

    def load_position(self):
        if os.path.exists(self.pos_file):
            with open(self.pos_file, "r") as f:
                pos = f.read().strip()
                self.root.geometry(pos)
        else:
            self.root.geometry("+100+100")

    def close_app(self, event=None):
        print("Right-click detected — exiting.")
        self.save_position()
        self.root.destroy()
        sys.exit(0)

def on_toggle(state):
    print(f"Toggle is now {'ON' if state else 'OFF'}")

def notify_toast(message):
    if ENABLE_TOAST:
        toast = Notification(app_id="Event Monitor",
                             title="Event Alert",
                             msg=message,
                             duration="short")
        toast.show()

def play_alert_sound():
    if ENABLE_SOUND and os.path.exists(SOUND_PATH):
        try:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(SOUND_PATH)
            pygame.mixer.music.play()
        except Exception as e:
            print(f"Sound error: {e}")

def tail_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        f.seek(0, os.SEEK_END)
        while True:
            line = f.readline()
            if not line:
                time.sleep(1)
                continue
            logic(line.strip())

def logic(line):
    global app
    for target in TARGET_LINES:
        if target in line:
            print(f"Matched: {target}")
            notify_toast(target)
            play_alert_sound()
            break  # Stop checking once one match is found

    if line.startswith("You have entered") and "Hideout" in line:
        print(f"Matched Hideout: {line.strip()}")
        notify_toast(line.strip())
        play_alert_sound()
        if app:
            app.set_state(False)  # Disable toggle when entering any hideout


    # for dialogue in MERCENARY_LINES:
    #     if dialogue in line:
    #         print(f"Matched Mercenary: {dialogue}")
    #         notify_toast(dialogue)
    #         if app:
    #             app.set_state(False)  
    #         break  # Stop checking once one match is found

if __name__ == "__main__":
    multiprocessing.freeze_support()

    # Create the GUI
    root = tk.Tk()
    app = FloatingToggle(root, "resources\\on.png", "resources\\off.png", callback=lambda state: print("Toggled:", state))

    # Start log file monitor in a background thread
    threading.Thread(target=tail_file, args=(FILE_PATH,), daemon=True).start()

    # Run the GUI (main thread)
    root.mainloop()
