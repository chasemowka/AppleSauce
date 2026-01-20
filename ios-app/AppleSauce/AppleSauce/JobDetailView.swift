import SwiftUI

struct JobDetailView: View {
    let job: Job
    
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
                
                Text(job.location)
                    .font(.subheadline)
                    .foregroundColor(.gray)
                
                Text("Description")
                    .font(.headline)
                Text(job.description)
                
                Text("Requirements")
                    .font(.headline)
                ForEach(job.requirements, id: \.self) { requirement in
                    Text("• \(requirement)")
                }
                
                Spacer()
            }
            .padding()
            
            // Sidebar for resume suggestions
            VStack(alignment: .leading) {
                Text("Resume Match")
                    .font(.headline)
                    .padding(.bottom)
                
                Text("Matching Skills:")
                    .font(.subheadline)
                    .bold()
                
                ForEach(job.requirements.prefix(2), id: \.self) { skill in
                    HStack {
                        Image(systemName: "checkmark.circle.fill")
                            .foregroundColor(.green)
                        Text(skill)
                    }
                }
                
                Text("Suggestions:")
                    .font(.subheadline)
                    .bold()
                    .padding(.top)
                
                Text("• Highlight \(job.requirements.first ?? "relevant") experience")
                Text("• Add \(job.company) keywords")
                
                Spacer()
            }
            .frame(width: 200)
            .padding()
            .background(Color.gray.opacity(0.1))
        }
        .navigationBarTitleDisplayMode(.inline)
    }
}