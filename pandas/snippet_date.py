import numpy as np
import pandas as pd

# create fake data.csv file
fake_df = pd.DataFrame(
    {
        "A": np.random.randint(0, 100, size=1000000),
        "B": np.random.rand(1000000),
        "dates": pd.date_range(start="1/1/2020", periods=1000000, freq="H"),
    }
)
fake_df.to_csv("data.csv", index=False)
print("Memory Usage Before Loading:")
fake_df.info(memory_usage="deep")
## Load data without date parsing
df = pd.read_csv("data.csv")

print("Memory Usage Without Parsing Dates:")
df.info(memory_usage="deep")

## Load data with date parsing
df = pd.read_csv("data.csv", parse_dates=["dates"])

print("Memory Usage With Parsing Dates:")
df.info(memory_usage="deep")
