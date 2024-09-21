from guppy import hpy
import pandas as pd


def create_large_dataframe():
    # Create a large DataFrame with random data
    df = pd.DataFrame({"A": range(1000000), "B": range(1000000)})
    return df


if __name__ == "__main__":
    hp = hpy()
    hp.setrelheap()  # Set the reference point for memory usage

    df = create_large_dataframe()

    heap = hp.heap()  # Get the current heap status
    print(heap)
