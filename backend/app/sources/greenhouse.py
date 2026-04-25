import requests
from app.parser.extractor import extract_requirements

USA_KEYWORDS = [
    "united states",
    "u.s.",
    "usa",
    "us",
    "remote",
    "new york",
    "california",
    "texas",
    "florida",
    "illinois",
    "arizona",
    "washington",
    "massachusetts",
    "virginia",
    "north carolina",
    "georgia",
    "pennsylvania",
    "new jersey",
    "colorado",
    "ohio",
    "michigan",
    "minnesota",
    "utah",
]


def is_usa_location(location):
    if not location:
        return False

    location_lower = location.lower()
    return any(keyword in location_lower for keyword in USA_KEYWORDS)


def fetch_job_detail(board, job_id):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs/{job_id}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    return data.get("content", "")


def fetch_greenhouse_jobs(board="stripe"):
    url = f"https://boards-api.greenhouse.io/v1/boards/{board}/jobs"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()

    jobs = []

    for job in data.get("jobs", []):
        title = job.get("title", "")
        location = job.get("location", {}).get("name", "")
        job_id = job.get("id")
        absolute_url = job.get("absolute_url", "")

        if not is_usa_location(location):
            continue

        try:
            description = fetch_job_detail(board, job_id)
        except Exception:
            description = ""

        requirements_found = extract_requirements(description)

        jobs.append({
            "source": "greenhouse",
            "company": board,
            "title": title,
            "location": location,
            "url": absolute_url,
            "description": description,
            "requirements_found": requirements_found,
        })

    return jobs