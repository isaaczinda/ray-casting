from geometry import normalized
import numpy as np

class ViewPort:
    ''' viewport screen that rays will be cast from '''

    def __init__(self, screenCenterPoint, targetPoint, eyeDistance, \
    screenDimensions=(25, 25), resolution=(100, 100), orientation=np.array([0, 1, 0])):

        self._eyeDistance = eyeDistance
        self.resolution = resolution
        self.screenDimensions = screenDimensions

        # points right
        horizontalVector = normalized(np.cross(targetPoint - screenCenterPoint, orientation)) * (screenDimensions[0] / 2.0)
        # points up
        verticalVector = normalized(np.cross(horizontalVector, targetPoint - screenCenterPoint)) * (screenDimensions[1] / 2.0)

        self.lowerLeft = screenCenterPoint - horizontalVector - verticalVector
        self.upperLeft = screenCenterPoint - horizontalVector + verticalVector
        self.lowerRight = screenCenterPoint + horizontalVector - verticalVector
        self.upperRight = screenCenterPoint + horizontalVector + verticalVector

        self._setup()

    def setResolution(self, resolution):
        self.resolution = resolution

    def width(self):
        ''' gets the width of the image '''
        return self.resolution[0]

    def height(self):
        ''' gets the height of the image '''
        return self.resolution[1]

    # def __init__(self, lowerLeft, upperRight, lowerRight, eyeDistance):
    #     ''' creates a new instance of ViewPort. A ViewPort is defined by
    #     a screen, with a viewer looking at the screen from some distance.
    #     '''
    #
    #     self._eyeDistance = eyeDistance
    #
    #     self.lowerLeft = lowerLeft
    #     self.upperRight = upperRight
    #     self.lowerRight = lowerRight
    #     self.upperLeft = lowerLeft + (upperRight - lowerRight)
    #
    #     self._setup()



    def _setup(self):
        ''' initializes data members because we have multiple constructors '''

        # points from screen towards eyePoint
        normal = normalized(np.cross(self.lowerRight - self.lowerLeft, \
            self.upperRight - self.lowerRight))

        # find center point in screen
        self.screenCenterPoint = ((self.upperRight - self.lowerLeft) / 2.0) \
            + self.lowerLeft

        self.eyePoint = self.screenCenterPoint + normal * self._eyeDistance

        # create vectors to be used in a parametric function that traces the entire screen
        self._horizontalVector = normalized(self.lowerRight - self.lowerLeft)
        self._verticalVector = normalized(self.upperRight - self.lowerRight)

    def getRay(self, x, y):
        ''' gets the location that a ray will be cast from, given x and y
        coord in the screen

        returns:: (coordinate, ray direction)

        raises IndexError if coordiante is out of screen
        '''

        if x > self.resolution[0] or y > self.resolution[1] or x < 0 or y < 0:
            raise IndexError("specified coordinate was out of screen")

        # the location that the ray will be cast from
        xRaySpacing = self.screenDimensions[0] / self.resolution[0]
        yRaySpacing = self.screenDimensions[1] / self.resolution[1]

        coordinate = x * self._horizontalVector * xRaySpacing + y * self._verticalVector * yRaySpacing + self.lowerLeft
        direction = normalized(coordinate - self.eyePoint)

        return (coordinate, direction)
