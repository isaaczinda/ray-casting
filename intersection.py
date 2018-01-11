import numpy as np
import time
from world import *

# add a bit of size to each triangle to account for floating point math
TRIANGLE_SCALE = .000001 # one millionth

class Intersection:
    ''' stores information about intersection between ray and triangle '''
    def __init__(self, point, triangle, distance):
        self.point = point
        self.distance = distance
        self.triangle = triangle

    def __str__(self):
        return "Intersection: at " + str(self.point)

def _inTriangle(triangle, point):
    ''' point should be a numpy row vector '''

    # translate, then project, then transform
    transformedPoint = ((point - triangle.translationVector).dot(triangle.projectionMatrix)).dot(triangle.transformationMatrix)

    # make sure that the points are within triangle (0, 0) (1, 0) (0, 1)
    # actually make the triangle limits a bit bigger so the triangle is easier to hit
    return transformedPoint[1] <= 1 - transformedPoint[0] + TRIANGLE_SCALE and \
        transformedPoint[0] >= -TRIANGLE_SCALE and \
        transformedPoint[1] >= -TRIANGLE_SCALE

def findIntersection(triangle, ray):
    ''' find intersection between trinagle and ray
    returns None if there was no intersection or an Intersection object '''

    # if the plane and ray are parallel, there can be no intersection
    if ray.direction.dot(triangle.normal) == 0:
        return None

    # we find this expression substituting the equation of a ray into the plane equation
    # ray is defined parametrically, this solves for value of t
    # triangle.A is a point in the triangle, doesn't matter which
    t = (triangle.A.dot(triangle.normal) - ray.point.dot(triangle.normal)) / (ray.direction.dot(triangle.normal))

    # make sure we only check the correct direction
    if t <= 0:
        return None

    # use value of t to find intersection point
    point = ray.point + t * ray.direction

    # add to list of intersections if intersection point is in triangle
    if _inTriangle(triangle, point):
        return Intersection(point, triangle, t)
