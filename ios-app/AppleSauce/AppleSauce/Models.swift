import Foundation

struct Resume: Identifiable, Codable {
    let id = UUID()
    let fileName: String
    let uploadDate: Date
    let text: String?
}

struct Job: Identifiable, Codable {
    let id: Int
    let title: String
    let company: String
    let skills: [String]
    
    var displayId: String {
        return UUID().uuidString
    }
}