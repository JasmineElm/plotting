#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" fill a canvas with boxes of (defined) random sizes"""
import random
import os
import tomllib

# local libraries
from helpers import svg, utils, draw

# Load config file
config_path = os.path.join(os.path.dirname(__file__), "config.toml")
with open(config_path, "rb") as f:
    config = tomllib.load(f)

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
STYLES = [STROKE_COLOUR, STROKE_WIDTH, FILL_COLOUR]

paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, DEFAULT_BLEED)
# set filename, creating output directory if necessary
filename = utils.create_dir(DEFAULT_OUTPUT_DIR) + utils.generate_filename()


# local variables
ITERATIONS = 100
BOXES_PER_ITERATION = 100

# boxes follow a fibonacci sequence
FIBONACCI_LENGTH = 10
FIBONACCI = utils.get_fibonacci_list(FIBONACCI_LENGTH)

# multiplier for box_size_list
multiplier = DEFAULT_PPMM
box_size_list = [x * multiplier for x in FIBONACCI]

utils.print_params({"paper_size": paper_size,
                    "drawable_area": drawable_area,
                    "filename": filename,
                    "iterations": ITERATIONS,
                    "boxes_per_iteration": BOXES_PER_ITERATION,
                    "box_size_list": box_size_list})


def set_box_list(viewbox, list_of_box_sizes, iterations, box_per_iteration):
    """ return a list of boxes """
    # print params
    boxes = []
    pct_complete = 0
    boxes_total = iterations * box_per_iteration
    for i in range(1, iterations+1):
        # iterations
        for j in range(1, box_per_iteration+1):
            # boxes per iteration
            box_size = random.choice(list_of_box_sizes[1:])
            # count down from iterations*boxes_per_iteration
            boxes_processed = (i - 1) * box_per_iteration + j
            pct_complete = utils.print_pct_complete(boxes_processed,
                                                    boxes_total,
                                                    pct_complete)
            box_x = random.randint(viewbox[0],
                                   viewbox[2] - box_size)
            box_y = random.randint(viewbox[1],
                                   viewbox[3] - box_size)
            if not any(box_x < x[0] + x[2] and box_x + box_size > x[0] and
                       box_y < x[1] + x[2] and box_y + box_size > x[1]
                       for x in boxes):
                boxes.append([box_x, box_y, box_size])
    for box in boxes:
        box[2] = box[2] - list_of_box_sizes[0]
    boxes.sort(key=lambda x: (x[0], x[1], x[2]))
    return boxes


def create_svg_list(viewbox, styles, box_size_list):
    """ return a list of svg elements """
    temp_svg_list = []
    boxes = set_box_list(viewbox, box_size_list, ITERATIONS,
                         BOXES_PER_ITERATION)
    for box in boxes:
        temp_svg_list.append(draw.box(box[:2], box[2], styles))
    return temp_svg_list


svg_list = []
svg_list.append(svg.svg_header(paper_size, drawable_area))
# svg_list.append(svg.set_background(drawable_area, BACKGROUND_COLOUR))
for item in create_svg_list(drawable_area, STYLES, box_size_list):
    svg_list.append(item)
svg_list.append(svg.svg_footer())

svg.write_file(filename, svg_list)
