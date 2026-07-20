#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
"""
import os
import tomllib

# local libraries
from helpers import svg, utils, draw

# Load config file and set DEFAULT parameters
config_path = os.path.join(os.path.dirname(__file__), "config.toml")
with open(config_path, "rb") as f:
    config = tomllib.load(f)
DEFAULT = config["DEFAULT"]
DEFAULT.update({"PAPER_SIZE": svg.set_image_size(DEFAULT['SIZE'],
                                                 DEFAULT['PPMM'],
                                                 DEFAULT['LANDSCAPE'])})
DEFAULT.update({"DRAWABLE_AREA": svg.set_drawable_area(DEFAULT['PAPER_SIZE'],
                                                       DEFAULT['BLEED'])})
DEFAULT.update({"FILENAME": utils.create_dir(
    DEFAULT['OUTPUT_DIR']) + utils.generate_filename()})


# LOCAL VARIABLES

GRID_SPACING = 3 * DEFAULT['PPMM']
MIN_CIRCLE_DIAMETER = 2 * DEFAULT['PPMM']
POINT_RADIUS = 0.5 * DEFAULT['PPMM']

# LOCAL FUNCTIONS


def paper_size_to_xy(paper_size):
    """Convert paper size to x,y coordinates"""
    return [0, 0, paper_size[0], paper_size[1]]

# set a grid of points that fill the drawable area


GRID_DIMENSIONS = paper_size_to_xy(DEFAULT['PAPER_SIZE'])
grid = svg.generate_square_grid(DEFAULT['DRAWABLE_AREA'], GRID_SPACING)

# draw a circle at each point
svg_list = []
# draw a box around the drawable area
X1 = draw.line([DEFAULT['DRAWABLE_AREA'][0], DEFAULT['DRAWABLE_AREA'][1]],
               [DEFAULT['DRAWABLE_AREA'][0], DEFAULT['DRAWABLE_AREA'][3]],
               DEFAULT['STYLES'][1], DEFAULT['STYLES'][0])
X2 = draw.line([DEFAULT['DRAWABLE_AREA'][2], DEFAULT['DRAWABLE_AREA'][1]],
               [DEFAULT['DRAWABLE_AREA'][2], DEFAULT['DRAWABLE_AREA'][3]],
               DEFAULT['STYLES'][1], DEFAULT['STYLES'][0])
Y1 = draw.line([DEFAULT['DRAWABLE_AREA'][0], DEFAULT['DRAWABLE_AREA'][1]],
               [DEFAULT['DRAWABLE_AREA'][2], DEFAULT['DRAWABLE_AREA'][1]],
               DEFAULT['STYLES'][1], DEFAULT['STYLES'][0])
Y2 = draw.line([DEFAULT['DRAWABLE_AREA'][0], DEFAULT['DRAWABLE_AREA'][3]],
               [DEFAULT['DRAWABLE_AREA'][2], DEFAULT['DRAWABLE_AREA'][3]],
               DEFAULT['STYLES'][1], DEFAULT['STYLES'][0])
svg_list.append(X1)
svg_list.append(X2)
svg_list.append(Y1)
svg_list.append(Y2)

for point in grid:
    circle = draw.circle(point, POINT_RADIUS, [0, 0, 0])
    svg_list.append(circle)

# draw a set of concentric circles until radius is greater than drawable area
centre = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
radius = MIN_CIRCLE_DIAMETER
while radius < max(DEFAULT['DRAWABLE_AREA'][2],
                   DEFAULT['DRAWABLE_AREA'][3]):
    circle = draw.circle(centre, radius, DEFAULT['STYLES'])
    svg_list.append(circle)
    radius += MIN_CIRCLE_DIAMETER

utils.print_params(DEFAULT)

# fill svg_list with svg objects

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)
