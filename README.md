# Mercenary Event Notifier

A simple Python app that monitors Path of Exile log files and notifies you when special mercenary events occur.  
It plays a sound, shows a popup, and includes a draggable toggle icon that indicates event status.

- Left click to Toggle Icon
- Right click to close program
---

## 🔧 Requirements

- Python 3.9 or higher  
- Windows 10 or 11  
- Steam or standalone Path of Exile installation

---

### 🐍 How to Install Python

1. Go to the official Python download page:  
   👉 [https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

2. Click **Download Python 3.x.x** for Windows (choose the latest version 3.9 or above)

3. Run the downloaded installer

4. **IMPORTANT:**  
   ✅ Check the box that says:
```

\[x] Add Python to PATH

````

5. Click **Install Now**

6. After installation, you can confirm it by opening **Command Prompt** and typing:
```bash
python --version
````

You should see something like:

```
Python 3.11.8
```

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

### 🔄 How to Update This Project

#### 🔹 If you used Git (recommended):

1. Open Command Prompt
2. Go to the project folder:
   ```bash
   cd path\to\mercenary
   ```
3. Pull the latest version:
   ```bash
   git pull
   ```
#### 🔹 If you downloaded a ZIP file:

1. Go to the GitHub page:
👉 https://github.com/RyuFive/mercenary

2. Click the green Code button → Download ZIP

3. Extract the new version and replace the old folder
4. 
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
