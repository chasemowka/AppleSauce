import os
from typing import Dict, List, Any, Optional
from dotenv import load_dotenv

load_dotenv()

# Try to import anthropic, gracefully handle if not available
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    anthropic = None


class LLMService:
    """Service for LLM-powered resume analysis and suggestions"""

    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY", "")
        self.client = None
        self.model = "claude-3-haiku-20240307"  # Fast and cost-effective for this use case

        if ANTHROPIC_AVAILABLE and self.api_key:
            self.client = anthropic.Anthropic(api_key=self.api_key)

    def is_available(self) -> bool:
        """Check if LLM service is configured and available"""
        return self.client is not None

    def extract_skills_semantic(self, resume_text: str) -> List[str]:
        """Use LLM to extract skills semantically from resume text"""
        if not self.is_available():
            return []

        try:
            prompt = f"""Analyze this resume and extract all technical skills, tools, frameworks, and technologies mentioned.
Return ONLY a JSON array of skill names, nothing else. Be thorough but avoid duplicates.
Focus on: programming languages, frameworks, databases, cloud services, tools, methodologies.

Resume:
{resume_text[:4000]}

Return format: ["skill1", "skill2", "skill3", ...]"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=500,
                messages=[{"role": "user", "content": prompt}]
            )

            # Parse the response
            content = response.content[0].text.strip()
            # Try to extract JSON array
            import json
            if content.startswith("["):
                return json.loads(content)
            return []

        except Exception as e:
            print(f"LLM skill extraction error: {e}")
            return []

    def generate_job_suggestions(
        self,
        resume_text: str,
        resume_skills: List[str],
        job_title: str,
        job_description: str,
        job_skills: List[str],
        matched_skills: List[str]
    ) -> List[Dict[str, str]]:
        """Generate personalized resume improvement suggestions for a specific job"""
        if not self.is_available():
            return self._get_fallback_suggestions(resume_skills, job_skills, matched_skills)

        try:
            missing_skills = [s for s in job_skills if s.lower() not in [m.lower() for m in matched_skills]]

            prompt = f"""You are a career advisor. Analyze this resume against the job posting and provide specific, actionable suggestions to improve the resume for this role.

RESUME SKILLS: {', '.join(resume_skills[:20])}
JOB TITLE: {job_title}
JOB REQUIRED SKILLS: {', '.join(job_skills)}
MATCHED SKILLS: {', '.join(matched_skills)}
MISSING SKILLS: {', '.join(missing_skills)}

JOB DESCRIPTION (excerpt):
{job_description[:1500]}

RESUME (excerpt):
{resume_text[:1500]}

Provide exactly 3-4 specific suggestions. For each suggestion, specify:
1. Priority: "high" (critical gap), "medium" (would help), or "low" (nice to have)
2. A brief title (5-7 words)
3. A specific action the candidate should take (1-2 sentences)

Return as JSON array:
[{{"priority": "high|medium|low", "title": "...", "action": "..."}}]"""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=600,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()
            import json

            # Try to find JSON in response
            start = content.find("[")
            end = content.rfind("]") + 1
            if start >= 0 and end > start:
                suggestions = json.loads(content[start:end])
                return suggestions

            return self._get_fallback_suggestions(resume_skills, job_skills, matched_skills)

        except Exception as e:
            print(f"LLM suggestion generation error: {e}")
            return self._get_fallback_suggestions(resume_skills, job_skills, matched_skills)

    def _get_fallback_suggestions(
        self,
        resume_skills: List[str],
        job_skills: List[str],
        matched_skills: List[str]
    ) -> List[Dict[str, str]]:
        """Generate basic suggestions without LLM"""
        suggestions = []

        # Find missing skills
        missing_skills = [s for s in job_skills if s.lower() not in [m.lower() for m in matched_skills]]

        if missing_skills:
            suggestions.append({
                "priority": "high",
                "title": f"Add missing skills: {', '.join(missing_skills[:3])}",
                "action": f"The job requires {', '.join(missing_skills[:3])} which aren't evident in your resume. Add relevant projects or experience demonstrating these skills."
            })

        if matched_skills:
            suggestions.append({
                "priority": "medium",
                "title": "Expand on matched skills",
                "action": f"You have {', '.join(matched_skills[:3])}. Quantify your achievements with these technologies (e.g., 'Reduced load time by 40% using React')."
            })

        suggestions.append({
            "priority": "low",
            "title": "Tailor your summary",
            "action": "Customize your professional summary to highlight experience most relevant to this specific role."
        })

        return suggestions

    def analyze_resume_quality(self, resume_text: str, sections: Dict[str, str]) -> Dict[str, Any]:
        """Analyze overall resume quality and provide feedback"""
        if not self.is_available():
            return self._get_fallback_quality_analysis(resume_text, sections)

        try:
            prompt = f"""Analyze this resume and provide a quality assessment.

RESUME:
{resume_text[:3000]}

Evaluate and return JSON with:
1. "score": overall score 1-100
2. "strengths": array of 2-3 strong points
3. "improvements": array of 2-3 areas to improve
4. "ats_friendly": boolean - is it ATS (applicant tracking system) friendly?

Return ONLY valid JSON."""

            response = self.client.messages.create(
                model=self.model,
                max_tokens=400,
                messages=[{"role": "user", "content": prompt}]
            )

            content = response.content[0].text.strip()
            import json

            start = content.find("{")
            end = content.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(content[start:end])

            return self._get_fallback_quality_analysis(resume_text, sections)

        except Exception as e:
            print(f"LLM quality analysis error: {e}")
            return self._get_fallback_quality_analysis(resume_text, sections)

    def _get_fallback_quality_analysis(self, resume_text: str, sections: Dict[str, str]) -> Dict[str, Any]:
        """Basic quality analysis without LLM"""
        score = 50
        strengths = []
        improvements = []

        # Check for key sections
        if "experience" in sections:
            score += 15
            strengths.append("Has work experience section")
        else:
            improvements.append("Add a clear work experience section")

        if "skills" in sections:
            score += 10
            strengths.append("Has dedicated skills section")
        else:
            improvements.append("Add a dedicated skills section")

        if "education" in sections:
            score += 10
            strengths.append("Includes education background")

        # Check length
        word_count = len(resume_text.split())
        if 300 <= word_count <= 800:
            score += 10
            strengths.append("Good length and detail level")
        elif word_count < 200:
            improvements.append("Resume may be too brief - add more detail")
        elif word_count > 1000:
            improvements.append("Consider condensing - resume may be too long")

        return {
            "score": min(score, 100),
            "strengths": strengths[:3],
            "improvements": improvements[:3],
            "ats_friendly": "skills" in sections and "experience" in sections
        }


# Initialize singleton
llm_service = LLMService()
