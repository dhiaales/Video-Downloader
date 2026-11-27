import os
from flask import Flask, render_template, request, send_file, jsonify
import yt_dlp

app = Flask(__name__)
DOWNLOAD_FOLDER = "/tmp/downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/download", methods=["POST"])
def download():
    url = request.json.get("url")
    if not url:
        return jsonify({"error": "No URL provided"}), 400

    ydl_opts = {
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s.%(ext)s",
        "format": "best[ext=mp4]/best",
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
