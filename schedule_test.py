#!/usr/bin/env python3
"""
Python port of schedule_test.sh script for testing ISL schedule functionality.
"""
import argparse
import glob
import os
import re
import subprocess
import sys

def run_test(test_file, isl_schedule_path, isl_schedule_cmp_path, srcdir):
    """Run schedule test with different component options."""
    print(test_file, flush=True)
    
    # Extract the base name and directory
    base = os.path.basename(test_file).replace('.sc', '')
    dir_path = os.path.dirname(test_file)
    ref = os.path.join(dir_path, f"{base}.st")
    test_output = f"test-{base}.st"
    
    # Extract options from the test file
    options = []
    with open(test_file, 'r') as f:
        content = f.read()
        match = re.search(r'OPTIONS:(.*)', content)
        if match:
            options = match.group(1).strip().split()
    
    # Run with both component options
    component_options = ["--schedule-whole-component", "--no-schedule-whole-component"]
    
    for comp_opt in component_options:
        with open(test_file, 'r') as input_file:
            with open(test_output, 'w') as output_file:
                cmd = [isl_schedule_path, comp_opt] + options
                result = subprocess.run(cmd,
                                      stdin=input_file,
                                      stdout=output_file,
                                      stderr=subprocess.PIPE,
                                      text=True)
                
                if result.returncode != 0:
                    print(f"Schedule test failed for {test_file} with options: {comp_opt} {' '.join(options)}", flush=True)
                    print(result.stderr, flush=True)
                    return False
                
                # Compare output with reference
                result = subprocess.run([isl_schedule_cmp_path, ref, test_output],
                                      stdout=subprocess.PIPE,
                                      stderr=subprocess.PIPE,
                                      text=True)
                
                if result.returncode != 0:
                    print(f"Schedule comparison failed for {test_file} with options: {comp_opt} {' '.join(options)}", flush=True)
                    print(result.stdout, flush=True)
                    print(result.stderr, flush=True)
                    return False
                
                print(f"  ✓ {comp_opt}", flush=True)
        
        # Remove test output file
        try:
            os.remove(test_output)
        except OSError:
            pass
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Run ISL schedule tests')
    parser.add_argument('--exeext', default='', help='Executable extension')
    parser.add_argument('--srcdir', required=True, help='Source directory path')
    parser.add_argument('--isl-schedule', default='isl_schedule', 
                        help='Path to isl_schedule executable')
    parser.add_argument('--isl-schedule-cmp', default='isl_schedule_cmp', 
                        help='Path to isl_schedule_cmp executable')
    args = parser.parse_args()

    isl_schedule_path = f"{args.isl_schedule}{args.exeext}"
    isl_schedule_cmp_path = f"{args.isl_schedule_cmp}{args.exeext}"
    
    print("Running schedule tests:", flush=True)
    
    test_pattern = os.path.join(args.srcdir, "test_inputs/schedule/*.sc")
    test_files = glob.glob(test_pattern)
    
    failed = False
    for test_file in test_files:
        if not run_test(test_file, isl_schedule_path, isl_schedule_cmp_path, args.srcdir):
            failed = True
    
    if failed:
        print("Some schedule tests failed!", flush=True)
        sys.exit(1)
    else:
        print("All schedule tests passed!", flush=True)
        sys.exit(0)

if __name__ == "__main__":
    main()