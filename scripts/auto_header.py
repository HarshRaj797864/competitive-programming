#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from datetime import datetime

class AutoHeader:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.templates_dir = self.root_dir / ".templates"
        
    def add_header_to_file(self, file_path, author="Competitive Programmer", contest_info=None):
        """Add header comment to a source file"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False
        
        # Determine file type and header style
        ext = file_path.suffix.lower()
        if ext in ['.cpp', '.cc', '.cxx', '.c', '.java']:
            comment_start, comment_end = "/*", "*/"
            line_comment = "//"
        elif ext in ['.py']:
            comment_start, comment_end = '"""', '"""'
            line_comment = "#"
        else:
            print(f"⚠️  Unsupported file type: {ext}")
            return False
        
        # Create header
        header_lines = [
            f"{comment_start}",
            f" * Author: {author}",
            f" * Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f" * File: {file_path.name}",
        ]
        
        if contest_info:
            header_lines.extend([
                f" * Platform: {contest_info.get('platform', 'Unknown')}",
                f" * Contest: {contest_info.get('contest', 'Unknown')}",
                f" * Problem: {contest_info.get('problem', 'Unknown')}",
            ])
        
        header_lines.extend([
            f" * Description: [Add problem description]",
            f" {comment_end}",
            ""
        ])
        
        # Read existing file content
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        except Exception as e:
            print(f"❌ Error reading file: {e}")
            return False
        
        # Check if header already exists
        if comment_start in existing_content and "Author:" in existing_content:
            print(f"⚠️  Header already exists in {file_path.name}")
            return True
        
        # Write new content with header
        new_content = '\n'.join(header_lines) + existing_content
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✅ Added header to {file_path.name}")
            return True
        except Exception as e:
            print(f"❌ Error writing file: {e}")
            return False
    
    def add_headers_to_directory(self, directory_path, author="Competitive Programmer"):
        """Add headers to all source files in a directory"""
        directory = Path(directory_path)
        
        if not directory.exists():
            print(f"❌ Directory not found: {directory}")
            return
        
        # Try to extract contest info from directory structure
        contest_info = self.extract_contest_info(directory)
        
        # Find source files
        source_extensions = ['.cpp', '.cc', '.cxx', '.c', '.py', '.java']
        source_files = []
        
        for ext in source_extensions:
            source_files.extend(directory.glob(f"*{ext}"))
        
        if not source_files:
            print(f"⚠️  No source files found in {directory}")
            return
        
        print(f"Found {len(source_files)} source file(s)")
        
        for file_path in source_files:
            self.add_header_to_file(file_path, author, contest_info)
    
    def extract_contest_info(self, directory):
        """Extract contest information from directory structure"""
        parts = directory.parts
        
        # Try to find pattern: platforms/Platform/Contest/Problem
        try:
            if 'platforms' in parts:
                platform_idx = parts.index('platforms')
                if len(parts) > platform_idx + 3:
                    return {
                        'platform': parts[platform_idx + 1],
                        'contest': parts[platform_idx + 2], 
                        'problem': parts[platform_idx + 3]
                    }
        except (ValueError, IndexError):
            pass
        
        # Try to read from problem_info.json
        info_file = directory / "problem_info.json"
        if info_file.exists():
            try:
                import json
                with open(info_file) as f:
                    return json.load(f)
            except:
                pass
        
        return None

def main():
    parser = argparse.ArgumentParser(description='Add headers to competitive programming files')
    parser.add_argument('path', help='File or directory path')
    parser.add_argument('--author', default='Competitive Programmer', help='Author name')
    
    args = parser.parse_args()
    
    auto_header = AutoHeader()
    path = Path(args.path)
    
    if path.is_file():
        auto_header.add_header_to_file(path, args.author)
    elif path.is_directory():
        auto_header.add_headers_to_directory(path, args.author)
    else:
        print(f"❌ Path not found: {path}")

if __name__ == "__main__":
    main()
