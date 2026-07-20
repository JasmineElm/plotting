#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
"""
import random
import math
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


def set_particles(count, pos_xy, radius):
    """
    Generate a list of particle positions within a given radius around
    a center point.

    Args:
        count (int): The number of particles to generate.
        pos_xy (list): The x and y coordinates of the center point.
        radius (float): The radius within which the particles should
        be generated.

    Returns:
        list: A list of particle positions, each represented as a
        list of x and y coordinates.
    """
    inner_circle = radius / 2
    return [[pos_xy[0] + random.uniform(inner_circle, radius) * math.cos(math.radians(random.uniform(0, 360))),
             pos_xy[1] + random.uniform(inner_circle, radius) * math.sin(math.radians(random.uniform(0, 360)))]
            for _ in range(count)]


def barnsley_fern(pos_xy, iterations):
    """
    Generate points for plotting the Barnsley Fern fractal.

    Parameters:
    pos_xy (tuple): The initial position (x, y) of the point.
    iterations (int): The number of iterations to generate points.

    Returns:
    list: A list of points representing the Barnsley Fern fractal.
    """
    points = []
    # defaults:

    x, y = pos_xy
    for _ in range(iterations):
        r = random.uniform(0, 100)
        if r < 1:
            x, y = 0, 0.16 * y
        elif r < 86:
            x, y = 0.85 * x + 0.04 * y, -0.04 * x + 0.85 * y + 1.6
        elif r < 93:
            x, y = 0.2 * x - 0.26 * y, 0.23 * x + 0.22 * y + 1.6
        else:
            x, y = -0.15 * x + 0.28 * y, 0.26 * x + 0.24 * y + 0.44
        points.append([x, y])
    return points


def points_to_compound_path(points_list):
    """ convert a list of points to a compound path """
    path = "M "
    for point in points_list:
        path += str(point[0]) + " " + str(point[1]) + " "
    path += "Z"
    stroke = f"stroke='{DEFAULT['STYLES'][0]}' stroke-width='{DEFAULT['STYLES'][1]}'"
    fill = f"fill='{DEFAULT['STYLES'][2]}'"
    return f"<path d='{path}' {stroke} {fill} />\n"

def fit_points_to_area(points, drawable_area):
    """ Scales and translates points to fit within the drawable area """
    min_x = min(p[0] for p in points)
    max_x = max(p[0] for p in points)
    min_y = min(p[1] for p in points)
    max_y = max(p[1] for p in points)

    range_x = max_x - min_x
    range_y = max_y - min_y

    target_min_x, target_min_y, target_max_x, target_max_y = drawable_area
    target_width = target_max_x - target_min_x
    target_height = target_max_y - target_min_y

    scale_x = target_width / range_x if range_x > 0 else 1
    scale_y = target_height / range_y if range_y > 0 else 1
    scale = min(scale_x, scale_y) * 0.9  # 10% padding

    offset_x = target_min_x + (target_width - range_x * scale) / 2
    offset_y = target_min_y + (target_height - range_y * scale) / 2

    fitted_points = []
    for x, y in points:
        new_x = offset_x + (x - min_x) * scale
        new_y = offset_y + (max_y - y) * scale # invert y for SVG coordinate system
        fitted_points.append([round(new_x, 2), round(new_y, 2)])
    return fitted_points


utils.print_params(DEFAULT)

svg_list = []
centre = [DEFAULT['DRAWABLE_AREA'][1], DEFAULT['DRAWABLE_AREA'][2]]

points_list = barnsley_fern(centre, 5000)
points_list = fit_points_to_area(points_list, DEFAULT['DRAWABLE_AREA'])
# draw the fern
svg_list.append(points_to_compound_path(points_list))

doc = svg.build_svg_file(
    DEFAULT['PAPER_SIZE'], DEFAULT['DRAWABLE_AREA'], svg_list)
svg.write_file(DEFAULT['FILENAME'], doc)
