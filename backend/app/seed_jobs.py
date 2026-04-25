import json
import os
from app.sources.greenhouse import fetch_greenhouse_jobs

CS_JOB_KEYWORDS = [
    # core engineering
    "software", "engineer", "developer",

    # data
    "data", "analytics", "analyst", "machine learning", "ai",

    # infrastructure / systems
    "cloud", "devops", "infrastructure", "platform", "sre",

    # security
    "security", "cybersecurity",

    # testing
    "qa", "test", "automation",

    # product / business tech roles
    "product", "product manager", "technical program", "program manager",

    # web/mobile
    "frontend", "backend", "full stack", "mobile", "ios", "android",

    # IT / systems
    "it", "systems", "network",
]


def is_cs_job(job):
    title = job.get("title", "").lower()
    description = job.get("description", "").lower()

    text = f"{title} {description}"

    return any(keyword in text for keyword in CS_JOB_KEYWORDS)


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
        "instacart",
    ]

    jobs = []

    for board in boards:
        try:
            board_jobs = fetch_greenhouse_jobs(board)
            filtered_jobs = [job for job in board_jobs if is_cs_job(job)]

            print(f"{board}: {len(filtered_jobs)} CS jobs found")
            jobs.extend(filtered_jobs)

        except Exception as e:
            print(f"Failed to fetch from {board}: {e}")

    print(f"Fetched {len(jobs)} computer science jobs total")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "jobs.json")

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(jobs, f, indent=2)

    print("Saved CS jobs to data/jobs.json")


if __name__ == "__main__":
    run()