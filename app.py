from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
from datetime import datetime
import subprocess

app = Flask(__name__)

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "static", "audio")
METADATA_FILE = os.path.join(os.path.dirname(__file__), "static", "audio", "metadata.json")
AUDIO_DATA_FILE = os.path.join(os.path.dirname(__file__), "static", "audio", "input.wav.txt")

os.makedirs(AUDIO_DIR, exist_ok=True)


def load_metadata():
    if os.path.exists(METADATA_FILE):
        with open(METADATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_metadata(data):
    with open(METADATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def load_audio_data():
    """Load STT extraction file."""
    if os.path.exists(AUDIO_DATA_FILE):
        with open(AUDIO_DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_audio_data(data):
    """Save STT extraction file."""
    with open(AUDIO_DATA_FILE, "a") as f:
        f.write(data)

# ── Pages ──────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/checkin")
def checkin():
    return render_template("checkin.html")


@app.route("/history")
def history():
    return render_template("history.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/admin")
def admin():
    return render_template("admin.html")


# ── API ────────────────────────────────────────────────────────────────────────

@app.route("/api/save-recording", methods=["POST"])
def save_recording():
    """Save an audio recording with the STT transcript sent from the browser."""
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided"}), 400

    audio_file = request.files["audio"]
    note = request.form.get("note", "").strip()
    mood = request.form.get("mood", "").strip()
    name = request.form.get("name", "Friend").strip()

    timestamp = datetime.now()
    filename = f"input_{timestamp.strftime('%Y%m%d_%H%M%S')}.webm"
    wav_filename = filename.replace(".webm", ".wav")
    filepath = os.path.join(AUDIO_DIR, filename)
    audio_file.save(filepath)

    metadata = load_metadata()
    entry = {
        "id": timestamp.strftime("%Y%m%d_%H%M%S"),
        "filename": filename,
        "date": timestamp.strftime("%B %d, %Y"),
        "time": timestamp.strftime("%I:%M %p"),
        "iso": timestamp.isoformat(),
        "mood": mood,
        "note": note,
        "name": name,
        "size_kb": round(os.path.getsize(filepath) / 1024, 1),
    }
    metadata.append(entry)
    save_metadata(metadata)

    conversion_output = subprocess.call([
        "ffmpeg", "-i", f"/home/immasushiroll/Windows/Users/jane8/repos/symptom-tracker/static/audio/{filename}", "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", f"/home/immasushiroll/Windows/Users/jane8/repos/symptom-tracker/static/audio/{wav_filename}"
    ])

    text_output = subprocess.call([
        "/home/immasushiroll/Windows/Users/jane8/repos/whisper.cpp/build/bin/whisper-cli",
        "-m", "/home/immasushiroll/Windows/Users/jane8/repos/whisper.cpp/models/ggml-base.en.bin",
        "-f", f"/home/immasushiroll/Windows/Users/jane8/repos/symptom-tracker/static/audio/{wav_filename}",
        "-otxt"
    ])

    print(f"\Success=0, Fail=1 for {filename}:{text_output}\n")

    # save_audio_data(text_output)

    return jsonify({"success": True, "entry": entry})


@app.route("/api/recordings")
def get_recordings():
    """Return all recording metadata, newest first."""
    metadata = load_metadata()
    return jsonify(sorted(metadata, key=lambda x: x["iso"], reverse=True))


@app.route("/api/recordings/<recording_id>", methods=["DELETE"])
def delete_recording(recording_id):
    """Delete a recording and its metadata entry."""
    metadata = load_metadata()
    entry = next((e for e in metadata if e["id"] == recording_id), None)
    if not entry:
        return jsonify({"error": "Not found"}), 404

    filepath = os.path.join(AUDIO_DIR, entry["filename"])
    if os.path.exists(filepath):
        os.remove(filepath)

    metadata = [e for e in metadata if e["id"] != recording_id]
    save_metadata(metadata)
    return jsonify({"success": True})


@app.route("/static/audio/<path:filename>")
def serve_audio(filename):
    return send_from_directory(AUDIO_DIR, filename)


if __name__ == "__main__":
    print("\n🌿 Health Tracker is running!")
    print("   Open your browser to: http://localhost:5000\n")
    app.run(debug=True, port=5000)
