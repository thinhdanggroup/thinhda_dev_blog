import pandas as pd

#  13:30:00+00:00

df = pd.read_csv(
    "price_data/vnd.csv",
)
# add 13:30:00+00:00 to datetime column
df["Datetime"] = pd.to_datetime(df["Datetime"]) + pd.Timedelta("13:30:00")
# include timestamp in the datetime column
df["Datetime"] = df["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S+00:00")
df.to_csv("price_data/vnd.csv", index=False)
