import Foundation

struct Resume: Identifiable {
    let id = UUID()
    let fileName: String
    let uploadDate: Date
    let skills: [String]
}

struct Job: Identifiable {
    let id = UUID()
    let title: String
    let company: String
    let location: String
    let description: String
    let requirements: [String]
}