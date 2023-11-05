#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import toml
from math import pi, cos, sin

# local libraries
import helpers/svg as svg
import helpers/draw as draw  # noqa: F401
import helpers/utils as utils

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

# LOCAL VARIABLES
line_count = 250

# LOCAL FUNCTIONS


def set_circle(drawable_area):
    """ set the xy, radius for the largest circle that fits in drawable_area
        circle will be centred on both axes, and be 95% of the smallest
        drawable_area dimension
    """
    pos_x = (drawable_area[0] + drawable_area[2]) / 2
    pos_y = (drawable_area[1] + drawable_area[3]) / 2
    pos_xy = [pos_x, pos_y]
    radius = (min(drawable_area[2] - drawable_area[0],
                  drawable_area[3] - drawable_area[1]) * 0.95) / 2
    return (pos_xy, radius)


def random_point_on_circle(circle):
    """
        Return a random point on a circle.
        Args:
            circle (tuple): A tuple containing the xy position of the centre of
            the circle and the radius.
    """
    angle = random.uniform(0, 2 * pi)
    # print("angle: {}".format(angle))
    x = circle[0][0] + circle[1] * cos(angle)
    y = circle[0][1] + circle[1] * sin(angle)

    return (x, y)


def random_lines_circle(circle, line_count):
    """
        Draw a number of lines from one edge of a circle to the other.
    """
    line_list = []
    for i in range(line_count):
        # start at one edge of the circle
        start_xy = random_point_on_circle(circle)
        end_xy = random_point_on_circle(circle)
        line_list.append((start_xy, end_xy))
    return line_list


# add your svg code here
circle = set_circle(drawable_area)
line_count = random.randint(int(line_count * 0.5), line_count)

svg_list = []
# fill svg_list with svg objects
circle = set_circle(drawable_area)
line_count = random.randint(int(line_count * 0.5), line_count)

print("circle radius: {}".format(circle[1]))
print("line count: {}".format(line_count))
# line_list = random_lines_circle(circle, line_count)
for line in random_lines_circle(circle, line_count):
    svg_list.append(draw.line(line[0], line[1], STROKE_WIDTH, STROKE_COLOUR))

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)

