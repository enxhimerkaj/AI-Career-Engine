import json
import os
from app.sources.greenhouse import fetch_greenhouse_jobs

def run():
    print("Fetching jobs...")

    boards = [
        "stripe",
        "coinbase",
        "robinhood",
        "plaid",
        "hubspot",
        "airbnb",
        "databricks",
        "snowflake",
        "asana",
        "notion",
        "figma",
        "dropbox",
        "twilio",
        "shopify",
        "discord",
        "square",
        "brex",
        "instacart"
    ]

    jobs = []

    for board in boards:
        try:
            board_jobs = fetch_greenhouse_jobs(board)
            print(f"{board}: {len(board_jobs)} jobs")
            jobs.extend(board_jobs)
        except Exception as e:
            print(f"Failed to fetch from {board}: {e}")

    print(f"Fetched {len(jobs)} jobs total")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "jobs.json")

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    print("Saved jobs to jobs.json")

if __name__ == "__main__":
    run()