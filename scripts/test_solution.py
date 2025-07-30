#!/usr/bin/env python3

import os
import sys
import subprocess
import time
import json
from pathlib import Path
import argparse

class SolutionTester:
    def __init__(self, problem_path):
        self.problem_dir = Path(problem_path)
        self.root_dir = self.problem_dir
        
        # Try to find the actual problem directory
        if not (self.problem_dir / "solution.cpp").exists() and not (self.problem_dir / "solution.py").exists():
            # Maybe we're given a relative path from root
            root = Path(__file__).parent.parent
            potential_path = root / problem_path
            if potential_path.exists():
                self.problem_dir = potential_path
        
        print(f"🧪 Testing problem in: {self.problem_dir}")
        self.results = []
    
    def find_solution_files(self):
        """Find all solution files in the directory"""
        solutions = {}
        
        cpp_file = self.problem_dir / "solution.cpp"
        py_file = self.problem_dir / "solution.py" 
        java_file = self.problem_dir / "Solution.java"
        
        if cpp_file.exists():
            solutions['cpp'] = cpp_file
        if py_file.exists():
            solutions['python'] = py_file
        if java_file.exists():
            solutions['java'] = java_file
        
        return solutions
    
    def compile_cpp(self, cpp_file):
        """Compile C++ solution with competitive programming flags"""
        executable = self.problem_dir / "solution"
        
        # Use competitive programming compiler flags
        compile_cmd = [
            "g++",
            "-std=c++17",
            "-O2",
            "-Wall",
            "-Wextra", 
            "-Wshadow",
            "-DLOCAL",  # Define LOCAL for debug macros
            "-o", str(executable),
            str(cpp_file)
        ]
        
        print(f"🔨 Compiling: {cpp_file.name}")
        result = subprocess.run(compile_cmd, capture_output=True, text=True)
        
        if result.returncode != 0:
            print("❌ Compilation failed:")
            print(result.stderr)
            return None
        
        print("✅ Compilation successful")
        return executable
    
    def compile_java(self, java_file):
        """Compile Java solution"""
        print(f"🔨 Compiling: {java_file.name}")
        result = subprocess.run(
            ["javac", str(java_file)], 
            capture_output=True, 
            text=True,
            cwd=str(self.problem_dir)
        )
        
        if result.returncode != 0:
            print("❌ Java compilation failed:")
            print(result.stderr)
            return None
        
        print("✅ Java compilation successful")
        return self.problem_dir / "Solution.class"
    
    def run_test_case(self, solution_file, lang, input_file, expected_file, test_name):
        """Run a single test case"""
        if not input_file.exists():
            print(f"⚠️  Input file {input_file} not found, skipping {test_name}")
            return
        
        print(f"\n🧪 Running {test_name}...")
        
        start_time = time.time()
        
        try:
            with open(input_file, 'r') as f:
                if lang == 'cpp':
                    result = subprocess.run(
                        [str(solution_file)],
                        stdin=f,
                        capture_output=True,
                        text=True,
                        timeout=5.0,
                        cwd=str(self.problem_dir)
                    )
                elif lang == 'python':
                    result = subprocess.run(
                        ["python3", str(solution_file)],
                        stdin=f,
                        capture_output=True,
                        text=True,
                        timeout=5.0,
                        cwd=str(self.problem_dir)
                    )
                elif lang == 'java':
                    result = subprocess.run(
                        ["java", "Solution"],
                        stdin=f,
                        capture_output=True,
                        text=True,
                        timeout=5.0,
                        cwd=str(self.problem_dir)
                    )
            
            execution_time = time.time() - start_time
            
            if result.returncode != 0:
                print(f"❌ Runtime Error in {test_name}")
                print(f"Error: {result.stderr}")
                self.results.append({
                    "test": test_name,
                    "status": "Runtime Error",
                    "time": execution_time,
                    "error": result.stderr.strip()
                })
                return
            
            # Get actual output
            actual_output = result.stdout.strip()
            
            # Compare with expected output if available
            if expected_file and expected_file.exists():
                with open(expected_file, 'r') as f:
                    expected_output = f.read().strip()
                
                if actual_output == expected_output:
                    print(f"✅ {test_name} PASSED ({execution_time:.3f}s)")
                    self.results.append({
                        "test": test_name,
                        "status": "Accepted", 
                        "time": execution_time
                    })
                else:
                    print(f"❌ {test_name} WRONG ANSWER ({execution_time:.3f}s)")
                    print(f"Expected:\n{expected_output}")
                    print(f"Got:\n{actual_output}")
                    self.results.append({
                        "test": test_name,
                        "status": "Wrong Answer",
                        "time": execution_time,
                        "expected": expected_output,
                        "actual": actual_output
                    })
            else:
                print(f"🔍 {test_name} OUTPUT ({execution_time:.3f}s):")
                print(actual_output)
                
                # Save output for manual verification
                output_file = self.problem_dir / "output.txt"
                with open(output_file, 'w') as f:
                    f.write(actual_output)
                
                self.results.append({
                    "test": test_name,
                    "status": "Output Generated",
                    "time": execution_time,
                    "output": actual_output
                })
        
        except subprocess.TimeoutExpired:
            print(f"⏰ {test_name} TIMEOUT (>5s)")
            self.results.append({
                "test": test_name,
                "status": "Time Limit Exceeded",
                "time": 5.0
            })
        except Exception as e:
            print(f"💥 {test_name} ERROR: {e}")
            self.results.append({
                "test": test_name,
                "status": "Error",
                "error": str(e)
            })
    
    def test_all_solutions(self):
        """Test all available solutions"""
        solutions = self.find_solution_files()
        
        if not solutions:
            print("❌ No solution files found!")
            return
        
        print(f"Found solutions: {list(solutions.keys())}")
        
        # Test cases to run
        test_cases = [
            ("sample_input.txt", "sample_output.txt", "Sample Test"),
            ("input.txt", "expected.txt", "Custom Test"),
            ("input.txt", None, "Input Test")  # Just run with input, no expected output
        ]
        
        for lang, solution_file in solutions.items():
            print(f"\n{'='*50}")
            print(f"Testing {lang.upper()} solution")
            print(f"{'='*50}")
            
            # Compile if needed
            executable = solution_file
            if lang == 'cpp':
                executable = self.compile_cpp(solution_file)
                if not executable:
                    continue
            elif lang == 'java':
                executable = self.compile_java(solution_file)
                if not executable:
                    continue
            
            # Run test cases
            for input_name, expected_name, test_name in test_cases:
                input_file = self.problem_dir / input_name
                expected_file = self.problem_dir / expected_name if expected_name else None
                
                self.run_test_case(executable, lang, input_file, expected_file, f"{test_name} ({lang})")
        
        # Print summary
        self.print_summary()
        
        # Save results
        self.save_results()
    
    def print_summary(self):
        """Print test summary"""
        print(f"\n{'='*60}")  
        print("TEST SUMMARY")
        print(f"{'='*60}")
        
        if not self.results:
            print("No tests were run!")
            return
        
        passed = sum(1 for r in self.results if r["status"] == "Accepted")
        total = len([r for r in self.results if r["status"] in ["Accepted", "Wrong Answer", "Runtime Error", "Time Limit Exceeded"]])
        
        print(f"Tests passed: {passed}/{total}")
        
        # Group by status
        status_count = {}
        for result in self.results:
            status = result["status"]
            status_count[status] = status_count.get(status, 0) + 1
        
        for status, count in status_count.items():
            emoji = {"Accepted": "✅", "Wrong Answer": "❌", "Runtime Error": "💥", 
                    "Time Limit Exceeded": "⏰", "Output Generated": "🔍"}.get(status, "❓")
            print(f"{emoji} {status}: {count}")
        
        if passed == total and total > 0:
            print("\n🎉 All tests passed!")
        elif passed > 0:
            print(f"\n⚠️  {total - passed} test(s) failed")
        else:
            print("\n❌ All tests failed")
    
    def save_results(self):
        """Save test results"""
        results_file = self.problem_dir / "test_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "results": self.results
            }, f, indent=2)
        print(f"\n📊 Results saved to: {results_file}")

def main():
    parser = argparse.ArgumentParser(description='Test competitive programming solutions')
    parser.add_argument('problem_path', help='Path to problem directory')
    
    args = parser.parse_args()
    
    tester = SolutionTester(args.problem_path)
    tester.test_all_solutions()

if __name__ == "__main__":
    main()
