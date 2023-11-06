#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" build a maze using simple lines
"""

import random
import toml

# local libraries
from helpers import svg, utils, draw


# Load config file
config = toml.load('config.toml')

# Paper sizes and pixels
A4 = config['paper_sizes']['A4']
A3 = config['paper_sizes']['A3']
ppmm = config['page']['pixels_per_mm']
bleed = config['page']['bleed']

out_dir = config['directories']['output']

# Stroke and fill colours
STROKE_COLOUR = config['colours']['stroke']
STROKE_WIDTH = ppmm
FILL_COLOUR = config['colours']['fill']
BACKGROUND_COLOUR = config['colours']['background']

# Default values
DEFAULT_SIZE = A3
DEFAULT_LANDSCAPE = True
DEFAULT_PPMM = ppmm

# LOCAL VARIABLES
DEFAULT_WALL_COUNT = 100


def set_wall_length(wall_count, viewport):
    """ set the length of the wall """
    return int(max(viewport[2], viewport[3]) / wall_count)


def set_type(emptiness=0.1):
    """ set the type of wall to draw """
    wall_bound = (1 - emptiness) / 2
    wall_type = 2
    if random.random() < emptiness:
        wall_type = 0  # none
    if random.random() < wall_bound + emptiness:
        wall_type = 1  # horizontal
    # if random.random() > wall_bound + emptiness:
    return wall_type


def generate_wall(x1, y1, length, wall_type):
    """draw a line of Length starting at x1,y1
    Type = 0 none, 1 horizontal, 2 vertical
    return [x1, y1, x2, y2]
    """
    if wall_type == 0:     # none
        x2 = x1
        y2 = y1
    if wall_type == 1:   # horizontal
        x2 = x1 + length
        y2 = y1
    else:             # vertical
        x2 = x1
        y2 = y1 + length
    return [x1, y1, x2, y2]


def build_maze(wall_count, viewport):
    """ build 2d array of walls """
    wall_length = set_wall_length(wall_count, viewport)
    maze_def = []
    for row in range(wall_count):
        maze_def.append([])
        for column in range(wall_count):
            maze_def[row].append([])
            maze_def[row][column] = generate_wall(
                row * wall_length, column *
                wall_length, wall_length, set_type())
    return maze_def


# create the output directory if it doesn't exist
utils.create_dir(out_dir)

# Set file parameters
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, bleed)
filename = out_dir + utils.generate_filename()

utils.print_params({"paper_size": paper_size,
                    "drawable_area": drawable_area,
                    "filename": filename,
                    "wall count": DEFAULT_WALL_COUNT})


# draw the maze
maze = build_maze(DEFAULT_WALL_COUNT, drawable_area)
svg_list = []
for i, section in enumerate(maze):
    for j, wall in enumerate(section):
        svg_list.append(draw.line(wall[:2], wall[2:], STROKE_WIDTH,
                                  STROKE_COLOUR))

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
