from world import *
from viewport import *
from geometry import *
from tkinter import Tk, Canvas, mainloop
from math import sin
from PIL import Image

w = World(normalized(np.array([0, 2, 1])))
obj = Object3D('./box.stl', createOpaqueMaterial((50, 50, 50)))
w.addObject(obj, np.array([0, 0, 0]))

print(obj.numberTriangles())

# this is a very wide angle
# lowerLeft, upperRight, lowerRight, eyeDistance):

# view = ViewPort(np.array([-25, -25, 50]), np.array([25, 25, 50]), np.array([25, -25, 50]), 50)

view = ViewPort(np.array([-20, 20, 20]), np.array([0, -20, 0]), 30)

image = Image.new('RGB', (view.width(), view.height()), "white")
pixels = pixels = image.load() # get pixels, put into array

# cast a ray for each pixel in the screen
for x in range(view.width()):
    for y in range(view.height()):
        rayCoordinate, rayDirection = view.getRay(x, y)

        intersection = w.findFirstIntersection(rayCoordinate, rayDirection)

        print(x, y)

        # if we didn't hit something, move along
        if intersection == None:
            continue

        # otherwise, color a pixel
        baseColor = intersection.material.color
        tint = determineTint(intersection.triangle, w.lightDirection)
        # use view.width - x to convert from cartesian coordinates
        pixels[view.width() - x,y] = (int(baseColor[0] * tint), int(baseColor[1] * tint), int(baseColor[2] * tint))


image.show()
