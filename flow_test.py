#!/usr/bin/env python3
"""
Python port of flow_test.sh script for testing ISL flow functionality.
"""
import argparse
import glob
import os
import subprocess
import sys

def run_test(test_file, isl_flow_path, isl_flow_cmp_path, srcdir):
    """Run a single flow test and compare the results."""
    print(test_file, flush=True)
    
    # Extract the base name and directory
    base = os.path.basename(test_file).replace('.ai', '')
    dir_path = os.path.dirname(test_file)
    test_output = f"test-{base}.flow"
    ref = os.path.join(dir_path, f"{base}.flow")
    
    # Run flow test
    with open(test_file, 'r') as input_file:
        with open(test_output, 'w') as output_file:
            result = subprocess.run([isl_flow_path],
                                   stdin=input_file,
                                   stdout=output_file,
                                   stderr=subprocess.PIPE,
                                   text=True)
            
            if result.returncode != 0:
                print(f"Flow test failed for {test_file}", flush=True)
                print(result.stderr, flush=True)
                return False
    
    # Compare output with reference
    result = subprocess.run([isl_flow_cmp_path, ref, test_output],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           text=True)
    
    if result.returncode != 0:
        print(f"Flow comparison failed for {test_file}:", flush=True)
        print(result.stdout, flush=True)
        print(result.stderr, flush=True)
        return False
    
    # Remove the temp file
    try:
        os.remove(test_output)
    except OSError:
        pass
    
    print(f"  ✓ flow test and comparison", flush=True)    
    return True

def main():
    parser = argparse.ArgumentParser(description='Run ISL flow tests')
    parser.add_argument('--exeext', default='', help='Executable extension')
    parser.add_argument('--srcdir', required=True, help='Source directory path')
    parser.add_argument('--isl-flow', default='isl_flow', help='Path to isl_flow executable')
    parser.add_argument('--isl-flow-cmp', default='isl_flow_cmp', help='Path to isl_flow_cmp executable')
    args = parser.parse_args()

    isl_flow_path = f"{args.isl_flow}{args.exeext}"
    isl_flow_cmp_path = f"{args.isl_flow_cmp}{args.exeext}"
    
    print("Running flow tests:", flush=True)
    
    test_pattern = os.path.join(args.srcdir, "test_inputs/flow/*.ai")
    test_files = glob.glob(test_pattern)
    
    failed = False
    for test_file in test_files:
        if not run_test(test_file, isl_flow_path, isl_flow_cmp_path, args.srcdir):
            failed = True
    
    if failed:
        print("Some flow tests failed!", flush=True)
        sys.exit(1)
    else:
        print("All flow tests passed!", flush=True)
        sys.exit(0)

if __name__ == "__main__":
    main()