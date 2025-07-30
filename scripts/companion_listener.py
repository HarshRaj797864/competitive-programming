#!/usr/bin/env python3
"""
Competitive Companion Listener
Automatically sets up problems when you click the Competitive Companion extension

Usage:
1. Install Competitive Companion browser extension
2. Run: python3 scripts/companion_listener.py
3. Go to any problem page and click the green + icon
4. Files will be automatically created!
"""

import json
import http.server
import socketserver
import threading
import os
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

# Configuration
PORT = 10043  # Default port for Competitive Companion
HOST = 'localhost'

class CompetitiveCompanionHandler(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests from Competitive Companion"""
        try:
            # Read the JSON data
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            problem_data = json.loads(post_data.decode('utf-8'))
            
            # Extract problem information
            name = problem_data.get('name', 'Unknown Problem')
            url = problem_data.get('url', '')
            platform = self.extract_platform(url)
            problem_id = problem_data.get('contestId', '') or self.extract_problem_id(url)
            
            # Generate problem name for directory
            problem_name = self.sanitize_name(name)
            
            print(f"\n🎯 Received problem: {name}")
            print(f"📍 Platform: {platform}")
            print(f"🔗 URL: {url}")
            print(f"🆔 Problem ID: {problem_id}")
            
            # Create problem directory and files
            self.setup_problem(platform, problem_name, problem_id, problem_data)
            
            # Send response
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Problem setup completed successfully!')
            
        except Exception as e:
            print(f"❌ Error processing request: {e}")
            self.send_response(500)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())
    
    def extract_platform(self, url):
        """Extract platform name from URL"""
        if not url:
            return "Unknown"
        
        domain = urlparse(url).netloc.lower()
        
        if 'codeforces' in domain:
            return 'Codeforces'
        elif 'leetcode' in domain:
            return 'LeetCode'
        elif 'atcoder' in domain:
            return 'AtCoder'
        elif 'hackerrank' in domain:
            return 'HackerRank'
        elif 'codechef' in domain:
            return 'CodeChef'
        elif 'spoj' in domain:
            return 'SPOJ'
        else:
            # Try to extract from domain
            platform_name = domain.split('.')[0]
            return platform_name.title()
    
    def extract_problem_id(self, url):
        """Extract problem ID from URL"""
        if not url:
            return "unknown"
        
        # For Codeforces: extract problem letter/number
        if 'codeforces.com' in url:
            parts = url.split('/')
            if 'problem' in parts:
                idx = parts.index('problem')
                if idx + 1 < len(parts):
                    return parts[idx + 1]
        
        # For other platforms, use a generic approach
        parts = url.split('/')
        return parts[-1] if parts[-1] else "unknown"
    
    def sanitize_name(self, name):
        """Convert problem name to directory-safe format"""
        # Remove special characters and convert to lowercase
        sanitized = ''.join(c if c.isalnum() or c in '-_ ' else '' for c in name)
        # Replace spaces with hyphens and convert to lowercase
        sanitized = sanitized.replace(' ', '-').lower()
        # Remove multiple consecutive hyphens
        while '--' in sanitized:
            sanitized = sanitized.replace('--', '-')
        return sanitized.strip('-')
    
    def setup_problem(self, platform, problem_name, problem_id, problem_data):
        """Set up problem files using the simple_setup.py script"""
        try:
            # Run the simple_setup.py script
            result = subprocess.run([
                sys.executable, 'scripts/simple_setup.py',
                platform, problem_name, problem_id
            ], capture_output=True, text=True, cwd=os.getcwd())
            
            if result.returncode == 0:
                print(f"✅ Successfully set up problem: {problem_name}")
                
                # Add additional problem data to metadata
                self.update_metadata(platform, problem_name, problem_data)
                
                # Create test cases file
                self.create_test_cases(platform, problem_name, problem_data)
                
                print(f"📁 Directory: platform/{platform}/{problem_name}/")
                
            else:
                print(f"❌ Error running setup script: {result.stderr}")
        
        except Exception as e:
            print(f"❌ Error setting up problem: {e}")
    
    def update_metadata(self, platform, problem_name, problem_data):
        """Update metadata file with additional information from Competitive Companion"""
        try:
            metadata_path = Path(f"platform/{platform}/{problem_name}/metadata.json")
            if metadata_path.exists():
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                # Add Competitive Companion data
                metadata.update({
                    'time_limit': problem_data.get('timeLimit', 0),
                    'memory_limit': problem_data.get('memoryLimit', 0),
                    'input_format': problem_data.get('input', {}).get('type', ''),
                    'output_format': problem_data.get('output', {}).get('type', ''),
                    'batch_size': problem_data.get('batchSize', 1),
                    'interactive': problem_data.get('interactive', False),
                    'group': problem_data.get('group', ''),
                    'contest_id': problem_data.get('contestId', ''),
                })
                
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                    
        except Exception as e:
            print(f"⚠️  Warning: Could not update metadata: {e}")
    
    def create_test_cases(self, platform, problem_name, problem_data):
        """Create test cases file from Competitive Companion data"""
        try:
            test_cases_path = Path(f"platform/{platform}/{problem_name}/test_cases.json")
            
            tests = problem_data.get('tests', [])
            if tests:
                test_data = {
                    'test_cases': []
                }
                
                for i, test in enumerate(tests):
                    test_data['test_cases'].append({
                        'id': i + 1,
                        'input': test.get('input', '').strip(),
                        'expected_output': test.get('output', '').strip()
                    })
                
                with open(test_cases_path, 'w') as f:
                    json.dump(test_data, f, indent=2)
                
                print(f"📝 Created {len(tests)} test cases")
            
        except Exception as e:
            print(f"⚠️  Warning: Could not create test cases: {e}")
    
    def log_message(self, format, *args):
        """Override to reduce logging"""
        pass  # Silent

def main():
    print("🚀 Starting Competitive Companion Listener...")
    print(f"🌐 Listening on http://{HOST}:{PORT}")
    print("📱 Install Competitive Companion browser extension")
    print("🎯 Go to any problem page and click the green + icon")
    print("⏹️  Press Ctrl+C to stop\n")
    
    # Check if setup script exists
    if not Path("scripts/simple_setup.py").exists():
        print("❌ Error: scripts/simple_setup.py not found!")
        print("Please make sure you have set up the simple_setup.py script first.")
        sys.exit(1)
    
    try:
        with socketserver.TCPServer((HOST, PORT), CompetitiveCompanionHandler) as httpd:
            print(f"✅ Server started successfully!")
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main()
