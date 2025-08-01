#!/usr/bin/env python3
"""
Stats Generator for Competitive Programming Solutions
Scans the platform directory and updates solutions.json with current statistics
"""

import json
import os
from pathlib import Path
from datetime import datetime
import re

def scan_problem_directory(platform_path):
    """Scan a platform directory for problems and extract metadata"""
    problems = []
    platform_name = platform_path.name
    
    print(f"   Scanning path: {platform_path}")
    
    try:
        problem_dirs = [d for d in platform_path.iterdir() if d.is_dir()]
        print(f"   Found {len(problem_dirs)} directories")
    except Exception as e:
        print(f"   ⚠️  Error reading directory {platform_path}: {e}")
        return problems
    
    for problem_dir in problem_dirs:
            
        # Calculate relative directory path safely
        try:
            relative_path = problem_dir.relative_to(Path.cwd())
            directory_path = str(relative_path)
        except ValueError:
            # Fallback if relative_to fails
            directory_path = f"platform/{platform_name}/{problem_dir.name}"
        
        problem_info = {
            'name': problem_dir.name,
            'platform': platform_name,
            'directory': directory_path,
            'files': [],
            'languages': [],
            'difficulty': 'Unknown',
            'status': 'Unknown',
            'url': '',
            'problem_id': '',
            'tags': [],
            'date_created': '',
            'last_modified': ''
        }
        
        # Read metadata.json if it exists
        metadata_file = problem_dir / 'metadata.json'
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    metadata = json.load(f)
                    problem_info.update({
                        'difficulty': metadata.get('difficulty', 'Unknown'),
                        'status': metadata.get('status', 'Unknown'),
                        'url': metadata.get('url', ''),
                        'problem_id': metadata.get('id', ''),
                        'tags': metadata.get('tags', []),
                        'date_created': metadata.get('created', '')
                    })
            except Exception as e:
                print(f"⚠️  Warning: Could not read metadata for {problem_dir.name}: {e}")
        
        # Scan for solution files
        solution_files = []
        languages = set()
        
        for file_path in problem_dir.iterdir():
            if file_path.is_file():
                file_info = {
                    'name': file_path.name,
                    'size': file_path.stat().st_size,
                    'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                }
                
                # Determine language and if it's a solution file
                if file_path.suffix == '.py':
                    languages.add('Python')
                    if 'solution' in file_path.stem.lower():
                        file_info['type'] = 'solution'
                elif file_path.suffix == '.cpp':
                    languages.add('C++')
                    if 'solution' in file_path.stem.lower():
                        file_info['type'] = 'solution'
                elif file_path.suffix == '.java':
                    languages.add('Java')
                    if 'solution' in file_path.stem.lower():
                        file_info['type'] = 'solution'
                elif file_path.suffix == '.js':
                    languages.add('JavaScript')
                    if 'solution' in file_path.stem.lower():
                        file_info['type'] = 'solution'
                elif file_path.name == 'README.md':
                    file_info['type'] = 'documentation'
                elif file_path.name == 'metadata.json':
                    file_info['type'] = 'metadata'
                elif file_path.name == 'test_cases.json':
                    file_info['type'] = 'test_cases'
                else:
                    file_info['type'] = 'other'
                
                solution_files.append(file_info)
                
                # Update last modified time for the problem
                if not problem_info['last_modified'] or file_info['last_modified'] > problem_info['last_modified']:
                    problem_info['last_modified'] = file_info['last_modified']
        
        problem_info['files'] = solution_files
        problem_info['languages'] = list(languages)
        
        # Try to determine status based on file content
        if not metadata_file.exists() or problem_info['status'] == 'Unknown':
            problem_info['status'] = determine_status(problem_dir)
        
        problems.append(problem_info)
    
    return problems

def determine_status(problem_dir):
    """Determine problem status based on file content analysis"""
    solution_files = [f for f in problem_dir.glob('solution.*') if f.suffix in ['.py', '.cpp', '.java', '.js']]
    
    if not solution_files:
        return 'not_started'
    
    # Check if solutions have meaningful content
    for solution_file in solution_files:
        try:
            with open(solution_file, 'r') as f:
                content = f.read()
                
            # Remove comments and whitespace
            lines = [line.strip() for line in content.split('\n') 
                    if line.strip() and not line.strip().startswith(('#', '//', '/*', '*', '"""'))]
            
            # Count non-template lines
            meaningful_lines = [line for line in lines 
                              if not any(template_word in line.lower() 
                                       for template_word in ['implementation here', 'todo', 'pass', '# test cases'])]
            
            if len(meaningful_lines) > 10:  # Arbitrary threshold
                return 'completed'
            elif len(meaningful_lines) > 5:
                return 'in_progress'
                
        except Exception:
            continue
    
    return 'started'

def calculate_statistics(problems):
    """Calculate overall statistics from problems list"""
    stats = {
        'total_problems': len(problems),
        'platforms': {},
        'difficulty_distribution': {
            'Easy': 0,
            'Medium': 0,
            'Hard': 0,
            'Unknown': 0
        },
        'language_distribution': {
            'Python': 0,
            'C++': 0,
            'Java': 0,
            'JavaScript': 0
        },
        'status_distribution': {
            'completed': 0,
            'in_progress': 0,
            'started': 0,
            'not_started': 0
        },
        'recent_activity': []
    }
    
    # Count by platform
    for problem in problems:
        platform = problem['platform']
        stats['platforms'][platform] = stats['platforms'].get(platform, 0) + 1
        
        # Count by difficulty
        difficulty = problem.get('difficulty', 'Unknown')
        if difficulty in stats['difficulty_distribution']:
            stats['difficulty_distribution'][difficulty] += 1
        else:
            stats['difficulty_distribution']['Unknown'] += 1
        
        # Count by status
        status = problem.get('status', 'not_started')
        if status in stats['status_distribution']:
            stats['status_distribution'][status] += 1
        
        # Count languages
        for language in problem.get('languages', []):
            if language in stats['language_distribution']:
                stats['language_distribution'][language] += 1
    
    # Get recent activity (last 10 modified problems)
    recent_problems = sorted(problems, 
                           key=lambda p: p.get('last_modified', ''), 
                           reverse=True)[:10]
    
    stats['recent_activity'] = [{
        'name': p['name'],
        'platform': p['platform'],
        'last_modified': p.get('last_modified', ''),
        'status': p.get('status', 'Unknown')
    } for p in recent_problems]
    
    return stats

def update_solutions_json(problems, stats):
    """Update solutions.json with current problems and statistics"""
    solutions_data = {
        'metadata': {
            'last_updated': datetime.now().isoformat(),
            'total_problems': stats['total_problems'],
            'platforms': stats['platforms'],
            'difficulty_distribution': stats['difficulty_distribution'],
            'language_distribution': stats['language_distribution'],
            'status_distribution': stats['status_distribution']
        },
        'statistics': stats,
        'problems': problems
    }
    
    # Write to solutions.json
    with open('solutions.json', 'w') as f:
        json.dump(solutions_data, f, indent=2)
    
    print(f"✅ Updated solutions.json with {len(problems)} problems")

def main():
    """Main function to scan directories and update statistics"""
    print("🔍 Scanning platform directories for problems...")
    print(f"📍 Current directory: {Path.cwd()}")
    
    platform_dir = Path('platform')
    if not platform_dir.exists():
        print("❌ Error: 'platform' directory not found!")
        print("Make sure you're running this from the repository root.")
        return
    
    print(f"📁 Platform directory: {platform_dir.absolute()}")
    all_problems = []
    
    # Scan each platform directory
    for platform_path in platform_dir.iterdir():
        if platform_path.is_dir():
            print(f"📁 Scanning {platform_path.name}...")
            try:
                platform_problems = scan_problem_directory(platform_path)
                all_problems.extend(platform_problems)
                print(f"   ✅ Found {len(platform_problems)} problems")
            except Exception as e:
                print(f"   ❌ Error scanning {platform_path.name}: {e}")
                continue
    
    if not all_problems:
        print("⚠️  No problems found. Have you set up any problems yet?")
        print("Run: python3 scripts/simple_setup.py LeetCode example-problem 1")
        return
    
    # Calculate statistics
    print("📊 Calculating statistics...")
    stats = calculate_statistics(all_problems)
    
    # Update solutions.json
    update_solutions_json(all_problems, stats)
    
    # Print summary
    print("\n📈 Statistics Summary:")
    print(f"   Total Problems: {stats['total_problems']}")
    print(f"   Platforms: {', '.join(f'{k}({v})' for k, v in stats['platforms'].items())}")
    print(f"   Completed: {stats['status_distribution']['completed']}")
    print(f"   In Progress: {stats['status_distribution']['in_progress']}")
    print(f"   Languages: {', '.join(f'{k}({v})' for k, v in stats['language_distribution'].items() if v > 0)}")

if __name__ == "__main__":
    main()
