import SwiftUI

extension Font {
    // Headings
    static let largeTitle = Font.system(size: 34, weight: .bold, design: .default)
    static let title1 = Font.system(size: 28, weight: .bold, design: .default)
    static let title2 = Font.system(size: 22, weight: .bold, design: .default)
    static let title3 = Font.system(size: 20, weight: .semibold, design: .default)
    
    // Body Text
    static let body = Font.system(size: 17, weight: .regular, design: .default)
    static let bodyMedium = Font.system(size: 17, weight: .medium, design: .default)
    static let callout = Font.system(size: 16, weight: .regular, design: .default)
    static let subheadline = Font.system(size: 15, weight: .regular, design: .default)
    
    // Small Text
    static let footnote = Font.system(size: 13, weight: .regular, design: .default)
    static let caption1 = Font.system(size: 12, weight: .regular, design: .default)
    static let caption2 = Font.system(size: 11, weight: .regular, design: .default)
}

struct TextStyle {
    static func heading1(_ text: String) -> some View {
        Text(text)
            .font(.title1)
            .foregroundColor(.textPrimary)
    }
    
    static func heading2(_ text: String) -> some View {
        Text(text)
            .font(.title2)
            .foregroundColor(.textPrimary)
    }
    
    static func heading3(_ text: String) -> some View {
        Text(text)
            .font(.title3)
            .foregroundColor(.textPrimary)
    }
    
    static func bodyText(_ text: String) -> some View {
        Text(text)
            .font(.body)
            .foregroundColor(.textPrimary)
    }
    
    static func bodySecondary(_ text: String) -> some View {
        Text(text)
            .font(.callout)
            .foregroundColor(.textSecondary)
    }
    
    static func caption(_ text: String) -> some View {
        Text(text)
            .font(.caption1)
            .foregroundColor(.textTertiary)
    }
}