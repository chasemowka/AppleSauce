import SwiftUI

struct JobListingsView: View {
    let jobs = [
        Job(title: "iOS Developer", company: "Tech Corp", location: "San Francisco", 
            description: "Build amazing iOS apps", requirements: ["Swift", "SwiftUI"]),
        Job(title: "Mobile Engineer", company: "StartupXYZ", location: "Remote", 
            description: "Cross-platform development", requirements: ["iOS", "Android"]),
        Job(title: "Senior iOS Dev", company: "BigTech", location: "Seattle", 
            description: "Lead iOS development", requirements: ["Swift", "Leadership"])
    ]
    
    var body: some View {
        NavigationView {
            List(jobs) { job in
                NavigationLink(destination: JobDetailView(job: job)) {
                    VStack(alignment: .leading, spacing: 4) {
                        Text(job.title)
                            .font(.headline)
                        Text(job.company)
                            .font(.subheadline)
                            .foregroundColor(.blue)
                        Text(job.location)
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                    .padding(.vertical, 4)
                }
            }
            .navigationTitle("Job Listings")
        }
    }
}