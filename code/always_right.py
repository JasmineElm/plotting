#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" draw a line that fits in the drawable area,
rotate 90% clockwise and repeat for iterations
"""
import random
import os
import tomllib

# local libraries
from helpers import svg, utils, draw  # noqa: F401


# Load config file
config_path = os.path.join(os.path.dirname(__file__), "config.toml")
with open(config_path, "rb") as f:
    config = tomllib.load(f)

# Paper sizes and pixels
DEFAULT_SIZE = config['paper_sizes']['A3']
DEFAULT_LANDSCAPE = True
DEFAULT_PPMM = config['page']['pixels_per_mm']
DEFAULT_BLEED = config['page']['bleed']

DEFAULT_OUTPUT_DIR = config['directories']['output']

# Stroke and fill colours
STROKE_COLOUR = config['colours']['stroke']
STROKE_WIDTH = config['page']['pixels_per_mm']
FILL_COLOUR = config['colours']['fill']

paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, DEFAULT_BLEED)
# set filename, creating output directory if necessary
filename = utils.create_dir(DEFAULT_OUTPUT_DIR) + utils.generate_filename()


# local variables
ITERATIONS = 80  # number of lines to draw
quantize_step = DEFAULT_PPMM * 10

utils.print_params({"paper_size": paper_size,
                    "drawable_area": drawable_area,
                    "filename": filename,
                    "iterations": ITERATIONS})


# Functions
def always_right(viewport, iterations):
    """ draw a line that fits in the drawable area,
    rotate 90% clockwise and repeat for iterations
    returns a list of coordinates
    """
    points = []
    # start at the centre of the drawable area
    x = random.randint(viewport[0], viewport[2])
    y = random.randint(viewport[1], viewport[3])
    points.append((x, y))

    for iteration in range(1, iterations+1):
        if iteration % 4 == 1:  # X increases, y stays the same
            x = random.randint(x, viewport[2])
        elif iteration % 4 == 2:  # Y increases, x stays the same
            y = random.randint(y, viewport[3])
        elif iteration % 4 == 3:  # X decreases, y stays the same
            x = random.randint(viewport[0], x)
        elif iteration % 4 == 0:  # Y decreases, x stays the same
            y = random.randint(viewport[1], y)
        points.append((x, y))

    points = [
        (utils.quantize(px, quantize_step), utils.quantize(py, quantize_step))
        for px, py in points
    ]
    return points


# reduce drawable area by quantize_step so the lines comfortably fit
drawable_area = (
    drawable_area[0] + quantize_step*2,
    drawable_area[1] + quantize_step*2,
    drawable_area[2] - quantize_step*2,
    drawable_area[3] - quantize_step*2
)

svg_list = []
points = always_right(drawable_area, ITERATIONS)

# build a compound path
PATH_D = "M " + " L ".join(f"{p[0]} {p[1]}" for p in points)
PATH_TAG = f"<path d='{PATH_D}' fill='{FILL_COLOUR}' stroke='{STROKE_COLOUR}' stroke-width='{STROKE_WIDTH}' />\n"
svg_list.append(PATH_TAG)

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
