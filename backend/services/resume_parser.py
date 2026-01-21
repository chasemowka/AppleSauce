import PyPDF2
from docx import Document
import io
import re
from typing import Dict, List, Any

# Expanded skill keywords for better extraction
TECH_SKILLS = [
    # Programming languages
    "python", "javascript", "typescript", "java", "c++", "c#", "go", "golang", "rust",
    "swift", "kotlin", "ruby", "php", "scala", "r", "matlab", "perl", "shell", "bash",
    # Web frameworks
    "react", "angular", "vue", "vue.js", "node.js", "nodejs", "express", "django",
    "flask", "fastapi", "spring", "rails", "laravel", "next.js", "nextjs", "svelte",
    # Cloud & DevOps
    "aws", "azure", "gcp", "google cloud", "docker", "kubernetes", "k8s", "terraform",
    "ansible", "jenkins", "ci/cd", "github actions", "gitlab", "circleci",
    # Databases
    "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "elasticsearch",
    "dynamodb", "cassandra", "oracle", "sqlite", "graphql",
    # Data & ML
    "machine learning", "deep learning", "tensorflow", "pytorch", "scikit-learn",
    "pandas", "numpy", "data science", "nlp", "computer vision", "ai",
    # Other tech
    "git", "linux", "unix", "rest api", "microservices", "agile", "scrum",
    "jira", "confluence", "figma", "html", "css", "sass", "webpack",
]

# Section header patterns
SECTION_PATTERNS = {
    "skills": r"(?i)^[\s]*(?:technical\s+)?skills?|technologies|tech\s+stack|competencies",
    "experience": r"(?i)^[\s]*(?:work\s+)?experience|employment|work\s+history|professional\s+experience",
    "education": r"(?i)^[\s]*education|academic|degrees?|qualifications",
    "summary": r"(?i)^[\s]*(?:professional\s+)?summary|objective|profile|about\s+me",
    "projects": r"(?i)^[\s]*projects?|portfolio",
    "certifications": r"(?i)^[\s]*certifications?|certificates?|licenses?",
}

# Date patterns for experience parsing
DATE_PATTERNS = [
    r"(?i)(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?\s*\d{4}",
    r"\d{1,2}/\d{4}",
    r"\d{4}\s*[-–]\s*(?:\d{4}|present|current)",
]


def parse_resume(content: bytes, filename: str) -> str:
    """Extract text from PDF or DOCX files (legacy function for compatibility)"""
    try:
        if filename.lower().endswith('.pdf'):
            return _parse_pdf(content)
        elif filename.lower().endswith('.docx'):
            return _parse_docx(content)
        else:
            return "Unsupported file format"
    except Exception as e:
        return f"Error parsing file: {str(e)}"


def parse_resume_structured(content: bytes, filename: str) -> Dict[str, Any]:
    """Extract structured data from PDF or DOCX files"""
    try:
        if filename.lower().endswith('.pdf'):
            text = _parse_pdf(content)
        elif filename.lower().endswith('.docx'):
            text = _parse_docx(content)
        else:
            return {"error": "Unsupported file format", "text": "", "skills": [], "sections": {}}

        # Extract structured data
        skills = _extract_skills(text)
        sections = _extract_sections(text)
        experience_years = _estimate_experience_years(text)

        return {
            "text": text,
            "skills": skills,
            "sections": sections,
            "experience_years": experience_years,
        }
    except Exception as e:
        return {"error": str(e), "text": "", "skills": [], "sections": {}}


def _parse_pdf(content: bytes) -> str:
    """Extract text from PDF"""
    pdf_file = io.BytesIO(content)
    reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


def _parse_docx(content: bytes) -> str:
    """Extract text from DOCX"""
    doc_file = io.BytesIO(content)
    doc = Document(doc_file)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def _extract_skills(text: str) -> List[str]:
    """Extract technical skills from resume text"""
    text_lower = text.lower()
    found_skills = []

    for skill in TECH_SKILLS:
        # Use word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill) + r'\b'
        if re.search(pattern, text_lower):
            # Normalize skill name (capitalize properly)
            normalized = skill.title() if len(skill) > 3 else skill.upper()
            if normalized not in found_skills:
                found_skills.append(normalized)

    return found_skills


def _extract_sections(text: str) -> Dict[str, str]:
    """Extract resume sections based on common headers"""
    sections = {}
    lines = text.split('\n')

    current_section = None
    current_content = []

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped:
            continue

        # Check if this line is a section header
        found_section = None
        for section_name, pattern in SECTION_PATTERNS.items():
            if re.match(pattern, line_stripped):
                found_section = section_name
                break

        if found_section:
            # Save previous section
            if current_section and current_content:
                sections[current_section] = '\n'.join(current_content).strip()
            current_section = found_section
            current_content = []
        elif current_section:
            current_content.append(line_stripped)

    # Save last section
    if current_section and current_content:
        sections[current_section] = '\n'.join(current_content).strip()

    return sections


def _estimate_experience_years(text: str) -> int:
    """Estimate years of experience from date ranges in resume"""
    text_lower = text.lower()

    # Look for explicit "X years of experience" patterns
    explicit_pattern = r'(\d+)\+?\s*(?:years?|yrs?)(?:\s+of)?\s+(?:experience|exp)'
    match = re.search(explicit_pattern, text_lower)
    if match:
        return int(match.group(1))

    # Try to find date ranges and calculate
    year_pattern = r'\b(20\d{2}|19\d{2})\b'
    years = [int(y) for y in re.findall(year_pattern, text)]

    if years:
        # Check for "present" or "current" indicating ongoing employment
        if re.search(r'\b(present|current|now)\b', text_lower):
            years.append(2026)  # Current year

        if len(years) >= 2:
            return max(years) - min(years)

    return 0