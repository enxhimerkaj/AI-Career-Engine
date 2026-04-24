import re
from html import unescape

STOP_PHRASES = {
    "the", "and", "or", "with", "for", "in", "of", "to", "a", "an",
    "is", "are", "be", "as", "on", "by", "from", "at", "this", "that"
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
    r"ability to ([^.;:\n]+)",
    r"responsible for ([^.;:\n]+)",
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
    parts = re.split(r",|/| and | or |\||;", text, flags=re.IGNORECASE)
    cleaned = []

    for part in parts:
        part = part.strip(" .:-").strip()
        if not part:
            continue
        if len(part) < 2:
            continue
        cleaned.append(part)

    return cleaned

def extract_bullet_like_phrases(text: str):
    phrases = []

    raw_lines = re.split(r"\n|•|- |\*", text)
    for line in raw_lines:
        line = clean_text(line)
        if not line:
            continue

        lowered = line.lower()
        if any(word in lowered for word in [
            "experience", "knowledge", "proficient", "familiarity",
            "ability", "required", "preferred", "bachelor", "master",
            "certification", "license", "skill", "background"
        ]):
            phrases.append(line)

    return phrases

def normalize_phrase(phrase: str) -> str:
    phrase = phrase.strip(" .:-").strip()
    phrase = re.sub(r"\s+", " ", phrase)

    if not phrase:
        return ""

    words = phrase.split()
    if len(words) > 8:
        phrase = " ".join(words[:8])

    if phrase.lower() in STOP_PHRASES:
        return ""

    return phrase

def extract_requirements(description: str):
    text = clean_text(description)
    if not text:
        return []

    found = []

    for pattern in LEAD_PATTERNS:
        matches = re.findall(pattern, text, flags=re.IGNORECASE)
        for match in matches:
            for phrase in split_phrases(match):
                normalized = normalize_phrase(phrase)
                if normalized:
                    found.append(normalized)

    bullet_lines = extract_bullet_like_phrases(description)
    for line in bullet_lines:
        line = normalize_phrase(line)
        if line:
            found.append(line)

    seen = set()
    results = []

    for item in found:
        key = item.lower()
        if key not in seen:
            seen.add(key)
            results.append(item)

    return results[:25]