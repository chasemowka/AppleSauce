import SwiftUI
import AuthenticationServices

struct LoginView: View {
    @ObservedObject var authManager: AuthManager
    @State private var showError = false
    @State private var errorMessage = ""

    var body: some View {
        ZStack {
            // Background gradient
            LinearGradient(
                gradient: Gradient(colors: [
                    Color(red: 0.35, green: 0.35, blue: 0.95),
                    Color(red: 0.55, green: 0.35, blue: 0.90)
                ]),
                startPoint: .topLeading,
                endPoint: .bottomTrailing
            )
            .ignoresSafeArea()

            VStack(spacing: 0) {
                Spacer()

                // App Icon/Logo
                VStack(spacing: 16) {
                    Image(systemName: "doc.text.magnifyingglass")
                        .font(.system(size: 80, weight: .light))
                        .foregroundColor(.white)

                    Text("AppleSauce")
                        .font(.system(size: 40, weight: .bold))
                        .foregroundColor(.white)

                    Text("Find your perfect job match")
                        .font(.system(size: 17, weight: .medium))
                        .foregroundColor(.white.opacity(0.8))
                }

                Spacer()

                // Features list
                VStack(alignment: .leading, spacing: 20) {
                    FeatureRow(icon: "doc.badge.plus", text: "Upload & analyze your resume")
                    FeatureRow(icon: "magnifyingglass", text: "Search jobs from top companies")
                    FeatureRow(icon: "chart.bar.fill", text: "Get personalized match scores")
                    FeatureRow(icon: "lightbulb.fill", text: "AI-powered improvement tips")
                }
                .padding(.horizontal, 40)

                Spacer()

                // Sign in with Apple button
                VStack(spacing: 16) {
                    SignInWithAppleButton(.signIn) { request in
                        request.requestedScopes = [.fullName, .email]
                    } onCompletion: { result in
                        handleSignInResult(result)
                    }
                    .signInWithAppleButtonStyle(.white)
                    .frame(height: 54)
                    .cornerRadius(12)

                    // Skip for now option
                    Button(action: {
                        // Continue as guest - just mark as "skipped"
                        UserDefaults.standard.set(true, forKey: "skipped_login")
                        authManager.isAuthenticated = true
                    }) {
                        Text("Continue as Guest")
                            .font(.system(size: 15, weight: .medium))
                            .foregroundColor(.white.opacity(0.7))
                    }
                }
                .padding(.horizontal, 30)
                .padding(.bottom, 50)
            }

            // Loading overlay
            if authManager.isLoading {
                Color.black.opacity(0.4)
                    .ignoresSafeArea()
                ProgressView()
                    .progressViewStyle(CircularProgressViewStyle(tint: .white))
                    .scaleEffect(1.5)
            }
        }
        .alert("Sign In Error", isPresented: $showError) {
            Button("OK", role: .cancel) { }
        } message: {
            Text(errorMessage)
        }
    }

    private func handleSignInResult(_ result: Result<ASAuthorization, Error>) {
        switch result {
        case .success(let authorization):
            if let appleCredential = authorization.credential as? ASAuthorizationAppleIDCredential {
                authManager.handleAppleSignIn(credential: appleCredential)
            }
        case .failure(let error):
            // Don't show error for user cancellation
            if (error as NSError).code != ASAuthorizationError.canceled.rawValue {
                errorMessage = error.localizedDescription
                showError = true
            }
        }
    }
}

struct FeatureRow: View {
    let icon: String
    let text: String

    var body: some View {
        HStack(spacing: 16) {
            Image(systemName: icon)
                .font(.system(size: 22))
                .foregroundColor(.white)
                .frame(width: 30)

            Text(text)
                .font(.system(size: 16, weight: .medium))
                .foregroundColor(.white.opacity(0.9))

            Spacer()
        }
    }
}

#Preview {
    LoginView(authManager: AuthManager.shared)
}
