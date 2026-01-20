from http.server import HTTPServer, SimpleHTTPRequestHandler
import os

os.chdir('/home/mowkacm/personal-app/web-preview')

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

print("🚀 AppleSauce Preview Server")
print("📱 Open in browser: http://localhost:8080")
print("Press Ctrl+C to stop\n")

httpd = HTTPServer(('localhost', 8080), CORSRequestHandler)
httpd.serve_forever()
