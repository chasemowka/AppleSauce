import SwiftUI

struct SuggestionCard: View {
    let title: String
    let description: String
    let priority: SuggestionPriority
    let onApplyTap: () -> Void
    
    enum SuggestionPriority {
        case high, medium, low
        
        var color: Color {
            switch self {
            case .high: return .error
            case .medium: return .warning
            case .low: return .success
            }
        }
        
        var text: String {
            switch self {
            case .high: return "High"
            case .medium: return "Medium"
            case .low: return "Low"
            }
        }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Text(priority.text)
                    .font(.caption1)
                    .fontWeight(.medium)
                    .foregroundColor(.white)
                    .padding(.horizontal, 8)
                    .padding(.vertical, 4)
                    .background(priority.color)
                    .cornerRadius(6)
                
                Spacer()
            }
            
            Text(title)
                .font(.callout)
                .fontWeight(.medium)
                .foregroundColor(.textPrimary)
                .lineLimit(2)
            
            Text(description)
                .font(.footnote)
                .foregroundColor(.textSecondary)
                .lineLimit(3)
            
            Button(action: onApplyTap) {
                Text("Apply Suggestion")
                    .font(.footnote)
                    .fontWeight(.medium)
                    .foregroundColor(.primaryBlue)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(Color.primaryBlue.opacity(0.1))
                    .cornerRadius(8)
            }
        }
        .padding(16)
        .background(Color.backgroundCard)
        .cornerRadius(12)
        .overlay(
            RoundedRectangle(cornerRadius: 12)
                .stroke(Color.borderLight, lineWidth: 1)
        )
    }
}

#Preview {
    SuggestionCard(
        title: "Add Technical Skills",
        description: "Include programming languages and frameworks relevant to your target role",
        priority: .high,
        onApplyTap: {}
    )
    .padding()
}