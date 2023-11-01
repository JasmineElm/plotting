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

# LOCAL VARIABLES
DEFAULT_WALL_COUNT = 100


def set_wall_length(wall_count, drawable_area):
    """ set the length of the wall """
    return int(max(drawable_area[2], drawable_area[3]) / wall_count)


def set_type(emptiness=0.1):
    """ set the type of wall to draw """
    wall_bound = (1 - emptiness) / 2
    if random.random() < emptiness:
        return 0  # empty
    elif random.random() < wall_bound + emptiness:
        return 1  # horizontal
    else:
        return 2  # vertical


def generate_wall(x1, y1, length, type):
    """draw a line of Length starting at x1,y1
    Type = 0 none, 1 horizontal, 2 vertical
    return [x1, y1, x2, y2]
    """
    if type == 0:     # none
        x2 = x1
        y2 = y1
    elif type == 1:   # horizontal
        x2 = x1 + length
        y2 = y1
    else:             # vertical
        x2 = x1
        y2 = y1 + length
    return [x1, y1, x2, y2]


def build_maze(wall_count, drawable_area):
    """ build 2d array of walls """
    wall_length = set_wall_length(wall_count, drawable_area)
    maze = []
    for i in range(wall_count):
        maze.append([])
        for j in range(wall_count):
            maze[i].append([])
            maze[i][j] = generate_wall(
                i * wall_length, j * wall_length, wall_length, set_type())
    return maze


# create the output directory if it doesn't exist
utils.create_dir(out_dir)

# Set up the SVG header
paper_size = svg.set_image_size(DEFAULT_SIZE, DEFAULT_PPMM, DEFAULT_LANDSCAPE)
drawable_area = svg.set_drawable_area(paper_size, bleed)

filename = out_dir + utils.generate_filename()

# print paper_size
print("paper_size: {}".format(paper_size))
print("drawable_area: {}".format(drawable_area))
print("filename: {}".format(filename))


# draw the maze
maze = build_maze(DEFAULT_WALL_COUNT, drawable_area)
svg_list = []
for i in range(len(maze)):
    for j in range(len(maze[i])):
        svg_list.append(draw.line(maze[i][j][:2], maze[i][j][2:],
                                  STROKE_WIDTH, STROKE_COLOUR))
# svg_list.append(svg.svg_footer())

doc = svg.build_svg_file(paper_size, drawable_area, svg_list)
svg.write_file(filename, doc)
