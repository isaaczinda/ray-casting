import numpy as np
import math

def findReflection(incident, normal):
    ''' finds the reflection of the normalized incidentVector off of plane with normalVector normal '''
    incidentCopy = np.copy(incident)

    # incidentVector should make an obtuse angle with normalVector
    # flip it if it makes an acute angle
    if incidentCopy.dot(normal) > 0:
        raise Exception("normal was facing the wrong way")

    diff = normal + incidentCopy
    return normal + diff

def normalized(a):
    ''' normalizes a vector '''
    return a / float(np.linalg.norm(a)) # divides vector by its length


def determineBrightness(triangle, lightNormal):
    ''' returns the tint of a face from 0 to 1 given light direction '''

    # when a light normal and triangle normal are opposite directions,
    # brightest color
    tint = -triangle.normal.dot(lightNormal)

    # we cannot have a tint < 0
    if tint < 0:
        return 0

    return tint


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
