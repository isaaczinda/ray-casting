import math

# maximum ammount that two angles can vary and still be called equal
MAX_EQUAL_DIFF = .001


class TestAngleClass(unittest.TestCase):
    def test_equality(self):
        a1 = Angle(1, 1)
        a2 = Angle(1, 1)
        a3 = Angle(1, 2)
        a4 = Angle(1.000001, 1)

        self.assertTrue(a1 == a2)
        self.assertFalse(a1 == a3)
        self.assertTrue(a1 == a4) # numbers that are very close should be equal

        # make sure that equality works even with overflow
        a5 = Angle(0, math.pi / 2 + .000001)
        a6 = Angle(0, math.pi / 2)
        self.assertEqual(a5, a6)

    def test_constructor(self):
        ''' makes sure that angle bounds are respected '''

        a1 = Angle(0, math.pi)
        a2 = Angle(0, math.pi * 3)
        a3 = Angle(math.pi, 0)

        # test phi correction
        self.assertEqual(a1, a3)
        self.assertEqual(a2, a3)

        a4 = Angle(3 * math.pi / 2.0, 3 * math.pi / 4)
        a5 = Angle(math.pi / 2.0, math.pi / 4.0)

        # test theta rotation
        self.assertEqual(a4, a5)

    def test_addition(self):
        a1 = Angle(math.pi, 0)
        a2 = Angle(math.pi, 0)
        self.assertEqual(a1 + a2, Angle(0, 0))

        a3 = Angle(0, math.pi / 4)
        a4 = Angle(0, math.pi / 4)
        self.assertEqual(a3 + a4, Angle(0, math.pi / 2))

class Angle:
    ''' stores information about orientation in 3D space '''
    def __init__(self, theta, phi):
        self.theta = theta
        self.phi = phi

        self._fixBounds()

    def __str__(self):
        ''' neatly print rotation information '''
        return str(self.theta) + ", " + str(self.phi)

    def _fixBounds(self):
        ''' makes sure that the input angles were not out of bounds '''

        # make sure phi is between pi and -pi
        self.phi = ((self.phi + math.pi) % (2 * math.pi)) - math.pi

        # if phi is out of the pi/2 to -pi/2 range, correct it by adjusting theta
        if abs(self.phi) > math.pi / 2.0:
            diff = abs(self.phi) - math.pi / 2.0 # always positive

            if self.phi > 0:
                self.phi -= 2 * diff
            else:
                self.phi += 2 * diff

            self.theta += math.pi

        # make sure that theta is within allowed bounds
        self.theta = self.theta % (2 * math.pi)

    def __add__(self, other):
        ''' add two angles together, return result '''
        return Angle(self.theta + other.theta, self.phi + other.phi)

    def __sub__(self, other):
         ''' subtract other from self '''
         return Angle(self.theta - other.theta, self.phi - other.phi)

    def __eq__(self, other):
        '''
        Test equality by converting to vectors, subtracting, then finding magnitude of result.
        '''

        firstVector = self.toVector()
        secondVector = other.toVector()
        sumVector = (firstVector[0] - secondVector[0], firstVector[1] - secondVector[1], firstVector[2] - secondVector[2])
        sumVectorMagnitude = math.sqrt(math.pow(sumVector[0], 2) + math.pow(sumVector[1], 2) + math.pow(sumVector[2], 2))

        return sumVectorMagnitude < MAX_EQUAL_DIFF

    def toVector(self):
        return (math.cos(self.theta)*math.cos(self.phi), math.sin(self.theta)*math.cos(self.phi), math.sin(self.phi))
