import pandas as pd
import numpy as np

## Create a large DataFrame with many zeros
large_df = pd.DataFrame(np.random.choice([0, 1], size=(10000, 1000), p=[0.95, 0.05]))

## Convert to SparseDataFrame
sparse_large_df = large_df.astype(pd.SparseDtype("float", fill_value=0))

print("Memory Usage of Dense DataFrame:")
print(large_df.memory_usage(deep=True).sum())
print("Memory Usage of Sparse DataFrame:")
print(sparse_large_df.memory_usage(deep=True).sum())
