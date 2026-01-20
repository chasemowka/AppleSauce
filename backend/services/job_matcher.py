import re
from typing import List, Dict

def match_jobs(resume_text: str, jobs: List[Dict]) -> List[Dict]:
    """Match jobs based on keyword overlap"""
    resume_words = set(re.findall(r'\b\w+\b', resume_text.lower()))
    matches = []
    
    for job in jobs:
        job_skills = [skill.lower() for skill in job["skills"]]
        matched_skills = [skill for skill in job_skills if skill in resume_words]
        
        if matched_skills:
            score = len(matched_skills) / len(job_skills)
            matches.append({
                **job,
                "matched_skills": matched_skills,
                "score": round(score, 2)
            })
    
    return sorted(matches, key=lambda x: x["score"], reverse=True)

def get_suggestions(jobs: List[Dict]) -> List[Dict]:
    """Get job suggestions (returns top 3 jobs)"""
    return jobs[:3]