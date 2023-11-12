#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
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

STYLES = [config["colours"]["stroke"],
          config["page"]["pixels_per_mm"],
          config["colours"]["fill"]]

# set paper size, drawable area, filename
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, DEFAULT_BLEED)
# set filename, creating output directory if necessary
filename = utils.create_dir(DEFAULT_OUTPUT_DIR) + utils.generate_filename()


# LOCAL VARIABLES


def generate_square_grid(canvas, grid_size, noise=0.05):
    """return a list of points that fit within the grid
        grid begins at canvas[0] + grid_size, canvas[1] + grid_size
        grid ends at canvas[2] - grid_size, canvas[3] - grid_size
        noise is a percentage of the grid_size"""
    return [(x + random.uniform(-grid_size * noise, grid_size * noise),
             y + random.uniform(-grid_size * noise, grid_size * noise))
            for x in range(canvas[0] + grid_size,
                           canvas[2] - grid_size, grid_size)
            for y in range(canvas[1] + grid_size,
                           canvas[3] - grid_size, grid_size)]


def get_neighbours(point, grid, radius):
    """return a list of points within radius of point"""
    return [p for p in grid if (point[0] - radius <= p[0] <= point[0] + radius
                                and point[1] - radius <=
                                p[1] <= point[1] + radius)]


def get_relationships(start_xy, end_xy, diag_def=3):
    """determine direction between end_xy and start_xy"""
    diff_x = end_xy[0] - start_xy[0]
    diff_y = end_xy[1] - start_xy[1]
    abs_diff_x = abs(diff_x)
    abs_diff_y = abs(diff_y)
    diag_x = diff_x / diag_def
    diag_y = diff_y / diag_def
    mode = ""
    # if diff_x > diff_y and diff Y < 1/3 diff_x, hotioontal
    if abs_diff_x > abs_diff_y and abs_diff_y < abs(diag_x):
        mode = "horizontal"
    # if diff_y > diff_x and diff_x < 1/3 diff_y, vertical
    if abs_diff_y > abs_diff_x and abs_diff_x < abs(diag_y):
        mode = "vertical"
    if diff_x > 0:
        if diff_y > 0:
            mode = "diagonal_down"
        else:
            mode = "diagonal_up"
    return mode


def join_points(point, neighbours, direction, sparseness=0.5):
    """return tuples of [start, end] points for each neighbour
    direction sets the direction of the line; horizontal, vertical, diagonal
    sparseness is whether to return all points or a subset"""
    # filter neighbours by direction
    neighbours = [n for n in neighbours
                  if get_relationships(point, n) == direction]
    # filter this list by sparseness
    neighbours = [n for n in neighbours if random.random() > sparseness]
    # return a list of tuples of [start, end] points
    return [[point, n] for n in neighbours]


utils.print_params(
    {"paper_size": paper_size,
     "drawable_area": drawable_area,
     "filename": filename}
)

# fill svg_list with svg objects
coord_list = generate_square_grid(drawable_area, 100, 0.5)
svg_list = []
line_list = []
for coord in coord_list:
    nodes = get_neighbours(coord, coord_list, 400)
    line_list += join_points(coord, nodes, "diagonal_up", 0.95)
    line_list += join_points(coord, nodes, "diagonal_down", 0.95)
    line_list += join_points(coord, nodes, "horizontal", 0.95)
    line_list += join_points(coord, nodes, "vertical", 0.95)
    # draw a circle at each point
    # svg_list.append(draw.circle(point[0], point[1], 2, STYLES))
for line in line_list:
    svg_list.append(draw.line(line[0], line[1],
                              STYLES[1], STYLES[0]))

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
