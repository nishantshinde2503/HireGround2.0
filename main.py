import json, os, shutil
from sources import adzuna, csv_reader, sheet_fetcher  # 💡 Add more as needed

JOBS_DIR = "jobs"
MAX_PAGES = 15

def shift_pages():
    os.makedirs(JOBS_DIR, exist_ok=True)

    # Delete the oldest page if exists
    oldest = os.path.join(JOBS_DIR, f"page_{MAX_PAGES}.json")
    if os.path.exists(oldest):
        os.remove(oldest)

    # Shift all pages up (page_14 → page_15, ..., page_1 → page_2)
    for i in range(MAX_PAGES - 1, 0, -1):
        src = os.path.join(JOBS_DIR, f"page_{i}.json")
        dst = os.path.join(JOBS_DIR, f"page_{i+1}.json")
        if os.path.exists(src):
            shutil.move(src, dst)

def fetch_and_save_jobs():
    all_jobs = []

    # 🌐 Adzuna
    try:
        adzuna_jobs = adzuna.fetch_jobs()
        all_jobs += adzuna_jobs
        print(f"✅ Adzuna jobs: {len(adzuna_jobs)}")
    except Exception as e:
        print(f"❌ Adzuna error: {e}")

    # 📄 CSV
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

    try:
        shift_pages()  # 🔄 Move old pages
        with open(os.path.join(JOBS_DIR, "page_1.json"), "w", encoding="utf-8") as f:
            json.dump({"results": all_jobs}, f, indent=2)
        print(f"✅ Saved {len(all_jobs)} jobs to page_1.json")
    except Exception as e:
        print(f"❌ Save error: {e}")

    return {"status": "success", "results": all_jobs}

if __name__ == "__main__":
    fetch_and_save_jobs()
