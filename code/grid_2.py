#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
"""
import math
import random
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

# LOCAL FUNCTIONS


def circle_outside_viewbox(viewbox, circle_list):
    """ if all points in circle_list are outside viewbox return True 
        x = viewbox[0] and x = viewbox[2] are the left and right edges
        y = viewbox[1] and y = viewbox[3] are the top and bottom edges
        points are [x, y] pairs
    """
    for point in circle_list:
        if point[0] > viewbox[0] and point[0] < viewbox[2]:
            if point[1] > viewbox[1] and point[1] < viewbox[3]:
                return True


def set_circle(pos_xy, radius, points, noise=0.5):
    """ set points on a circle of radius at pos_xy """
    # points are set by 360/points +/- (noise *(360/points))
    points_list = []
    for i in range(points):
        angle = (360/points) * i
        angle += random.uniform(-noise, noise) * (360/points)
        x = pos_xy[0] + radius * math.cos(math.radians(angle))
        y = pos_xy[1] + radius * math.sin(math.radians(angle))
        points_list.append([x, y])
    return points_list


def set_circular_grid(viewbox, centre_xy, size, noise=0.1):
    """Set circular grid using concentric circles"""
    in_viewbox = True
    points_list = []
    points = 2
    while in_viewbox:
        size = size + math.sqrt(size)
        points = points + 1
        circle = set_circle(centre_xy, size, points, noise)
        in_viewbox = circle_outside_viewbox(viewbox, circle)
        points_list.extend(circle)
    return points_list


utils.print_params(DEFAULT)

svg_list = []
# fill svg_list with svg objects
points_centre = svg.get_centre(DEFAULT['DRAWABLE_AREA'])
coord_list = set_circular_grid(DEFAULT['DRAWABLE_AREA'],
                               points_centre, 80, 0.91)
line_list = []
for circle in coord_list:
    nodes = svg.get_neighbours(circle, coord_list, 400)
    line_list += svg.join_points(circle, nodes, "horizontal", 0.99, 5)
    line_list += svg.join_points(circle, nodes, "vertical", 0.95, 5)

for line in line_list:
    svg_list.append(draw.line(line[0], line[1],
                              DEFAULT['STYLES'][1],
                              DEFAULT['STYLES'][0]))
doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)
