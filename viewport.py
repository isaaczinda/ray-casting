from geometry import normalized
import numpy as np

class Ray:
    def __init__(self, point, direction):
        self.point = point
        self.direction = direction

    def __str__(self):
        return "Ray: " + str(self.point) + ", " + str(self.direction)

class ViewPort:
    ''' creates a viewport screen that rays will be cast from.
    Precalculates the paths that all rays will take on creation.
    '''

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

        self._precalculateRays()


    def getRay(self, x, y):
        ''' Gets the location that a ray will be cast from, given x and y
        coord in the screen. The rays have been precalcualted for speed.
        Returns Ray object.
        '''

        return self._rays[x][y]

    def _precalculateRays(self):
        # create array that will contain all ray information
        self._rays = []

        for x in range(self.width()):
            self._rays.append([])

            for y in range(self.height()):
                # the location that the ray will be cast from
                xRaySpacing = self.screenDimensions[0] / self.resolution[0]
                yRaySpacing = self.screenDimensions[1] / self.resolution[1]

                coordinate = x * self._horizontalVector * xRaySpacing + y * self._verticalVector * yRaySpacing + self.lowerLeft
                direction = normalized(coordinate - self.eyePoint)

                # [y, x] because we select row, then column
                self._rays[x].append(Ray(coordinate, direction))

# run some tests!
if __name__ == '__main__':
    view = ViewPort(np.array([0, 0, 10]), np.array([0, 0, 0]), 10)

    print(view.getRay(50, 50))
