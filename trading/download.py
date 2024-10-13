import pandas as pd

import vnquant.data as dt


def get_stock(value: str):
    loader = dt.DataLoader(value, "2018-01-01", "2024-10-08")
    data = loader.download()
    data.head()
    # Pivot the DataFrame to get desired columns
    # Extract data for 'VIC' as a one-dimensional Series
    data = data.stack().reset_index()

    # Datetime,code,High,Low,Open,Close,Adj Close,Volume,value_match
    # Attributes,code,high,low,open,close,adjust,volume_match,value_match
    data["Datetime"] = pd.to_datetime(data["date"]) + pd.Timedelta("13:30:00")
    # include timestamp in the datetime column
    data["Datetime"] = data["Datetime"].dt.strftime("%Y-%m-%d %H:%M:%S+00:00")

    data["High"] = data["high"]
    data["Low"] = data["low"]
    data["Open"] = data["open"]
    data["Close"] = data["close"]
    data["Adj Close"] = data["adjust"]
    data["Volume"] = data["volume_match"]
    data["value_match"] = data["value_match"]
    data.reset_index()
    data.sort_values(by=["Datetime"], ascending=[True], inplace=True)
    # delete these columns date,Symbols,code,high,low,open,close,adjust,volume_match,value_match
    data = data.drop(
        columns=[
            "date",
            "high",
            "low",
            "open",
            "close",
            "adjust",
            "Symbols",
            "code",
            "volume_match",
            "value_match",
        ]
    )
    data.to_csv(f"price_data/{value}.csv", index=False)


def main():
    stocks = [
        "ACB",
        "BCM",
        "BID",
        "BVH",
        "CTG",
        "FPT",
        "GAS",
        "GVR",
        "HDB",
        "HPG",
        "MBB",
        "MSN",
        "MWG",
        "PLX",
        "POW",
        "SAB",
        "SHB",
        "SSB",
        "SSI",
        "STB",
        "TCB",
        "TPB",
        "VCB",
        "VHM",
        "VIB",
        "VIC",
        "VJC",
        "VNM",
        "VPB",
        "VRE",
        "E1VFVN30"
    ]

    for s in stocks:
        get_stock(s)


if __name__ == "__main__":
    main()
