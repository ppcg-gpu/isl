#!/usr/bin/env python3
"""
Python port of codegen_test.sh script for testing ISL code generation.
"""
import argparse
import glob
import os
import subprocess
import sys
import shlex

def run_test(test_file, isl_codegen_path, diff_cmd, srcdir):
    """Run a single codegen test."""
    print(test_file, flush=True)

    # Extract the base name and directory
    base = os.path.basename(test_file)
    ext = ".st" if base.endswith(".st") else ".in"
    base = base.replace(ext, "")
    out = base + ".c"
    test_output = "test-" + out
    dir_path = os.path.dirname(test_file)
    ref = os.path.join(dir_path, out)

    # Run codegen
    with open(test_file, 'r') as input_file:
        with open(test_output, 'w') as output_file:
            result = subprocess.run([isl_codegen_path],
                                  stdin=input_file,
                                  stdout=output_file,
                                  stderr=subprocess.PIPE,
                                  text=True)

            if result.returncode != 0:
                print(f"Codegen failed for {test_file}", flush=True)
                print(result.stderr, flush=True)
                return False

    diff_command = shlex.split(diff_cmd.strip('\"'))
    diff_command.extend([ref, test_output])

    result = subprocess.run(diff_command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           text=True)

    if result.returncode != 0:
        print(f"Diff failed for {test_file}:", flush=True)
        print(result.stdout, flush=True)
        print(result.stderr, flush=True)
        return False

    # Remove the temp file
    try:
        os.remove(test_output)
    except OSError:
        pass

    print(f"  ✓ code generation and diff check", flush=True)
    return True

def main():
    parser = argparse.ArgumentParser(description='Run ISL codegen tests')
    parser.add_argument('--exeext', default='', help='Executable extension')
    parser.add_argument('--srcdir', required=True, help='Source directory path')
    parser.add_argument('--isl-codegen', default='isl_codegen', help='Path to isl_codegen executable')
    parser.add_argument('--diff', default='diff', help='Path to diff executable with optional arguments')

    # Allow extra args to be passed through as part of diff command
    args, extra_args = parser.parse_known_args()

    # Nothing to do with extra_args as they won't be passed as separate arguments
    # in the CMake case where --diff="${CMAKE_COMMAND} -E compare_files"

    isl_codegen_path = f"{args.isl_codegen}{args.exeext}"

    print("Running codegen tests:", flush=True)

    test_patterns = [
        os.path.join(args.srcdir, "test_inputs/codegen/*.st"),
        os.path.join(args.srcdir, "test_inputs/codegen/cloog/*.st"),
        os.path.join(args.srcdir, "test_inputs/codegen/*.in"),
        os.path.join(args.srcdir, "test_inputs/codegen/omega/*.in"),
        os.path.join(args.srcdir, "test_inputs/codegen/pldi2012/*.in")
    ]

    all_test_files = []
    for pattern in test_patterns:
        all_test_files.extend(glob.glob(pattern))

    failed = False
    for test_file in all_test_files:
        if not run_test(test_file, isl_codegen_path, args.diff, args.srcdir):
            failed = True

    if failed:
        print("Some codegen tests failed!", flush=True)
        sys.exit(1)
    else:
        print("All codegen tests passed!", flush=True)
        sys.exit(0)

if __name__ == "__main__":
    main()
