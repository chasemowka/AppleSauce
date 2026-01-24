import Foundation

class APIService {
    // Change this to your Mac's local IP when testing on physical device
    // For simulator, localhost works fine
    static let baseURL = "http://127.0.0.1:8001"

    // MARK: - Helper to add auth header
    private static func addAuthHeader(to request: inout URLRequest) {
        if let token = AuthManager.shared.getToken() {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }
    }

    // MARK: - Resume Endpoints

    // Upload resume (authenticated - saves to profile)
    static func uploadResume(fileURL: URL, completion: @escaping (Result<ResumeParseResponse, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/user/resumes/upload")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        addAuthHeader(to: &request)

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var data = Data()
        data.append("--\(boundary)\r\n".data(using: .utf8)!)
        data.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileURL.lastPathComponent)\"\r\n".data(using: .utf8)!)
        data.append("Content-Type: application/pdf\r\n\r\n".data(using: .utf8)!)

        if let fileData = try? Data(contentsOf: fileURL) {
            data.append(fileData)
        }
        data.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = data

        URLSession.shared.dataTask(with: request) { responseData, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            // If auth fails, fallback to public endpoint
            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 401 {
                uploadResumePublic(fileURL: fileURL, completion: completion)
                return
            }

            guard let responseData = responseData else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
                return
            }

            do {
                let result = try JSONDecoder().decode(ResumeParseResponse.self, from: responseData)
                completion(.success(result))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    // Upload resume (public - no auth required)
    static func uploadResumePublic(fileURL: URL, completion: @escaping (Result<ResumeParseResponse, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/upload-resume")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"

        let boundary = UUID().uuidString
        request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")

        var data = Data()
        data.append("--\(boundary)\r\n".data(using: .utf8)!)
        data.append("Content-Disposition: form-data; name=\"file\"; filename=\"\(fileURL.lastPathComponent)\"\r\n".data(using: .utf8)!)
        data.append("Content-Type: application/pdf\r\n\r\n".data(using: .utf8)!)

        if let fileData = try? Data(contentsOf: fileURL) {
            data.append(fileData)
        }
        data.append("\r\n--\(boundary)--\r\n".data(using: .utf8)!)

        request.httpBody = data

        URLSession.shared.dataTask(with: request) { responseData, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let responseData = responseData else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
                return
            }

            do {
                let result = try JSONDecoder().decode(ResumeParseResponse.self, from: responseData)
                completion(.success(result))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    // MARK: - Job Endpoints

    // Get job listings
    static func getJobs(query: String = "software developer", completion: @escaping (Result<[Job], Error>) -> Void) {
        var components = URLComponents(string: "\(baseURL)/jobs")!
        components.queryItems = [URLQueryItem(name: "query", value: query)]

        var request = URLRequest(url: components.url!)
        addAuthHeader(to: &request)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
                return
            }

            do {
                let result = try JSONDecoder().decode(JobsResponse.self, from: data)
                completion(.success(result.jobs))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    // Match resume to jobs
    static func matchJobs(resumeText: String, completion: @escaping (Result<[JobMatch], Error>) -> Void) {
        let url = URL(string: "\(baseURL)/match")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        addAuthHeader(to: &request)

        let body = ["resume_text": resumeText]
        request.httpBody = try? JSONEncoder().encode(body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
                return
            }

            do {
                let result = try JSONDecoder().decode(MatchResponse.self, from: data)
                completion(.success(result.matches))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    // Get resume suggestions for a job
    static func getSuggestions(resumeText: String, jobId: Int, completion: @escaping (Result<[String], Error>) -> Void) {
        let url = URL(string: "\(baseURL)/suggestions")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        addAuthHeader(to: &request)

        let body = ["resume_text": resumeText, "job_id": jobId] as [String : Any]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
                return
            }

            do {
                let result = try JSONDecoder().decode(SuggestionsResponse.self, from: data)
                completion(.success(result.suggestions))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    // MARK: - User/Dashboard Endpoints

    // Get user dashboard stats
    static func getDashboard(completion: @escaping (Result<DashboardResponse, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/user/dashboard")!
        var request = URLRequest(url: url)
        addAuthHeader(to: &request)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
                return
            }

            do {
                let result = try JSONDecoder().decode(DashboardResponse.self, from: data)
                completion(.success(result))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    // MARK: - Saved Jobs

    // Save a job
    static func saveJob(_ job: Job, matchPercentage: Int? = nil, completion: @escaping (Result<Bool, Error>) -> Void) {
        let url = URL(string: "\(baseURL)/user/saved-jobs")!
        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        addAuthHeader(to: &request)

        var body: [String: Any] = [
            "title": job.title,
            "company": job.company
        ]
        if let percentage = matchPercentage {
            body["match_percentage"] = percentage
        }

        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            if let httpResponse = response as? HTTPURLResponse, httpResponse.statusCode == 200 || httpResponse.statusCode == 201 {
                completion(.success(true))
            } else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "Failed to save job"])))
            }
        }.resume()
    }

    // Get saved jobs
    static func getSavedJobs(completion: @escaping (Result<[SavedJob], Error>) -> Void) {
        let url = URL(string: "\(baseURL)/user/saved-jobs")!
        var request = URLRequest(url: url)
        addAuthHeader(to: &request)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "", code: -1, userInfo: [NSLocalizedDescriptionKey: "No data"])))
                return
            }

            do {
                let result = try JSONDecoder().decode(SavedJobsResponse.self, from: data)
                completion(.success(result.savedJobs))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

// MARK: - Response Models

struct ResumeParseResponse: Codable, @unchecked Sendable {
    let text: String?
    let filename: String
    let skills: [String]?
    let sections: [String: String]?
    let id: Int?

    enum CodingKeys: String, CodingKey {
        case text, filename, skills, sections, id
    }
}

struct JobsResponse: Codable, @unchecked Sendable {
    let jobs: [Job]
}

struct MatchResponse: Codable, @unchecked Sendable {
    let matches: [JobMatch]
}

struct JobMatch: Codable, @unchecked Sendable {
    let job: Job
    let score: Double
}

struct SuggestionsResponse: Codable, @unchecked Sendable {
    let suggestions: [String]
}

struct DashboardResponse: Codable, @unchecked Sendable {
    let user: DashboardUser
    let resumes: ResumeStats
    let jobs: JobStats

    struct DashboardUser: Codable {
        let name: String?
        let email: String
    }

    struct ResumeStats: Codable {
        let count: Int
        let primary: PrimaryResume?
    }

    struct PrimaryResume: Codable {
        let id: Int
        let filename: String
        let skillsCount: Int?
        let qualityScore: Int?

        enum CodingKeys: String, CodingKey {
            case id, filename
            case skillsCount = "skills_count"
            case qualityScore = "quality_score"
        }
    }

    struct JobStats: Codable {
        let saved: Int
        let applied: Int
        let interviewing: Int
        let total: Int
    }
}

struct SavedJob: Codable, Identifiable, @unchecked Sendable {
    let id: Int
    let title: String
    let company: String
    let location: String?
    let url: String?
    let matchPercentage: Int?
    let status: String
    let createdAt: String?

    enum CodingKeys: String, CodingKey {
        case id, title, company, location, url, status
        case matchPercentage = "match_percentage"
        case createdAt = "created_at"
    }
}

struct SavedJobsResponse: Codable, @unchecked Sendable {
    let savedJobs: [SavedJob]
    let count: Int

    enum CodingKeys: String, CodingKey {
        case savedJobs = "saved_jobs"
        case count
    }
}
