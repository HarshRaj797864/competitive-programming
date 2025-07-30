#!/usr/bin/env python3

import os
import sys
import json
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse

class BatchOperations:
    def __init__(self):
        self.root_dir = Path(__file__).parent.parent
        self.platforms_dir = self.root_dir / "platforms"
    
    def find_all_problems(self, platform=None):
        """Find all problem directories"""
        problems = []
        
        search_dir = self.platforms_dir
        if platform:
            search_dir = self.platforms_dir / platform
            if not search_dir.exists():
                print(f"❌ Platform not found: {platform}")
                return []
        
        # Find directories with solution files
        for solution_file in search_dir.rglob("solution.*"):
            problem_dir = solution_file.parent
            if problem_dir not in problems:
                problems.append(problem_dir)
        
        # Also check for Java files
        for java_file in search_dir.rglob("Solution.java"):
            problem_dir = java_file.parent
            if problem_dir not in problems:
                problems.append(problem_dir)
        
        return sorted(problems)
    
    def test_problem(self, problem_dir):
        """Test a single problem and return results"""
        try:
            result = subprocess.run([
                "python3", 
                str(self.root_dir / "scripts" / "test_solution.py"),
                str(problem_dir)
            ], capture_output=True, text=True, timeout=30)
            
            # Extract results from output
            success = "All tests passed!" in result.stdout
            return {
                "problem": str(problem_dir.relative_to(self.platforms_dir)),
                "success": success,
                "output": result.stdout,
                "error": result.stderr if result.returncode != 0 else None
            }
        except subprocess.TimeoutExpired:
            return {
                "problem": str(problem_dir.relative_to(self.platforms_dir)),
                "success": False,
                "error": "Timeout"
            }
        except Exception as e:
            return {
                "problem": str(problem_dir.relative_to(self.platforms_dir)),
                "success": False,
                "error": str(e)
            }
    
    def batch_test(self, platform=None, parallel=True, max_workers=4):
        """Test multiple problems"""
        problems = self.find_all_problems(platform)
        
        if not problems:
            print("❌ No problems found!")
            return
        
        print(f"🧪 Found {len(problems)} problems to test...")
        
        if parallel:
            print(f"🚀 Running tests in parallel with {max_workers} workers...")
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_problem = {
                    executor.submit(self.test_problem, problem): problem 
                    for problem in problems
                }
                
                results = []
                for future in as_completed(future_to_problem):
                    result = future.result()
                    results.append(result)
                    
                    # Print progress
                    status = "✅" if result["success"] else "❌"
                    print(f"{status} {result['problem']}")
        else:
            results = []
            for i, problem in enumerate(problems, 1):
                print(f"🧪 Testing {i}/{len(problems)}: {problem.relative_to(self.platforms_dir)}")
                result = self.test_problem(problem)
                results.append(result)
                
                status = "✅" if result["success"] else "❌"
                print(f"{status} Done")
        
        # Print summary
        self.print_test_summary(results)
        
        # Save detailed results
        self.save_batch_results(results)
    
    def print_test_summary(self, results):
        """Print summary of batch test results"""
        print("\n" + "="*60)
        print("BATCH TEST SUMMARY")
        print("="*60)
        
        passed = sum(1 for r in results if r["success"])
        total = len(results)
        
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {total - passed}")
        print(f"📊 Success Rate: {passed/total*100:.1f}%")
        
        if total - passed > 0:
            print(f"\n❌ Failed problems:")
            for result in results:
                if not result["success"]:
                    print(f"   - {result['problem']}")
                    if result.get("error"):
                        print(f"     Error: {result['error']}")
    
    def save_batch_results(self, results):
        """Save batch test results to file"""
        results_file = self.root_dir / "batch_test_results.json"
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "total_problems": len(results),
            "passed": sum(1 for r in results if r["success"]),
            "results": results
        }
        
        with open(results_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\n📊 Detailed results saved to: {results_file}")
    
    def add_headers_batch(self, platform=None, author="Competitive Programmer"):
        """Add headers to all problems"""
        problems = self.find_all_problems(platform)
        
        if not problems:
            print("❌ No problems found!")
            return
        
        print(f"📝 Adding headers to {len(problems)} problems...")
        
        for problem_dir in problems:
            try:
                subprocess.run([
                    "python3",
                    str(self.root_dir / "scripts" / "auto_header.py"),
                    str(problem_dir),
                    "--author", author
                ], check=True, capture_output=True)
                print(f"✅ {problem_dir.relative_to(self.platforms_dir)}")
            except subprocess.CalledProcessError:
                print(f"❌ {problem_dir.relative_to(self.platforms_dir)}")

def main():
    parser = argparse.ArgumentParser(description='Batch operations for competitive programming')
    parser.add_argument('command', choices=['test', 'header'], help='Operation to perform')
    parser.add_argument('--platform', help='Specific platform to operate on')
    parser.add_argument('--author', default='Competitive Programmer', help='Author name for headers')
    parser.add_argument('--no-parallel', action='store_true', help='Disable parallel execution')
    parser.add_argument('--max-workers', type=int, default=4, help='Maximum parallel workers')
    
    args = parser.parse_args()
    
    batch_ops = BatchOperations()
    
    if args.command == 'test':
        batch_ops.batch_test(
            platform=args.platform,
            parallel=not args.no_parallel,
            max_workers=args.max_workers
        )
    elif args.command == 'header':
        batch_ops.add_headers_batch(
            platform=args.platform,
            author=args.author
        )

if __name__ == "__main__":
    main()
