import SwiftUI

struct ContentView: View {
    @StateObject private var authManager = AuthManager.shared
    @State private var selectedTab = 0

    var body: some View {
        Group {
            if authManager.isAuthenticated {
                MainAppView(selectedTab: $selectedTab, authManager: authManager)
            } else {
                LoginView(authManager: authManager)
            }
        }
        .animation(.easeInOut(duration: 0.3), value: authManager.isAuthenticated)
    }
}

struct MainAppView: View {
    @Binding var selectedTab: Int
    @ObservedObject var authManager: AuthManager

    var body: some View {
        ZStack(alignment: .bottom) {
            // Main Content Layer
            Group {
                switch selectedTab {
                case 0:
                    DashboardView()
                case 1:
                    ResumeUploadView()
                case 2:
                    JobListingsView()
                default:
                    DashboardView()
                }
            }
            .frame(maxWidth: .infinity, maxHeight: .infinity)

            // Background Gradient for Floating Menu
            LinearGradient(gradient: Gradient(colors: [Color.backgroundPrimary.opacity(0), Color.backgroundPrimary]), startPoint: .top, endPoint: .bottom)
                .frame(height: 100)
                .allowsHitTesting(false)

            // Floating Dock
            HStack(spacing: 0) {
                TabButton(icon: "house.fill", title: "Home", isSelected: selectedTab == 0) {
                    selectedTab = 0
                }

                TabButton(icon: "doc.text.viewfinder", title: "Check", isSelected: selectedTab == 1) {
                    selectedTab = 1
                }

                TabButton(icon: "briefcase.fill", title: "Jobs", isSelected: selectedTab == 2) {
                    selectedTab = 2
                }
            }
            .padding(6)
            .background(Color.backgroundCard)
            .clipShape(Capsule())
            .shadow(color: Color.black.opacity(0.15), radius: 20, x: 0, y: 10)
            .padding(.horizontal, 40)
            .padding(.bottom, 20)
        }
        .background(Color.backgroundPrimary)
        .ignoresSafeArea(.keyboard)
        .environment(\.authManager, authManager)
    }
}

struct TabButton: View {
    let icon: String
    let title: String
    let isSelected: Bool
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            VStack(spacing: 4) {
                Image(systemName: icon)
                    .font(.system(size: 20, weight: isSelected ? .bold : .medium))
                    .foregroundColor(isSelected ? .white : .textTertiary)
                    .padding(12)
                    .background(
                        Circle()
                            .fill(isSelected ? Color.primaryBrand : Color.clear)
                    )
            }
            .frame(maxWidth: .infinity)
        }
    }
}

// MARK: - Environment Key for AuthManager
private struct AuthManagerKey: EnvironmentKey {
    static let defaultValue: AuthManager = AuthManager.shared
}

extension EnvironmentValues {
    var authManager: AuthManager {
        get { self[AuthManagerKey.self] }
        set { self[AuthManagerKey.self] = newValue }
    }
}

#Preview {
    ContentView()
}
