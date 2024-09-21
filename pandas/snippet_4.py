import numpy as np
import pandas as pd

# create fake data.csv file
fake_df = pd.DataFrame(
    {"A": np.random.randint(0, 100, size=1000000), "B": np.random.rand(1000000)}
)
fake_df.to_csv("data.csv", index=False)
print("Memory Usage Before Loading:")
fake_df.info(memory_usage="deep")

## Specify data types for each column
dtype_spec = {"A": "int32", "B": "float32"}

## Load data with specified data types
df = pd.read_csv("data.csv", dtype=dtype_spec)

print("Data Types After Loading:")
print(df.dtypes)
print("Memory Usage After Loading:")
df.info(memory_usage="deep")
