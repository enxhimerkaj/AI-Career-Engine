import re
from html import unescape

CS_KEYWORDS = {
    # programming languages
    "python", "java", "javascript", "typescript", "c#", "c++", "php", "ruby",
    "go", "swift", "kotlin", "r", "scala",

    # web/frontend
    "html", "css", "react", "angular", "vue", "next.js", "tailwind",
    "bootstrap", "jquery",

    # backend
    "node.js", "express", "flask", "django", "fastapi", "spring boot",
    ".net", "asp.net", "rest api", "restful api", "graphql",

    # databases
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "oracle",
    "sql server", "redis",

    # cloud/devops
    "aws", "azure", "google cloud", "gcp", "docker", "kubernetes",
    "git", "github", "gitlab", "ci/cd", "linux", "bash",

    # data/ai
    "machine learning", "deep learning", "artificial intelligence",
    "ai", "data analysis", "data analytics", "pandas", "numpy",
    "scikit-learn", "tensorflow", "pytorch", "power bi", "tableau",

    # cybersecurity/networking
    "cybersecurity", "networking", "network security", "siem",
    "firewalls", "encryption",

    # software skills
    "debugging", "testing", "unit testing", "api development",
    "object oriented programming", "oop", "agile", "scrum",
    "software development", "web development", "full stack",
    "frontend", "backend",
}

LEAD_PATTERNS = [
    r"experience with ([^.;:\n]+)",
    r"experience in ([^.;:\n]+)",
    r"proficiency in ([^.;:\n]+)",
    r"proficient in ([^.;:\n]+)",
    r"knowledge of ([^.;:\n]+)",
    r"knowledge in ([^.;:\n]+)",
    r"familiarity with ([^.;:\n]+)",
    r"background in ([^.;:\n]+)",
    r"understanding of ([^.;:\n]+)",
    r"required skills[:\-]?\s*([^.\n]+)",
    r"qualifications[:\-]?\s*([^.\n]+)",
    r"requirements[:\-]?\s*([^.\n]+)",
    r"preferred qualifications[:\-]?\s*([^.\n]+)",
]


def clean_text(text: str) -> str:
    if not text:
        return ""

    text = unescape(text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_phrases(text: str):
    return [
        part.strip(" .:-").strip()
        for part in re.split(r",|/| and | or |\||;", text, flags=re.IGNORECASE)
        if part.strip(" .:-").strip()
    ]


def normalize_phrase(phrase: str) -> str:
    phrase = phrase.strip(" .:-").strip()
    phrase = re.sub(r"\s+", " ", phrase)

    if not phrase:
        return ""

    return phrase


def is_cs_related(phrase: str) -> bool:
    phrase_lower = phrase.lower()

    for keyword in CS_KEYWORDS:
        if keyword in phrase_lower:
            return True

    return False


def extract_cs_keywords(text: str):
    found = []

    text_lower = text.lower()

    for keyword in CS_KEYWORDS:
        if keyword in text_lower:
            found.append(keyword)

    return found


def extract_requirements(description: str):
    text = clean_text(description)

    if not text:
        return []

    found = []

    for pattern in LEAD_PATTERNS:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)

        for match in matches:
            phrases = split_phrases(match)

            for phrase in phrases:
                normalized = normalize_phrase(phrase)

                if normalized and is_cs_related(normalized):
                    found.append(normalized)

    found.extend(extract_cs_keywords(text))

    seen = set()
    results = []

    for item in found:
        clean_item = normalize_phrase(item)
        key = clean_item.lower()

        if key not in seen:
            seen.add(key)
            results.append(clean_item)

    return results[:25]