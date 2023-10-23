import math
import random
import svg
import toml


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


# local variables
"""Put local variables here"""
iterations = 80  # number of lines to draw
quantize_step = ppmm * 10


# Functions
"""Put local functions here"""


def draw_line(coordinates, color, width):
    """Draw a line from coordinates[0], coordinates[1] to coordinates[2],
    coordinates[3]
    """
    svg_line = (
        f'<line x1="{coordinates[0]}" y1="{coordinates[1]}" '
        f'x2="{coordinates[2]}" y2="{coordinates[3]}" '
        f'stroke="{color}" stroke-width="{width}" />\n'
    )
    return svg_line


def quantize(value, step):
    """Quantize value to the nearest step
    """
    return int(math.floor(value / step) * step)+step


def always_right(drawable_area, iterations):
    """ draw a line that fits in the drawable area,
    rotate 90% clockwise and repeat for iterations
    returns a list of lists of coordinates
    """
    lines = []
    print("drawable_area: {}".format(drawable_area))
    print("iterations: {}".format(iterations))
    # start at the centre of the drawable area
    x = random.randint(drawable_area[0], drawable_area[2])
    y = random.randint(drawable_area[1], drawable_area[3])
    for iteration in range(1, iterations+1):
        if iteration % 4 == 1:  # X increases, y stays the same
            x2 = random.randint(x, drawable_area[2])
            lines.append([x, y, x2, y])
            x = x2
        elif iteration % 4 == 2:  # Y increases, x stays the same
            y2 = random.randint(y, drawable_area[3])
            lines.append([x, y, x, y2])
            y = y2
        elif iteration % 4 == 3:  # X decreases, y stays the same
            x2 = random.randint(drawable_area[0], x)
            lines.append([x, y, x2, y])
            x = x2
        elif iteration % 4 == 0:  # Y decreases, x stays the same
            y2 = random.randint(drawable_area[1], y)
            lines.append([x, y, x, y2])
            y = y2
    lines = [
        [
            quantize(x, quantize_step),
            quantize(y, quantize_step),
            quantize(x2, quantize_step),
            quantize(y2, quantize_step)
        ]
        for x, y, x2, y2 in lines
    ]
    return lines


# Set up the SVG header
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, bleed)

print("drawable_area: {}".format(drawable_area))

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
# reduce drawable area by quantize_step so the lines comfortably fit
drawable_area = (
    drawable_area[0] + quantize_step*2,
    drawable_area[1] + quantize_step*2,
    drawable_area[2] - quantize_step*2,
    drawable_area[3] - quantize_step*2
)

lines = always_right(drawable_area, iterations)
for line in lines:
    svg_list.append(draw_line(line, STROKE_COLOUR, STROKE_WIDTH))
svg_list.append(svg_footer)

# Write the SVG file
svg_file = open(filename, 'w')
svg_file.writelines(svg_list)
svg_file.close()
