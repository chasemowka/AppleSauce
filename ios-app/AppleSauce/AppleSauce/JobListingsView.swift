import SwiftUI

struct JobListingsView: View {
    @State private var jobs: [Job] = []
    @State private var isLoading = false
    @State private var errorMessage: String?
    
    var body: some View {
        NavigationView {
            Group {
                if isLoading {
                    ProgressView("Loading jobs...")
                } else if let error = errorMessage {
                    VStack {
                        Text("Error: \(error)")
                            .foregroundColor(.red)
                        Button("Retry") {
                            loadJobs()
                        }
                    }
                } else {
                    List(jobs, id: \.displayId) { job in
                        NavigationLink(destination: JobDetailView(job: job)) {
                            VStack(alignment: .leading, spacing: 4) {
                                Text(job.title)
                                    .font(.headline)
                                Text(job.company)
                                    .font(.subheadline)
                                    .foregroundColor(.blue)
                                Text(job.skills.joined(separator: ", "))
                                    .font(.caption)
                                    .foregroundColor(.gray)
                            }
                            .padding(.vertical, 4)
                        }
                    }
                }
            }
            .navigationTitle("Job Listings")
            .onAppear {
                loadJobs()
            }
        }
    }
    
    func loadJobs() {
        isLoading = true
        errorMessage = nil
        
        APIService.getJobs { result in
            DispatchQueue.main.async {
                isLoading = false
                switch result {
                case .success(let fetchedJobs):
                    self.jobs = fetchedJobs
                case .failure(let error):
                    self.errorMessage = error.localizedDescription
                }
            }
        }
    }
}