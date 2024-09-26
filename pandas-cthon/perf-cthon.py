import timeit

import pandas as pd

val = ""
for i in range(100):
    val += f"{i / 100},"

val = val[:-1]

## Sample DataFrame
df = pd.DataFrame({"values": [val] * 50000})

df["values"] = df["values"]


## Pure Python function for comparison
def python_recursive_calc(value, threshold):
    values = value.split(",")
    if len(values) == 1:
        return 0
    if float(values[0]) > threshold:
        return 1 + python_recursive_calc(",".join(values[1:]), threshold)
    return python_recursive_calc(",".join(values[1:]), threshold)


## Wrapper for Cython function
def apply_cython(row, threshold):
    from recursive_calculation import cython_recursive_calc

    return cython_recursive_calc(row, threshold)


## Time pure Python transformation
python_time = timeit.timeit(
    lambda: df["values"].apply(lambda row: python_recursive_calc(row, 0.5)), number=10
)
print(f"Python execution time: {python_time:.4f} seconds")

## Time Cython-enhanced transformation
cython_time = timeit.timeit(
    lambda: df["values"].apply(lambda row: apply_cython(row, 0.5)), number=10
)
print(f"Cython execution time: {cython_time:.4f} seconds")
