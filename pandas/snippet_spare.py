import pandas as pd
import numpy as np

## Create a regular Series with many zeros
data = pd.Series([0, 0, 1, 0, 2, 0, 0, 3, 0] * 100000)
print("\nMemory Usage of Regular Series:")
data.info(memory_usage="deep")

## Convert to SparseSeries
sparse_data = data.astype(pd.SparseDtype("float", fill_value=0))

print("\nMemory Usage of Sparse Series:")
sparse_data.info(memory_usage="deep")


print("=========================================")

## Create a regular DataFrame with many zeros
df = pd.DataFrame(
    {
        "A": [0, 0, 1, 0, 2] * 100000,
        "B": [0, 3, 0, 0, 0] * 100000,
        "C": [0, 0, 0, 4, 0] * 100000,
    }
)

print("\nMemory Usage of Regular DataFrame:")
df.info(memory_usage="deep")

## Convert to SparseDataFrame
sparse_df = df.astype(pd.SparseDtype("float", fill_value=0))

print("\nMemory Usage of Sparse DataFrame:")
sparse_df.info(memory_usage="deep")
