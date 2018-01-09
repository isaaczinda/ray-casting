import numpy as np
import time
from viewport import *
from geometry import Triangle

def inTriangle(triangle, points):
    # 3D space -> homogeneous coordinates
    projectionMatrix = np.array([[1, 0, 0], [0, 1, 0]])
    triangle = projectionMatrix.dot(triangle)

    # calculate translation that makes first point in triangle the origin
    translation = triangle[:, 0:1]

    # find linear transformation where B and C map to [1, 0] and [0, 1]
    # slicing cuts off first column, which is zeroes
    linearTransformation = np.linalg.inv(triangle[:, 1:])

    # startTime = time.time()

    # transform points in the same way that transformed triangles
    transformedPoints = linearTransformation.dot(projectionMatrix.dot(points) - translation)

    # iterate over all columns in matrix
    # make sure that the points are within triangle (0, 0) (1, 0) (0, 1)
    inTriangle = [column[1] <= 1 - column[0] and column[0] >= 0 and column[1] >= 0 for column in transformedPoints.T]

    return inTriangle

def findIntersections(triangle, rays):
    ''' find intersection between rays and triangle
    does not modify triangle or rays objects '''

    planeNormal = np.cross(triangle[0] - triangle[1], triangle[1] - triangle[2])
    planePoint = triangle[0]

    # # create the array beforehand so we don't have to continually reallocate
    # intersections = np.empty([rays.width, rays.height])
    # intersections.fill(False)



    intersectionPoints = []
    intersectionCoords = []
    intersectionDistance = []

    lastTime = time.time()

    # coord tracks the coordinate of the ray that we are using in the screen
    # starting from the top left
    for x in range(rays.width()):
        for y in range(rays.height()):

            ray = rays.getRay(x, y)

            # if the plane and ray are parallel, there can be no intersection
            if ray.direction.dot(planeNormal) == 0:
                continue

            # we find this expression substituting the equation of a ray into the plane equation
            # ray is defined parametrically, this solves for value of t
            t = (planePoint.dot(planeNormal) - ray.point.dot(planeNormal)) / (ray.direction.dot(planeNormal))

            # make sure we only check the correct direction
            if t <= 0:
                continue

            # these aren't huge CPU hogs
            # use value of t to find intersection point
            intersectionPoints.append(ray.point + t * ray.direction)
            intersectionCoords.append((x, y))
            intersectionDistance.append(t)




    print("time to get intersection points", time.time() - lastTime)
    lastTime = time.time()

    # reformat intersectionPoints to be a numpy matrix of column vectors
    # get the locations where rays intersect area inside triangle
    # transform triangle into column vector of points
    pointInTriangle = inTriangle(triangle.T, np.array(intersectionPoints).T)

    print("time to get in triangle", time.time() - lastTime)
    lastTime = time.time()

    # save data about where intersections happened
    intersections = {}

    for i in range(len(intersectionPoints)):
        if pointInTriangle[i]:
            intersections[intersectionCoords[i]] = (intersectionPoints[i])

    print("time to create intersection dictionary", time.time() - lastTime)
    lastTime = time.time()

    # for key in intersections.keys():
    #     print(key)


if __name__ == '__main__':
    # viewport facing the origin
    view = ViewPort(np.array([0, 0, 30]), np.array([0, 0, 0]), 10)

    triangle = Triangle([0, 0, 0], [5, 0, 0], [0, 5, 0])

    startTime = time.time()
    findIntersections(triangle, view)
    print(time.time() - startTime)
