"""
    This module contains functions used in the body of svg files
"""


def line(start_xy, end_xy, width, colour):
    """return a line from start_xy to end_xy"""
    linedef = """<line x1="{}" y1="{}" x2="{}" y2="{}" """.format(
        start_xy[0], start_xy[1], end_xy[0], end_xy[1])
    style = """stroke-width="{}" stroke="{}" />""".format(width, colour)
    return linedef + " " + style + "\n"


def box(start_xy, box_size, stroke_colour, stroke_width, fill_colour):
    """ draw a box """
    position = """ x="{}" y="{}" """.format(start_xy[0], start_xy[1])
    size = """ width="{}" height="{}" """.format(box_size, box_size)
    stroke = """ stroke="{}" stroke-width="{}" """.format(
        stroke_colour, stroke_width)
    fill = """ fill="{}" """.format(fill_colour)
    return """<rect {} {} {} {} />""".format(
        position, size, stroke, fill)


def circle(cx, cy, r, stroke_colour, stroke_width, fill_colour):
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
        stroke_colour, stroke_width, fill_colour)
    return circle_def + "\n" + circle_style + "\n"


def set_background(drawable_area, background_colour):
    """
    returns a rectangle of background_colour the size of the drawable area
    """
    return box(drawable_area[:2], drawable_area[2] - drawable_area[0],
               background_colour, 0, background_colour)


def quadratic_curve(start_xy, control_xy, end_xy, stroke_width, stroke_colour):
    """ return a quadratic curve """
    start = """<path d="M {} {} """.format(start_xy[0], start_xy[1])
    control = """Q {} {} """.format(control_xy[0], control_xy[1])
    end = """{} {}" stroke="{}" stroke-width="{}" fill="none" />""".format(
        end_xy[0], end_xy[1], stroke_colour, stroke_width)
    return start + control + end
