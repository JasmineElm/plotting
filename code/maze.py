import sys
import datetime
import random
# create svg file of concentric circles using python
A4 = (210, 297)
A3 = (297, 420)
ppmm = 5  # pixels per mm

STROKE_COLOUR = "black"
STROKE_WIDTH = ppmm


DEFAULT_PAPER_SIZE = A3
DEFAULT_LANDSCAPE = True
DEFAULT_WALL_COUNT = 80
DEFAULT_PIXELS_PER_MM = ppmm


def set_landscape(paper_size, landscape):
    """
    Sets the landscape orientation of a paper size.

    Args:
      paper_size (tuple): A tuple containing the dimensions of the paper size
      in the form (width, height).
      landscape (bool): A boolean value indicating whether the paper should be
      in landscape orientation.

    Returns:
      tuple: A tuple containing the dimensions of the paper size in the form
      (width, height), with the dimensions swapped if landscape is True.
    """
    if landscape:
        return (paper_size[1], paper_size[0])
    else:
        return paper_size


def set_image_size(paper_size, ppmm):
    """
    Calculates the size of the image in pixels based on the paper size and
    pixels per millimeter.

    Args:
      paper_size (tuple): A tuple containing the width and height of the paper
      in millimeters.
      ppmm (float): The number of pixels per millimeter.

    Returns:
      tuple: A tuple containing the width and height of the image in pixels.
    """
    return (int(paper_size[0] * ppmm), int(paper_size[1] * ppmm))


def set_canvas_size(image_size):
    """
    Calculates the size of the canvas for concentric circles based on the
    given image size.

    Args:
      image_size (tuple): A tuple containing the width and height of the image.

    Returns:
      tuple: A tuple containing the width and height of the canvas for
      concentric circles.
    """
    return (int(image_size[0] * 0.95), int(image_size[1] * 0.95))


def centre_canvas(paper_size, canvas_size):
    """ centre the canvas on the page """
    pos_x = int((paper_size[0] - canvas_size[0]) / 2)
    pos_y = int((paper_size[1] - canvas_size[1]) / 2)
    return (pos_x, pos_y)


def svg_header(paper_size, canvas_size):
    """
    Returns an SVG header string with the specified paper and canvas sizes.

    Args:
      paper_size (tuple): A tuple containing the width and height of the paper.
      canvas_size (tuple): A tuple containing the width and height of the
      canvas.

    Returns:
      str: An SVG header string with the specified paper and canvas sizes.
    """
    offset_x, offset_y = centre_canvas(paper_size, canvas_size)
    xml1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
    xml2 = """<svg width="{}" height="{}" viewBox="{} {} {} {}" """.format(
        paper_size[0], paper_size[1],
        offset_x, offset_y, canvas_size[0], canvas_size[1])
    xml3 = """xmlns="http://www.w3.org/2000/svg" version="1.1">"""
    return xml1 + "\n" + xml2 + "\n" + xml3 + "\n"


def svg_footer():
    return "</svg>"


def set_wall_length(wall_count, canvas_size):
    """ set the length of the walls
    Wall length = Min(canvas_size[0], canvas_size[1]) / wall_count """
    return int(max(canvas_size[0], canvas_size[1]) / wall_count)


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


def draw_wall(x1, y1, x2, y2, canvas_size):
    """draw a line of Length starting at x1,y1
    return [x1, y1, x2, y2]
    """
    # if any point is outside the canvas, don't draw
    if x1 < 0 or x1 > canvas_size[0] or y1 < 0 or y1 > canvas_size[1]:
        return ""
    start_pos = """<line x1="{}" y1="{}" """.format(x1, y1)
    end_pos = """x2="{}" y2="{}" """.format(x2, y2)
    style = """stroke="{}" stroke-width="{}" />""".format(
        STROKE_COLOUR, STROKE_WIDTH)
    return start_pos + end_pos + style + "\n"


def build_maze(wall_count, canvas_size):
    """ build 2d array of walls """
    wall_length = set_wall_length(wall_count, canvas_size)
    maze = []
    for i in range(wall_count):
        maze.append([])
        for j in range(wall_count):
            maze[i].append([])
            maze[i][j] = generate_wall(
                i * wall_length, j * wall_length, wall_length, set_type())
    return maze


def generate_filename():
    """Generates a filename for the SVG file based on the name of the script,
    the current date, and the current time.

    Returns:
      str: The filename in the format "<name of script>_<date>_<time>.svg".
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    return "{}_{}.svg".format(sys.argv[0], timestamp)


def write_svg_file(filename, svg_list):
    """
    Write an array of SVG lines to a file.

    Args:
      filename (str): The name of the file to write to.
      svg_list (list): A list of strings representing SVG lines.

    Returns:
      None
    """
    with open(filename, "w") as f:
        for line in svg_list:
            f.write(line)
# main ###


def create_svg_list(paper_size, circle_count):
    """
    Create a list of SVG elements representing concentric circles.

    Args:
      paper_size (tuple): A tuple of two integers representing the width and
      height of the paper in millimeters.
      circle_count (int): The number of concentric circles to draw.

    Returns:
      list: A list of SVG elements representing the concentric circles.
    """
    image_size = set_image_size(paper_size, ppmm)
    canvas_size = set_canvas_size(image_size)
    svg_list = []
    svg_list.append(svg_header(image_size, canvas_size))
    # draw the maze
    maze = build_maze(DEFAULT_WALL_COUNT, canvas_size)
    for i in range(DEFAULT_WALL_COUNT):
        for j in range(DEFAULT_WALL_COUNT):
            svg_list.append(draw_wall(
                maze[i][j][0], maze[i][j][1], maze[i][j][2], maze[i][j][3],
                canvas_size))

    svg_list.append(svg_footer())
    return svg_list


def main():
    file_name = generate_filename()
    paper_size = set_image_size(DEFAULT_PAPER_SIZE, DEFAULT_PIXELS_PER_MM)
    paper_size = set_landscape(paper_size, DEFAULT_LANDSCAPE)
    svg_list = create_svg_list(
        paper_size, DEFAULT_WALL_COUNT)
    write_svg_file(file_name, svg_list)


if __name__ == "__main__":
    main()
