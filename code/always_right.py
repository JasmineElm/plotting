# Description: Draw a line that fits in the drawable area,
import random
import toml

# local libraries
import svg
import draw
import utils


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


# local variables
"""Put local variables here"""
iterations = 80  # number of lines to draw
quantize_step = ppmm * 10


# Functions


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
            (utils.quantize(x, quantize_step),
             utils.quantize(y, quantize_step)),
            (utils.quantize(x2, quantize_step),
             utils.quantize(y2, quantize_step))
        ]
        for x, y, x2, y2 in lines
    ]
    return lines


# create the output directory if it doesn't exist
utils.create_dir(out_dir)

# Set up the SVG header
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, bleed)

print("drawable_area: {}".format(drawable_area))

svg_header = svg.svg_header(paper_size, drawable_area)
svg_footer = svg.svg_footer()

filename = out_dir + utils.generate_filename()

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
    print("line: {}".format(line))
    print("line[:1]: {}".format(line[:2]))
    print("line[1:]: {}".format(line[2:]))
    svg_list.append(draw.line(line[0], line[1], STROKE_WIDTH, STROKE_COLOUR))
svg_list.append(svg_footer)

# Write the SVG file
svg_file = open(filename, 'w')
svg_file.writelines(svg_list)
svg_file.close()
