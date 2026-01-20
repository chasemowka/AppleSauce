import requests
import os
from typing import List, Dict, Optional

class JobAPIService:
    """Service to fetch jobs from multiple sources"""
    
    def __init__(self):
        # Get API keys from environment variables
        self.rapidapi_key = os.getenv("RAPIDAPI_KEY", "")
        
    def search_indeed_jobs(self, query: str, location: str = "United States", num_pages: int = 1) -> List[Dict]:
        """
        Search jobs using JSearch API (aggregates Indeed, LinkedIn, etc.)
        Free tier: 2,500 requests/month
        Sign up: https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch
        """
        if not self.rapidapi_key:
            print("Warning: RAPIDAPI_KEY not set. Using mock data.")
            return self._get_mock_jobs(query)
        
        url = "https://jsearch.p.rapidapi.com/search"
        
        headers = {
            "X-RapidAPI-Key": self.rapidapi_key,
            "X-RapidAPI-Host": "jsearch.p.rapidapi.com"
        }
        
        querystring = {
            "query": query,
            "page": "1",
            "num_pages": str(num_pages),
            "date_posted": "all"
        }
        
        try:
            response = requests.get(url, headers=headers, params=querystring, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Transform to our format
            jobs = []
            for job in data.get("data", []):
                jobs.append({
                    "id": hash(job.get("job_id", "")),
                    "title": job.get("job_title", ""),
                    "company": job.get("employer_name", ""),
                    "location": job.get("job_city", "") + ", " + job.get("job_state", ""),
                    "description": job.get("job_description", ""),
                    "url": job.get("job_apply_link", ""),
                    "posted_date": job.get("job_posted_at_datetime_utc", ""),
                    "skills": self._extract_skills(job.get("job_description", "")),
                    "salary": job.get("job_salary", "Not specified"),
                    "source": "Indeed/JSearch"
                })
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching from JSearch API: {e}")
            return self._get_mock_jobs(query)
    
    def search_company_careers(self, company: str, keywords: str = "") -> List[Dict]:
        """
        Search specific company career pages
        Companies: Netflix, AWS, Microsoft, Oracle, L3Harris, OpenAI
        """
        company_urls = {
            "netflix": "https://jobs.netflix.com/api/search",
            "aws": "https://www.amazon.jobs/en/search.json",
            "microsoft": "https://careers.microsoft.com/professionals/us/en/search-results",
            "oracle": "https://careers.oracle.com/api/jobs",
            "l3harris": "https://careers.l3harris.com/api/jobs",
            "openai": "https://openai.com/careers/search"
        }
        
        company_lower = company.lower()
        
        if company_lower == "aws" or company_lower == "amazon":
            return self._fetch_amazon_jobs(keywords)
        elif company_lower == "netflix":
            return self._fetch_netflix_jobs(keywords)
        elif company_lower == "microsoft":
            return self._fetch_microsoft_jobs(keywords)
        else:
            # For now, return placeholder for other companies
            return [{
                "id": hash(company + keywords),
                "title": f"Software Engineer at {company}",
                "company": company,
                "location": "Various Locations",
                "description": f"Check {company}'s career page for current openings",
                "url": company_urls.get(company_lower, f"https://{company_lower}.com/careers"),
                "skills": keywords.split(),
                "salary": "Competitive",
                "source": f"{company} Careers"
            }]
    
    def _fetch_amazon_jobs(self, keywords: str) -> List[Dict]:
        """Fetch jobs from Amazon/AWS careers API"""
        url = "https://www.amazon.jobs/en/search.json"
        params = {
            "offset": 0,
            "result_limit": 10,
            "sort": "recent",
            "business_category[]": "amazon-web-services",
            "normalized_location[]": "USA"
        }
        
        if keywords:
            params["search"] = keywords
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            for job in data.get("jobs", []):
                jobs.append({
                    "id": hash(job.get("id_icims", "")),
                    "title": job.get("title", ""),
                    "company": "Amazon Web Services",
                    "location": job.get("location", ""),
                    "description": job.get("description", ""),
                    "url": f"https://www.amazon.jobs{job.get('job_path', '')}",
                    "posted_date": job.get("posted_date", ""),
                    "skills": self._extract_skills(job.get("description", "")),
                    "salary": "Competitive",
                    "source": "AWS Careers"
                })
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching AWS jobs: {e}")
            return []
    
    def _fetch_netflix_jobs(self, keywords: str) -> List[Dict]:
        """Fetch jobs from Netflix careers"""
        # Netflix uses Greenhouse API
        url = "https://api.greenhouse.io/v1/boards/netflix/jobs"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            jobs = []
            for job in data.get("jobs", [])[:10]:  # Limit to 10
                if keywords.lower() in job.get("title", "").lower():
                    jobs.append({
                        "id": job.get("id", 0),
                        "title": job.get("title", ""),
                        "company": "Netflix",
                        "location": job.get("location", {}).get("name", ""),
                        "description": job.get("content", ""),
                        "url": job.get("absolute_url", ""),
                        "posted_date": job.get("updated_at", ""),
                        "skills": self._extract_skills(job.get("content", "")),
                        "salary": "Competitive",
                        "source": "Netflix Careers"
                    })
            
            return jobs
            
        except Exception as e:
            print(f"Error fetching Netflix jobs: {e}")
            return []
    
    def _fetch_microsoft_jobs(self, keywords: str) -> List[Dict]:
        """Fetch jobs from Microsoft careers"""
        # Microsoft careers API endpoint
        url = "https://careers.microsoft.com/professionals/us/en/search-results"
        
        # For now, return placeholder - Microsoft's API requires more complex auth
        return [{
            "id": hash("microsoft" + keywords),
            "title": f"Software Engineer - {keywords}",
            "company": "Microsoft",
            "location": "Redmond, WA",
            "description": "Visit Microsoft Careers for current openings",
            "url": "https://careers.microsoft.com",
            "skills": keywords.split(),
            "salary": "Competitive",
            "source": "Microsoft Careers"
        }]
    
    def _extract_skills(self, description: str) -> List[str]:
        """Extract common tech skills from job description"""
        common_skills = [
            "python", "javascript", "java", "react", "node.js", "aws", "docker",
            "kubernetes", "sql", "mongodb", "typescript", "go", "rust", "swift",
            "machine learning", "ai", "devops", "ci/cd", "agile", "rest api"
        ]
        
        description_lower = description.lower()
        found_skills = [skill for skill in common_skills if skill in description_lower]
        
        return found_skills[:5]  # Return top 5
    
    def _get_mock_jobs(self, query: str) -> List[Dict]:
        """Return mock jobs when API is not available"""
        return [
            {
                "id": 1,
                "title": f"Software Engineer - {query}",
                "company": "TechCorp",
                "location": "San Francisco, CA",
                "description": f"Looking for {query} experience",
                "url": "https://example.com/job1",
                "skills": ["python", "javascript", "react"],
                "salary": "$120k - $180k",
                "source": "Mock Data"
            },
            {
                "id": 2,
                "title": f"Senior Developer - {query}",
                "company": "StartupXYZ",
                "location": "Remote",
                "description": f"Remote position for {query}",
                "url": "https://example.com/job2",
                "skills": ["python", "aws", "docker"],
                "salary": "$140k - $200k",
                "source": "Mock Data"
            }
        ]

# Initialize service
job_api_service = JobAPIService()
