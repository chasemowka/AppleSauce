import re
from typing import List, Dict, Set

# Skill synonyms for better matching
SKILL_SYNONYMS = {
    "javascript": ["js", "ecmascript"],
    "typescript": ["ts"],
    "python": ["py", "python3"],
    "golang": ["go"],
    "nodejs": ["node.js", "node"],
    "postgresql": ["postgres", "psql"],
    "kubernetes": ["k8s"],
    "amazon web services": ["aws"],
    "google cloud platform": ["gcp", "google cloud"],
    "machine learning": ["ml"],
    "artificial intelligence": ["ai"],
    "continuous integration": ["ci/cd", "ci", "cd"],
    "react.js": ["react", "reactjs"],
    "vue.js": ["vue", "vuejs"],
    "next.js": ["next", "nextjs"],
}


def _normalize_skill(skill: str) -> Set[str]:
    """Return a set of normalized variations for a skill"""
    skill_lower = skill.lower().strip()
    variations = {skill_lower}

    # Add synonyms
    for canonical, synonyms in SKILL_SYNONYMS.items():
        if skill_lower == canonical or skill_lower in synonyms:
            variations.add(canonical)
            variations.update(synonyms)

    return variations


def _calculate_skill_score(resume_skills: List[str], job_skills: List[str]) -> tuple:
    """Calculate skill match score and return matched skills"""
    if not job_skills:
        return 0.0, []

    # Normalize resume skills
    resume_skill_set = set()
    for skill in resume_skills:
        resume_skill_set.update(_normalize_skill(skill))

    # Find matches
    matched_skills = []
    for job_skill in job_skills:
        job_skill_variations = _normalize_skill(job_skill)
        if resume_skill_set & job_skill_variations:
            matched_skills.append(job_skill)

    score = len(matched_skills) / len(job_skills) if job_skills else 0
    return score, matched_skills


def _calculate_title_score(resume_text: str, job_title: str) -> float:
    """Calculate how well the job title matches resume content"""
    if not job_title:
        return 0.0

    resume_lower = resume_text.lower()
    title_words = job_title.lower().split()

    # Remove common words
    stop_words = {"the", "a", "an", "and", "or", "at", "in", "for", "-", "/"}
    title_words = [w for w in title_words if w not in stop_words and len(w) > 2]

    if not title_words:
        return 0.0

    matches = sum(1 for word in title_words if word in resume_lower)
    return matches / len(title_words)


def _calculate_keyword_score(resume_text: str, job_description: str) -> float:
    """Calculate general keyword overlap between resume and job description"""
    if not job_description:
        return 0.0

    # Extract significant words from job description
    job_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', job_description.lower()))
    resume_words = set(re.findall(r'\b[a-zA-Z]{4,}\b', resume_text.lower()))

    # Remove very common words
    common_words = {"with", "that", "this", "have", "from", "they", "will", "been",
                    "would", "could", "should", "about", "which", "their", "there",
                    "what", "when", "where", "work", "working", "experience", "team"}
    job_words -= common_words
    resume_words -= common_words

    if not job_words:
        return 0.0

    overlap = len(job_words & resume_words)
    return min(overlap / 20, 1.0)  # Cap at 1.0, expect ~20 keyword matches for full score


def match_jobs(resume_text: str, jobs: List[Dict], resume_skills: List[str] = None) -> List[Dict]:
    """
    Match jobs based on weighted scoring:
    - 50% skill match
    - 30% title match
    - 20% keyword overlap
    """
    # Extract skills from resume text if not provided
    if resume_skills is None:
        resume_skills = []
        # Fall back to extracting words as potential skills
        resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
        resume_skills = list(resume_words)

    matches = []

    for job in jobs:
        job_skills = job.get("skills", [])
        job_title = job.get("title", "")
        job_description = job.get("description", "")

        # Calculate component scores
        skill_score, matched_skills = _calculate_skill_score(resume_skills, job_skills)
        title_score = _calculate_title_score(resume_text, job_title)
        keyword_score = _calculate_keyword_score(resume_text, job_description)

        # Weighted combination: 50% skills, 30% title, 20% keywords
        total_score = (skill_score * 0.5) + (title_score * 0.3) + (keyword_score * 0.2)

        # Convert to percentage (0-100)
        match_percentage = int(round(total_score * 100))

        matches.append({
            **job,
            "matched_skills": matched_skills,
            "match_percentage": match_percentage,
            "score_breakdown": {
                "skills": round(skill_score * 100),
                "title": round(title_score * 100),
                "keywords": round(keyword_score * 100)
            }
        })

    # Sort by match percentage descending
    return sorted(matches, key=lambda x: x["match_percentage"], reverse=True)


def get_suggestions(jobs: List[Dict]) -> List[Dict]:
    """Get job suggestions (returns top 3 jobs)"""
    return jobs[:3]