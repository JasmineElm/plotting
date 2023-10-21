import sys
import datetime
import random

# Paper sizes and pixels
A4 = (210, 297)
A3 = (297, 420)
ppmm = 5  # pixels per mm

# Stroke and fill colours
STROKE_COLOUR = "black"
STROKE_WIDTH = ppmm
FILL_COLOUR = "none"
BACKGROUND_COLOUR = "blue"


# Default values
DEFAULT_PAPER_SIZE = A3
DEFAULT_LANDSCAPE = True
DEFAULT_PIXELS_PER_MM = ppmm

iterations = 100
boxes_per_iteration = iterations * 10

# boxes follow a fibonacci sequence
fibonacci = [0.3, 1, 2, 3, 5, 8, 13]
# multiplier for box_size_list
multiplier = 50
box_size_list = [x * multiplier for x in fibonacci]


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


def set_viewbox(paper_size, canvas_size):
    """ centre the canvas on the page """
    pos_x = int((paper_size[0] - canvas_size[0]) / 2)
    pos_y = int((paper_size[1] - canvas_size[1]) / 2)
    return (pos_x, pos_y)


def set_background(paper_size, background_colour):
    """
    Returns an SVG element representing the background of the image.

    Args:
      paper_size (tuple): A tuple containing the width and height of the paper
      in millimeters.
      background_colour (str): A string representing the background colour.

    Returns:
      str: An SVG element representing the background of the image.
    """
    return """<rect width="{}mm" height="{}mm" fill="{}" />""".format(
        paper_size[0], paper_size[1], background_colour)


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
    offset_x, offset_y = set_viewbox(paper_size, canvas_size)
    xml1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
    xml2 = """<svg width="{}" height="{}" viewBox="{} {} {} {}" """.format(
        paper_size[0], paper_size[1],
        offset_x, offset_y, canvas_size[0], canvas_size[1])
    xml3 = """xmlns="http://www.w3.org/2000/svg" version="1.1">"""
    return xml1 + "\n" + xml2 + "\n" + xml3 + "\n"


def svg_footer():
    return "</svg>"


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


def set_box_size(box_size_list):
    """ return a random box size from the list, not including box_size_list[0] """
    return random.choice(box_size_list[1:])


def set_box_list(canvas_size, box_size_list, image_size, iterations, boxes_per_iteration):
    """ return a list of boxes """
    boxes = []
    viewbox = set_viewbox(image_size, canvas_size)
    viewbox = viewbox + canvas_size
    print("paper_size: {}".format(image_size))
    print("canvas_size: {}".format(canvas_size))
    print("viewbox: {}".format(viewbox))

    for i in range(iterations):
        # iterations
        for j in range(boxes_per_iteration):
            # boxes per iteration
            box_size = set_box_size(box_size_list)
            box_x = random.randint(0, canvas_size[0] - box_size)
            box_y = random.randint(0, canvas_size[1] - box_size)
            # quantize box_x and box_y to box_size_list[0]
            # box_x = box_x - (box_x % box_size_list[0])
            # box_y = box_y - (box_y % box_size_list[0])
            # boxes cannot any other box + box_size_list[0] in any direction
            if not any(box_x < x[0] + x[2] and box_x + box_size > x[0] and
                       box_y < x[1] + x[2] and box_y + box_size > x[1]
                       for x in boxes):
                boxes.append([box_x, box_y, box_size])
                boxes = [x for x in boxes if not (x[0] < viewbox[0] or
                                                  x[0] + x[2] > viewbox[0] + canvas_size[0]
                                                  or x[1] < viewbox[1] or
                                                  x[1] + x[2] > viewbox[1] + canvas_size[1])]
                # for each box, reduce width and height by box_size_list[0]
    for box in boxes:
        box[2] = box[2] - box_size_list[0]
    boxes.sort(key=lambda x: (x[0], x[1], x[2]))
    # strip any boxes that overlap the viewbox edges

    print("Number of boxes: {}".format(len(boxes)))
    print("Number of iterations: {}".format(iterations))
    print("Number of boxes per iteration: {}".format(boxes_per_iteration))
    print("Viewbox: {}".format(viewbox))
    return boxes


def draw_box(box_x, box_y, box_size, stroke_colour, stroke_width, fill_colour):
    """ draw a box """
    position = """ x="{}" y="{}" """.format(box_x, box_y)
    size = """ width="{}" height="{}" """.format(box_size, box_size)
    stroke = """ stroke="{}" stroke-width="{}" """.format(
        stroke_colour, stroke_width)
    fill = """ fill="{}" """.format(fill_colour)
    return """<rect {} {} {} {} />""".format(
        position, size, stroke, fill)


def create_svg_list(paper_size, stroke_colour, stroke_width, fill_colour):
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
    # svg_list.append(set_background(image_size, BACKGROUND_COLOUR))
    # draw the boxes
    box_list = []
    box_list = set_box_list(canvas_size, box_size_list, image_size, iterations, boxes_per_iteration)
    for box in box_list:
        svg_list.append(draw_box(box[0], box[1], box[2], stroke_colour,
                                 stroke_width, fill_colour))
    svg_list.append(svg_footer())
    return svg_list


def main():
    file_name = generate_filename()
    paper_size = set_image_size(DEFAULT_PAPER_SIZE, DEFAULT_PIXELS_PER_MM)
    paper_size = set_landscape(paper_size, DEFAULT_LANDSCAPE)
    svg_list = create_svg_list(paper_size, STROKE_COLOUR,
                               STROKE_WIDTH, FILL_COLOUR)
    write_svg_file(file_name, svg_list)


if __name__ == "__main__":
    main()
