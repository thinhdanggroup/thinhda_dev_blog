import numpy as np
import pandas as pd

# create fake data.csv file
fake_df = pd.DataFrame(
    {"A": np.random.randint(0, 100, size=1000000), "B": np.random.rand(1000000)}
)
fake_df.to_csv("data.csv", index=False)
print("Memory Usage Before Loading:")
fake_df.info(memory_usage="deep")

## Specify the columns to load
use_cols = ["A"]

## Load only the specified columns
df = pd.read_csv("data.csv", usecols=use_cols)

print("Loaded Data Types:")
print(df.dtypes)
print("Memory Usage After Loading Specific Columns:")
df.info(memory_usage="deep")
