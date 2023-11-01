#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def set_image_size(paper_size, ppmm, landscape=True):
    if landscape:
        return (int(paper_size[1] * ppmm), int(paper_size[0] * ppmm))
    else:
        return (int(paper_size[0] * ppmm), int(paper_size[1] * ppmm))


def set_landscape(paper_size, landscape):
    if landscape:
        return (paper_size[1], paper_size[0])
    else:
        return paper_size


def set_drawable_area(paper_size, bleed_xy):
    min_x = int((paper_size[0] * bleed_xy[0] / 100)/2)
    min_y = int((paper_size[1] * bleed_xy[1] / 100)/2)
    max_x = paper_size[0] - min_x
    max_y = paper_size[1] - min_y
    return (min_x, min_y, max_x, max_y)


def is_in_drawable_area(xy1, xy2, drawable_area):
    """ return True if both points are in drawable_area """
    if xy1[0] < drawable_area[0] or xy1[0] > drawable_area[2] or \
       xy1[1] < drawable_area[1] or xy1[1] > drawable_area[3] or \
       xy2[0] < drawable_area[0] or xy2[0] > drawable_area[2] or \
       xy2[1] < drawable_area[1] or xy2[1] > drawable_area[3]:
        return False
    else:
        return True


def svg_header(paper_size, drawable_area):
    """
    Returns an SVG header string with the specified paper and canvas sizes.

    Args:
      paper_size (tuple): A tuple containing the width and height of the paper.
      canvas_size (tuple): A tuple containing the width and height of the
      canvas.

    Returns:
      str: An SVG header string with the specified paper and canvas sizes.
    """
    xml1 = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>"""
    xml2 = """<svg width="{}" height="{}" viewBox="{} {} {} {}" """.format(
        paper_size[0], paper_size[1], drawable_area[0],
        drawable_area[1], drawable_area[2], drawable_area[3])
    xml3 = """xmlns="http://www.w3.org/2000/svg" version="1.1">"""
    return xml1 + "\n" + xml2 + "\n" + xml3 + "\n"


def svg_footer():
    return "</svg>"


def svg_list_to_string(svg_list):
    """ convert a list of SVG lines to a string """
    return "\n".join(svg_list)


def build_svg_file(paper_size, drawable_area, svg_list):
    """ build the SVG file from the following parts:
        header
        svg_list
        footer
    """
    svg_list.insert(0, svg_header(paper_size, drawable_area))
    svg_list.append(svg_footer())
    return svg_list


def write_file(filename, svg_list):
    """ Write the SVG file """
    with open(filename, "w") as svg_file:
        for line in svg_list:
            svg_file.write(line + "\n")
