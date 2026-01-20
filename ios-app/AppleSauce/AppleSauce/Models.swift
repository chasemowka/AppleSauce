import Foundation

struct Resume: Identifiable, Codable, @unchecked Sendable {
    var id = UUID()
    let fileName: String
    let uploadDate: Date
    let text: String?
    
    enum CodingKeys: String, CodingKey {
        case fileName, uploadDate, text
    }
}

struct Job: Identifiable, Codable, @unchecked Sendable {
    let id: Int
    let title: String
    let company: String
    let skills: [String]
    
    var displayId: String {
        return UUID().uuidString
    }
    
    enum CodingKeys: String, CodingKey {
        case id, title, company, skills
    }
}