#!/usr/bin/env python3
"""
Simple test runner for the competence analyzer project
Run this from the project root directory
"""

import os
import sys
import subprocess

def main():
    """Run tests with proper path setup"""
    
    # Get project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Add src to Python path
    src_path = os.path.join(project_root, 'src')
    sys.path.insert(0, src_path)
    
    # Change to project directory
    os.chdir(project_root)
    
    print("=" * 50)
    print("Running Python Competence Analyzer Tests")
    print("=" * 50)
    
    try:
        # Try to run tests using python -m unittest
        test_dir = os.path.join(project_root, 'test')
        test_file = os.path.join(test_dir, 'test_analyzer.py')
        
        if os.path.exists(test_file):
            print(f"Running tests from: {test_file}")
            result = subprocess.run([sys.executable, test_file], 
                                  cwd=project_root,
                                  capture_output=True, 
                                  text=True)
            
            print("STDOUT:")
            print(result.stdout)
            
            if result.stderr:
                print("STDERR:")
                print(result.stderr)
            
            if result.returncode == 0:
                print("\n✅ All tests passed!")
            else:
                print(f"\n❌ Tests failed with exit code: {result.returncode}")
                
            return result.returncode
        else:
            print(f"❌ Test file not found: {test_file}")
            return 1
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)