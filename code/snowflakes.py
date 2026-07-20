#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    snowflake-like drawing
"""
import os
import tomllib
import math

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

# LOCAL FUNCTIONS

def snowflake(center, arms, radius, depth, styles):
    """Draw a snowflake"""
    linearray = []
    if depth == 0:
        return linearray

    x, y = center
    # draw arms of snowflake, 360/arms degrees apart, radiaus long
    length = radius
    two_thirds = 2 / 3
    sqrt_third = math.sqrt(3) / 3
    for i in range(arms):
        # draw a line of length radius
        while depth > 0:
            len_third = length / 3
            len_sqrt_third = length * sqrt_third
            linearray.append(
                draw.line([x, y], [x + length, y], styles[1], styles[0]))
            # 2/3 of the way along the line, draw a new line at 60 degrees
            # of length radius/3
            linearray.append(draw.line(
                [x + length * two_thirds, y], [x + length * two_thirds + len_third, y + len_sqrt_third], styles[1], styles[0]))
            # 2/3 of the way along the line, draw a new line at -60
            # degrees of length radius/3
            linearray.append(draw.line(
                [x + length * two_thirds, y], [x + length * two_thirds + len_third, y - len_sqrt_third], styles[1], styles[0]))
            depth -= 1
            length = len_third
            x = length * two_thirds
            y = len_sqrt_third
    return linearray


utils.print_params(DEFAULT)

svg_list = []
# fill svg_list with svg objects

center = [DEFAULT['DRAWABLE_AREA'][2] / 2, DEFAULT['DRAWABLE_AREA'][3] / 2]
# append snowflake to svg_list
snowflake_list = snowflake(center, 7, 100, 5, DEFAULT['STYLES'])
for line in snowflake_list:
    svg_list.append(line)

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)
