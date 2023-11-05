#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import toml

# local libraries
import helpers/svg as svg
import helpers/draw as draw  # noqa: F401
import helpers/utils as utils

"""
    Skeleton file for new scripts
"""

# pylint: disable=duplicate-code

# Load config file
config = toml.load('config.toml')

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
utils.print_params({"paper_size": paper_size,
                    "drawable_area": drawable_area,
                    "filename": filename})


# local variables
"""Put local variables here"""
ITERATIONS = 80  # number of lines to draw
quantize_step = DEFAULT_PPMM * 10


# Functions


def always_right(drawable_area, iterations):
    """ draw a line that fits in the drawable area,
    rotate 90% clockwise and repeat for iterations
    returns a list of lists of coordinates
    """
    lines = []
    print("drawable_area: {}".format(drawable_area))
    print("iterations: {}".format(iterations))
    # start at the centre of the drawable area
    x = random.randint(drawable_area[0], drawable_area[2])
    y = random.randint(drawable_area[1], drawable_area[3])
    for iteration in range(1, iterations+1):
        if iteration % 4 == 1:  # X increases, y stays the same
            x2 = random.randint(x, drawable_area[2])
            lines.append([x, y, x2, y])
            x = x2
        elif iteration % 4 == 2:  # Y increases, x stays the same
            y2 = random.randint(y, drawable_area[3])
            lines.append([x, y, x, y2])
            y = y2
        elif iteration % 4 == 3:  # X decreases, y stays the same
            x2 = random.randint(drawable_area[0], x)
            lines.append([x, y, x2, y])
            x = x2
        elif iteration % 4 == 0:  # Y decreases, x stays the same
            y2 = random.randint(drawable_area[1], y)
            lines.append([x, y, x, y2])
            y = y2
    lines = [
        [
            (utils.quantize(x, quantize_step),
             utils.quantize(y, quantize_step)),
            (utils.quantize(x2, quantize_step),
             utils.quantize(y2, quantize_step))
        ]
        for x, y, x2, y2 in lines
    ]
    return lines


# reduce drawable area by quantize_step so the lines comfortably fit
drawable_area = (
    drawable_area[0] + quantize_step*2,
    drawable_area[1] + quantize_step*2,
    drawable_area[2] - quantize_step*2,
    drawable_area[3] - quantize_step*2
)

svg_list = []
line_objects = always_right(drawable_area, ITERATIONS)
for line in line_objects:
    svg_list.append(draw.line(line[0], line[1], STROKE_WIDTH, STROKE_COLOUR))

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
