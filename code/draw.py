""" This module contains functions used in the body of svg files
"""


def line(start_xy, end_xy, width, colour):
    """return a line from start_xy to end_xy"""
    return """<line x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="{}"
           stroke="{}" />""".format(
        start_xy[0], start_xy[1], end_xy[0], end_xy[1], width, colour)


def box(start_xy, box_size, stroke_colour, stroke_width, fill_colour):
    """ draw a box """
    position = """ x="{}" y="{}" """.format(start_xy[0], start_xy[1])
    size = """ width="{}" height="{}" """.format(box_size, box_size)
    stroke = """ stroke="{}" stroke-width="{}" """.format(
        stroke_colour, stroke_width)
    fill = """ fill="{}" """.format(fill_colour)
    return """<rect {} {} {} {} />""".format(
        position, size, stroke, fill)


def set_background(drawable_area, background_colour):
    """
    returns a rectangle of background_colour the size of the drawable area
    
    """
    return box(drawable_area[:2], drawable_area[2] - drawable_area[0],
               background_colour, 0, background_colour)
