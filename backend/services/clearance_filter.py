from enum import Enum
from typing import List, Dict, Optional
import re

class ClearanceLevel(Enum):
    NONE = "none"
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"

class ClearanceFilter:
    """Service to filter jobs by security clearance requirements"""
    
    # Keywords for each clearance level
    CLEARANCE_KEYWORDS = {
        ClearanceLevel.CONFIDENTIAL: [
            "confidential clearance", "confidential security clearance"
        ],
        ClearanceLevel.SECRET: [
            "secret clearance", "secret security clearance", "security clearance"
        ],
        ClearanceLevel.TOP_SECRET: [
            "top secret", "ts/sci", "ts clearance", "top secret clearance",
            "sci clearance", "polygraph"
        ]
    }
    
    def extract_clearance_level(self, job_description: str) -> ClearanceLevel:
        """Extract clearance requirement from job description"""
        description_lower = job_description.lower()
        
        # Check for Top Secret first (most specific)
        for keyword in self.CLEARANCE_KEYWORDS[ClearanceLevel.TOP_SECRET]:
            if keyword in description_lower:
                return ClearanceLevel.TOP_SECRET
        
        # Check for Secret
        for keyword in self.CLEARANCE_KEYWORDS[ClearanceLevel.SECRET]:
            if keyword in description_lower:
                return ClearanceLevel.SECRET
        
        # Check for Confidential
        for keyword in self.CLEARANCE_KEYWORDS[ClearanceLevel.CONFIDENTIAL]:
            if keyword in description_lower:
                return ClearanceLevel.CONFIDENTIAL
        
        return ClearanceLevel.NONE
    
    def filter_jobs_by_clearance(self, jobs: List[Dict], required_level: ClearanceLevel) -> List[Dict]:
        """Filter jobs by clearance level"""
        filtered_jobs = []
        
        for job in jobs:
            job_clearance = self.extract_clearance_level(job.get("description", ""))
            job["clearance_level"] = job_clearance.value
            
            if required_level == ClearanceLevel.NONE or job_clearance == required_level:
                filtered_jobs.append(job)
        
        return filtered_jobs

clearance_filter = ClearanceFilter()