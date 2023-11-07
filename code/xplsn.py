#!/usr/bin/env python3

import random
import datetime
import sys
import math
# import re

##
A3 = (297, 420)
A4 = (210, 297)

DEFAULT_MAX_LINES = 3600
DEFAULT_MAX_CIRCLES = 30
# circle_radius = 30
DEFAULT_PAPER_SIZE = "A4"
DEFAULT_LANDSCAPE = True
DEFAULT_MINIMUM_RADIUS = 5
DEFAULT_RANDOM_AMOUNT = 0.5

# create a svg file caontaining a number of randomly placed and sized circles

inner_radius = 10
# outer_radius = (min(PAPER_SIZE[0], PAPER_SIZE[1]) / 2)
MAX_LINES = random.randint(3, DEFAULT_MAX_LINES)


# def usage():
#     print("usage: {} [paper size] [number of circles] [number of lines]".format(
#         sys.argv[0]))
#     print("paper size: A3 or A4, default is A4")
#     print("Landscape: Bool, default is{}".format(DEFAULT_LANDSCAPE))
#     print("number of circles: integer, default is{}".format(DEFAULT_MAX_CIRCLES))
#     print("number of lines: integer, default is{}".format(DEFAULT_MAX_LINES))
#     print("run with no arguments to use defaults")
#     print("example: {} A3 10 100".format(sys.argv[0]))
#     sys.exit(1)


# def parse_args():
#     """ parse commandline arguments:
#         return paper size, landscape, number of circles, number of lines
#         as a tuple.  If arg is missing, use defaults"""
#     # start with defaults, overwrite with commandline arguments
#     PAPER_SIZE = DEFAULT_PAPER_SIZE
#     LANDSCAPE = DEFAULT_LANDSCAPE
#     MAX_CIRCLES = DEFAULT_MAX_CIRCLES
#     MAX_LINES = DEFAULT_MAX_LINES
#     if len(sys.argv) == 1:
#         usage()
#         return (PAPER_SIZE, LANDSCAPE, MAX_CIRCLES, MAX_LINES)
#     # 1 arg: paper size
#     else:
#         integer_seen = False
#         for arg in sys.argv[1:]:
#             # if arg is a paper size, set paper size
#             if re.match(r"[aA][3-4]", arg):
#                 PAPER_SIZE = arg
#             # if arg is a boolean, set landscape
#             elif re.match(r"[tT][rR][uU][eE]", arg) or re.match(r"[fF][aA][lL][sS][eE]", arg):
#                 LANDSCAPE = arg
#             # first integer is number of circles
#             elif arg.isdigit() and not integer_seen:
#                 MAX_CIRCLES = int(arg)
#                 integer_seen = True
#             # second integer is number of lines
#             elif arg.isdigit() and integer_seen:
#                 MAX_LINES = int(arg)
#             else:
#                 usage()
#         return (PAPER_SIZE, LANDSCAPE, MAX_CIRCLES, MAX_LINES)


# def print_args(args):
#     print(" running with arguments:")
#     print(" paper size: {}".format(args[0]))
#     print(" landscape: {}".format(args[1]))
#     print(" number of circles: {}".format(args[2]))
#     print(" number of lines: {}".format(args[3]))


# PAGE SET UP ############


# def landscape(paper_size, is_landscape=False):
#     """Return the dimensions of a paper size in landscape mode"""
#     if is_landscape:
#         return (paper_size[1], paper_size[0])
#     else:
#         return paper_size


# def set_image_size(paper_size, bleed=5):
#     """ set the image size to the paper size minus the bleed"""
#     bleed_x = paper_size[0] * bleed / 100
#     bleed_y = paper_size[1] * bleed / 100
#     return (paper_size[0] - bleed_x, paper_size[1] - bleed_y)


# FILE NAME ############

# def get_script_name():
#     """return the name of the script without the path and without the
#     extension"""
#     if len(sys.argv) > 0:
#         script_name = sys.argv[0].split("/")[-1].split(".")[0]
#     elif len(sys.argv) == 0:
#         script_name = __file__.split("/")[-1].split(".")[0]
#     else:
#         script_name = "random_circles"
#     return script_name


# def filename():
#     """Return a filename with a timestamp"""
#     now = datetime.datetime.now()
#     suffix = now.strftime("%Y%m%d-%H%M%S")
#     default_file_prefix = get_script_name()
#     return default_file_prefix + "_" + suffix + ".svg"


# CIRCLE FUNCTIONS ############


# def set_outer_radius(paper_size, bleed=5):
#     """set the outer radius of the circle to the smaller dimension of the paper
#     size minus the bleed"""
#     return min(paper_size[0], paper_size[1]) / 2


def set_min_radius(circle_count, paper_size, min_radius=DEFAULT_MINIMUM_RADIUS):
    """the more circles requested, the smaller the minimum radius"""
    return max(int(min(paper_size[0], paper_size[1]) / circle_count), min_radius)


# SVG FUNCTIONS ############


# def get_svg_header(width, height):
#     header = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
#     <svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg" version="1.1">
#     """.format(width, height)
#     return header


# def draw_line(x1, y1, x2, y2, color="black", width=1):
#     line = '<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-{}="1" />\n'.format(
#         x1, y1, x2, y2, color, width)
#     return line

# draw a circle in the middle of the canvas of diameter inner_radius


# def draw_circle(x, y, radius, color="black", width=1, fill="none"):
#     circle = '<circle cx="{}" cy="{}" r="{}" stroke="{}" stroke-width="{}" fill="{}" />\n'.format(
#         x, y, radius, color, width, fill)
#     return circle


def remove_intersecting_circles(circles):
    # if x1, y1, r1 intersect y2, y2, r2, remove the smaller circle
    for circle in circles:
        x1, y1, r1 = circle
        for other_circle in circles:
            x2, y2, r2 = other_circle
            if circle != other_circle:
                distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
                if distance < r1 + r2:
                    if r1 < r2:
                        circles.remove(circle)
                    else:
                        circles.remove(other_circle)


def relation(viewbox):
    """Return a number between 0 and 1, depending on the distance of the point
    (x,y) from the center of the canvas"""
    distance = math.sqrt(
        (viewbox[0] - viewbox[2] / 2)**2 + (viewbox[1] - viewbox[3] / 2)**2)
    return distance / (viewbox[2] / 2)


# for each MAX_LINES, draw a line from the circumference of the inner circle to
# the circumference of the outer circle
lines = []


# def get_seed(amount):
#     """return a random number between 0 and 1, weighted by amount"""
#     return 1-(random.random()*amount)


# def place_lines(inner_radius, outer_radius, max_lines, randomness):
#     """places lines on the canvas.  randomness is a number between 0 and 1
#     that determines the angle of the line placement (0 is lines equally sapced,
#     1 is random)"""
#     for i in range(0, max_lines):
#         angle_seed = get_seed(randomness)
#         line_seed = get_seed(randomness)
#         angle = 2 * math.pi * MAX_LINES*angle_seed
#         # start position is on the circumference of the inner circle
#         x1 = inner_radius * math.cos(angle) + outer_radius
#         y1 = inner_radius * math.sin(angle) + outer_radius
#     # choose a random value between inner_radius and outer_radius
#         length = inner_radius + (outer_radius - inner_radius) * line_seed
#         x2 = length * math.cos(angle) + outer_radius
#         y2 = length * math.sin(angle) + outer_radius
#         lines.append(draw_line(x1, y1, x2, y2))



def build_circle_list(circle_count, canvas_size, relation):
    """build a list of circles with x, y, radius"""
    circles = []
    for i in range(0, circle_count):
        coords = []
        x = canvas_size[0] * random.random()
        y = canvas_size[1] * random.random()
        radius = circle_radius * relation(x, y) * random.random()
        coords = [x, y, radius]
        circles.append(coords)
    return circles


# render the svg file
filename = filename()
with open(filename, "w") as f:
    f.write(get_svg_header())
    for line in lines:
        f.write(line)
    for circle in circles:
        # remove intersecting circles
        remove_intersecting_circles(circles)
        f.write(draw_circle(circle[0], circle[1], circle[2], fill="white"))
    draw_circle(PAPER_SIZE[0] / 2, PAPER_SIZE[1] /
                2, inner_radius, fill="white")
    f.write("""</svg>""")
