import numpy as np
import math

POINT_IN_TRIANGLE_MAX_DIFF = .001


class Triangle:
    def __init__(self, A, B, C):
        ''' construct triangle from three points stored in python arrays '''
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)

        # points stored as row vector
        self._points = np.array([A, B, C])

        self.normal = np.cross(self.A - self.B, self.B - self.C)

        # does setup for ray triangle intersection code
        self._calculateTransformations()

    def _calculateTransformations(self):
        # calculate translation that makes first point in triangle the origin
        self.translation = self._points[0][0:2]

        print("triangle:")
        print(self._points)
        print(self.translation)
        print(self._points[1:, :2] - self.translation)

        # find linear transformation where B and C map to [1, 0] and [0, 1]
        # slicing cuts off first row, which is zeroes
        # slicing cuts off laws column, removing Z component
        self.transformation = np.linalg.inv(self._points[1:, :2] - self.translation)

def findReflection(incidentVector, normalVector):
    ''' finds the reflection of the normalized incidentVector off of plane with normalVector normal '''
    incident = np.copy(incidentVector)
    normal = np.copy(normalVector)

    # incidentVector should make an obtuse angle with normalVector
    # flip it if it makes an acute angle
    if incident.dot(normal) > 0:
        normal *= -1

    incident *= -1
    diff = normal - incident
    reflected = normal + diff

    return reflected

def normalized(a):
    ''' normalizes a vector '''
    return a / float(np.linalg.norm(a)) # divides vector by its length

def findNormal(triangle):
    '''
    triangle is a 2D array containing three points
    points are stored in counterclockwise order from angle which they are intended to be viewed
    '''
    x = triangle[1] - triangle[0]
    y = triangle[2] - triangle[1]

    return normalized(np.cross(x, y))

def determineTint(triangle, lightNormal):
    ''' returns the tint of a face from 0 to 1 given light direction '''
    triangleNormal = findNormal(triangle)

    return abs(triangleNormal.dot(lightNormal))


def findRefraction(incidentVector, normalVector, firstIndex, secondIndex):
    incident = np.copy(incidentVector)
    normal = np.copy(normalVector)

    # incidentVector should make an obtuse angle with normalVector
    # flip it if it makes an acute angle
    if incident.dot(normal) > 0:
        normal *= -1

    xa = normal + incident

    invertedNormal = -np.copy(normal) # make a copy of the normal, going the other way
    xb = xa * (float(firstIndex) / float(secondIndex))

    return invertedNormal + xb

def rayPlaneIntersection(planePoint, planeNormal, rayPoint, rayDirection):
    '''
    finds the intersection between a plane and a ray
    if rayPoint is on the specified plane, no collision is said to occur
    raises ValueError if the plane and ray are parallel
    returns empty array if there was no collision
    '''

    # if the plane and ray are parallel
    if rayDirection.dot(planeNormal) == 0:
        raise ValueError

    # we find this expression substituting the equation of a ray into the plane equation
    # ray is defined parametrically, this solves for value of t
    t = (planePoint.dot(planeNormal) - rayPoint.dot(planeNormal)) / (rayDirection.dot(planeNormal))

    # make sure we only check the correct direction
    if t <= 0:
        return np.array([])

    # use value of t to find intersection point
    point = rayPoint + t * rayDirection

    return point

def pointInTriangle(A, B, C, P):
    '''
    checks if a point is in a triangle, given that it is in the triangle's plane
    http://www.nerdparadise.com/math/pointinatriangle
    '''
    AP = P - A
    AB = B - A
    BP = P - B
    BC = C - B
    CP = P - C
    CA = A - C

    crossProducts = np.array([np.cross(AP, AB), np.cross(BP, BC), np.cross(CP, CA)])

    # normalize all cross products so their direction can be compared
    # remove all zero vectors
    normalizedCrossProducts = [normalized(i) for i in crossProducts if not (i == np.array([0, 0, 0])).all()]

    # make sure that all cross products are BASICALLY the same
    # there will be some difference because of floating point math

    firstDiff = 0
    secondDiff = 0

    # if we are on a corner
    if len(normalizedCrossProducts) == 1:
        return True
    elif len(normalizedCrossProducts) == 2:
        firstDiff = np.linalg.norm(normalizedCrossProducts[0] - normalizedCrossProducts[1])
    else:
        firstDiff = np.linalg.norm(normalizedCrossProducts[0] - normalizedCrossProducts[1])
        secondDiff = np.linalg.norm(normalizedCrossProducts[0] - normalizedCrossProducts[2])

    # if the cross products all points in basically the same direction
    if firstDiff < POINT_IN_TRIANGLE_MAX_DIFF and secondDiff < POINT_IN_TRIANGLE_MAX_DIFF:
        return True

    return False

def checkIntersection(triangle, rayPoint, rayDirection):
    ''' returns whether or not triangle and ray intersect '''
    result = getIntersectionPoint(triangle, rayPoint, rayDirection)

    # if there was no intersection
    if np.array_equal(result, np.array([])):
        return False

    return True

def getIntersectionPoint(triangle, rayPoint, rayDirection):
    ''' returns point where triangle and ray intersect, returns empty
    array if they don't '''

    planeNormal = findNormal(triangle)

    # if the plane is parallel to the ray, there can be no intersection
    if planeNormal.dot(rayDirection) == 0:
        return np.array([])

    intersectionPoint = rayPlaneIntersection(triangle[0], planeNormal, rayPoint, rayDirection)

    # if there was no intersection, None is returned instead of numpy array
    if np.array_equal(intersectionPoint, np.array([])):
        return np.array([])

    # check if this point is in the triangle
    if pointInTriangle(triangle[0], triangle[1], triangle[2], intersectionPoint):
        return intersectionPoint
    else:
        return np.array([])
