# Point in Triangle Speed

## pointInTriangle in geometry.py

```python
import timeit

setup = '''
import numpy as np
from geometry import pointInTriangle
'''

statement = 'pointInTriangle(np.array([0, 0, 1]), np.array([0, 0, -1]), np.array([10, 0, 0]), np.array([1, 0, 0]))'

print(timeit.timeit(statement, number=1000, setup=setup))
```

speed was .122 / 1000 runs of pointInTriangle

# CUDA

https://github.com/cudamat/cudamat/blob/master/INSTALL.md
