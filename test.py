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

    def test_find_refraction(self):
        incident = np.array([0, 0, -1])
        normal = np.array([0, 0, 1])

        # no change in light because incident was normal to surface
        self.assertTrue((findRefraction(incident, normal, 1, 1) == incident).all())
        self.assertTrue((findRefraction(incident, normal, 10, 1) == incident).all())

        # if indices are the same, there is no change in light's path
        incident2 = np.array([1, 1, 0])
        self.assertTrue((findRefraction(incident2, normal, 1, 1) == incident2).all())


class TestViewPortClass(unittest.TestCase):
    def test_constructor(self):
        view = ViewPort(np.array([0, 0, 0]), np.array([10, 10, 0]), np.array([10, 0, 0]), 5)

        self.assertTrue(np.array_equal(np.array([5, 5, 5]), view.eyePoint))
        self.assertEqual(view.width, 10)
        self.assertEqual(view.height, 10)

    def test_get_ray(self):
        view = ViewPort(np.array([0, 0, 0]), np.array([10, 10, 0]), np.array([10, 0, 0]), 5)

        # check one ray
        ray = view.getRay(0, 5)
        # make sure that the coordinate is right
        self.assertTrue(np.array_equal(ray.point, np.array([0, 5, 0])))
        # make sure direction is right, account for floating point math
        self.assertAlmostEqual(ray.direction[0], -1 / math.sqrt(2))
        self.assertAlmostEqual(ray.direction[1], 0)
        self.assertAlmostEqual(ray.direction[2], -1 / math.sqrt(2))

        # check a different ray
        ray = view.getRay(10, 0)
        # make sure that the coordinate is right
        self.assertTrue(np.array_equal(ray.point, np.array([10, 0, 0])))
        # make sure direction is right, account for floating point math
        self.assertAlmostEqual(ray.direction[0], 1 / math.sqrt(3))
        self.assertAlmostEqual(ray.direction[1], -1 / math.sqrt(3))
        self.assertAlmostEqual(ray.direction[2], -1 / math.sqrt(3))


# only run tests if this file was explicitely run
if __name__ == '__main__':
    unittest.main()
