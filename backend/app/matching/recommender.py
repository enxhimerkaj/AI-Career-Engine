import json
import os

EDUCATION_ORDER = {
    "No degree": 0,
    "Associate": 1,
    "Bachelor": 2,
    "Master": 3,
    "Doctorate": 4,
}

TECH_ROLE_KEYWORDS = [
    "software", "developer", "engineer", "frontend", "backend", "full stack",
    "data", "analyst", "analytics", "machine learning", "ai",
    "cloud", "devops", "security", "cybersecurity", "qa", "test",
    "product", "program manager", "technical program", "it", "support",
    "systems", "network", "ux", "ui", "designer"
]


def load_jobs():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "..", "data", "jobs.json")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_list(items):
    return [item.strip() for item in items if item and item.strip()]


def detect_required_education(description):
    text = description.lower()

    if "phd" in text or "doctorate" in text:
        return "Doctorate"
    if "master" in text or "master's" in text:
        return "Master"
    if "bachelor" in text or "bachelor's" in text or "bs in" in text or "ba in" in text:
        return "Bachelor"
    if "associate" in text:
        return "Associate"

    return None


def education_matches(user_level, required_level):
    if not required_level:
        return True

    return EDUCATION_ORDER.get(user_level, 0) >= EDUCATION_ORDER.get(required_level, 0)


def text_similarity_score(search_terms, job_title, description):
    score = 0
    title_lower = job_title.lower()
    description_lower = description.lower()

    for term in search_terms:
        term = term.lower().strip()

        if not term:
            continue

        if term in title_lower:
            score += 45
        elif term in description_lower:
            score += 20

        term_words = set(term.split())
        title_words = set(title_lower.split())
        description_words = set(description_lower.split())

        score += len(term_words & title_words) * 10
        score += len(term_words & description_words) * 3

    return min(score, 50)


def calculate_requirement_score(user_skills, job_requirements):
    if not job_requirements:
        return 0, [], []

    user_skills_lower = [skill.lower().strip() for skill in user_skills if skill.strip()]
    matched = []
    missing = []

    for requirement in job_requirements:
        req_lower = requirement.lower().strip()
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
            matched.append(requirement)
        else:
            missing.append(requirement)

    score = int((len(matched) / len(job_requirements)) * 35)
    return score, matched, missing


def is_tech_related_job(title, description):
    text = f"{title} {description}".lower()
    return any(keyword in text for keyword in TECH_ROLE_KEYWORDS)


def suggest_projects_for_job(title, missing_requirements):
    title_lower = title.lower()
    missing_text = " ".join(missing_requirements).lower()
    projects = []

    if any(x in title_lower for x in ["software", "developer", "frontend", "backend", "full stack"]):
        projects.append("Build a full-stack web application with authentication and a database")
        projects.append("Create a REST API project and connect it to a React frontend")

    elif any(x in title_lower for x in ["data", "analytics", "analyst", "etl"]):
        projects.append("Build a data analysis dashboard using Python, SQL, and visualization tools")
        projects.append("Create a data cleaning and reporting project using a real dataset")

    elif any(x in title_lower for x in ["machine learning", "ai", "ml"]):
        projects.append("Build a machine learning prediction project using Scikit-learn")
        projects.append("Create an AI-powered app that uses user input to generate recommendations")

    elif any(x in title_lower for x in ["product manager", "product"]):
        projects.append("Create a product case study with user research, roadmap, and feature prioritization")
        projects.append("Build a product requirements document for a tech product idea")

    elif any(x in title_lower for x in ["program manager", "technical program"]):
        projects.append("Create a technical project roadmap with milestones, risks, and success metrics")
        projects.append("Build a Jira-style workflow case study for a software team")

    elif any(x in title_lower for x in ["support", "help desk", "it"]):
        projects.append("Create an IT support troubleshooting knowledge base project")
        projects.append("Build a ticket classification or support dashboard project")

    elif any(x in title_lower for x in ["ux", "ui", "designer"]):
        projects.append("Create a UX case study for a web or mobile app")
        projects.append("Build a Figma prototype and explain the design decisions")

    else:
        projects.append("Build a portfolio project that demonstrates the main responsibilities of this role")
        projects.append("Create a case study showing how you would solve a real problem in this field")

    if "sql" in missing_text:
        projects.append("Add SQL database work to one of your projects")
    if "cloud" in missing_text or "aws" in missing_text or "azure" in missing_text:
        projects.append("Deploy one project using a cloud platform")

    return projects[:3]


def suggest_certifications_for_job(title, missing_requirements):
    title_lower = title.lower()
    missing_text = " ".join(missing_requirements).lower()
    certs = []

    if any(x in title_lower for x in ["data", "analytics", "analyst"]):
        certs.append("Google Data Analytics Certificate")

    if any(x in title_lower for x in ["software", "developer", "engineer"]):
        certs.append("AWS Certified Cloud Practitioner")

    if any(x in title_lower for x in ["support", "help desk", "it"]):
        certs.append("CompTIA A+")
        certs.append("Google IT Support Certificate")

    if any(x in title_lower for x in ["product manager", "product"]):
        certs.append("Google Project Management Certificate")

    if any(x in title_lower for x in ["program manager", "technical program"]):
        certs.append("CAPM or Google Project Management Certificate")

    if any(x in title_lower for x in ["ux", "ui", "designer"]):
        certs.append("Google UX Design Certificate")

    if "aws" in missing_text:
        certs.append("AWS Certified Cloud Practitioner")
    if "azure" in missing_text:
        certs.append("Microsoft Azure Fundamentals")
    if "security" in missing_text or "cybersecurity" in missing_text:
        certs.append("CompTIA Security+")

    if not certs:
        certs.append("Focus on projects first, then choose a certification based on the role requirements")

    return certs[:2]


def build_why_match(preferred_title, experience_titles, matched_requirements, missing_requirements, education_match):
    reasons = []

    if preferred_title:
        reasons.append(f"it relates to your target role of {preferred_title}")

    if experience_titles:
        reasons.append(f"your background includes {', '.join(experience_titles[:2])}")

    if matched_requirements:
        reasons.append(f"you already match skills like {', '.join(matched_requirements[:3])}")

    if missing_requirements:
        reasons.append(f"you can improve by learning {', '.join(missing_requirements[:3])}")

    if not education_match:
        reasons.append("there may be an education gap")

    if not reasons:
        return "This job appears relevant based on your profile."

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

        if not is_tech_related_job(job_title, description):
            continue

        job_requirements = normalize_list(
            job.get("requirements_found", job.get("skills_found", []))
        )

        title_score = text_similarity_score(search_terms, job_title, description)

        requirement_score, matched_requirements, missing_requirements = calculate_requirement_score(
            user_skills,
            job_requirements
        )

        required_education = detect_required_education(description)
        education_match = education_matches(highest_education_level, required_education)
        education_score = 15 if education_match else 0

        total_score = min(title_score + requirement_score + education_score, 100)

        if total_score < 12:
            continue

        results.append({
            "title": job_title,
            "company": job.get("company", "Not listed"),
            "location": job.get("location", "Not listed"),
            "url": job.get("url", ""),
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
    return results[:20]