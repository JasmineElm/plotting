import random
import toml

# local imports
import helpers/draw as draw
import helpers/svg as svg
import helpers/utils as utils

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
STROKE_WIDTH = config['stroke']['width']
FILL_COLOUR = config['colours']['fill']
BACKGROUND_COLOUR = config['colours']['background']

# Default values
DEFAULT_SIZE = A3
DEFAULT_LANDSCAPE = True
DEFAULT_PPMM = ppmm

# local variables
iterations = 100
boxes_per_iteration = 100 

# boxes follow a fibonacci sequence
fibonacci = [1, 2, 3, 5, 8, 13, 21]
# multiplier for box_size_list
multiplier = ppmm
box_size_list = [x * multiplier for x in fibonacci]


def set_box_list(drawable_area, box_size_list, iterations, box_per_iteration):
    """ return a list of boxes """
    # print params
    print("drawable_area: {}".format(drawable_area))
    print("box_size_list: {}".format(box_size_list))
    print("iterations: {}".format(iterations))
    print("boxes_per_iteration: {}".format(box_per_iteration))
    boxes = []
    for i in range(1, iterations+1):
        # iterations
        for j in range(1, box_per_iteration+1):
            # boxes per iteration
            box_size = random.choice(box_size_list[1:])
            # count down from iterations*boxes_per_iteration
            boxes_left = iterations*box_per_iteration - i*j
            print("boxes left: {}".format(boxes_left))
            box_x = random.randint(drawable_area[0],
                                   drawable_area[2] - box_size)
            box_y = random.randint(drawable_area[1],
                                   drawable_area[3] - box_size)
            # quantize box_x and box_y to box_size_list[0]
            # box_x = box_x - (box_x % box_size_list[0])
            # box_y = box_y - (box_y % box_size_list[0])
            # boxes cannot any other box + box_size_list[0] in any direction
            if not any(box_x < x[0] + x[2] and box_x + box_size > x[0] and
                       box_y < x[1] + x[2] and box_y + box_size > x[1]
                       for x in boxes):
                boxes.append([box_x, box_y, box_size])
            boxes = [x for x in boxes if not (x[0] < drawable_area[0] or
                                              x[0] + x[2] > drawable_area[2]
                                              or x[1] < drawable_area[1] or
                                              x[1] + x[2] > drawable_area[3]
                                              )]
    for box in boxes:
        box[2] = box[2] - box_size_list[0]
    boxes.sort(key=lambda x: (x[0], x[1], x[2]))
    return boxes


def create_svg_list(drawable_area, stroke_colour, stroke_width, fill_colour):

    svg_list = []
    boxes = set_box_list(drawable_area, box_size_list, iterations,
                         boxes_per_iteration)
    for box in boxes:
        svg_list.append(draw.box(box[:2], box[2], stroke_colour,
                                 stroke_width, fill_colour))
    return svg_list


# Set up the SVG header
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, bleed)
print("paper_size: {}".format(paper_size))
print("drawable_area: {}".format(drawable_area))

filename = out_dir + utils.generate_filename()

svg_list = []
svg_list.append(svg.svg_header(paper_size, drawable_area))
# svg_list.append(svg.set_background(drawable_area, BACKGROUND_COLOUR))
for item in create_svg_list(drawable_area, STROKE_COLOUR,
                            STROKE_WIDTH, FILL_COLOUR):
    svg_list.append(item)
svg_list.append(svg.svg_footer())

svg.write_file(filename, svg_list)
