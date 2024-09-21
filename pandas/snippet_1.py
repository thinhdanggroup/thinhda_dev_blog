import pandas as pd

## Sample DataFrame
data = {
    "A": range(1000),
    "B": [x * 2.5 for x in range(1000)],
    "C": ["foo" for _ in range(1000)],
}
df = pd.DataFrame(data)

## Summary of the DataFrame, including memory usage
print("=== Summary of the DataFrame before conversion ===")
print(df.memory_usage(deep=True).sum())

df["A"] = pd.to_numeric(df["A"], downcast="integer")
df["B"] = pd.to_numeric(df["B"], downcast="float")
df["C"] = df["C"].astype("category")

print("=== Summary of the DataFrame after conversion ===")
print(df.memory_usage(deep=True).sum())
