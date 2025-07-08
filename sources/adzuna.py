import requests, os
from dotenv import load_dotenv
load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

def fetch_jobs():
    api_url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={APP_KEY}&where=India&results_per_page=25"
    res = requests.get(api_url)
    data = res.json()
    return [{
        "title": job.get("title"),
        "company": {"display_name": job.get("company", {}).get("display_name")},
        "location": {"display_name": job.get("location", {}).get("display_name")},
        "created": job.get("created"),
        "redirect_url": job.get("redirect_url"),
        "description": job.get("description")
    } for job in data.get("results", [])]
