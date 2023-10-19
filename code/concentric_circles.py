import sys
import datetime
import random
# create svg file of concentric circles using python
A4 = (210, 297)
A3 = (297, 420)
ppmm = 5  # pixels per mm

STROKE_COLOUR = "black"
STROKE_WIDTH = ppmm
FILL_COLOUR = "none"
NOISE = 0.05

DEFAULT_PAPER_SIZE = A3
DEFAULT_LANDSCAPE = True
DEFAULT_CIRCLES = 80
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


# def set_svg_background(paper_size):
#     """ set the background colour """
#     return """<rect width="{}" height="{}" style="fill:{}" />""".format(
#         paper_size[0], paper_size[1], background_color)


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


def draw_circle(cx, cy, r):
    """
    Returns an SVG circle element as a string with the specified center
    coordinates and radius.

    Args:
      cx (float): The x-coordinate of the center of the circle.
      cy (float): The y-coordinate of the center of the circle.
      r (float): The radius of the circle.

    Returns:
      str: An SVG circle element as a string.
    """
    circle_def = """<circle cx="{}" cy="{}" r="{}" """.format(cx, cy, r)
    circle_style = """stroke="{}" stroke-width="{}" fill="{}" />""".format(
        STROKE_COLOUR, STROKE_WIDTH, FILL_COLOUR)
    return circle_def + "\n" + circle_style + "\n"


def calculate_max_radius(canvas_size):
    """
    Calculates the maximum radius that can be used for concentric circles on a
    canvas of the given size.

    Args:
      canvas_size (tuple): A tuple containing the width and height of the
      canvas.

    Returns:
      int: The maximum radius that can be used for concentric circles on the
      canvas.
    """
    return min(canvas_size)


def weighted_random(weight):
    """ """
    return random.random()*weight


def skew_centre(canvas_size):
    """Returns a tuple with the coordinates of the centre of the canvas,
    skewed by a random amount.

    Args:
      canvas_size (tuple): A tuple with the width and height of the canvas.

    Returns:
      tuple: A tuple with the x and y coordinates of the skewed centre of the
      canvas.
    """
    skewed_x = canvas_size[0] * (1+weighted_random(NOISE)) / 2
    skewed_y = canvas_size[1] * (1+weighted_random(NOISE)) / 2
    return (int(skewed_x), int(skewed_y))


def generate_circle_list(paper_size, circle_count):
    """
    Generate a list of circle radii.

    Args:
      paper_size (tuple): The size of the paper to draw on.
      circle_count (int): The number of circles to generate.

    Returns:
      list: A list of circle radii.

    """
    canvas_size = set_canvas_size(paper_size)
    max_radius = calculate_max_radius(canvas_size)
    circle_list = []
    for i in range(circle_count):
        circle_list.append(
            int(max_radius * ((i+i*weighted_random(NOISE)) / circle_count)))
    return circle_list


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
    for i in generate_circle_list(image_size, circle_count):
        skew_x, skew_y = skew_centre(canvas_size)
        svg_list.append(draw_circle(skew_x, skew_y, i))
    svg_list.append(svg_footer())
    return svg_list


def main():
    file_name = generate_filename()
    paper_size = set_image_size(DEFAULT_PAPER_SIZE, DEFAULT_PIXELS_PER_MM)
    paper_size = set_landscape(paper_size, DEFAULT_LANDSCAPE)
    svg_list = create_svg_list(
        paper_size, DEFAULT_CIRCLES)
    write_svg_file(file_name, svg_list)


if __name__ == "__main__":
    main()
