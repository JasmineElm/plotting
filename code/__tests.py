#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""simple test script to run pylint check each script exits with a
non-zero status if any of the following are true
"""
import os
import sys
import shutil
from pylint import lint
import tomllib

config_path = os.path.join(os.path.dirname(__file__), "config.toml")
with open(config_path, "rb") as f:
    config = tomllib.load(f)
DEFAULT_OUTPUT_DIR = config["directories"]["output"]
TEST_OUTPUT_DIR = DEFAULT_OUTPUT_DIR
THRESHOLD = config["lint"]["threshold"]
THIS_FILE = os.path.basename(__file__)
LINTRC = config["lint"]["rcfile"]


def get_files():
    """Get list of files to check using local paths"""
    files = []
    for root, _, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".py") and filename != THIS_FILE:
                path = os.path.join(root, filename)
                if "template/skeleton.py" not in path.replace(os.sep, "/"):
                    files.append(path)
    return files


def run_file(filename):
    """Run each script using python3 and store its generated SVG"""
    cmd = f"python3 {filename}"
    os.system(cmd)


def check_threshold(score, filename, threshold=THRESHOLD):
    """check score against threshold and return boolean pass/fail"""
    if score < threshold:
        print(f"Score {score} for {filename} is below threshold {threshold}")
        return False
    return True


def lint_file(filename, rcfile, threshold=THRESHOLD):
    """run pylint on filename, using custom rcfile"""
    print(f"Checking {filename}...")
    score = lint.Run([filename] + ["--rcfile", rcfile],
                     exit=False).linter.stats.global_note
    return check_threshold(score, filename, threshold)


# def clear_output_dir():
#     """clear output directory of SVGs to isolate the next test"""
#     if os.path.exists(DEFAULT_OUTPUT_DIR):
#         for f in os.listdir(DEFAULT_OUTPUT_DIR):
#             path = os.path.join(DEFAULT_OUTPUT_DIR, f)
#             if os.path.isfile(path) and f.endswith('.svg'):
#                 os.remove(path)


files = get_files()
all_passed = True

for file in files:
    run_file(file)
    if not lint_file(file, LINTRC, THRESHOLD):
        all_passed = False
    # clear_output_dir()

if not all_passed:
    sys.exit(1)
