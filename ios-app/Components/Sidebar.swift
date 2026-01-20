import SwiftUI

struct Sidebar: View {
    @Binding var selectedSection: SidebarSection
    let suggestionCount: Int
    
    enum SidebarSection: String, CaseIterable {
        case dashboard = "Dashboard"
        case suggestions = "Suggestions"
        case jobs = "Jobs"
        case resume = "Resume"
        case settings = "Settings"
        
        var icon: String {
            switch self {
            case .dashboard: return "house"
            case .suggestions: return "lightbulb"
            case .jobs: return "briefcase"
            case .resume: return "doc.text"
            case .settings: return "gear"
            }
        }
    }
    
    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header
            VStack(alignment: .leading, spacing: 8) {
                Text("Resume AI")
                    .font(.title2)
                    .fontWeight(.bold)
                    .foregroundColor(.textPrimary)
                
                Text("Optimize your career")
                    .font(.caption1)
                    .foregroundColor(.textSecondary)
            }
            .padding(.horizontal, 20)
            .padding(.top, 20)
            .padding(.bottom, 24)
            
            // Navigation Items
            VStack(spacing: 4) {
                ForEach(SidebarSection.allCases, id: \.self) { section in
                    SidebarItem(
                        section: section,
                        isSelected: selectedSection == section,
                        badgeCount: section == .suggestions ? suggestionCount : nil
                    ) {
                        selectedSection = section
                    }
                }
            }
            .padding(.horizontal, 12)
            
            Spacer()
            
            // Footer
            VStack(alignment: .leading, spacing: 8) {
                Divider()
                    .padding(.horizontal, 8)
                
                HStack(spacing: 12) {
                    Circle()
                        .fill(Color.success)
                        .frame(width: 32, height: 32)
                        .overlay(
                            Text("JD")
                                .font(.caption1)
                                .fontWeight(.medium)
                                .foregroundColor(.white)
                        )
                    
                    VStack(alignment: .leading, spacing: 2) {
                        Text("John Doe")
                            .font(.footnote)
                            .fontWeight(.medium)
                            .foregroundColor(.textPrimary)
                        
                        Text("Premium Plan")
                            .font(.caption2)
                            .foregroundColor(.textSecondary)
                    }
                    
                    Spacer()
                }
                .padding(.horizontal, 20)
                .padding(.bottom, 20)
            }
        }
        .frame(width: 240)
        .background(Color.backgroundSecondary)
        .overlay(
            Rectangle()
                .fill(Color.borderLight)
                .frame(width: 1),
            alignment: .trailing
        )
    }
}

struct SidebarItem: View {
    let section: Sidebar.SidebarSection
    let isSelected: Bool
    let badgeCount: Int?
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 12) {
                Image(systemName: section.icon)
                    .font(.system(size: 16, weight: .medium))
                    .foregroundColor(isSelected ? .primaryBlue : .textSecondary)
                    .frame(width: 20)
                
                Text(section.rawValue)
                    .font(.callout)
                    .fontWeight(isSelected ? .medium : .regular)
                    .foregroundColor(isSelected ? .primaryBlue : .textPrimary)
                
                Spacer()
                
                if let count = badgeCount, count > 0 {
                    Text("\(count)")
                        .font(.caption2)
                        .fontWeight(.medium)
                        .foregroundColor(.white)
                        .padding(.horizontal, 6)
                        .padding(.vertical, 2)
                        .background(Color.error)
                        .cornerRadius(8)
                }
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 10)
            .background(
                RoundedRectangle(cornerRadius: 8)
                    .fill(isSelected ? Color.primaryBlue.opacity(0.1) : Color.clear)
            )
        }
        .buttonStyle(PlainButtonStyle())
    }
}

#Preview {
    Sidebar(selectedSection: .constant(.suggestions), suggestionCount: 3)
}