#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import toml

# local libraries
import helpers/svg as svg
import helpers/draw as draw  # noqa: F401
import helpers/utils as utils

"""
    Skeleton file for new scripts
"""

# pylint: disable=duplicate-code

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

# LOCAL FUNCTIONS

svg_list = []
# fill svg_list with svg objects

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
