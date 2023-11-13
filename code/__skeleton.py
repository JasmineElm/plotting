#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Skeleton file for new scripts
"""
import toml

# local libraries
from helpers import svg, utils, draw  # pylint: disable=import-error


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

# LOCAL FUNCTIONS


utils.print_params(
    {"paper_size": paper_size,
     "drawable_area": drawable_area,
     "filename": filename}
)

svg_list = []
# fill svg_list with svg objects

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
