import csv

def fetch_jobs():
    jobs = []
    with open('jobs.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            jobs.append({
                "title": row["title"],
                "company": {"display_name": row["company"]},
                "location": {"display_name": row["location"]},
                "created": row["created"],
                "redirect_url": row["url"],
                "description": row.get("description", "")
            })
    return jobs
