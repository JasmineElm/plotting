#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import toml
# LOCAL MODULES
import svg   # Local module - functions to build svg files
import draw  # Local module - functions to draw svg objects

""" Skeleton script for creating svg files
    use this skeleton to quickly prototype svg creations
    the `draw` module contains functions to draw svg objects
    the `svg` module contains functions to create svg files"""

# Load config file
config = toml.load('config.toml')

# Stroke and fill colours
STROKE_COLOUR = config['colours']['stroke']
STROKE_WIDTH = config['page']['pixels_per_mm']
FILL_COLOUR = config['colours']['fill']
# Paper size, orientation, bleed
PAPER_SIZE = config['paper_sizes']['A3']
LANDSCAPE = True
PPMM = config['page']['pixels_per_mm']
BLEED = config['page']['bleed']

# local variables
"""Put local variables here"""

# Functions
"""Put local functions here"""

# Set up the SVG header
paper_size = svg.set_image_size(PAPER_SIZE, PPMM, LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, BLEED)
svg_header = svg.svg_header(paper_size, drawable_area)
svg_footer = svg.svg_footer()
filename = svg.generate_filename()

# print paper_size
print("paper_size: {}".format(paper_size))
print("drawable_area: {}".format(drawable_area))
print("filename: {}".format(filename))

# Write the SVG file
svg_list = []
svg_list.append(svg_header)
"""Add svg objects here"""

svg_list.append(svg_footer)

# Write the SVG file
svg_file = open(filename, 'w')
svg_file.writelines(svg_list)
svg_file.close()
