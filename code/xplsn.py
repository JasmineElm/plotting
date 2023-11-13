#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
"""
import math
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
STYLE_LIST = [STROKE_COLOUR, STROKE_WIDTH, FILL_COLOUR]
CIRCLE_STYLE_LIST = [STROKE_COLOUR, STROKE_WIDTH, 'white']
# set paper size, drawable area, filename
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, DEFAULT_BLEED)
# set filename, creating output directory if necessary
filename = utils.create_dir(DEFAULT_OUTPUT_DIR) + utils.generate_filename()


# LOCAL VARIABLES
MAX_LINES = 100
MAX_CIRCLES = 10
MAX_RADIUS = 0.125
NOISE = 0.5

# LOCAL FUNCTIONS


def set_line(inner_circle, outer_circle, max_lines, noise):
    """draw a line or random length starting at inner_circle
    ending between inner and outer circles


    Args:
        inner_circle ((x,y)r): position and radius of inner circle
        outer_circle ((x,y)r): position and radius of outer circle
        line_number (int): line number
        noise (float): random noise to add to line length, and position
    """
    angle_seed = 1 - random.random() * noise
    line_seed = 1 - random.random() * noise
    angle = 2 * math.pi * max_lines * angle_seed
    x1 = inner_circle[0][0] + inner_circle[1] * math.cos(angle)
    y1 = inner_circle[0][1] + inner_circle[1] * math.sin(angle)
    # choose a random value between inner_radius and outer_radius
    length = inner_circle[1] + \
        (outer_circle[1] - inner_circle[1]) * line_seed
    x2 = length * math.cos(angle) + inner_circle[0][0]
    y2 = length * math.sin(angle) + inner_circle[0][1]
    return [[x1, y1], [x2, y2]]


outer_crcl = svg.set_circle(drawable_area)
inner_crcl = svg.set_circle(drawable_area, 0.03)
# set radius of inner circle to 1/10 of outer circle
print(inner_crcl, outer_crcl)
print(drawable_area)

svg_list = []

for i in range(0, MAX_LINES):
    line_def = set_line(inner_crcl, outer_crcl, i, NOISE)
    svg_list.append(draw.line(line_def[0], line_def[1],
                              STROKE_WIDTH, STROKE_COLOUR))

for i in range(0, MAX_CIRCLES):
    point = svg.get_random_point(drawable_area)
    radius = MAX_RADIUS * outer_crcl[1] * \
        svg.get_centrality(drawable_area, point)
    print(point, radius)
    circle_def = [point, radius]
    svg_list.append(draw.circle(circle_def[0],
                                circle_def[1], CIRCLE_STYLE_LIST))


utils.print_params(
    {"paper_size": paper_size,
     "drawable_area": drawable_area,
     "filename": filename,
        "max lines": MAX_LINES,
        "max circles": MAX_CIRCLES}
)

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
