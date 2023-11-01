#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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
        print("{}: {}".format(key, value))
    return None

# Math functions


def quantize(value, step):
    """Quantize value to the nearest step
    """
    return int(math.floor(value / step) * step)+step
