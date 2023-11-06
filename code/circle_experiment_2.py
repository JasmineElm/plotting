#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" Create a circle using lines joining random points on the
    circumference with arcs
"""

import toml

# local libraries
from helpers import svg, utils, draw

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


# LOCAL VARIABLES
LINE_COUNT = 250

# LOCAL FUNCTIONS


def random_lines_circle(circle, line_count):
    """
        Draw a number of lines from one edge of a circle to the other.
    """
    line_list = []
    pct_complete = 0
    for i in range(line_count):
        pct_complete = utils.print_pct_complete(i, line_count, pct_complete)
        start_xy = utils.random_point_on_circle(circle)
        end_xy = utils.random_point_on_circle(circle)
        # control is a point within the circle
        control_xy = utils.random_point_on_circle(circle)
        line_list.append((start_xy, control_xy, end_xy))
    return line_list


# add your svg code here
svg_list = []
# fill svg_list with svg objects
circle_def = svg.set_circle(drawable_area)
utils.print_params({"paper_size": paper_size,
                    "drawable_area": drawable_area,
                    "filename": filename,
                    "line count": LINE_COUNT,
                    "circle diameter": circle_def[1]})

for line in random_lines_circle(circle_def, LINE_COUNT):
    svg_list.append(draw.quadratic_curve(line[0], line[1], line[2],
                                         STROKE_WIDTH, STROKE_COLOUR))

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
