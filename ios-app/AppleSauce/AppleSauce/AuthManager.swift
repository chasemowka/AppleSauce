import Foundation
import AuthenticationServices

/// Manages authentication state and token storage
class AuthManager: ObservableObject {
    static let shared = AuthManager()

    @Published var isAuthenticated = false
    @Published var currentUser: AuthUser?
    @Published var isLoading = false

    private let tokenKey = "auth_token"
    private let userIdKey = "apple_user_id"
    private let userKey = "current_user"

    private init() {
        // Check for existing session on init
        checkExistingSession()
    }

    // MARK: - Public Methods

    /// Check if user has existing valid session
    func checkExistingSession() {
        if let token = getToken(), let userData = UserDefaults.standard.data(forKey: userKey) {
            do {
                let user = try JSONDecoder().decode(AuthUser.self, from: userData)
                self.currentUser = user
                self.isAuthenticated = true

                // Verify Apple ID credential state
                if let appleUserId = UserDefaults.standard.string(forKey: userIdKey) {
                    checkAppleCredentialState(userId: appleUserId)
                }
            } catch {
                print("Failed to decode stored user: \(error)")
                logout()
            }
        }
    }

    /// Handle successful Apple Sign In
    func handleAppleSignIn(credential: ASAuthorizationAppleIDCredential) {
        isLoading = true

        let userId = credential.user
        let email = credential.email
        let fullName = [credential.fullName?.givenName, credential.fullName?.familyName]
            .compactMap { $0 }
            .joined(separator: " ")
        let identityToken = credential.identityToken.flatMap { String(data: $0, encoding: .utf8) }

        // Store Apple User ID for credential state checks
        UserDefaults.standard.set(userId, forKey: userIdKey)

        // Send to backend
        authenticateWithBackend(
            userId: userId,
            email: email,
            fullName: fullName.isEmpty ? nil : fullName,
            identityToken: identityToken
        )
    }

    /// Logout and clear all stored data
    func logout() {
        UserDefaults.standard.removeObject(forKey: tokenKey)
        UserDefaults.standard.removeObject(forKey: userIdKey)
        UserDefaults.standard.removeObject(forKey: userKey)

        DispatchQueue.main.async {
            self.isAuthenticated = false
            self.currentUser = nil
        }
    }

    /// Get stored auth token
    func getToken() -> String? {
        return UserDefaults.standard.string(forKey: tokenKey)
    }

    // MARK: - Private Methods

    private func authenticateWithBackend(userId: String, email: String?, fullName: String?, identityToken: String?) {
        guard let url = URL(string: "\(APIService.baseURL)/auth/apple") else {
            isLoading = false
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        var body: [String: Any] = ["user_id": userId]
        if let email = email { body["email"] = email }
        if let fullName = fullName { body["full_name"] = fullName }
        if let token = identityToken { body["identity_token"] = token }

        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { [weak self] data, response, error in
            DispatchQueue.main.async {
                self?.isLoading = false
            }

            if let error = error {
                print("Auth error: \(error.localizedDescription)")
                return
            }

            guard let data = data else { return }

            do {
                let authResponse = try JSONDecoder().decode(AuthResponse.self, from: data)

                // Store token
                UserDefaults.standard.set(authResponse.accessToken, forKey: self?.tokenKey ?? "")

                // Store user data
                if let userData = try? JSONEncoder().encode(authResponse.user) {
                    UserDefaults.standard.set(userData, forKey: self?.userKey ?? "")
                }

                DispatchQueue.main.async {
                    self?.currentUser = authResponse.user
                    self?.isAuthenticated = true
                }
            } catch {
                print("Failed to decode auth response: \(error)")
            }
        }.resume()
    }

    private func checkAppleCredentialState(userId: String) {
        let provider = ASAuthorizationAppleIDProvider()
        provider.getCredentialState(forUserID: userId) { [weak self] state, error in
            DispatchQueue.main.async {
                switch state {
                case .authorized:
                    // Credential is valid
                    break
                case .revoked, .notFound:
                    // User revoked access or not found - logout
                    self?.logout()
                case .transferred:
                    // Account transferred to different team
                    break
                @unknown default:
                    break
                }
            }
        }
    }
}

// MARK: - Models

struct AuthResponse: Codable {
    let accessToken: String
    let tokenType: String
    let user: AuthUser

    enum CodingKeys: String, CodingKey {
        case accessToken = "access_token"
        case tokenType = "token_type"
        case user
    }
}

struct AuthUser: Codable, Identifiable {
    let id: Int
    let email: String
    let name: String?
    let pictureUrl: String?

    enum CodingKeys: String, CodingKey {
        case id, email, name
        case pictureUrl = "picture_url"
    }
}
