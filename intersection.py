import numpy as np
import time
from viewport import *
from geometry import Triangle

def inTriangle(triangle, point):
    ''' point should be a numpy row vector '''
    
    # remove Z component of point
    transformedPoint = (point[0:2] - triangle.translation).dot(triangle.transformation)

    # print(transformedPoint)

    # make sure that the points are within triangle (0, 0) (1, 0) (0, 1)
    return transformedPoint[1] <= 1 - transformedPoint[0] and transformedPoint[0] >= 0 and transformedPoint[1] >= 0

def findIntersection(triangle, ray):
    ''' returns None if there was no intersection or an Intersection object '''

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
    if inTriangle(triangle, point):
        return Intersection(point, triangle, t)

def findIntersections(triangle, viewport):
    ''' find intersection between rays and triangle
    does not modify triangle or rays objects '''

    lastTime = time.time()

    # save data about where intersections happened
    intersections = {}

    # coord tracks the coordinate of the ray that we are using in the screen
    # starting from the top left
    for x in range(viewport.width()):
        for y in range(viewport.height()):
            ray = viewport.getRay(x, y)
            findIntersection(triangle, ray)


if __name__ == '__main__':
    # viewport facing the origin
    view = ViewPort(np.array([0, 0, 30]), np.array([0, 0, 0]), 10)

    triangle = Triangle([0, 0, 0], [5, 0, 0], [0, 5, 0])

    startTime = time.time()
    findIntersections(triangle, view)
    print(time.time() - startTime)
