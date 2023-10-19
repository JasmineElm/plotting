#!/usr/bin/env python3

import random
import datetime
import sys

# create a svg file caontaining a number of randomly placed and sized circles
dim_x = 1000
dim_y = 1000
min_circles = 10
max_circles = 100
min_radius = 10
max_radius = 100

def get_script_name():
    """return the name of the script without the path and without the
    extension"""
    if len(sys.argv) > 0:
        script_name = sys.argv[0].split("/")[-1].split(".")[0]
    elif len(sys.argv) == 0:
        script_name = __file__.split("/")[-1].split(".")[0]
    else:
        script_name = "random_circles"
    return script_name



def filename():
    """Return a filename with a timestamp"""
    now = datetime.datetime.now()
    suffix=now.strftime("%Y%m%d-%H%M%S")
    default_file_prefix = get_script_name()
    return default_file_prefix + "_" + suffix + ".svg"
# create a svg file
header="""<?xml version="1.0" encoding="UTF-8" standalone="no"?> 
<svg width="{}" height="{}" xmlns="http://www.w3.org/2000/svg" version="1.1">
""".format(dim_x, dim_y)

footer="""</svg>"""

# create a list of circles
circles = []
for i in range(random.randint(min_circles, max_circles)):
    x = random.randint(0, dim_x)
    y = random.randint(0, dim_y)
    r = random.randint(min_radius, max_radius)
    # if x+r > dim_x, or y+r > dim_y, do not append the circle to the list
    if x+r > dim_x or y+r > dim_y:
        continue
    else: 
      circles.append((x, y, r))

# create a list of svg circle elements
circle_elements = []
for c in circles:
    circle_elements.append('<circle cx="{}" cy="{}" r="{}" fill="none" stroke="black" stroke-width="1"/>'.format(c[0], c[1], c[2]))

# write the svg file
filename = filename()
with open(filename, "w") as f:
    f.write(header)
    for e in circle_elements:
        f.write(e)
    f.write(footer)
