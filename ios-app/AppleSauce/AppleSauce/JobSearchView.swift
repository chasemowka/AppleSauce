import SwiftUI

struct JobSearchView: View {
    @State private var searchText = ""
    @State private var jobs: [Job] = []
    
    var body: some View {
        VStack {
            SearchBar(text: $searchText, onSearchButtonClicked: searchJobs)
            
            List(jobs) { job in
                JobCard(job: job)
            }
        }
        .navigationTitle("Job Search")
    }
    
    private func searchJobs() {
        APIService.shared.searchJobs(keywords: searchText) { result in
            DispatchQueue.main.async {
                switch result {
                case .success(let fetchedJobs):
                    self.jobs = fetchedJobs
                case .failure:
                    self.jobs = []
                }
            }
        }
    }
}

struct SearchBar: View {
    @Binding var text: String
    let onSearchButtonClicked: () -> Void
    
    var body: some View {
        HStack {
            TextField("Search jobs...", text: $text)
                .textFieldStyle(RoundedBorderTextFieldStyle())
                .onSubmit {
                    onSearchButtonClicked()
                }
            
            Button("Search", action: onSearchButtonClicked)
        }
        .padding()
    }
}

struct JobCard: View {
    let job: Job
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(job.title)
                    .font(.headline)
                Text(job.company)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
                Text(job.location)
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            
            Spacer()
            
            MatchIndicator(percentage: job.matchPercentage)
        }
        .padding(.vertical, 4)
    }
}

struct MatchIndicator: View {
    let percentage: Int
    
    private var color: Color {
        switch percentage {
        case 51...100: return .green
        case 50: return .yellow
        default: return .red
        }
    }
    
    var body: some View {
        ZStack {
            Circle()
                .fill(color)
                .frame(width: 40, height: 40)
            
            Text("\(percentage)%")
                .font(.caption)
                .fontWeight(.bold)
                .foregroundColor(.white)
        }
    }
}

struct Job: Identifiable {
    let id = UUID()
    let title: String
    let company: String
    let location: String
    let matchPercentage: Int
}