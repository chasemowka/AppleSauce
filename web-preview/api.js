// AppleSauce API Client
const API_BASE = 'http://127.0.0.1:8000';

const api = {
    // Search jobs from all sources
    async searchJobs(query = 'software developer', source = 'all') {
        const params = new URLSearchParams({ query, source });
        const response = await fetch(`${API_BASE}/jobs?${params}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        const data = await response.json();
        return data.jobs || [];
    },

    // Search company-specific jobs
    async searchCompanyJobs(company, keywords = '') {
        try {
            const params = keywords ? `?keywords=${encodeURIComponent(keywords)}` : '';
            const response = await fetch(`${API_BASE}/jobs/company/${company}${params}`);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error(`Error fetching ${company} jobs:`, error);
            return [];
        }
    },

    // Upload and parse resume
    async uploadResume(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const response = await fetch(`${API_BASE}/upload-resume`, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Error uploading resume:', error);
            return null;
        }
    },

    // Match jobs against resume
    async matchJobs(resumeText, jobs) {
        try {
            const response = await fetch(`${API_BASE}/match`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ resume_text: resumeText, jobs })
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Error matching jobs:', error);
            return [];
        }
    }
};
