import os
import sys
import json
from pathlib import Path

def create_directory_structure():
    """Create the basic directory structure if it doesn't exist"""
    directories = [
        "platform",
        "platform/LeetCode",
        "platform/Codeforces", 
        "platform/AtCoder",
        "platform/HackerRank",
        "scripts",
        "templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created/verified directory: {directory}")

def create_templates():
    """Create template files"""
    
    # Python template
    python_template = '''"""
Problem: {problem_name}
Platform: {platform}
Problem ID: {problem_id}
URL: {url}

Time Complexity: O()
Space Complexity: O()
"""

class Solution:
    def solve(self):
        # Implementation here
        pass

def main():
    solution = Solution()
    # Test cases
    pass

if __name__ == "__main__":
    main()
'''
    
    # C++ template
    cpp_template = '''/*
Problem: {problem_name}
Platform: {platform}
Problem ID: {problem_id}
URL: {url}

Time Complexity: O()
Space Complexity: O()
*/

#include <iostream>
#include <vector>
#include <string>
#include <unordered_map>
#include <unordered_set>
#include <queue>
#include <stack>
#include <algorithm>

using namespace std;

class Solution {{
public:
    // Implementation here
}};

int main() {{
    Solution solution;
    // Test cases
    return 0;
}}
'''
    
    # Write templates
    with open("templates/template.py", "w") as f:
        f.write(python_template)
    
    with open("templates/template.cpp", "w") as f:
        f.write(cpp_template)
    
    print("Created template files")

def get_problem_url(platform, problem_id, problem_name):
    """Generate problem URL based on platform"""
    urls = {
        "LeetCode": f"https://leetcode.com/problems/{problem_name}/",
        "Codeforces": f"https://codeforces.com/problem/{problem_id}",
        "AtCoder": f"https://atcoder.jp/contests/{problem_name}/tasks/{problem_id}",
        "HackerRank": f"https://www.hackerrank.com/challenges/{problem_name}/problem"
    }
    return urls.get(platform, f"https://{platform.lower()}.com/")

def setup_problem(platform, problem_name, problem_id):
    """Set up a new problem directory and files"""
    
    # Create problem directory
    problem_dir = Path(f"platform/{platform}/{problem_name}")
    problem_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate URL
    url = get_problem_url(platform, problem_id, problem_name)
    
    # Create problem files from templates
    template_vars = {
        'problem_name': problem_name.replace('-', ' ').title(),
        'platform': platform,
        'problem_id': problem_id,
        'url': url
    }
    
    # Create Python solution file
    with open("templates/template.py", "r") as f:
        python_content = f.read().format(**template_vars)
    
    with open(problem_dir / "solution.py", "w") as f:
        f.write(python_content)
    
    # Create C++ solution file
    with open("templates/template.cpp", "r") as f:
        cpp_content = f.read().format(**template_vars)
    
    with open(problem_dir / "solution.cpp", "w") as f:
        f.write(cpp_content)
    
    # Create README
    readme_content = f"""# {template_vars['problem_name']}

**Platform:** {platform}  
**Problem ID:** {problem_id}  
**URL:** {url}

## Problem Description
<!-- Add problem description here -->

## Approach
<!-- Describe your approach here -->

## Complexity Analysis
- **Time Complexity:** O()
- **Space Complexity:** O()

## Files
- `solution.py` - Python implementation
- `solution.cpp` - C++ implementation
"""
    
    with open(problem_dir / "README.md", "w") as f:
        f.write(readme_content)
    
    # Create/update problem metadata
    metadata = {
        'name': template_vars['problem_name'],
        'platform': platform,
        'id': problem_id,
        'url': url,
        'difficulty': '',  # To be filled later
        'tags': [],        # To be filled later
        'status': 'not_started',
        'created': str(Path(problem_dir).stat().st_ctime)
    }
    
    with open(problem_dir / "metadata.json", "w") as f:
        json.dump(metadata, f, indent=2)
    
    print(f"✅ Successfully set up problem: {template_vars['problem_name']}")
    print(f"📁 Directory: {problem_dir}")
    print(f"🔗 URL: {url}")
    print(f"📝 Files created: solution.py, solution.cpp, README.md, metadata.json")

def main():
    if len(sys.argv) != 4:
        print("Usage: python3 scripts/simple_setup.py <platform> <problem-name> <problem-id>")
        print("Example: python3 scripts/simple_setup.py LeetCode flood-fill 733")
        sys.exit(1)
    
    platform = sys.argv[1]
    problem_name = sys.argv[2]
    problem_id = sys.argv[3]
    
    print("🚀 Setting up competitive programming environment...")
    
    # Create directory structure and templates
    create_directory_structure()
    create_templates()
    
    # Set up the specific problem
    setup_problem(platform, problem_name, problem_id)
    
    print("\n✨ Setup complete! You can now start working on your problem.")
    print(f"💡 Navigate to: platform/{platform}/{problem_name}/")

if __name__ == "__main__":
    main()
