import SwiftUI

struct JobCard: View {
    let title: String
    let company: String
    let location: String
    let salary: String?
    let isBookmarked: Bool
    let onBookmarkTap: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text(title)
                        .font(.title3)
                        .foregroundColor(.textPrimary)
                        .lineLimit(2)
                    
                    Text(company)
                        .font(.callout)
                        .foregroundColor(.textSecondary)
                }
                
                Spacer()
                
                Button(action: onBookmarkTap) {
                    Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                        .foregroundColor(isBookmarked ? .primaryBlue : .textTertiary)
                        .font(.system(size: 18))
                }
            }
            
            HStack {
                Label(location, systemImage: "location")
                    .font(.footnote)
                    .foregroundColor(.textSecondary)
                
                if let salary = salary {
                    Spacer()
                    Text(salary)
                        .font(.footnote)
                        .foregroundColor(.success)
                        .fontWeight(.medium)
                }
            }
        }
        .padding(16)
        .background(Color.backgroundCard)
        .cornerRadius(12)
        .shadow(color: .black.opacity(0.05), radius: 8, x: 0, y: 2)
    }
}

#Preview {
    JobCard(
        title: "iOS Developer",
        company: "Tech Company",
        location: "San Francisco, CA",
        salary: "$120k - $150k",
        isBookmarked: false,
        onBookmarkTap: {}
    )
    .padding()
}