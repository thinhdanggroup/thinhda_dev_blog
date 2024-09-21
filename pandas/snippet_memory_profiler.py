from memory_profiler import profile
import pandas as pd


@profile
def create_large_dataframe():
    # Create a large DataFrame with random data
    df = pd.DataFrame({"A": range(1000000), "B": range(1000000)})
    return df


if __name__ == "__main__":
    df = create_large_dataframe()
