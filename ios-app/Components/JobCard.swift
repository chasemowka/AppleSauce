import SwiftUI

struct JobCard: View {
    let title: String
    let company: String
    let location: String
    let salary: String?
    let isBookmarked: Bool
    let onBookmarkTap: () -> Void
    
    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 6) {
                    Text(title)
                        .font(.title3)
                        .foregroundColor(.textPrimary)
                        .lineLimit(2)
                    
                    Text(company)
                        .font(.bodyMedium)
                        .foregroundColor(.textSecondary)
                }
                
                Spacer()
                
                Button(action: onBookmarkTap) {
                    Image(systemName: isBookmarked ? "bookmark.fill" : "bookmark")
                        .foregroundColor(isBookmarked ? .primaryBrand : .textTertiary)
                        .font(.system(size: 20))
                        .padding(8)
                        .background(Color.backgroundPrimary)
                        .clipShape(Circle())
                }
            }
            
            HStack(spacing: 8) {
                Label(location, systemImage: "location.fill")
                    .font(.caption1)
                    .padding(.horizontal, 10)
                    .padding(.vertical, 6)
                    .background(Color.backgroundPrimary)
                    .foregroundColor(.textSecondary)
                    .cornerRadius(20)
                
                if let salary = salary {
                    Text(salary)
                        .font(.caption1)
                        .padding(.horizontal, 10)
                        .padding(.vertical, 6)
                        .background(Color.success.opacity(0.1))
                        .foregroundColor(.success)
                        .cornerRadius(20)
                }
                
                Spacer()
            }
        }
        .padding(20)
        .background(Color.backgroundCard)
        .cornerRadius(24)
        .shadow(color: .black.opacity(0.08), radius: 12, x: 0, y: 6)
        .overlay(
            RoundedRectangle(cornerRadius: 24)
                .stroke(Color.white.opacity(0.5), lineWidth: 1)
        )
    }
}

#Preview {
    ZStack {
        Color.backgroundPrimary.ignoresSafeArea()
        JobCard(
            title: "Senior iOS Engineer",
            company: "Apple Inc.",
            location: "Cupertino, CA",
            salary: "$180k - $220k",
            isBookmarked: true,
            onBookmarkTap: {}
        )
        .padding()
    }
}