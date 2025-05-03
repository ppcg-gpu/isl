#!/usr/bin/env python3
"""
Python port of bound_test.sh script for testing ISL bound functionality.
"""
import argparse
import os
import subprocess
import sys

def run_test(test_file, isl_bound_path, srcdir):
    """Run bound test with bernstein and range options."""
    print(test_file, flush=True)
    
    test_input_path = os.path.join(srcdir, "test_inputs", test_file)
    
    # Run with bernstein option
    with open(test_input_path, 'r') as input_file:
        bernstein_cmd = [isl_bound_path, "-T", "--bound=bernstein"]
        result = subprocess.run(bernstein_cmd, 
                               stdin=input_file, 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
        if result.returncode != 0:
            print(f"Bernstein test failed for {test_file}", flush=True)
            print(result.stdout, flush=True)
            return False
        print(f"  ✓ bernstein", flush=True)
    
    # Run with range option
    with open(test_input_path, 'r') as input_file:
        range_cmd = [isl_bound_path, "-T", "--bound=range"]
        result = subprocess.run(range_cmd, 
                               stdin=input_file, 
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               text=True)
        if result.returncode != 0:
            print(f"Range test failed for {test_file}", flush=True)
            print(result.stdout, flush=True)
            return False
        print(f"  ✓ range", flush=True)
    
    return True

def check_executable(path):
    """Check if the executable exists and is executable."""
    return os.path.isfile(path) and os.access(path, os.X_OK)

def main():
    parser = argparse.ArgumentParser(description='Run ISL bound tests')
    parser.add_argument('--exeext', default='', help='Executable extension')
    parser.add_argument('--srcdir', required=True, help='Source directory path')
    parser.add_argument('--isl-bound', default='isl_bound', help='Path to isl_bound executable')
    args = parser.parse_args()

    isl_bound_path = f"{args.isl_bound}{args.exeext}"
    
    # Check if isl_bound executable exists
    if not check_executable(isl_bound_path):
        # Try to find it in the build directory relative to the current directory
        build_dirs = ['build', '..', '../build', 'build/bin', '../build/bin']
        found = False
        
        for build_dir in build_dirs:
            candidate = os.path.join(build_dir, f"isl_bound{args.exeext}")
            if check_executable(candidate):
                isl_bound_path = candidate
                found = True
                print(f"Found isl_bound at {isl_bound_path}", flush=True)
                break
        
        if not found:
            print(f"ERROR: Could not find isl_bound executable at {isl_bound_path}", flush=True)
            print("Make sure the ISL project is built and provide the correct path with --isl-bound", flush=True)
            sys.exit(1)
    
    # Check if test inputs directory exists
    test_inputs_dir = os.path.join(args.srcdir, "test_inputs")
    if not os.path.isdir(test_inputs_dir):
        print(f"ERROR: Test inputs directory not found at {test_inputs_dir}", flush=True)
        print("Make sure the --srcdir points to the ISL source directory", flush=True)
        sys.exit(1)
    
    bound_tests = [
        "basicLinear2.pwqp",
        "basicLinear.pwqp",
        "basicTestParameterPosNeg.pwqp",
        "basicTest.pwqp",
        "devos.pwqp",
        "equality1.pwqp",
        "equality2.pwqp",
        "equality3.pwqp",
        "equality4.pwqp",
        "equality5.pwqp",
        "faddeev.pwqp",
        "linearExample.pwqp",
        "neg.pwqp",
        "philippe3vars3pars.pwqp",
        "philippe3vars.pwqp",
        "philippeNeg.pwqp",
        "philippePolynomialCoeff1P.pwqp",
        "philippePolynomialCoeff.pwqp",
        "philippe.pwqp",
        "product.pwqp",
        "split.pwqp",
        "test3Deg3Var.pwqp",
        "toplas.pwqp",
        "unexpanded.pwqp",
    ]
    
    print("Running bound tests:", flush=True)
    
    for test_file in bound_tests:
        if not run_test(test_file, isl_bound_path, args.srcdir):
            sys.exit(1)
    
    print("All bound tests passed!", flush=True)
    sys.exit(0)

if __name__ == "__main__":
    main()