## Create a sample DataFrame
import pandas as pd

df = pd.DataFrame(
    {"Country": ["USA", "Canada", "USA", "Mexico", "Canada", "USA"] * 100000}
)

print("Original Data Types:")
print(df.dtypes)
print("Original Memory Usage:")
df.info(memory_usage="deep")

## Convert object type to category
df["Country"] = df["Country"].astype("category")

print("\nConverted Data Types:")
print(df.dtypes)
print("Converted Memory Usage:")
df.info(memory_usage="deep")
