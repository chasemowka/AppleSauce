import SwiftUI

struct JobDetailView: View {
    let job: Job
    @State private var suggestions: [String] = []
    @State private var isLoadingSuggestions = false
    
    var body: some View {
        HStack {
            // Main job details
            VStack(alignment: .leading, spacing: 16) {
                Text(job.title)
                    .font(.largeTitle)
                    .bold()
                
                Text(job.company)
                    .font(.title2)
                    .foregroundColor(.blue)
                
                Text("Required Skills")
                    .font(.headline)
                    .padding(.top)
                
                ForEach(job.skills, id: \.self) { skill in
                    Text("• \(skill)")
                }
                
                Spacer()
                
                Button(action: {
                    // Open job posting URL
                }) {
                    Text("Apply Now")
                        .frame(maxWidth: .infinity)
                        .padding()
                        .background(Color.blue)
                        .foregroundColor(.white)
                        .cornerRadius(10)
                }
            }
            .padding()
            
            // Sidebar for resume suggestions
            VStack(alignment: .leading) {
                Text("Resume Suggestions")
                    .font(.headline)
                    .padding(.bottom)
                
                if isLoadingSuggestions {
                    ProgressView()
                } else if suggestions.isEmpty {
                    Text("Upload a resume to get personalized suggestions")
                        .font(.caption)
                        .foregroundColor(.gray)
                } else {
                    ForEach(suggestions, id: \.self) { suggestion in
                        HStack(alignment: .top) {
                            Image(systemName: "lightbulb.fill")
                                .foregroundColor(.orange)
                            Text(suggestion)
                                .font(.caption)
                        }
                        .padding(.bottom, 8)
                    }
                }
                
                Spacer()
            }
            .frame(width: 200)
            .padding()
            .background(Color.gray.opacity(0.1))
        }
        .navigationBarTitleDisplayMode(.inline)
        .onAppear {
            loadSuggestions()
        }
    }
    
    func loadSuggestions() {
        isLoadingSuggestions = true
        
        // For now, use placeholder resume text
        // In production, get this from uploaded resume
        let placeholderResume = "iOS developer with Swift experience"
        
        APIService.getSuggestions(resumeText: placeholderResume, jobId: job.id) { result in
            DispatchQueue.main.async {
                isLoadingSuggestions = false
                if case .success(let fetchedSuggestions) = result {
                    self.suggestions = fetchedSuggestions
                }
            }
        }
    }
}