#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""simple test script to run pylint check each script exits with a
non-zero status if any of the following are true
"""
import os
import sys
from pylint import lint
import toml

config = toml.load("config.toml")
DEFAULT_OUTPUT_DIR = config["directories"]["output"]
THRESHOLD = config["lint"]["threshold"]
THIS_FILE = os.path.basename(__file__)
LINTRC = config["lint"]["rcfile"]


def get_files():
    """Get list of files to check using local paths"""
    files = []
    for root, _, filenames in os.walk("."):
        for filename in filenames:
            if filename.endswith(".py") and filename != THIS_FILE:
                files.append(os.path.join(root, filename))
    return files

def run_file(filename):
    """Run each script using python3"""
    cmd = "python3 " + filename
    os.system(cmd)


def check_threshold(score, threshold=THRESHOLD):
    """check score against threshold"""
    if score < threshold:
        print(f"Score {score} is below threshold {threshold}")
        sys.exit(1)


def lint_file(filename, rcfile, threshold=THRESHOLD):
    """run pylint on filename, using custom rcfile"""
    print(f"Checking {filename}...")
    score = lint.Run([filename] + ["--rcfile", rcfile],
                     exit=False).linter.stats.global_note
    check_threshold(score, threshold)


def clear_output_dir():
    """clear output directory"""
    cmd = "rm -rf " + DEFAULT_OUTPUT_DIR + "*"
    os.system(cmd)


files = get_files()

for file in files:
    run_file(file)
    lint_file(file, LINTRC, THRESHOLD)
    clear_output_dir()


