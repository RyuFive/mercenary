import time
import os
import sys
import threading
import multiprocessing
from PIL import Image, ImageTk
import tkinter as tk
import pygame
from winotify import Notification
import re

# === CONFIG ===
# Steam and Standalone default log paths
STEAM_LOG_PATH = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\Path of Exile\\logs\\client.txt"
STANDALONE_LOG_PATH = "C:\\Program Files (x86)\\Grinding Gear Games\\Path of Exile\\logs\\client.txt"
# Auto-select whichever path exists
if os.path.exists(STEAM_LOG_PATH):
    FILE_PATH = STEAM_LOG_PATH
elif os.path.exists(STANDALONE_LOG_PATH):
    FILE_PATH = STANDALONE_LOG_PATH
else:
    raise FileNotFoundError("Could not find Path of Exile log file in default locations.")

TARGET_LINES = {
    "A Reflecting Mist has manifested nearby.",
    "The Nameless Seer has appeared nearby.",
}

MERCENARY_HOUSES = {
    "Cyaxan",
    "Azadi",
    "Keita",
    "Bardiya",
    "Keita",
}

# ✅ Feature toggles
ENABLE_TOAST = True
ENABLE_SOUND = True
ENABLE_ICON = True

# 🔔 Sound file path (MP3 or WAV)
SOUND_PATH = "resources\\alert.mp3"  # Put a short sound file here
SOUND2_PATH = "resources\\failed.mp3"  # Optional second sound file

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

    def get_state(self):
        return self.state
    
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

def play_failed_sound():
    if ENABLE_SOUND and os.path.exists(SOUND2_PATH):
        try:
            pygame.init()
            pygame.mixer.init()
            pygame.mixer.music.load(SOUND2_PATH)
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

exclude_pattern = re.compile(r'''
^\[SCENE\]|
^\[DXC\]|
^\[InGameAudioManager\]|
^\[SHADER\]|
^Got\sInstance\sDetails\sfrom\slogin\sserver$|
^Doodad\shash:|
^Tile\shash:|
^Async\sconnecting\sto\s\S+:\d+$|
^Connecting\sto\sinstance\sserver\sat\s\S+:\d+$|
^Connect\stime\sto\sinstance\sserver\swas\s\d+ms$|
^Generating\slevel\s\d+\sarea\s".+?"\swith\sseed\s\d+$|
^Client-Safe\sInstance\sID\s=|
^Joined\sguild\snamed\s.*$|
^Matching\sobject\sfound\sfor\sInstanceClientActionUpdate,.*$|
^Client\scouldn't\sexecute\sa\striggered\saction\sfrom\sthe\sserver.*$|
^Instant/Triggered\sactionwas\sserialized\sto\sthe\sclient.*$|
^Failed\sto\screate\seffect\sgraph\snode.*$|
^Precalc*$|
^Action\sId\s=\s\d+$|
^action\s*type\s*id\s*=\s*\d+$|
^action_id:\s*\d+$|
^skill_instance_id:\s*\d+$|
^object_id:\s*\d+$|
^target_id:\s*\d+$|
^flags:\s*\d+$|
^object_id\sId\s=\s\d+$|
^target_id\sId\s=\s\d+$|
^Detach\sId\s=\s\d+$|
^Skill\sType\sId\s=\s\d+$|
^Skill\sInstance\sId\s=\d+$|
^flags\sId\s=\s\d+$|
^Steam\sstats\sstored$|
^Replacing\sawake\sobject\swith\sid\s.*$|
^:\sTrade\saccepted$
''', re.VERBOSE)

# Print initial message
print("Mercenary Monitor started. Monitoring log file:")
print("------------------------------")

def logic(line):
    global app
    line = line[line.find(']') + 1:].strip()

    if exclude_pattern.match(line):
        # app.close_app()  # Close app if excluded line is detected
        return

    print(repr(line))
    
    for target in TARGET_LINES:
        if target in line:
            print(f"Matched: {target}")
            notify_toast(target)
            play_alert_sound()
            break  # Stop checking once one match is found

    if "You have entered" and "Hideout" in line:
        if "Syndicate" in line:
            print("Thats not your Hideout, ignoring...")
        elif app:
            if app.get_state():
                play_failed_sound()
                notify_toast("You didn't defeat the mercenary yet!")
            app.set_state(True)  # Reset toggle when entering any hideout


    for house in MERCENARY_HOUSES:
        if house in line:
            if app:
                if app.get_state() == False:
                    break
                play_alert_sound()
                app.set_state(False)  
            break  # Stop checking once one match is found

if __name__ == "__main__":
    multiprocessing.freeze_support()

    # Create the GUI
    root = tk.Tk()
    app = FloatingToggle(root, "resources\\on.png", "resources\\off.png", callback=lambda state: print("Toggled:", state))

    # Start log file monitor in a background thread
    threading.Thread(target=tail_file, args=(FILE_PATH,), daemon=True).start()

    # Run the GUI (main thread)
    root.mainloop()
