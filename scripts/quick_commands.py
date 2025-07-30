#!/usr/bin/env python3

import sys
import subprocess
from pathlib import Path

def run_command(cmd):
    """Run a shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def setup_problem_interactive():
    """Interactive problem setup"""
    print("🚀 Quick Problem Setup")
    print("=" * 30)
    
    platform = input("Platform (cf/ac/lc/cc): ").strip()
    contest = input("Contest ID/Name: ").strip()
    problem = input("Problem Code (A/B/C/etc): ").strip()
    name = input("Problem Name (optional): ").strip()
    url = input("Problem URL (optional): ").strip()
    
    cmd_parts = [
        "python3", "scripts/setup_problem.py",
        platform, contest, problem
    ]
    
    if name:
        cmd_parts.extend(["--name", f'"{name}"'])
    if url:
        cmd_parts.extend(["--url", f'"{url}"'])
    
    cmd = " ".join(cmd_parts)
    print(f"\n🔄 Running: {cmd}")
    
    success, stdout, stderr = run_command(cmd)
    
    if success:
        print("✅ Problem setup completed!")
        print(stdout)
    else:
        print("❌ Setup failed!")
        print(stderr)

def test_current_directory():
    """Test solutions in current directory"""
    current_dir = Path.cwd()
    
    # Check if we're in a problem directory
    if any((current_dir / f"solution.{ext}").exists() for ext in ["cpp", "py", "java"]):
        print(f"🧪 Testing solutions in: {current_dir.name}")
        success, stdout, stderr = run_command(f"python3 scripts/test_solution.py {current_dir}")
        
        if success:
            print(stdout)
        else:
            print("❌ Testing failed!")
            print(stderr)
    else:
        print("❌ No solution files found in current directory")
        print("Available files:", list(current_dir.glob("*")))

def main():
    if len(sys.argv) < 2:
        print("Quick Commands:")
        print("  setup  - Interactive problem setup")
        print("  test   - Test current directory")
        print("  header - Add headers to current directory")
        return
    
    command = sys.argv[1].lower()
    
    if command == "setup":
        setup_problem_interactive()
    elif command == "test":
        test_current_directory()
    elif command == "header":
        current_dir = Path.cwd()
        success, stdout, stderr = run_command(f"python3 scripts/auto_header.py {current_dir}")
        print(stdout if success else stderr)
    else:
        print(f"Unknown command: {command}")

if __name__ == "__main__":
    main()
