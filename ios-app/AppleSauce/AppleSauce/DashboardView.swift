import SwiftUI

struct DashboardView: View {
    var body: some View {
        NavigationView {
            ScrollView {
                VStack(spacing: 20) {
                    // Stats Cards
                    HStack(spacing: 15) {
                        StatCard(title: "Total Jobs", value: "247", color: .blue)
                        StatCard(title: "Matches", value: "12", color: .green)
                        StatCard(title: "Resume", value: "✓", color: .orange)
                    }
                    .padding(.horizontal)
                    
                    // Recent Jobs Section
                    VStack(alignment: .leading, spacing: 12) {
                        HStack {
                            Text("Recent Jobs")
                                .font(.headline)
                                .fontWeight(.semibold)
                            Spacer()
                            Button("View All") {}
                                .font(.caption)
                                .foregroundColor(.blue)
                        }
                        .padding(.horizontal)
                        
                        VStack(spacing: 8) {
                            JobCard(title: "iOS Developer", company: "Tech Corp", location: "Remote")
                            JobCard(title: "Swift Engineer", company: "StartupXYZ", location: "San Francisco")
                            JobCard(title: "Mobile Developer", company: "BigTech Inc", location: "Seattle")
                        }
                    }
                    
                    // Quick Actions
                    VStack(spacing: 12) {
                        Text("Quick Actions")
                            .font(.headline)
                            .fontWeight(.semibold)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .padding(.horizontal)
                        
                        VStack(spacing: 10) {
                            ActionButton(title: "Upload Resume", icon: "doc.badge.plus", color: .blue)
                            ActionButton(title: "Search Jobs", icon: "magnifyingglass", color: .green)
                            ActionButton(title: "View Matches", icon: "heart.fill", color: .red)
                        }
                        .padding(.horizontal)
                    }
                }
                .padding(.vertical)
            }
            .navigationTitle("Dashboard")
        }
    }
}

struct StatCard: View {
    let title: String
    let value: String
    let color: Color
    
    var body: some View {
        VStack(spacing: 8) {
            Text(value)
                .font(.title2)
                .fontWeight(.bold)
                .foregroundColor(color)
            Text(title)
                .font(.caption)
                .foregroundColor(.secondary)
        }
        .frame(maxWidth: .infinity)
        .padding()
        .background(Color(.systemGray6))
        .cornerRadius(12)
    }
}

struct JobCard: View {
    let title: String
    let company: String
    let location: String
    
    var body: some View {
        HStack {
            VStack(alignment: .leading, spacing: 4) {
                Text(title)
                    .font(.subheadline)
                    .fontWeight(.medium)
                Text(company)
                    .font(.caption)
                    .foregroundColor(.secondary)
                Text(location)
                    .font(.caption2)
                    .foregroundColor(.secondary)
            }
            Spacer()
            Button("Apply") {}
                .font(.caption)
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(8)
        }
        .padding()
        .background(Color(.systemBackground))
        .cornerRadius(10)
        .shadow(color: .black.opacity(0.05), radius: 2, x: 0, y: 1)
        .padding(.horizontal)
    }
}

struct ActionButton: View {
    let title: String
    let icon: String
    let color: Color
    
    var body: some View {
        Button(action: {}) {
            HStack {
                Image(systemName: icon)
                    .foregroundColor(color)
                Text(title)
                    .fontWeight(.medium)
                Spacer()
                Image(systemName: "chevron.right")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            .padding()
            .background(Color(.systemGray6))
            .cornerRadius(10)
        }
        .foregroundColor(.primary)
    }
}

#Preview {
    DashboardView()
}