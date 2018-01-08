import timeit

setup = '''
import numpy as np
from geometry import pointInTriangle
'''

statement = 'pointInTriangle(np.array([0, 0, 1]), np.array([0, 0, -1]), np.array([10, 0, 0]), np.array([1, 0, 0]))'

print(timeit.timeit(statement, number=1000, setup=setup))

# for i in range(0, 10000):
