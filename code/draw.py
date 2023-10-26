""" This module contains functions used in the body of svg files
"""


def line(start_xy, end_xy, width, colour):
    """return a line from start_xy to end_xy"""
    return """<line x1="{}" y1="{}" x2="{}" y2="{}" stroke-width="{}"
           stroke="{}" />""".format(
        start_xy[0], start_xy[1], end_xy[0], end_xy[1], width, colour)
