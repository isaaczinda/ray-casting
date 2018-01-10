from world import *
from viewport import *
from geometry import determineBrightness
from tkinter import Tk, Canvas, mainloop
from math import sin
from PIL import Image
import sys

world = World(np.array([.2, .2, .2])) # set level of ambient light

# add objects
world.addObject('./box.stl', createOpaqueMaterial(np.array([0, 1, 1])), position=np.array([0, 0, 0]))
world.addObject('./box.stl', createOpaqueMaterial(np.array([1, 0, 1])), position=np.array([10, 10, -5]))
world.addObject('./box.stl', createOpaqueMaterial(np.array([1, 1, 0])), position=np.array([20, 20, -10]))
world.addObject('./box.stl', createOpaqueMaterial(np.array([0, 1, 1])), position=np.array([30, 30, -15]))
world.addObject('./box.stl', createOpaqueMaterial(np.array([1, 0, 1])), position=np.array([40, 40, -20]))

# add lights
world.addLight(Light(np.array([80, 150, 50]), np.array([.25, .25, .25])))
world.addLight(Light(np.array([80, 150, 0]), np.array([.25, .25, .25])))
world.addLight(Light(np.array([80, 150, -50]), np.array([.25, .25, .25])))

# setup viewport
viewport = ViewPort(np.array([40, 100, 100]), np.array([0, -20, 0]), 70, resolution=(400, 400))

image = Image.new('RGB', (viewport.width(), viewport.height()), "white")
pixels = pixels = image.load() # get pixels, put into array

def progress(count, total, status=''):
    ''' code from: https://gist.github.com/vladignatyev/06860ec2040cb497f0f3 '''
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', status))
    sys.stdout.flush()

# coord tracks the coordinate of the ray that we are using in the screen
# starting from the top left
for x in range(viewport.width()):
    progress(x, viewport.width())

    for y in range(viewport.height()):
        intersection = world.findFirstIntersection(viewport.getRay(x, y))

        # if we need to color something
        if intersection != None:
            color = world.colorAtIntersection(intersection)

            # use view.height - y - 1 to convert from cartesian coordinates
            pixels[x, viewport.height() - y - 1] = (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))

image.show()
