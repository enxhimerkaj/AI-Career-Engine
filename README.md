# AI Career Engine

AI-powered web app that recommends computer science jobs based on your profile, skills, and experience.

---

## Features

* Match users to real job listings
* Skill gap analysis (matched vs missing skills)
* Suggested projects to improve your profile
* Suggested certifications based on job requirements
* Real job data fetched from company job boards

---

## Tech Stack

Frontend:

* React

Backend:

* FastAPI (Python)

Other:

* Greenhouse API (job data)
* Custom matching algorithm

---

## How It Works

1. User fills out:

   * Preferred job title
   * Skills
   * Experience
   * Education

2. Backend:

   * Fetches real job listings
   * Extracts requirements
   * Matches user profile with jobs

3. Output:

   * Job matches
   * Match score
   * Missing skills
   * Suggested projects & certifications

---

## Setup

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install fastapi uvicorn requests
python -m app.seed_jobs
python -m uvicorn app.main:app --reload
```

### Frontend

```bash
cd ..
npm install
npm start
```

---

## Notes

* This project focuses on computer science and tech-related roles
* Job data is fetched from public APIs and stored locally
* Matching logic is rule-based with scoring

---

## Future Improvements

* Improve AI matching accuracy
* Add more job sources (not just Greenhouse)
* Deploy full-stack app
* Save/bookmark jobs
* Add authentication

---

## Author

Enxhi Merkaj
