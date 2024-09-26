import pandas as pd
import numpy as np
import time

from cython_functions import csquare

## Sample DataFrame
df = pd.DataFrame({"A": np.random.rand(100000000)})


## Pure Python function
def square(x):
    return x * x


## Timing pure Python
start_time = time.time()
df["B"] = df["A"].apply(square)
python_time = time.time() - start_time

## Timing Cython
start_time = time.time()
df["B"] = df["A"].apply(csquare)
cython_time = time.time() - start_time

print(f"Pure Python Time: {python_time:.4f} seconds")
print(f"Cython Time: {cython_time:.4f} seconds")
