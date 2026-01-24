// AppleSauce API Client
const API_BASE = 'http://127.0.0.1:8001';

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

    // Get Dashboard Stats
    async getDashboard(token) {
        try {
            const response = await fetch(`${API_BASE}/user/dashboard`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Dashboard error:', error);
            return null;
        }
    },

    // Upload and parse resume
    async uploadResume(file, token) {
        try {
            const formData = new FormData();
            formData.append('file', file);

            const headers = {};
            if (token) headers['Authorization'] = `Bearer ${token}`;

            const response = await fetch(`${API_BASE}/user/resumes/upload`, {
                method: 'POST',
                headers: headers,
                body: formData
            });

            // Fallback to public endpoint if auth fails or not provided
            if (response.status === 401 || response.status === 404) {
                return this.uploadResumePublic(file);
            }

            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (error) {
            console.error('Error uploading resume:', error);
            return this.uploadResumePublic(file);
        }
    },

    async uploadResumePublic(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            const response = await fetch(`${API_BASE}/upload-resume`, {
                method: 'POST',
                body: formData
            });
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            return await response.json();
        } catch (e) {
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
