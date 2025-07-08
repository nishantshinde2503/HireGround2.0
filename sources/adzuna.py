import requests
import os

# ✅ Get Adzuna keys directly from Render environment
APP_ID = os.environ.get("APP_ID")
APP_KEY = os.environ.get("APP_KEY")

def fetch_jobs():
    api_url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&where=India&results_per_page=25"
    
    try:
        res = requests.get(api_url)
        res.raise_for_status()
        data = res.json()

        return [{
            "title": job.get("title", "No title"),
            "company": {"display_name": job.get("company", {}).get("display_name", "Unknown")},
            "location": {"display_name": job.get("location", {}).get("display_name", "India")},
            "created": job.get("created"),
            "redirect_url": job.get("redirect_url"),
            "description": job.get("description", "")
        } for job in data.get("results", [])]

    except Exception as e:
        print(f"❌ Adzuna Fetch Error: {e}")
        return []
