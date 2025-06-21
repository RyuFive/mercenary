# Mercenary Event Notifier

A simple Python app that monitors Path of Exile log files and notifies you when special mercenary events occur.  
It plays a sound, shows a popup, and includes a draggable toggle icon that indicates event status.

---

## 🔧 Requirements

- Python 3.9 or higher  
- Windows 10 or 11  
- Steam or standalone Path of Exile installation

---

## 🛠 Installation (Python Script)

1. **Clone or download this repo**
   ```bash
   git clone https://github.com/RyuFive/mercenary.git
   cd mercenary
   ```

2. **Install required Python packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the script**
   ```bash
   python Mercenary.py
   ```

---

## 🎵 Resources

Make sure these files are present in the same folder as the script:

- `on.png` – Toggle icon (active)
- `off.png` – Toggle icon (inactive)
- `alert.mp3` – Sound to play when an event is detected

You can customize these with your own icons and sounds if desired.

---

## ✅ Features

- Watches your `client.txt` log file for specific PoE events
- Plays a sound and shows a popup when a mercenary appears
- Drag-and-drop floating icon to toggle detection
- Automatically turns off when an event is found
- Compatible with both Steam and standalone PoE installations


---

## ❓ Troubleshooting

- **No popup or sound?** Make sure your `client.txt` path is correct and the sound/image files are in the right location.
- **Script doesn’t start?** Check that all required packages are installed (`pip install -r requirements.txt`)

---

## 👤 Credits

Created by [RyuFive](https://github.com/RyuFive)  
Inspired by Path of Exile league mechanics and QoL alert tools.
