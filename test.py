import unittest
import math
from geometry import *
import numpy as np
from world import *
from viewport import *

MAX_VECTOR_DIFF = .0001

class TestGeometryFunctions(unittest.TestCase):
    def test_find_reflection(self):
        incident = np.array([0, 0, -1])
        normal = np.array([0, 0, 1])
        reflection = np.array([0, 0, 1])
        self.assertTrue((findReflection(incident, normal) == reflection).all())

        # should still work even if normal points the other way
        incident2 = np.array([0, 0, -1])
        normal2 = np.array([0, 0, -1])
        reflection2 = np.array([0, 0, 1])
        self.assertTrue((findReflection(incident2, normal2) == reflection2).all())

        # test at a funny angle
        incident3 = np.array([1, 0, -1])
        normal3 = np.array([0, 0, 1])
        reflection3 = np.array([1, 0, 1])
        self.assertTrue((findReflection(incident3, normal3) == reflection3).all())

    def test_find_normal(self):
        points = np.array([[0, 0, 0], [0, 10, 0], [-10, 10, 0]])
        expectedNormal = np.array([0, 0, 1])
        self.assertTrue((findNormal(points) ==  expectedNormal).all())

    def test_find_refraction(self):
        incident = np.array([0, 0, -1])
        normal = np.array([0, 0, 1])

        # no change in light because incident was normal to surface
        self.assertTrue((findRefraction(incident, normal, 1, 1) == incident).all())
        self.assertTrue((findRefraction(incident, normal, 10, 1) == incident).all())

        # if indices are the same, there is no change in light's path
        incident2 = np.array([1, 1, 0])
        self.assertTrue((findRefraction(incident2, normal, 1, 1) == incident2).all())

    def test_ray_plane_intersection(self):
        # ray points into board
        rayPoint = np.array([0, 0, 10])
        rayDirection = np.array([0, 0, -1])
        planeNormal = np.array([-1, 0, -1])
        planePoint = np.array([-5, 0, 0])

        # checks a normal intersection
        expected = np.array([0, 0, -5])
        result = rayPlaneIntersection(planePoint, planeNormal, rayPoint, rayDirection)
        self.assertTrue(np.array_equal(result, expected))

        # ray is pointing wrong way; intersection never occurs
        result2 = rayPlaneIntersection(planePoint, planeNormal, rayPoint, np.array([0, 0, 1]))
        self.assertTrue(np.array_equal(result2, np.array([])))

    def test_ray_plane_intersection_exception(self):
        ''' make sure that parallel plane and ray raises ValueError '''
        # ray points into board
        rayPoint = np.array([0, 0, 10])
        rayDirection = np.array([0, 0, 1])
        planeNormal = np.array([1, 0, 0])
        planePoint = np.array([-5, 0, 0])

        # make sure that
        with self.assertRaises(ValueError):
            rayPlaneIntersection(planePoint, planeNormal, rayPoint, rayDirection)

    def test_point_in_triangle(self):
        A = np.array([0, 0, 0])
        B = np.array([0, 10, 0])
        C = np.array([10, 10, 0])

        inTriangle = np.array([1, 2, 0])
        edgeTriangle = np.array([0, 1, 0])
        outTriangle = np.array([-1, 0, 0])

        self.assertTrue(pointInTriangle(A, B, C, inTriangle))
        self.assertTrue(pointInTriangle(A, B, C, edgeTriangle))
        self.assertFalse(pointInTriangle(A, B, C, outTriangle))

    def test_check_intersection(self):
        firstTriangle = np.array([[1, 0, 0], [10, 0, 0], [10, 10, 0]]) # misses
        secondTriangle = np.array([[0, 0, 0], [0, 0, 10], [0, 10, 10]]) # misses, plane is paralell to ray
        thirdTriangle = np.array([[-5, -5, 0], [5, 10, 0], [5, -5, 0]]) # hits

        rayPosition = np.array([0, 0, 1])
        rayDirection = np.array([0, 0, -1])

        self.assertFalse(checkIntersection(firstTriangle, rayPosition, rayDirection))
        self.assertFalse(checkIntersection(secondTriangle, rayPosition, rayDirection))
        self.assertTrue(checkIntersection(thirdTriangle, rayPosition, rayDirection))

class TestWorldClass(unittest.TestCase):
    def test_setup_world(self):
        ''' makes sure all methods work '''
        w = World()
        obj = Object3D('./triangle.stl', createOpaqueMaterial((0, 0, 0)))
        w.addObject(obj, np.array([0, 0, 0]))


    def test_triangle_iterator(self):
        ''' makes sure triangle iterator works '''
        w = World()
        opaqueMaterial = createOpaqueMaterial((0, 0, 0))
        transparentMaterial = createTransparentMaterial(1)

        # this STL contains only this triangle:
        #   [  0.,   0.,  10.],
        #   [ 10.,   0.,  10.],
        #   [ 10.,  10.,  10.]
        opaqueObject = Object3D('./triangle.stl', opaqueMaterial)
        transparentObject = Object3D('./triangle.stl', transparentMaterial)

        w.addObject(opaqueObject, np.array([0, 0, 0]))
        w.addObject(transparentObject, np.array([1, 1, 1])) # shift object a bit

        # use triangle iterator to get an array of triangles
        triangleList = [i for i in w.triangles()]

        # make sure that vertices are right
        self.assertTrue(np.array_equal(triangleList[0][0], np.array([[0, 0, 10], [10, 0, 10], [10, 10, 10]])))
        self.assertTrue(np.array_equal(triangleList[1][0], np.array([[1, 1, 11], [11, 1, 11], [11, 11, 11]])))

        # make sure that materials are right
        self.assertEqual(triangleList[0][1], opaqueMaterial)
        self.assertEqual(triangleList[1][1], transparentMaterial)

    def test_find_first_intersection(self):
        ''' creates a world, and finds intersections in this world '''
        w = World()
        material = createOpaqueMaterial((0, 0, 0))
        obj = Object3D('./triangle.stl', material)

        w.addObject(obj, np.array([0, 0, 0]))
        w.addObject(obj, np.array([0, 0, -1])) # shift object a bit

        # intersects with second triangle
        intersection = w.findFirstIntersection(np.array([0, 0, 0]), np.array([0, 0, 1]))
        self.assertTrue(np.array_equal(intersection.point, np.array([0, 0, 9])))

        # ray is pointing wrong way; no intersection
        intersection = w.findFirstIntersection(np.array([0, 0, 0]), np.array([0, 0, -1]))
        self.assertEqual(intersection, None)

        # intersects with first triangle
        intersection = w.findFirstIntersection(np.array([0, 0, 11]), np.array([0, 0, -1]))
        self.assertTrue(np.array_equal(intersection.point, np.array([0, 0, 10])))

class TestViewPortClass(unittest.TestCase):
    def test_constructor(self):
        view = ViewPort(np.array([0, 0, 0]), np.array([10, 10, 0]), np.array([10, 0, 0]), 5)

        self.assertTrue(np.array_equal(np.array([5, 5, 5]), view.eyePoint))
        self.assertEqual(view.width, 10)
        self.assertEqual(view.height, 10)

    def test_get_ray(self):
        view = ViewPort(np.array([0, 0, 0]), np.array([10, 10, 0]), np.array([10, 0, 0]), 5)

        # check one ray
        rayCoordinate, rayDirection = view.getRay(0, 5)
        # make sure that the coordinate is right
        self.assertTrue(np.array_equal(rayCoordinate, np.array([0, 5, 0])))
        # make sure direction is right, account for floating point math
        self.assertAlmostEqual(rayDirection[0], -1 / math.sqrt(2))
        self.assertAlmostEqual(rayDirection[1], 0)
        self.assertAlmostEqual(rayDirection[2], -1 / math.sqrt(2))

        # should get an error because this is out of bounds
        with self.assertRaises(IndexError):
            view.getRay(10, 11)


        # check a different ray
        rayCoordinate, rayDirection = view.getRay(10, 0)
        # make sure that the coordinate is right
        self.assertTrue(np.array_equal(rayCoordinate, np.array([10, 0, 0])))
        # make sure direction is right, account for floating point math
        self.assertAlmostEqual(rayDirection[0], 1 / math.sqrt(3))
        self.assertAlmostEqual(rayDirection[1], -1 / math.sqrt(3))
        self.assertAlmostEqual(rayDirection[2], -1 / math.sqrt(3))


# only run tests if this file was explicitely run
if __name__ == '__main__':
    unittest.main()
