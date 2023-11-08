#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Draw some circles on a canvas
"""
import random
import toml

# local libraries
from helpers import svg, utils, draw


# Load config file
config = toml.load("config.toml")

# Paper sizes and pixels
DEFAULT_SIZE = config["paper_sizes"]["A3"]
DEFAULT_LANDSCAPE = True
DEFAULT_PPMM = config["page"]["pixels_per_mm"]
DEFAULT_BLEED = config["page"]["bleed"]

DEFAULT_OUTPUT_DIR = config["directories"]["output"]

# Stroke and fill colours
STROKE_COLOUR = config["colours"]["stroke"]
STROKE_WIDTH = config["page"]["pixels_per_mm"]
FILL_COLOUR = config["colours"]["fill"]

# set paper size, drawable area, filename
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, DEFAULT_BLEED)
# set filename, creating output directory if necessary
filename = utils.create_dir(DEFAULT_OUTPUT_DIR) + utils.generate_filename()


# LOCAL VARIABLES
CIRCLE_COUNT = 100
MIN_RADIUS = 10
MAX_RADIUS = 100
# LOCAL FUNCTIONS


def circle_to_square(circle):
    """Convert a circle to a square"""
    x = circle[0]
    y = circle[1]
    r = circle[2]
    return ([x - r, y - r], [x + r, y + r])


def cleanse_circle(circle, viewbox):
    """Remove circles that are outside the drawable area"""
    ret_val = False
    square = circle_to_square(circle)
    if svg.is_in_drawable_area(square[0], square[1], viewbox):
        ret_val = True
    return ret_val


def set_circle_list(circles_count, min_radius, max_radius, viewbox):
    """Create a list of circles"""
    circles = []
    for i in range(circles_count):
        pct_complete = 0
        pct_complete = utils.print_pct_complete(i, circles_count, pct_complete)
        x = random.randint(viewbox[0], viewbox[2])
        y = random.randint(viewbox[1], viewbox[3])
        r = random.randint(min_radius, max_radius)
        if cleanse_circle((x, y, r), viewbox):
            circles.append((x, y, r))
    return circles


utils.print_params(
    {"paper_size": paper_size, "drawable_area": drawable_area, "filename": filename}
)

svg_list = []
circle_list = set_circle_list(CIRCLE_COUNT, MIN_RADIUS, MAX_RADIUS, drawable_area)
for circle_def in circle_list:
    svg_list.append(
        draw.circle(
            circle_def[0],
            circle_def[1],
            circle_def[2],
            STROKE_COLOUR,
            STROKE_WIDTH,
            FILL_COLOUR,
        )
    )

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
