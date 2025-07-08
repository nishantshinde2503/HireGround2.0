import csv
import requests

# 🔗 Replace this with your own public CSV link
CSV_URL = "https://docs.google.com/spreadsheets/d/e/REPLACE_WITH_YOUR_LINK/pub?output=csv"

def fetch_jobs():
    jobs = []
    try:
        res = requests.get(CSV_URL)
        res.raise_for_status()
        content = res.text.splitlines()
        reader = csv.DictReader(content)
        for row in reader:
            jobs.append({
                "title": row["title"],
                "company": {"display_name": row["company"]},
                "location": {"display_name": row["location"]},
                "created": row["created"],
                "redirect_url": row["url"],
                "description": row.get("description", "")
            })
    except Exception as e:
        print(f"❌ Sheet Fetch Error: {e}")
    return jobs
