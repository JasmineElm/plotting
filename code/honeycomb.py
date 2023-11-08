#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    honeycomb: fill a page with hexagons
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
STYLE_LIST = [STROKE_COLOUR, STROKE_WIDTH, FILL_COLOUR]
# set paper size, drawable area, filename
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, DEFAULT_BLEED)
# set filename, creating output directory if necessary
filename = utils.create_dir(DEFAULT_OUTPUT_DIR) + utils.generate_filename()


# LOCAL VARIABLES


DENSITY = 90  # % of hexagons to draw
HEX_SIZE = 20  # how many hexagons can fit in smallest dimension
POINTS = 6  # number of points that make up the polygon

# LOCAL FUNCTIONS


utils.print_params(
    {"paper_size": paper_size,
     "drawable_area": drawable_area,
     "filename": filename}
)

svg_list = []
# fill svg_list with svg objects
SIZE = svg.set_polygon_size(drawable_area, HEX_SIZE)
GAP = int(SIZE)

# in both dimensions, GAP = GAP+(SIZE/2)
for x in range(drawable_area[0], drawable_area[2], SIZE + GAP):
    for count, line in enumerate(range(drawable_area[1],
                                       drawable_area[3], int(SIZE / 2))):
        if random.randint(0, 100) < DENSITY:
            if count % 2 == 0:
                xy_pos = (x + (SIZE + GAP)/2, line)
            else:
                xy_pos = (x, line)
            points_def = svg.set_polygon(xy_pos, SIZE, POINTS)
            POINTS_DEF_STRING = utils.list_to_string(points_def)
            svg_list.append(draw.polygon(POINTS_DEF_STRING, STYLE_LIST))

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
