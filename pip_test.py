#!/usr/bin/env python3
"""
Python port of pip_test.sh script for testing ISL PIP functionality.
"""
import argparse
import os
import subprocess
import sys

def run_test(test_file, isl_pip_path, srcdir):
    """Run a PIP test with different format and context options."""
    print(test_file, flush=True)
    
    test_input_path = os.path.join(srcdir, "test_inputs", test_file)
    
    # Run all combinations of format and context options
    test_configs = [
        ["--format=set", "--context=gbr"],
        ["--format=set", "--context=lexmin"],
        ["--format=affine", "--context=gbr"],
        ["--format=affine", "--context=lexmin"]
    ]
    
    for config in test_configs:
        with open(test_input_path, 'r') as input_file:
            cmd = [isl_pip_path, "-T"] + config
            result = subprocess.run(cmd, 
                                   stdin=input_file, 
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   text=True)
            
            if result.returncode != 0:
                config_str = " ".join(config)
                print(f"PIP test failed for {test_file} with options: {config_str}", flush=True)
                print(result.stdout, flush=True)
                return False
            
            config_str = " ".join(config)
            print(f"  ✓ {config_str}", flush=True)
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Run ISL PIP tests')
    parser.add_argument('--exeext', default='', help='Executable extension')
    parser.add_argument('--srcdir', required=True, help='Source directory path')
    parser.add_argument('--isl-pip', default='isl_pip', help='Path to isl_pip executable')
    args = parser.parse_args()

    isl_pip_path = f"{args.isl_pip}{args.exeext}"
    
    print("Running PIP tests:", flush=True)
    
    pip_tests = [
        "boulet.pip",
        "brisebarre.pip",
        "cg1.pip",
        "esced.pip",
        "ex2.pip",
        "ex.pip",
        "exist.pip",
        "exist2.pip",
        "fimmel.pip",
        "max.pip",
        "negative.pip",
        "seghir-vd.pip",
        "small.pip",
        "sor1d.pip",
        "square.pip",
        "sven.pip",
        "tobi.pip"
    ]
    
    for test_file in pip_tests:
        if not run_test(test_file, isl_pip_path, args.srcdir):
            sys.exit(1)
    
    print("All PIP tests passed!", flush=True)
    sys.exit(0)

if __name__ == "__main__":
    main()