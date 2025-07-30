#!/usr/bin/env python3

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path

class ProblemSetup:
    def __init__(self):
        # Get the root directory (parent of scripts)
        self.root_dir = Path(__file__).parent.parent
        self.platforms_dir = self.root_dir / "platforms"
        self.templates_dir = self.root_dir / ".templates"  # Your dot-prefixed templates
        self.cph_dir = self.root_dir / ".cph"
        
        print(f"🏠 Root directory: {self.root_dir}")
        print(f"📁 Platforms directory: {self.platforms_dir}")
        print(f"📄 Templates directory: {self.templates_dir}")
    
    def get_platform_name(self, platform_input):
        """Convert platform shortcuts to full names matching your structure"""
        platform_map = {
            'cf': 'Codeforces',
            'codeforces': 'Codeforces',
            'ac': 'AtCoder', 
            'atcoder': 'AtCoder',
            'lc': 'LeetCode',
            'leetcode': 'LeetCode',
            'cc': 'CodeChef',
            'codechef': 'CodeChef',
            'tc': 'TopCoder',
            'topcoder': 'TopCoder'
        }
        return platform_map.get(platform_input.lower(), platform_input.title())
    
    def setup_problem(self, platform, contest, problem_code, problem_name=None, url=None):
        """Setup a new problem in your existing structure"""
        
        platform_name = self.get_platform_name(platform)
        
        # Create problem directory in platforms folder
        problem_dir = self.platforms_dir / platform_name / contest / problem_code
        problem_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"📂 Creating problem directory: {problem_dir}")
        
        # Create metadata for problem tracking
        metadata = {
            "platform": platform_name,
            "contest": contest,
            "problem_code": problem_code,
            "problem_name": problem_name or f"{problem_code}",
            "url": url,
            "created_at": datetime.now().isoformat(),
            "solved": False,
            "attempts": 0,
            "best_time": None,
            "notes": "",
            "tags": [],
            "difficulty": None
        }
        
        # Save metadata
        metadata_file = problem_dir / "problem_info.json"
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Created metadata: {metadata_file}")
        
        # Copy templates if they exist
        self.copy_templates(problem_dir)
        
        # Create test files
        self.create_test_files(problem_dir)
        
        # Create .cph problem file for CPH integration
        self.create_cph_file(platform_name, contest, problem_code, problem_name, url)
        
        # Create README
        self.create_readme(problem_dir, problem_name or problem_code)
        
        print(f"🎉 Problem setup complete!")
        print(f"📍 Location: {problem_dir}")
        
        return problem_dir
    
    def copy_templates(self, problem_dir):
        """Copy template files from .templates directory"""
        if not self.templates_dir.exists():
            print(f"⚠️  Templates directory not found: {self.templates_dir}")
            return
        
        template_files = {
            'cpp': ['template.cpp', 'main.cpp', 'solution.cpp'],
            'py': ['template.py', 'main.py', 'solution.py'],
            'java': ['Template.java', 'Main.java', 'Solution.java']
        }
        
        for lang, possible_names in template_files.items():
            template_found = False
            for template_name in possible_names:
                template_path = self.templates_dir / template_name
                if template_path.exists():
                    # Determine output filename
                    if lang == 'cpp':
                        output_name = f"solution.cpp"
                    elif lang == 'py':
                        output_name = f"solution.py"
                    elif lang == 'java':
                        output_name = f"Solution.java"
                    
                    output_path = problem_dir / output_name
                    
                    # Copy template content
                    with open(template_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    with open(output_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    print(f"📄 Copied template: {template_name} -> {output_name}")
                    template_found = True
                    break
            
            if not template_found:
                print(f"⚠️  No {lang} template found in {self.templates_dir}")
    
    def create_test_files(self, problem_dir):
        """Create input/output test files"""
        test_files = [
            "input.txt",
            "output.txt", 
            "expected.txt",
            "sample_input.txt",
            "sample_output.txt"
        ]
        
        for filename in test_files:
            filepath = problem_dir / filename
            if not filepath.exists():
                filepath.touch()
        
        print(f"📝 Created test files")
    
    def create_cph_file(self, platform, contest, problem_code, problem_name, url):
        """Create .cph file for Competitive Programming Helper integration"""
        if not self.cph_dir.exists():
            self.cph_dir.mkdir()
        
        cph_filename = f"{platform}_{contest}_{problem_code}.prob"
        cph_file = self.cph_dir / cph_filename
        
        cph_data = {
            "name": problem_name or problem_code,
            "group": f"{platform} - {contest}",
            "url": url or "",
            "interactive": False,
            "memoryLimit": 256,
            "timeLimit": 2000,
            "tests": [
                {
                    "input": "",
                    "output": ""
                }
            ],
            "testType": "single",
            "input": {
                "type": "stdin"
            },
            "output": {
                "type": "stdout"
            },
            "languages": {
                "java": {
                    "mainClass": "Main",
                    "taskClass": "Task"
                }
            },
            "batch": {
                "id": f"{platform.lower()}-{contest}-{problem_code.lower()}",
                "size": 1
            },
            "srcPath": str(self.platforms_dir / platform / contest / problem_code / "solution.cpp")
        }
        
        with open(cph_file, 'w') as f:
            json.dump(cph_data, f, indent=2)
        
        print(f"🔗 Created CPH file: {cph_filename}")
    
    def create_readme(self, problem_dir, problem_name):
        """Create README with problem information"""
        readme_content = f"""# {problem_name}

## Problem Statement
[Add problem statement here]

## Input Format
[Describe input format]

## Output Format  
[Describe output format]

## Constraints
[Add constraints]

## Sample Input
```
[Add sample input to sample_input.txt]
```

## Sample Output
```
[Add sample output to sample_output.txt]
```

## Solution Approach
[Describe your approach]

## Notes
- Time Complexity: 
- Space Complexity: 
- Tags: 

## Files
- `solution.cpp` - Main C++ solution
- `solution.py` - Python solution  
- `Solution.java` - Java solution
- `input.txt` - Test input
- `expected.txt` - Expected output
"""
        
        readme_file = problem_dir / "README.md"
        with open(readme_file, 'w') as f:
            f.write(readme_content)
        
        print(f"📖 Created README: README.md")

def main():
    parser = argparse.ArgumentParser(description='Setup a competitive programming problem')
    parser.add_argument('platform', help='Platform (cf, ac, lc, cc, etc.)')
    parser.add_argument('contest', help='Contest name/ID')
    parser.add_argument('problem', help='Problem code (A, B, C, etc.)')
    parser.add_argument('--name', help='Problem name')
    parser.add_argument('--url', help='Problem URL')
    
    args = parser.parse_args()
    
    setup = ProblemSetup()
    setup.setup_problem(args.platform, args.contest, args.problem, args.name, args.url)

if __name__ == "__main__":
    main()
