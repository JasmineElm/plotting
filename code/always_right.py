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
"""Put local variables here
"""
iterations = 30 # number of lines to draw
quantize_step = 30 
# Functions
"""Put local functions here
"""


def draw_line(coordinates, color, width):
    """Draw a line from coordinates[0], coordinates[1] to coordinates[2],
    coordinates[3]
    """
    svg_line = """<line x1="{}" y1="{}" x2="{}" y2="{}" stroke="{}" stroke-width="{}" />\n""".format(
        coordinates[0], coordinates[1], coordinates[2], coordinates[3], color, width)
    return svg_line


def quantize(value, step):
    """Quantize value to the nearest step
    """
    return int(round(value / step) * step)


def always_right(drawable_area, iterations):
    """ draw a line that fits in the drawable area,
    rotate 90% clockwise and repeat for iterations
    returns a list of lists of coordinates
    """
    lines = []
    print("drawable_area: {}".format(drawable_area))
    print("iterations: {}".format(iterations))
    #start at the centre of the drawable area
    x = drawable_area[0] + (drawable_area[2] - drawable_area[0]) / 2
    y = drawable_area[1] + (drawable_area[3] - drawable_area[1]) / 2
    centre = [x, y]
    for iteration in range(1, iterations+1):
        if iteration %4 == 1:   # X increases, y stays the same
            x2 = random.randint(x, drawable_area[2])
            lines.append([x, y, x2, y])
            x = x2
        elif iteration %4 == 2: # Y increases, x stays the same
            y2 = random.randint(y, drawable_area[3])
            lines.append([x, y, x, y2])
            y = y2
        elif iteration %4 == 3: # X decreases, y stays the same
            x2 = random.randint(drawable_area[0], x)
            lines.append([x, y, x2, y])
            x = x2
        elif iteration %4 == 0: # Y decreases, x stays the same
            y2 = random.randint(drawable_area[1], y)
            lines.append([x, y, x, y2])
            y = y2
    # join the first x, y to the last x2, y2 using lines and 90% rotation/s
    # quantize the coordinates to the nearest quantize_step using a lambda
    # function
    # join the first and last coordinates using a horizontal and vertial line
    lines.append([lines[0][0], lines[0][1], lines[iterations-1][0], lines[0][1]])
    lines.append([lines[iterations-1][0], lines[iterations-1][1], lines[iterations-1][0], lines[iterations-1][1]])
    lines = [[quantize(x, quantize_step), quantize(y, quantize_step),
              quantize(x2, quantize_step), quantize(y2, quantize_step)]
             for x, y, x2, y2 in lines]
    return lines

        

# Set up the SVG header
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, bleed)
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
# add your svg code here
lines = always_right(drawable_area, iterations)
for line in lines:
    svg_list.append(draw_line(line, STROKE_COLOUR, STROKE_WIDTH))
svg_list.append(svg_footer)

# Write the SVG file
svg_file = open(filename, 'w')
svg_file.writelines(svg_list)
svg_file.close()
