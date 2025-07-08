import json
from sources import adzuna, csv_reader, sheet_fetcher  # 🧩 Add more sources as needed

def fetch_and_save_jobs():
    all_jobs = []

    # 🌐 Adzuna API
    try:
        all_jobs += adzuna.fetch_jobs()
        print(f"✅ Adzuna jobs: {len(all_jobs)}")
    except Exception as e:
        print(f"❌ Adzuna error: {e}")

    # 📄 CSV File
    try:
        csv_jobs = csv_reader.fetch_jobs()
        all_jobs += csv_jobs
        print(f"✅ CSV jobs: {len(csv_jobs)}")
    except Exception as e:
        print(f"❌ CSV error: {e}")

    # ☁️ Google Sheet
    try:
        sheet_jobs = sheet_fetcher.fetch_jobs()
        all_jobs += sheet_jobs
        print(f"✅ Google Sheet jobs: {len(sheet_jobs)}")
    except Exception as e:
        print(f"❌ Sheet error: {e}")

    # 🧾 Save all to jobs.json
    try:
        with open("jobs.json", "w", encoding="utf-8") as f:
            json.dump({"results": all_jobs}, f, indent=2)
        print(f"✅ Combined: {len(all_jobs)} jobs saved to jobs.json")
    except Exception as e:
        print(f"❌ Error saving file: {e}")

    return {"status": "success", "results": all_jobs}

if __name__ == "__main__":
    fetch_and_save_jobs()
