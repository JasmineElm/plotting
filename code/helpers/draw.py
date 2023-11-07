"""
    This module contains functions used in the body of svg files
"""


def line(start_xy, end_xy, width, colour):
    """return a line from start_xy to end_xy"""
    linedef = f"<line x1='{start_xy[0]}' y1='{start_xy[1]}' "
    linedef += f" x2='{end_xy[0]}' y2='{end_xy[1]}' "
    style = f"stroke-width='{width}' stroke='{colour}' />"
    return linedef + style + "\n"


def box(start_xy, box_size, stroke_colour, stroke_width, fill_colour):
    """draw a box"""
    position = f" x='{start_xy[0]}' y='{start_xy[1]}' "
    size = f" width='{box_size}' height='{box_size}' "
    stroke = f" stroke='{stroke_colour}' stroke-width='{stroke_width}' "
    fill = f" fill='{fill_colour}' "
    return f"<rect {position}{size}{stroke}{fill}/>"


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
    circle_def = f"<circle cx='{cx}' cy='{cy}' r='{r}' "
    circle_style = f"stroke='{stroke_colour}' stroke-width='{stroke_width}' "
    circle_style += f"fill='{fill_colour}' />"
    return circle_def + "\n" + circle_style + "\n"


def set_background(drawable_area, background_colour):
    """
    returns a rectangle of background_colour the size of the drawable area
    """
    return box(
        drawable_area[:2],
        drawable_area[2] - drawable_area[0],
        background_colour,
        0,
        background_colour,
    )


def quadratic_curve(start_xy, control_xy, end_xy, stroke_width, stroke_colour, fill_colour='none'):
    """return a quadratic curve"""
    start = f"<path d='M {start_xy[0]} {start_xy[1]} "
    control = f"Q {control_xy[0]} {control_xy[1]} "
    end = f"{end_xy[0]} {end_xy[1]}' "
    style = (
        f"stroke='{stroke_colour}' "
        f"stroke-width='{stroke_width}' "
        f"fill='{fill_colour}' />"
    )
    return start + control + end + style + "\n"
