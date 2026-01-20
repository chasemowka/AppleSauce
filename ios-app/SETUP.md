# iOS App Local Setup Guide

## Prerequisites
- Xcode 13+ installed
- Backend server running on `localhost:8000`

## Step 1: Start the Backend Server

```bash
cd ~/personal-app/backend
source venv/bin/activate
python main.py
```

The server should start on `http://localhost:8000`

## Step 2: Open iOS Project in Xcode

1. Open Xcode
2. File → Open → Navigate to `~/personal-app/ios-app/AppleSauce/AppleSauce/`
3. Create a new Xcode project:
   - Choose "App" template
   - Product Name: `AppleSauce`
   - Interface: SwiftUI
   - Language: Swift
   - Save in `~/personal-app/ios-app/AppleSauce/`

4. Add all the Swift files to your project:
   - AppleSauceApp.swift
   - ContentView.swift
   - Models.swift
   - APIService.swift
   - ResumeUploadView.swift
   - JobListingsView.swift
   - JobDetailView.swift

## Step 3: Configure Network Permissions

Add this to your `Info.plist`:

```xml
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsLocalNetworking</key>
    <true/>
    <key>NSAllowsArbitraryLoads</key>
    <true/>
</dict>
```

This allows the app to connect to localhost.

## Step 4: Run the App

1. Select iPhone simulator (iPhone 14 or newer recommended)
2. Click the Play button or press `Cmd + R`
3. The app will launch in the simulator

## Testing the Connection

1. Go to the "Job Listings" tab
2. You should see jobs loaded from the backend:
   - Software Engineer at TechCorp
   - Data Scientist at DataInc
   - Frontend Developer at WebStudio

3. Click on a job to see details and suggestions

## Troubleshooting

### "Cannot connect to localhost"
- Make sure backend is running: `curl http://localhost:8000/jobs`
- Check that Info.plist has network permissions

### "No jobs appearing"
- Check Xcode console for error messages
- Verify backend is responding: `curl http://localhost:8000/jobs`

### Testing on Physical Device
If testing on a real iPhone:
1. Find your Mac's local IP: `ifconfig | grep "inet "`
2. Update `APIService.swift` line 5:
   ```swift
   static let baseURL = "http://YOUR_MAC_IP:8000"
   ```
3. Make sure iPhone and Mac are on same WiFi network

## Next Steps

- Upload a real resume to test parsing
- Implement resume storage
- Add authentication
- Connect to real job APIs
