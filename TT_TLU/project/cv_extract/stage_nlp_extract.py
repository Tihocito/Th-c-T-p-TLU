import re
from rapidfuzz import fuzz
from typing import List, Optional

LANGUAGES = [
    "python", "java", "c#", "c++", "javascript", "typescript",
    "php", "ruby", "go", "rust", "swift", "kotlin",
    "sql", "scala", "dart", "bash", "powershell", "r",
]

FRAMEWORKS = [
    "react", "angular", "vue", "node.js", "django", "flask",
    "spring", "spring boot", ".net", "laravel",
    "tensorflow", "pytorch", "pandas", "numpy", "scikit-learn",
    "flutter", "react native", "express", "fastapi",
    "next.js", "nuxt.js", "svelte",
]

DATABASES = [
    "mysql", "postgresql", "mongodb", "redis", "sqlite",
    "oracle", "elasticsearch", "cassandra", "dynamodb",
    "mariadb", "firebase", "sql server", "clickhouse",
]

EDUCATION_LEVELS = [
    "phd", "ph.d", "doctorate", "master",
    "bachelor", "b.s", "b.a", "msc", "mba", "associate",
]


def clean_ocr_errors_smart(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"(\d)[lI]", r"\1 1", text)
    text = re.sub(r"[lI](\d)", r"1\1", text)
    text = re.sub(r"(\d)o", r"\1 0", text, flags=re.I)
    text = re.sub(r"o(\d)", r"0\1", text, flags=re.I)
    return text


def clean_text(text: str) -> str:
    text = re.sub(r"[\r\n]+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_emails_from_ocr(raw_text: str) -> List[str]:
    if not raw_text:
        return []
    text = re.sub(r"([a-zA-Z0-9._%+-])\s*\n\s*([a-zA-Z0-9._%+-]+@)", r"\1\2", raw_text)
    emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    return sorted(set(e.lower().strip(".,;:()[]{}<> ") for e in emails))


def find_phone_number(text: str) -> Optional[str]:
    if not text:
        return None

    patterns = [
        r"(\+84|0)\s*[\d\-\s\.]{8,15}",
        r"\b\d{9,12}\b",
    ]

    for p in patterns:
        m = re.search(p, text)
        if m:
            phone = re.sub(r"\D", "", m.group(0))
            if phone.startswith("84") and not phone.startswith("+"):
                return "+" + phone
            return phone
    return None


def find_full_name(text: str) -> Optional[str]:
    if not text:
        return None

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:6]:
        if "@" in line or re.search(r"\d", line):
            continue
        parts = line.split()
        if 2 <= len(parts) <= 4 and (line.istitle() or line.isupper()):
            return line.title()
    return None


def find_applied_position(text: str) -> Optional[str]:
    if not text:
        return None

    lines = [l.strip() for l in text.split("\n") if l.strip()]
    for line in lines[:20]:
        lower = line.lower()
        if any(k in lower for k in ["position", "apply for", "vị trí", "title"]):
            m = re.search(r"(position|apply for|vị trí|title)[:\-]?\s*(.+)", line, re.I)
            if m:
                return m.group(2).strip().title()

        if any(word in lower for word in ["developer", "engineer", "manager", "analyst"]):
            if not re.search(r"\d", line):
                return line.title()
    return None


def find_years_experience(text: str) -> Optional[int]:
    m = re.search(r"(\d{1,2})\+?\s*(years|year|nam|năm)", text, re.I)
    if m:
        return int(m.group(1))
    return None


def extract_education_level(text: str, threshold=80) -> Optional[str]:
    lower = text.lower()
    for e in EDUCATION_LEVELS:
        if e in lower:
            return e
    for e in EDUCATION_LEVELS:
        if fuzz.partial_ratio(e, lower) >= threshold:
            return e
    return None


def simple_skill_match(text: str, skills: List[str], score_threshold=85):
    lower = text.lower()
    found = set()
    for s in skills:
        if s in lower or fuzz.partial_ratio(s.lower(), lower) >= score_threshold:
            found.add(s)
    return sorted(found)


def extract_languages(text: str):
    return simple_skill_match(text, LANGUAGES)


def extract_frameworks(text: str):
    return simple_skill_match(text, FRAMEWORKS)


def extract_databases(text: str):
    return simple_skill_match(text, DATABASES)
