import numpy as np
from stl import mesh
from geometry import *
import sys
from intersection import *
from viewport import *

class Triangle:
    xyProjectionMatrix = np.array([[1, 0], [0, 1], [0, 0]])
    yzProjectionMatrix = np.array([[0, 0], [1, 0], [0, 1]])
    xzProjectionMatrix = np.array([[1, 0], [0, 0], [0, 1]])

    def __init__(self, A, B, C, normal, material):
        ''' construct triangle from three points stored in python arrays '''
        self.A = np.array(A)
        self.B = np.array(B)
        self.C = np.array(C)
        self.material = material

        # points stored as row vector
        self._points = np.array([A, B, C])

        self.normal = normal

        # does setup for ray triangle intersection code
        self._calculateTransformations()

    def _calculateTransformations(self):
        # calculate translation that makes first point in triangle the origin
        self.translationVector = self._points[0]

        # maps onto x-y plane
        self.projectionMatrix = np.array([[1, 0], [0, 1], [0, 0]])

        # remove first row, which is just origin point
        translated = (self._points - self.translationVector)[1:, :]

        # find the right projection matrix
        # we try projecting onto three different planes
        if np.linalg.det(translated.dot(Triangle.xyProjectionMatrix)) != 0:
            self.projectionMatrix = Triangle.xyProjectionMatrix
        elif np.linalg.det(translated.dot(Triangle.xzProjectionMatrix)) != 0:
            self.projectionMatrix = Triangle.xzProjectionMatrix
        else:
            self.projectionMatrix = Triangle.yzProjectionMatrix

        # find the matrix that transforms our second two points to [1, 0] and [0, 1]
        self.transformationMatrix = np.linalg.inv(translated.dot(self.projectionMatrix))


class Material:
    ''' holds collection of rules about how reflection and refraction occur '''

    def __init__(self, ambientReflection, diffuseReflection, shininess, specularIntensity):
        self.ambientReflection = ambientReflection
        self.diffuseReflection = diffuseReflection
        self.shininess = shininess
        self.specularIntensity = specularIntensity


def createOpaqueMaterial(reflectedColor, specularIntensity):
    ''' creates an opaque material that absorbs certain types of light '''
    return Material(reflectedColor, reflectedColor, 50, specularIntensity)

class Light:
    def __init__(self, position, color):
        ''' specify position and color of light as numpy arrays '''
        self.position = position
        self.color = color


class World:
    def __init__(self, ambientLight, viewport):
        ''' creates a new world '''
        self.ambientLight = ambientLight
        self.lights = []
        self.triangles = []
        self.viewport = viewport

    def addLight(self, light):
        ''' add a point light to the world '''
        self.lights.append(light)

    def addObject(self, filepathToSTL, material, position=np.array([0, 0, 0])):
        ''' adds an Object3D to the world
        must specify STL file to import object from, STL file must define triangles
        with counterclockwise points
        may specify a position, default is (0, 0, 0)
        '''

        importedMesh = mesh.Mesh.from_file(filepathToSTL)

        # extracts triangles from mesh and adds to world
        for i in range(len(importedMesh.v0)):
            triangle = Triangle(importedMesh.v0[i] + position, importedMesh.v1[i] + position, \
                importedMesh.v2[i] + position, normalized(importedMesh.normals[i]), material)

            self.triangles.append(triangle)

    def _intersectionInRange(self, ray, distanceRange):
        ''' checks if there are any intersections certain distances along the ray '''

        for triangle in self.triangles:
            intersection = findIntersection(triangle, ray)

            if intersection != None and intersection.distance >= distanceRange[0] \
                and intersection.distance <= distanceRange[1]:

                return True

        return False

    def findFirstIntersection(self, ray):
        ''' returns an intersection object if the ray hits a triangle in this
        world, otherwise returns None '''

        shortestDistance = 10000
        firstIntersection = None

        for triangle in self.triangles:
            currentIntersection = findIntersection(triangle, ray)

            if currentIntersection != None and currentIntersection.distance < shortestDistance:
                firstIntersection = currentIntersection
                shortestDistance = currentIntersection.distance

        return firstIntersection

    def _lightVisibleAtIntersection(self, light, intersection):
        ''' checks if a light shines on an intersection '''

        direction = normalized(light.position - intersection.point)
        ray = Ray(intersection.point, direction)
        distanceToLight = np.linalg.norm(light.position - intersection.point)

        # check if there are any triangles between this triangle and the light
        # .1 ensures we don't check intersection with 'current' triangle
        return not self._intersectionInRange(ray, (.1, distanceToLight))

    def colorAtIntersection(self, intersection):
        ''' gets the color of light reflected off an
        intersection. checks to make sure we are not in shadow '''

        # start with contribution from ambient light
        color = self.ambientLight * intersection.triangle.material.ambientReflection


        # we will check the contribution from each light
        for light in self.lights:
            lightDirection = normalized(intersection.point - light.position)

            # if light is visible at intersection
            if self._lightVisibleAtIntersection(light, intersection):

                # calculate diffuse reflection
                diffuseIntensity = -lightDirection.dot(intersection.triangle.normal)

                if diffuseIntensity < 0:
                    diffuseIntensity = 0

                color += diffuseIntensity * light.color * intersection.triangle.material.diffuseReflection

                # calculate specular reflection
                viewVector = normalized(intersection.point - self.viewport.eyePoint)
                lightReflectionVector = normalized(findReflection(lightDirection, intersection.triangle.normal))

                specularIntensity = -viewVector.dot(lightReflectionVector)

                if specularIntensity < 0:
                    specularIntensity = 0

                color += math.pow(specularIntensity, intersection.triangle.material.shininess) * light.color \
                    * intersection.triangle.material.specularIntensity


        # no color can be > 1
        return np.array([1 if swatch > 1 else swatch for swatch in color])
