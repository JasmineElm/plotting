#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    SVG functions
"""
import math
import random


def set_image_size(paper_size, ppmm, landscape=True):
    """Set the size of the image in pixels.

    Args:
        paper_size (tuple): (width, height)
        ppmm (int): (pixels per mm)
        landscape (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """
    out_size = (int(paper_size[0] * ppmm), int(paper_size[1] * ppmm))
    return set_landscape(out_size, landscape)


def set_landscape(paper_size, landscape):
    """rotates a paper size tuple if landscape is True

    Args:
        paper_size (tuple): (width, height)
        landscape (bool): True if landscape

    Returns:
        tuple: (width, height)
    """
    if landscape:
        paper_size = (paper_size[1], paper_size[0])
    return paper_size


def set_drawable_area(paper_size, bleed_xy):
    """ returns a tuple of the drawable area defined by the bleed

    Args:
        paper_size (tuple): (width, height)
        bleed_xy (int): percentage of bleed

    Returns:
        tuple: (min_x, min_y, max_x, max_y)
    """
    min_x = int((paper_size[0] * bleed_xy[0] / 100)/2)
    min_y = int((paper_size[1] * bleed_xy[1] / 100)/2)
    max_x = paper_size[0] - min_x
    max_y = paper_size[1] - min_y
    return (min_x, min_y, max_x, max_y)


def is_in_drawable_area(xy1, xy2, drawable_area):
    """ return True if both points are in drawable_area """
    return (drawable_area[0] <= xy1[0] <= drawable_area[2] and
            drawable_area[1] <= xy1[1] <= drawable_area[3] and
            drawable_area[0] <= xy2[0] <= drawable_area[2] and
            drawable_area[1] <= xy2[1] <= drawable_area[3])


# Circles

def calculate_max_radius(drawable_area):
    """
    Calculates the maximum radius that can be used for concentric circles on a
    canvas of the given size.

    Args:
      drawable_area (tuple): the width and height of the
      canvas.

    Returns:
      int: The maximum radius that can be used for concentric circles on the
      canvas.
    """
    return min(drawable_area[3] - drawable_area[1],
               drawable_area[2] - drawable_area[0]) * 0.5


def set_circle(drawable_area, size=0.95):
    """ set the xy, radius for the largest circle that fits in drawable_area
        circle will be centred on both axes, and be 95% of the smallest
        drawable_area dimension
    """
    pos_x = (drawable_area[0] + drawable_area[2]) / 2
    pos_y = (drawable_area[1] + drawable_area[3]) / 2
    pos_xy = [pos_x, pos_y]
    radius = calculate_max_radius(drawable_area) * size
    return (pos_xy, radius)

# Header and footer


def svg_header(paper_size, drawable_area):
    """
    Returns an SVG header string with the specified paper and canvas sizes.

    Args:
        paper_size (tuple): the width and height of the paper.
        canvas_size (tuple): the width and height of the canvas.

    Returns:
        str: An SVG header string with the specified paper and canvas sizes.
    """
    xml1 = "<?xml version='1.0' encoding='UTF-8' standalone='no'?>"
    xml1 += f"<svg width='{paper_size[0]}' height='{paper_size[1]}' "
    xml1 += f"viewBox='{drawable_area[0]} {drawable_area[1]} "
    xml1 += f"{drawable_area[2]} {drawable_area[3]}' "
    xml1 += "xmlns='http://www.w3.org/2000/svg' version='1.1'>"
    return xml1 + '\n'


def svg_footer():
    """return the SVG footer"""
    return "</svg>"

# build SVG file


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
    with open(filename, "w", encoding="utf-8") as svg_file:
        for line in svg_list:
            svg_file.write(line + "\n")


# overlap functions

def circles_intersect(circle_a, circle_b):
    """ return True if circles intersect """
    distance = math.sqrt((circle_a[0] - circle_b[0])**2 +
                         (circle_a[1] - circle_b[1])**2)
    # return True if distance between centres is less than sum of radii
    return distance < circle_a[2] + circle_b[2]


def set_bounding_box(points_list):
    """ return a bounding box for a list of points """
    min_x = min(points_list, key=lambda x: x[0])[0]
    min_y = min(points_list, key=lambda x: x[1])[1]
    max_x = max(points_list, key=lambda x: x[0])[0]
    max_y = max(points_list, key=lambda x: x[1])[1]
    return (min_x, min_y, max_x, max_y)


def bounding_box_intersect(box_a, box_b):
    """ return True if bounding boxes overlap """
    if box_a[2] < box_b[0] or box_a[0] > box_b[2] or \
       box_a[3] < box_b[1] or box_a[1] > box_b[3]:
        return False
    return True


# Positioning functions


def get_centrality(viewbox, xy):
    """_summary_

    Args:
        viewbox ([xy1, xy2]): canvas size
        xy ([x,y]): point to check

    Returns:
        float: float between 0 and 1, depending on the distance of
        (x,y) from the centre of the canvas
        0 = centre, 1 = edge
    """
    distance = math.sqrt((viewbox[0] - xy[0])**2 + (viewbox[1] - xy[1])**2) \
        / math.sqrt((viewbox[0] - viewbox[2])**2 +
                    (viewbox[1] - viewbox[3])**2)
    return distance


def get_centre(viewbox):
    """Return the centre of the canvas"""
    return ((viewbox[2] - viewbox[0]) / 2, (viewbox[3] - viewbox[1]) / 2)


def get_random_point(viewbox):
    """Return a random point within the canvas"""
    return (random.randint(viewbox[0], viewbox[2]),
            random.randint(viewbox[1], viewbox[3]))


def set_polygon_size(viewable_area, polygons_per_min_dimension):
    """Set a polygon size based on how many will fit
       in the smallest dimension

    Args:
        viewable_area ([xy1, xy2]): drawable area
        polygons_per_min_dimension (int): how many polygons can fit in the
                                          smallest dimension
    returns:
        int: size of polygon
    """
    smallest_dimension = min(viewable_area[2] - viewable_area[0],
                             viewable_area[3] - viewable_area[1])
    return int(smallest_dimension / polygons_per_min_dimension)


def set_polygon(xy, polygon_size, points):
    """_summary_

    Args:
        xy ([x,y]): xy coordinates of centre of polygon
        polygon_size (int): diameter of polygon
        points (int): number of points that make up the polygon
    Returns:
        list: list of points that make up the polygon
    """
    polygon = []
    for i in range(points):
        # set a point on the circumference
        angle = i * (2 * math.pi / points)
        polygon.append(xy[0] + math.cos(angle) * polygon_size / 2)
        polygon.append(xy[1] + math.sin(angle) * polygon_size / 2)
    return polygon
