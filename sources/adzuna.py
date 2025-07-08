import os
import requests

def fetch_jobs():
    app_id = os.environ.get("APP_ID")
    app_key = os.environ.get("APP_KEY")

    if not app_id or not app_key:
        raise ValueError("APP_ID or APP_KEY not set in environment.")

    api_url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={app_id}&app_key={app_key}&where=India&results_per_page=25"

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
