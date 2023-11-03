#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import random
import toml

# local libraries
import svg
import draw  # noqa: F401
import utils

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
NOISE = 0.05
CIRCLE_COUNT = 80
# LOCAL FUNCTIONS


def calculate_max_radius(drawable_area):
    """
    Calculates the maximum radius that can be used for concentric circles on a
    canvas of the given size.

    Args:
      drawable_area (tuple): A tuple containing the width and height of the
      canvas.

    Returns:
      int: The maximum radius that can be used for concentric circles on the
      canvas.
    """
    return min(drawable_area[3] - drawable_area[1],
               drawable_area[2] - drawable_area[0]) * 0.45


def weighted_random(weight):
    """ """
    return random.random()*weight


def skew_centre(drawable_area):
    """Returns a tuple with the coordinates of the centre of the canvas,
    skewed by a random amount.

    Args:
      drawable_area [list]: list of min_x, min_y, max_x, max_y

    Returns:
      tuple: A tuple with the x and y coordinates of the skewed centre of the
      canvas.
    """
    skewed_x = drawable_area[0] + \
        (drawable_area[2] - drawable_area[0]) * (1+weighted_random(NOISE)) / 2
    skewed_y = drawable_area[1] + \
        (drawable_area[3] - drawable_area[1]) * (1+weighted_random(NOISE)) / 2
    return (int(skewed_x), int(skewed_y))


def generate_circle_list(drawable_area, circle_count):
    """
    Generate a list of circle radii.

    Args:
      paper_size (tuple): The size of the paper to draw on.
      circle_count (int): The number of circles to generate.

    Returns:
      list: A list of circle radii.

    """
    max_radius = calculate_max_radius(drawable_area)
    circle_list = []
    for i in range(circle_count):
        circle = int(max_radius * ((i+i*weighted_random(NOISE))
                                   / circle_count))
        if circle < max_radius:
            circle_list.append(circle)
        else:
            circle_list.append(max_radius)
            
    return circle_list


svg_list = []
# fill svg_list with svg objects
for i in generate_circle_list(drawable_area, CIRCLE_COUNT):
    skew_x, skew_y = skew_centre(drawable_area)
    svg_list.append(draw.circle(skew_x, skew_y, i, STROKE_COLOUR,
                                STROKE_WIDTH, FILL_COLOUR))

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
