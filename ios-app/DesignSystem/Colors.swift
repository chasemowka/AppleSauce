import SwiftUI

extension Color {
    // Primary Colors
    static let primaryBlue = Color(red: 0.0, green: 0.48, blue: 1.0) // Keep standard blue for system consistency
    static let primaryBrand = Color(red: 0.35, green: 0.35, blue: 0.95) // Vibrant Blurple used in Opera/Arc styles
    static let primaryDark = Color(red: 0.05, green: 0.05, blue: 0.06) // Deep almost-black
    
    // Background Colors
    static let backgroundPrimary = Color(red: 0.96, green: 0.96, blue: 0.97) // Soft gray base (#F5F5F7)
    static let backgroundSecondary = Color.white
    static let backgroundCard = Color.white
    static let backgroundOverlay = Color.black.opacity(0.4)
    
    // Text Colors
    static let textPrimary = Color(red: 0.08, green: 0.08, blue: 0.10) // High contrast
    static let textSecondary = Color(red: 0.45, green: 0.45, blue: 0.50) // Softer secondary
    static let textTertiary = Color(red: 0.70, green: 0.70, blue: 0.75)
    
    // Accent Colors
    static let success = Color(red: 0.15, green: 0.80, blue: 0.45) // Vibrant mint green
    static let warning = Color(red: 1.0, green: 0.65, blue: 0.10)
    static let error = Color(red: 1.0, green: 0.25, blue: 0.25)
    
    // Border Colors
    static let borderLight = Color.white.opacity(0.8)
    static let borderMedium = Color(red: 0.90, green: 0.90, blue: 0.92)
    
    // Gradients
    static let brandGradient = LinearGradient(
        gradient: Gradient(colors: [
            Color(red: 0.35, green: 0.35, blue: 0.95),
            Color(red: 0.60, green: 0.35, blue: 0.90)
        ]),
        startPoint: .topLeading,
        endPoint: .bottomTrailing
    )
}