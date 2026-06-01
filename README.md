# 🌿 My Health Journal
Something just to track the symptoms of patients (mostly for my dad) and relay it to healthcare providers (not actually doing that, that's looking like a lot of legal talks)

A simple, privacy-first weekly health check-in app for patients and older adults.
All audio recordings are saved **locally on your computer** — nothing goes to the internet.

---

## 📁 File Structure

```
health-tracker/
├── app.py                  ← Flask server (run this!)
├── requirements.txt        ← Python dependencies
├── README.md
├── templates/
│   ├── base.html           ← Shared layout (navbar, footer)
│   ├── index.html          ← Home page
│   ├── checkin.html        ← Step-by-step recording wizard
│   ├── history.html        ← Listen back to past check-ins
│   ├── about.html          ← How the app works / privacy info
│   └── admin.html          ← Admin panel (all recordings + delete)
└── static/
    ├── css/
    │   └── main.css        ← All styles
    ├── js/
    │   └── main.js         ← Shared JS utilities
    └── audio/
        ├── metadata.json   ← Auto-created: recording index
        └── *.webm          ← Auto-created: your audio files
```

---

## 🚀 Setup (one-time)

### Requirements
- Python 3.8 or newer
- A modern web browser (Chrome, Edge, Firefox, Safari)

### Steps

1. **Open a terminal** in VS Code (`Terminal → New Terminal`)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   python app.py
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

That's it! The app will create the `static/audio/` folder automatically.

---

## 📄 Pages

| URL | Page | Description |
|-----|------|-------------|
| `/` | Home | Welcome screen with quick links |
| `/checkin` | Check-In | 5-step wizard: name → mood → record → note → save |
| `/history` | My History | Listen back to all saved recordings |
| `/about` | About | Privacy info and usage tips |
| `/admin` | Admin Panel | View, download, and delete all recordings |

---

## 🔒 Privacy

- Recordings are saved as `.webm` files in `static/audio/`
- A `metadata.json` file stores names, moods, notes, and timestamps
- **Nothing leaves your computer** — no internet connection needed after first load (fonts are loaded from Google Fonts on first visit; remove the font link in `base.html` to make it fully offline)

---

## 🔧 Troubleshooting

**Microphone not working?**
- Make sure your browser has microphone permission for `localhost`
- In Chrome: click the 🔒 icon in the address bar → allow microphone

**Port already in use?**
- Change `port=5000` to another number (e.g. `5001`) in `app.py`

**Recordings not saving?**
- Make sure `static/audio/` folder exists (the app creates it automatically)
- Run the app with `python app.py` not by opening the HTML file directly
