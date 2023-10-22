
import toml
import svg
from math import pi, cos, sin
import random

"""Skeleton for svg creation
"""

# Load config file
config = toml.load('config.toml')

# Paper sizes and pixels
A4 = config['paper_sizes']['A4']
A3 = config['paper_sizes']['A3']
ppmm = config['page']['pixels_per_mm']
bleed = config['page']['bleed']

# Stroke and fill colours
STROKE_COLOUR = config['colours']['stroke']
STROKE_WIDTH = ppmm
FILL_COLOUR = config['colours']['fill']
BACKGROUND_COLOUR = config['colours']['background']

# Default values
DEFAULT_SIZE = A3
DEFAULT_LANDSCAPE = True
DEFAULT_PPMM = ppmm

# Local variables
line_count = 250

# Functions


def set_circle(drawable_area):
    """ set the xy, radius for the largest circle that fits in drawable_area
        circle will be centred on both axes, and be 95% of the smallest
        drawable_area dimension
    """
    pos_x = (drawable_area[0] + drawable_area[2]) / 2
    pos_y = (drawable_area[1] + drawable_area[3]) / 2
    pos_xy = [pos_x, pos_y]
    radius = (min(drawable_area[2] - drawable_area[0],
                  drawable_area[3] - drawable_area[1]) * 0.95) / 2
    return (pos_xy, radius)


def random_point_on_circle(circle):
    """
        Return a random point on a circle.
        Args:
            circle (tuple): A tuple containing the xy position of the centre of
            the circle and the radius.
    """
    angle = random.uniform(0, 2 * pi)
    # print("angle: {}".format(angle))
    x = circle[0][0] + circle[1] * cos(angle)
    y = circle[0][1] + circle[1] * sin(angle)

    return (x, y)


def random_lines_circle(circle, line_count):
    """
        Draw a number of lines from one edge of a circle to the other.
    """
    line_list = []
    for i in range(line_count):
        # start at one edge of the circle
        start_xy = random_point_on_circle(circle)
        end_xy = random_point_on_circle(circle)
        line_list.append((start_xy, end_xy))
    return line_list


def draw_line(start_xy, end_xy, colour, width):
    """
        Draw a line from start_xy to end_xy
    """
    line = '<line x1="{}" y1="{}" x2="{}" y2="{}" '.format(
        start_xy[0], start_xy[1], end_xy[0], end_xy[1])
    line += 'stroke="{}" stroke-width="{}" />'.format(colour, width)
    return line


# Set up the SVG header
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, bleed)
svg_header = svg.svg_header(paper_size, drawable_area)
svg_footer = svg.svg_footer()
filename = svg.generate_filename()

# print paper_size
print("paper_size: {}".format(paper_size))
print("filename: {}".format(filename))

# Write the SVG file
svg_list = []
svg_list.append(svg_header)

# add your svg code here
circle = set_circle(drawable_area)
line_count = random.randint(int(line_count * 0.5), line_count)

print("circle radius: {}".format(circle[1]))
print("line count: {}".format(line_count))
line_list = random_lines_circle(circle, line_count)
for line in line_list:
    svg_list.append(draw_line(line[0], line[1], STROKE_COLOUR, STROKE_WIDTH))
svg_list.append(svg_footer)

# Write the SVG file
svg_file = open(filename, 'w')
svg_file.writelines(svg_list)
svg_file.close()
