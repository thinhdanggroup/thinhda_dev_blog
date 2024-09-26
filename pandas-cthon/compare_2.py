from timeit import timeit

import pandas as pd
import numpy as np
from Cython import inline

# Sample DataFrame
df = pd.DataFrame({"A": np.random.rand(100000)})


# Complex numerical function
def complex_computation(x):
    result = 0
    for i in range(100):
        result += np.sin(x) * np.cos(x)
    return result


# Using pandas apply with pure Python
total_time = timeit(
    lambda: df["A"].apply(complex_computation),
    number=10,
)
print(f"Total time: {total_time:.4f} seconds")

# Cython version of the function
cython_code = """
from math import sin, cos

def cython_complex_computation(double x):
    cdef double result = 0
    for i in range(100):
        result += sin(x) * cos(x)
    return result
"""

cython_func = inline(cython_code, force=True)

# Using pandas apply with Cython

total_time = timeit(
    lambda: df["A"].apply(cython_func),
    number=10,
)
print(f"Total time: {total_time:.4f} seconds")
