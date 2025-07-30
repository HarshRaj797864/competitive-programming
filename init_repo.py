#!/usr/bin/env python3
"""
Initialize competitive programming repository structure
Run this first to set up your repository
"""

import os
from pathlib import Path

def create_gitignore():
    """Create .gitignore file"""
    gitignore_content = """# Compiled files
*.exe
*.out
*.o
*.class
*.pyc
__pycache__/

# IDE files
.vscode/
.idea/
*.swp
*.swo

# OS files
.DS_Store
Thumbs.db

# Temporary files
*.tmp
*.temp

# Build directories
build/
dist/

# Logs
*.log
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content)
    print("Created .gitignore")

def create_readme():
    """Create main README.md"""
    readme_content = """# Competitive Programming Solutions

This repository contains my solutions to various competitive programming problems from different platforms.

## Structure

```
competitive-programming/
├── platform/
│   ├── LeetCode/
│   ├── Codeforces/
│   ├── AtCoder/
│   └── HackerRank/
├── scripts/
│   ├── simple_setup.py      # Setup new problems
│   └── init_repo.py         # Initialize repository
├── templates/
│   ├── template.py          # Python template
│   └── template.cpp         # C++ template
└── README.md
```

## Quick Start

1. **Set up a new problem:**
   ```bash
   python3 scripts/simple_setup.py <platform> <problem-name> <problem-id>
   ```
   
   Example:
   ```bash
   python3 scripts/simple_setup.py LeetCode flood-fill 733
   ```

2. **Navigate to problem directory:**
   ```bash
   cd platform/LeetCode/flood-fill/
   ```

3. **Start coding:**
   - Edit `solution.py` for Python implementation
   - Edit `solution.cpp` for C++ implementation
   - Update `README.md` with problem description and approach

## Platforms

- **LeetCode** - Algorithm and data structure problems
- **Codeforces** - Competitive programming contests
- **AtCoder** - Japanese competitive programming platform
- **HackerRank** - Programming challenges and assessments

## Templates

Each problem comes with:
- Pre-configured solution files (Python & C++)
- README template for documentation
- Metadata file for tracking progress

## Usage Tips

- Use descriptive commit messages
- Document your approach in README files
- Include time/space complexity analysis
- Add test cases to verify solutions

Happy coding! 🚀
"""
    
    with open("README.md", "w") as f:
        f.write(readme_content)
    print("Created README.md")

def main():
    print("🚀 Initializing competitive programming repository...")
    
    # Create scripts directory
    Path("scripts").mkdir(exist_ok=True)
    
    # Create .gitignore and README
    create_gitignore()
    create_readme()
    
    print("✅ Repository initialized successfully!")
    print("\nNext steps:")
    print("1. Save the simple_setup.py script to scripts/simple_setup.py")
    print("2. Run: python3 scripts/simple_setup.py LeetCode flood-fill 733")

if __name__ == "__main__":
    main()
