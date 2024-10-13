import csv
import re

import pandas as pd

FILE_NAME = "trading_results.csv"


def parse_log(data: str):
    pattern = r"Trading Results\n-+\n(.*?)End trading for (\w+)"
    matches = re.findall(pattern, data, re.DOTALL)

    # Prepare CSV data
    csv_data = []
    headers = [
        "Start date", "End date", "Duration", "Starting balance", "Ending balance",
        "Ending NAV", "Total return", "Maximum drawdown", "Total no. trades",
        "No. long trades", "No. short trades", "Total fees paid",
        "Total volume traded", "Average daily volume", "Positions still open", "Trading for"
    ]
    extra_headers = ["Return Value", "Percent Value"]

    for match in matches:
        results, trading_for = match
        lines = results.strip().split("\n")
        row = {}
        for line in lines:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            if key == "Total return":
                return_value, percent_value = re.match(r"\$(.*?) \((.*?)%\)", value).groups()
                row["Return Value"] = return_value
                row["Percent Value"] = percent_value
            else:
                row[key] = value
        row["Trading for"] = trading_for

        csv_data.append(row)

        for key in row.keys():
            if key not in headers and key not in extra_headers:
                headers.append(key)
                headers = list(set(headers))

    # Write to CSV
    with open(FILE_NAME, "w", newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=headers + extra_headers)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)


def main():
    with open('app.log', 'r') as file:
        data = file.read()

    parse_log(data)

    df = pd.read_csv(
        FILE_NAME
    )

    print(df["Percent Value"].mean())


if __name__ == "__main__":
    main()
