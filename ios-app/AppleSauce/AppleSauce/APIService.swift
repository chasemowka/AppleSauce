import Foundation

class APIService {
    // Change this to your Mac's local IP when testing on physical device
    // For simulator, localhost works fine
    static let baseURL = "http://localhost:8000"
    
    // Upload resume
    static func uploadResume(fileURL: URL, completion: @escaping (Result<ResumeParseResponse, Error>) -> Void) {
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
    
    // Get job listings
    static func getJobs(completion: @escaping (Result<[Job], Error>) -> Void) {
        let url = URL(string: "\(baseURL)/jobs")!
        
        URLSession.shared.dataTask(with: url) { data, response, error in
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
}

// Response models
struct ResumeParseResponse: Codable {
    let text: String
    let filename: String
}

struct JobsResponse: Codable {
    let jobs: [Job]
}

struct MatchResponse: Codable {
    let matches: [JobMatch]
}

struct JobMatch: Codable {
    let job: Job
    let score: Double
}

struct SuggestionsResponse: Codable {
    let suggestions: [String]
}
