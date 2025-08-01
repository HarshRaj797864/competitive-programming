#!/usr/bin/env python3
"""
README Generator for Competitive Programming Repository
Generates README.md with current statistics and problem listings
"""

import json
from datetime import datetime
from pathlib import Path

def load_solutions_data():
    """Load data from solutions.json"""
    try:
        with open('solutions.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: solutions.json not found!")
        print("Please run stats_generator.py first")
        return None
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing solutions.json: {e}")
        return None

def generate_stats_badges(stats):
    """Generate badge-style statistics for the README"""
    badges = []
    
    total = stats['total_problems']
    completed = stats['status_distribution']['completed']
    
    badges.append(f"![Total Problems](https://img.shields.io/badge/Total%20Problems-{total}-blue)")
    badges.append(f"![Solved](https://img.shields.io/badge/Solved-{completed}-green)")
    
    if total > 0:
        completion_rate = int((completed / total) * 100)
        badges.append(f"![Progress](https://img.shields.io/badge/Progress-{completion_rate}%25-orange)")
    
    # Platform badges
    for platform, count in stats['platforms'].items():
        badges.append(f"![{platform}](https://img.shields.io/badge/{platform}-{count}-lightgrey)")
    
    return badges

def generate_platform_tables(problems):
    """Generate markdown tables for each platform"""
    platforms = {}
    
    # Group problems by platform
    for problem in problems:
        platform = problem['platform']
        if platform not in platforms:
            platforms[platform] = []
        platforms[platform].append(problem)
    
    tables = []
    
    for platform, platform_problems in platforms.items():
        # Sort by status (completed first) then by name
        platform_problems.sort(key=lambda p: (
            0 if p['status'] == 'completed' else 1 if p['status'] == 'in_progress' else 2,
            p['name']
        ))
        
        table = f"\n### {platform} ({len(platform_problems)} problems)\n\n"
        table += "| Problem | Difficulty | Status | Languages | Last Updated |\n"
        table += "|---------|------------|--------|-----------|-------------|\n"
        
        for problem in platform_problems:
            name = problem['name'].replace('-', ' ').title()
            
            # Create link if URL exists
            if problem.get('url'):
                name_link = f"[{name}]({problem['url']})"
            else:
                name_link = name
            
            # Add problem directory link
            dir_link = f"[📁]({problem['directory']})"
            name_cell = f"{name_link} {dir_link}"
            
            difficulty = problem.get('difficulty', 'Unknown')
            status = format_status(problem.get('status', 'Unknown'))
            languages = ', '.join(problem.get('languages', []))
            
            last_updated = problem.get('last_modified', '')
            if last_updated:
                try:
                    date_obj = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                    last_updated = date_obj.strftime('%Y-%m-%d')
                except:
                    last_updated = 'Unknown'
            
            table += f"| {name_cell} | {difficulty} | {status} | {languages} | {last_updated} |\n"
        
        tables.append(table)
    
    return tables

def format_status(status):
    """Format status with emoji"""
    status_map = {
        'completed': '✅ Completed',
        'in_progress': '🟡 In Progress',
        'started': '🟠 Started',
        'not_started': '⚪ Not Started',
        'Unknown': '❓ Unknown'
    }
    return status_map.get(status, status)

def generate_recent_activity(stats):
    """Generate recent activity section"""
    recent = stats.get('recent_activity', [])
    if not recent:
        return ""
    
    activity_section = "\n## 📈 Recent Activity\n\n"
    
    for activity in recent[:5]:  # Show last 5
        name = activity['name'].replace('-', ' ').title()
        platform = activity['platform']
        status = format_status(activity['status'])
        
        date = activity.get('last_modified', '')
        if date:
            try:
                date_obj = datetime.fromisoformat(date.replace('Z', '+00:00'))
                date_str = date_obj.strftime('%b %d, %Y')
            except:
                date_str = 'Recently'
        else:
            date_str = 'Recently'
        
        activity_section += f"- **{name}** ({platform}) - {status} - {date_str}\n"
    
    return activity_section

def generate_statistics_section(stats):
    """Generate detailed statistics section"""
    section = "\n## 📊 Statistics\n\n"
    
    # Overview
    section += "### Overview\n"
    section += f"- **Total Problems**: {stats['total_problems']}\n"
    section += f"- **Completed**: {stats['status_distribution']['completed']}\n"
    section += f"- **In Progress**: {stats['status_distribution']['in_progress']}\n"
    section += f"- **Started**: {stats['status_distribution']['started']}\n\n"
    
    # Platform breakdown
    section += "### By Platform\n"
    for platform, count in stats['platforms'].items():
        completed = sum(1 for p in stats.get('problems', []) 
                       if p['platform'] == platform and p.get('status') == 'completed')
        section += f"- **{platform}**: {count} total, {completed} completed\n"
    section += "\n"
    
    # Language breakdown
    section += "### By Language\n"
    for language, count in stats['language_distribution'].items():
        if count > 0:
            section += f"- **{language}**: {count} solutions\n"
    
    return section

def generate_readme(solutions_data):
    """Generate the complete README content"""
    stats = solutions_data.get('statistics', {})
    problems = solutions_data.get('problems', [])
    metadata = solutions_data.get('metadata', {})
    
    # Header
    readme = "# 🚀 Competitive Programming Solutions\n\n"
    readme += "My journey through competitive programming problems from various platforms.\n\n"
    
    # Badges
    badges = generate_stats_badges(stats)
    for badge in badges:
        readme += badge + " "
    readme += "\n\n"
    
    # Quick Stats
    readme += "## 🎯 Quick Stats\n\n"
    readme += f"**Last Updated**: {datetime.now().strftime('%B %d, %Y')}\n\n"
    
    total = stats['total_problems']
    completed = stats['status_distribution']['completed']
    if total > 0:
        completion_rate = (completed / total) * 100
        readme += f"**Progress**: {completed}/{total} problems solved ({completion_rate:.1f}%)\n\n"
    
    # Recent Activity
    readme += generate_recent_activity(stats)
    
    # Usage Instructions
    readme += "\n## 🛠️ Setup & Usage\n\n"
    readme += "### Quick Start\n"
    readme += "```bash\n"
    readme += "# Set up a new problem manually\n"
    readme += "python3 scripts/simple_setup.py LeetCode two-sum 1\n\n"
    readme += "# Or use Competitive Companion (automatic)\n"
    readme += "python3 scripts/companion_listener.py\n"
    readme += "# Then click the green + icon on any problem page\n"
    readme += "```\n\n"
    
    readme += "### Repository Structure\n"
    readme += "```\n"
    readme += "competitive-programming/\n"
    readme += "├── platform/\n"
    readme += "│   ├── LeetCode/\n"
    readme += "│   ├── Codeforces/\n"
    readme += "│   └── AtCoder/\n"
    readme += "├── scripts/          # Automation tools\n"
    readme += "└── templates/        # Code templates\n"
    readme += "```\n\n"
    
    # Platform tables
    readme += "## 📚 Problems by Platform\n"
    platform_tables = generate_platform_tables(problems)
    for table in platform_tables:
        readme += table
    
    # Detailed statistics
    readme += generate_statistics_section(stats)
    
    # Footer
    readme += "\n## 🤝 Contributing\n\n"
    readme += "Feel free to suggest improvements or optimizations! Check out [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.\n\n"
    readme += "## 📄 License\n\n"
    readme += "This repository is for educational purposes. Individual problem solutions may be subject to platform-specific terms.\n\n"
    readme += "---\n\n"
    readme += "**Happy Coding!** 🎉\n\n"
    readme += f"*Auto-generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} by [update_readme.py](scripts/update_readme.py)*\n"
    
    return readme

def main():
    """Main function to generate README"""
    print("📝 Generating README.md...")
    
    # Load solutions data
    solutions_data = load_solutions_data()
    if not solutions_data:
        return
    
    # Generate README content
    readme_content = generate_readme(solutions_data)
    
    # Write README.md
    with open('README.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ README.md updated successfully!")
    
    # Print summary
    stats = solutions_data.get('statistics', {})
    print(f"📊 Included {stats['total_problems']} problems from {len(stats['platforms'])} platforms")

if __name__ == "__main__":
    main()
