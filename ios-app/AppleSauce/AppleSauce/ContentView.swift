import SwiftUI

struct ContentView: View {
    var body: some View {
        TabView {
            ResumeUploadView()
                .tabItem {
                    Image(systemName: "doc.badge.plus")
                    Text("Resume")
                }
            
            JobListingsView()
                .tabItem {
                    Image(systemName: "list.bullet")
                    Text("Jobs")
                }
        }
    }
}