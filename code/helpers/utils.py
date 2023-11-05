#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=consider-using-f-string
# using f-strings, but still clocks an error :/
"""
    General utility functions
"""
import os
import sys
import datetime
import math


def create_dir(dir_path):
    """
    Creates a directory at the specified path if it does not already exist.

    Args:
        dir_path (str): The path of the directory to create.

    Returns:
        None
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path


def generate_filename():
    """Generates a filename for the SVG file based on the name of the script,
    the current date, and the current time.

    Returns:
      str: The filename in the format "<name of script>_<date>_<time>.svg".
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = sys.argv[0].split(".py")[0]
    return "{}_{}.svg".format(name, timestamp)


def print_params(param_dict):
    """ print the parameters """
    for key, value in param_dict.items():
        print(f"{key}: {value}")


# Math functions


def quantize(value, step, strategy="floor"):
    """quantize a value to the nearest step, using the specified strategy
    floor - round down to nearest step
    ceil - round up to nearest step
    round - round to nearest step

    Args:
        value (number): input value to quantize
        step (int): quantize step size
        strategy (str, optional): floor, ceil or round. Defaults to "floor".

    Returns:
        int : quantized value
    """
    # if floor, round down to nearest step
    if strategy == "floor":
        ret_val = int(math.floor(value / step) * step)
    # if ceil, round up to nearest step
    elif strategy == "ceil":
        ret_val = int(math.ceil(value / step) * step)
    # if round, round to nearest step
    elif strategy == "round":
        ret_val = int(round(value / step) * step)
    return ret_val
