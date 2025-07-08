import time
import datetime
import requests
import json
import random
from dotenv import load_dotenv
import os

# 🌱 Load secrets
load_dotenv()
APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

def is_daytime():
    now = datetime.datetime.now().time()
    return datetime.time(8, 0) <= now <= datetime.time(22, 0)

def fetch_and_save_jobs():
    try:
        page = random.randint(1, 5)

        API_URL = (
            f"https://api.adzuna.com/v1/api/jobs/in/search/{page}"
            f"?app_id={APP_ID}&app_key={APP_KEY}"
            f"&where=India&results_per_page=25"
            f"&sort_by=date&max_days_old=1"
        )

        res = requests.get(API_URL)
        res.raise_for_status()
        data = res.json()

        jobs = data.get("results", [])

        formatted = [{
            "title": job.get("title", "No title"),
            "company": {
                "display_name": job.get("company", {}).get("display_name", "Unknown")
            },
            "location": {
                "display_name": job.get("location", {}).get("display_name", "India")
            },
            "created": job.get("created", ""),
            "redirect_url": job.get("redirect_url", ""),
            "description": job.get("description", "")
        } for job in jobs]

        with open("jobs.json", "w", encoding="utf-8") as f:
            json.dump({"results": formatted}, f, indent=2)

        print(f"✅ {len(formatted)} jobs refreshed at {datetime.datetime.now().strftime('%d-%b %H:%M:%S')}")

    except Exception as e:
        print(f"❌ Error: {e}")

# 🔁 Infinite loop with smart delay
while True:
    fetch_and_save_jobs()

    if is_daytime():
        time.sleep(15 * 60)  # 15 mins
    else:
        time.sleep(60 * 60)  # 1 hour
