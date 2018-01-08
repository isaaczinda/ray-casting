import numpy as np
from stl import mesh
from geometry import *
import sys

class Object3D:
    ''' created a 3D object in the secified material from an STL file '''
    def __init__(self, filepathToSTL, material):
        self.mesh = mesh.Mesh.from_file(filepathToSTL)
        self.material = material

    def numberTriangles(self):
        ''' gets the number of triangles in an object '''
        return len(self.mesh.v0)

class Material:
    ''' holds collection of rules about how reflection and refraction occur '''

    def __init__(self, transparent, refractionIndex, color):
        self.transparent = transparent
        self.refractionIndex = refractionIndex
        self.color = color

def createTransparentMaterial(refractionIndex):
    ''' creates a transparent material with refractionIndex '''
    return Material(True, refractionIndex, (0, 0, 0))

def createOpaqueMaterial(color):
    ''' creates an opaque material that absorbs certain types of light '''
    return Material(False, 1, color)

class Intersection:
    ''' contains information about the intersection between a ray and a
    shape '''

    def __init__(self, triangle, point, material):
        self.triangle = triangle
        self.point = point
        self.material = material

class TriangleIterator:
    '''
    iterates over triangles in this World
    returns tuples containing their material and vertices
    '''

    def __init__(self, worldObject):
        self.objectIndex = 0
        self.triangleIndex = 0
        self.worldObject = worldObject
        self.numberObjects = len(self.worldObject.objects)


    def __iter__(self):
        return self

    def __next__(self):
        # if there are no triangles left to search, go to the beginning of next object
        numTriangles = len(self.worldObject.objects[self.objectIndex].mesh.points)
        if self.triangleIndex >= numTriangles:
            self.triangleIndex = 0
            self.objectIndex += 1

        # iterate until there are no more objects left
        if self.objectIndex < self.numberObjects:
            points = self.worldObject.objects[self.objectIndex].mesh.points[self.triangleIndex]
            trianglePoints = np.reshape(np.copy(points), (3, 3)) # this is a 2D array

            # since this whole object has a position, move it accordingly
            for triangle in trianglePoints:
                triangle += self.worldObject.objectPositions[self.objectIndex]

            triangleMaterial = self.worldObject.objects[self.objectIndex].material
            self.triangleIndex += 1

            return (trianglePoints, triangleMaterial)

        # if we have been through all of the objects
        else:
            raise StopIteration()

class World:
    def __init__(self, lightDirection=np.array([0, 0, 1])):
        ''' creates a new world, may specify which direction light comes
        from '''
        self.lightDirection = lightDirection
        self.objects = []
        self.objectPositions = []

    def addObject(self, obj, position=np.array([0, 0, 0])):
        ''' adds an Object3D to the world
        may specify a position, default is (0, 0, 0) '''
        self.objects.append(obj)
        self.objectPositions.append(position)

    def triangles(self):
        ''' creates an iterator to look through all triangles in world '''
        return TriangleIterator(self)

    def findFirstIntersection(self, rayPoint, rayDirection):
        '''
        finds the first intersection between a world and a ray
        returns Intersection object if there was an intersection, None
        if there was no intersection
        '''

        smallestDistance = sys.float_info.max # nothing can be larger than this!
        intersection = None

        for triangle, material in self.triangles():
            intersectionPoint = getIntersectionPoint(triangle, rayPoint, rayDirection)

            # if there was an intersection
            if not np.array_equal(intersectionPoint, np.array([])):
                distance = np.linalg.norm(rayPoint - intersectionPoint)

                # if this is the closest intersection yet
                if distance < smallestDistance:
                    intersection = Intersection(triangle, intersectionPoint, material)
                    smallestDistance = distance

        return intersection
