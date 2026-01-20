import SwiftUI

struct UploadButton: View {
    let title: String
    let isUploading: Bool
    let onTap: () -> Void
    
    var body: some View {
        Button(action: onTap) {
            HStack(spacing: 8) {
                if isUploading {
                    ProgressView()
                        .scaleEffect(0.8)
                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                } else {
                    Image(systemName: "arrow.up.doc")
                        .font(.system(size: 16, weight: .medium))
                }
                
                Text(isUploading ? "Uploading..." : title)
                    .font(.callout)
                    .fontWeight(.medium)
            }
            .foregroundColor(.white)
            .padding(.horizontal, 20)
            .padding(.vertical, 12)
            .background(
                RoundedRectangle(cornerRadius: 10)
                    .fill(isUploading ? Color.textSecondary : Color.primaryBlue)
            )
        }
        .disabled(isUploading)
        .animation(.easeInOut(duration: 0.2), value: isUploading)
    }
}

struct UploadDropZone: View {
    let onFileDrop: () -> Void
    
    var body: some View {
        VStack(spacing: 16) {
            Image(systemName: "doc.badge.plus")
                .font(.system(size: 48))
                .foregroundColor(.textTertiary)
            
            VStack(spacing: 4) {
                Text("Drop your resume here")
                    .font(.callout)
                    .fontWeight(.medium)
                    .foregroundColor(.textPrimary)
                
                Text("or tap to browse files")
                    .font(.footnote)
                    .foregroundColor(.textSecondary)
            }
            
            UploadButton(title: "Choose File", isUploading: false, onTap: onFileDrop)
        }
        .padding(32)
        .frame(maxWidth: .infinity)
        .background(Color.backgroundSecondary)
        .cornerRadius(16)
        .overlay(
            RoundedRectangle(cornerRadius: 16)
                .stroke(Color.borderMedium, style: StrokeStyle(lineWidth: 2, dash: [8]))
        )
    }
}

#Preview {
    VStack(spacing: 20) {
        UploadButton(title: "Upload Resume", isUploading: false, onTap: {})
        UploadButton(title: "Upload Resume", isUploading: true, onTap: {})
        UploadDropZone(onFileDrop: {})
    }
    .padding()
}