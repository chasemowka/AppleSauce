import SwiftUI
import UniformTypeIdentifiers

struct ResumeUploadView: View {
    @State private var showingDocumentPicker = false
    @State private var uploadedResumes: [Resume] = []
    
    var body: some View {
        NavigationView {
            VStack {
                Button("Upload Resume") {
                    showingDocumentPicker = true
                }
                .padding()
                .background(Color.blue)
                .foregroundColor(.white)
                .cornerRadius(8)
                
                List(uploadedResumes) { resume in
                    VStack(alignment: .leading) {
                        Text(resume.fileName)
                            .font(.headline)
                        Text("Uploaded: \(resume.uploadDate, style: .date)")
                            .font(.caption)
                            .foregroundColor(.gray)
                    }
                }
            }
            .navigationTitle("Resume Upload")
            .sheet(isPresented: $showingDocumentPicker) {
                DocumentPicker { url in
                    let resume = Resume(
                        fileName: url.lastPathComponent,
                        uploadDate: Date(),
                        text: nil
                    )
                    uploadedResumes.append(resume)
                }
            }
        }
    }
}

struct DocumentPicker: UIViewControllerRepresentable {
    let onDocumentPicked: (URL) -> Void
    
    func makeUIViewController(context: Context) -> UIDocumentPickerViewController {
        let picker = UIDocumentPickerViewController(forOpeningContentTypes: [UTType.pdf, UTType.text])
        picker.delegate = context.coordinator
        return picker
    }
    
    func updateUIViewController(_ uiViewController: UIDocumentPickerViewController, context: Context) {}
    
    func makeCoordinator() -> Coordinator {
        Coordinator(self)
    }
    
    class Coordinator: NSObject, UIDocumentPickerDelegate {
        let parent: DocumentPicker
        
        init(_ parent: DocumentPicker) {
            self.parent = parent
        }
        
        func documentPicker(_ controller: UIDocumentPickerViewController, didPickDocumentsAt urls: [URL]) {
            if let url = urls.first {
                parent.onDocumentPicked(url)
            }
        }
    }
}