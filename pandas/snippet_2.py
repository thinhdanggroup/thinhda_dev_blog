import pandas as pd
import numpy as np

## Create a sample DataFrame
df = pd.DataFrame(
    {"A": np.random.randint(0, 100, size=1000000), "B": np.random.rand(1000000)}
)

print("Original Data Types:")
print(df.dtypes)
print("Original Memory Usage:")
print(df.memory_usage(deep=True).sum())

## Downcast numeric columns
df["A"] = pd.to_numeric(df["A"], downcast="integer")
df["B"] = pd.to_numeric(df["B"], downcast="float")

print("\nDowncasted Data Types:")
print(df.dtypes)
print("Downcasted Memory Usage:")
print(df.memory_usage(deep=True).sum())
