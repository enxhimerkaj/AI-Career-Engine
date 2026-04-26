from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.matching.recommender import match_jobs

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserProfile(BaseModel):
    preferredJobTitle: str = ""
    highestEducationLevel: str = ""
    major: str = ""
    university: str = ""
    experienceTitles: List[str] = Field(default_factory=list)
    currentSkills: List[str] = Field(default_factory=list)

@app.get("/")
def root():
    return {"message": "Backend is running"}

@app.post("/match-jobs")
def match_jobs_api(profile: UserProfile):
    return {"jobs": match_jobs(profile.model_dump())}
@app.get("/job-count")
def job_count():
    from app.matching.recommender import load_jobs
    jobs = load_jobs()
    return {"job_count": len(jobs)}