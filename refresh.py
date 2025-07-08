from flask import Flask, jsonify
from main import fetch_and_save_jobs
from threading import Thread
import time
from datetime import datetime
import pytz

app = Flask(__name__)

from flask import send_from_directory

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/jobs.json')
def serve_jobs_json():
    return send_from_directory('.', 'jobs.json')

@app.route('/<path:filename>')
def serve_static_files(filename):
    return send_from_directory('.', filename)

# 🌏 Set IST timezone
IST = pytz.timezone('Asia/Kolkata')

# ♻️ Smart Auto Refresh Function
def smart_auto_refresher():
    while True:
        now = datetime.now(IST)
        hour = now.hour

        # ⏱️ Adjust refresh interval based on time
        if 8 <= hour < 22:
            interval = 20 * 60  # 20 mins
            print(f"🕒 {now.strftime('%H:%M')} — Day Refresh (20 mins)")
        else:
            interval = 60 * 60  # 1 hour
            print(f"🌙 {now.strftime('%H:%M')} — Night Refresh (1 hr)")

        try:
            result = fetch_and_save_jobs()
            print(f"✅ {len(result.get('results', []))} jobs fetched @ {now.strftime('%d-%b %I:%M %p')}")
        except Exception as e:
            print(f"❌ Refresh Error: {e}")

        time.sleep(interval)

# 🚀 Start background thread
def start_background_refresh():
    thread = Thread(target=smart_auto_refresher, daemon=True)
    thread.start()

# 🧠 Optional: Manual trigger route (just in case)
@app.route("/refresh", methods=["GET"])
def manual_refresh():
    try:
        result = fetch_and_save_jobs()
        return jsonify({
            "status": "success",
            "fetched": len(result.get("results", []))
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        })

# 🎯 Start Flask + Background Job
if __name__ == "__main__":
    start_background_refresh()
    app.run(host="0.0.0.0", port=5000, debug=True)
