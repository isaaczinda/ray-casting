import numpy as np
import time


# 0, 2, 0
# 0, 0, 4
# 0, 0, 0
triangle = np.array([[1, 2, 0], [-1, 0, 4], [0, 0, 0]])
points = np.random.rand(3,10000)

# 3D space -> homogeneous coordinates
projectionMatrix = np.array([[1, 0, 0], [0, 1, 0]])
triangle = projectionMatrix.dot(triangle)

# calculate translation that makes first point in triangle the origin
translation = triangle[:, 0:1]

# find linear transformation where B and C map to [1, 0] and [0, 1]
# slicing cuts off first column, which is zeroes
linearTransformation = np.linalg.inv(triangle[:, 1:])

startTime = time.time()

# transform points in the same way that transformed triangles
transformedPoints = linearTransformation.dot(projectionMatrix.dot(points) - translation)

# iterate over all columns in matrix
# make sure that the points are within triangle (0, 0) (1, 0) (0, 1)
inTriangle = [column[1] <= 1 - column[0] and column[0] >= 0 and column[1] >= 0 for column in transformedPoints.T]
