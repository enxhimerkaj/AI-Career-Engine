import json
import os

EDUCATION_ORDER = {
    "No degree": 0,
    "Associate": 1,
    "Bachelor": 2,
    "Master": 3,
    "Doctorate": 4,
}

def load_jobs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "data", "jobs.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

def normalize_list(items):
    return [item.strip() for item in items if item and item.strip()]

def detect_required_education(description):
    description_lower = description.lower()

    if "phd" in description_lower or "doctorate" in description_lower:
        return "Doctorate"
    if "master" in description_lower or "master's" in description_lower:
        return "Master"
    if "bachelor" in description_lower or "bachelor's" in description_lower or "bs in" in description_lower or "ba in" in description_lower:
        return "Bachelor"
    if "associate" in description_lower:
        return "Associate"

    return None

def education_matches(user_level, required_level):
    if not required_level:
        return True
    return EDUCATION_ORDER.get(user_level, 0) >= EDUCATION_ORDER.get(required_level, 0)

def text_similarity_score(search_terms, job_title, description):
    score = 0
    job_title_lower = job_title.lower()
    description_lower = description.lower()

    for term in search_terms:
        term = term.lower().strip()
        if not term:
            continue

        if term in job_title_lower:
            score += 35
        elif term in description_lower:
            score += 18

        term_words = set(term.split())
        title_words = set(job_title_lower.split())
        desc_words = set(description_lower.split())

        score += len(term_words & title_words) * 8
        score += len(term_words & desc_words) * 3

    return min(score, 50)

def calculate_requirement_score(user_skills, job_requirements):
    if not job_requirements:
        return 0, [], []

    user_skills_lower = [skill.lower().strip() for skill in user_skills if skill.strip()]
    matched = []
    missing = []

    for req in job_requirements:
        req_lower = req.lower().strip()
        matched_flag = False

        for skill in user_skills_lower:
            if skill in req_lower or req_lower in skill:
                matched_flag = True
                break

            req_words = set(req_lower.split())
            skill_words = set(skill.split())

            if len(req_words & skill_words) > 0:
                matched_flag = True
                break

        if matched_flag:
            matched.append(req)
        else:
            missing.append(req)

    score = int((len(matched) / len(job_requirements)) * 35)
    return score, matched, missing

def suggest_projects_for_job(title, missing_requirements):
    title_lower = title.lower()
    projects = []

    if any(x in title_lower for x in ["data", "analytics", "etl", "engineer"]):
        if any(x in " ".join(missing_requirements).lower() for x in ["sql", "python"]):
            projects.append("Build a data pipeline project using SQL and Python")
        if any("etl" in x.lower() for x in missing_requirements):
            projects.append("Create an ETL project that cleans and loads data into a database")
        if any(x in " ".join(missing_requirements).lower() for x in ["aws", "azure", "gcp", "cloud"]):
            projects.append("Build a cloud-based data workflow project")

    elif any(x in title_lower for x in ["support", "help desk", "technical support", "it"]):
        projects.append("Create an IT support troubleshooting knowledge base project")
        projects.append("Document a device setup and support workflow project")

    elif any(x in title_lower for x in ["learning", "instructional", "designer", "lxd"]):
        projects.append("Build a sample LMS course module with learner-centered design")
        projects.append("Create an instructional design portfolio case study")

    elif any(x in title_lower for x in ["project manager", "project coordinator"]):
        projects.append("Build a project planning case study with roadmap, timeline, and risks")
        projects.append("Create a Jira-based workflow and reporting demo")

    else:
        projects.append("Build a portfolio project that demonstrates the core responsibilities of this role")
        projects.append("Create a case study showing how you would solve a real problem in this field")

    return projects[:3]

def suggest_certifications_for_job(title, missing_requirements):
    title_lower = title.lower()
    certs = []

    if any(x in title_lower for x in ["data", "analytics", "etl", "engineer"]):
        if any("aws" in x.lower() for x in missing_requirements):
            certs.append("AWS Certified Cloud Practitioner")
        if any("azure" in x.lower() for x in missing_requirements):
            certs.append("Microsoft Azure Data Fundamentals")
        if any("gcp" in x.lower() or "google cloud" in x.lower() for x in missing_requirements):
            certs.append("Google Cloud Digital Leader")
        if any(x in " ".join(missing_requirements).lower() for x in ["sql", "data analysis"]):
            certs.append("Google Data Analytics Certificate")

    elif any(x in title_lower for x in ["support", "help desk", "it"]):
        certs.append("CompTIA A+")
        certs.append("Google IT Support Certificate")

    elif any(x in title_lower for x in ["project manager", "project coordinator"]):
        certs.append("Google Project Management Certificate")
        certs.append("CAPM")

    elif any(x in title_lower for x in ["ux", "designer", "ui"]):
        certs.append("Google UX Design Certificate")

    if not certs:
        certs = [
            "No obvious certification requirement detected",
            "Focus on projects and matching the listed requirements"
        ]

    return certs[:2]

def build_why_match(preferred_title, experience_titles, matched_requirements, missing_requirements, education_match):
    reasons = []

    if preferred_title:
        reasons.append(f"it relates to your target role of {preferred_title}")
    if experience_titles:
        reasons.append(f"your background includes {', '.join(experience_titles[:2])}")
    if matched_requirements:
        reasons.append(f"you already match requirements like {', '.join(matched_requirements[:3])}")
    if missing_requirements:
        reasons.append(f"you still need requirements like {', '.join(missing_requirements[:3])}")
    if not education_match:
        reasons.append("there is also an education gap")

    return "This job appears relevant because " + ", ".join(reasons) + "."

def match_jobs(user_profile):
    jobs = load_jobs()

    preferred_title = user_profile.get("preferredJobTitle", "")
    experience_titles = normalize_list(user_profile.get("experienceTitles", []))
    user_skills = normalize_list(user_profile.get("currentSkills", []))
    highest_education_level = user_profile.get("highestEducationLevel", "No degree")

    search_terms = [preferred_title] + experience_titles
    results = []

    for job in jobs:
        job_title = job.get("title", "")
        description = job.get("description", "")

        # supports BOTH old jobs.json (skills_found) and new one (requirements_found)
        job_requirements = normalize_list(
            job.get("requirements_found", job.get("skills_found", []))
        )

        title_score = text_similarity_score(search_terms, job_title, description)
        requirement_score, matched_requirements, missing_requirements = calculate_requirement_score(
            user_skills, job_requirements
        )

        required_education = detect_required_education(description)
        education_match = education_matches(highest_education_level, required_education)
        education_score = 15 if education_match else 0

        total_score = min(title_score + requirement_score + education_score, 100)

        if total_score < 12:
            continue

        results.append({
            "title": job_title,
            "company": job.get("company"),
            "location": job.get("location"),
            "match_score": total_score,
            "matched_skills": matched_requirements,
            "missing_skills": missing_requirements,
            "education_match": education_match,
            "missing_education": required_education if not education_match else None,
            "why_match": build_why_match(
                preferred_title,
                experience_titles,
                matched_requirements,
                missing_requirements,
                education_match
            ),
            "projects": suggest_projects_for_job(job_title, missing_requirements),
            "certifications": suggest_certifications_for_job(job_title, missing_requirements),
        })

    results.sort(key=lambda x: x["match_score"], reverse=True)
    return results