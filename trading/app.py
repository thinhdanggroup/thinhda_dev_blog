import os
from multiprocessing import Process

from autotrader import AutoTrader
import yaml


def trade():
    # Create AutoTrader instance, configure it, and run backtest
    at = AutoTrader()
    at.configure(
        verbosity=1,
        show_plot=False,
        home_dir="src",
        # feed="yahoo",
    )
    at.add_data(
        data_dict={
            "ACB": "ACB.csv",
            "BCM": "BCM.csv",
            "BID": "BID.csv",
            "BVH": "BVH.csv",
            "CTG": "CTG.csv",
            "FPT": "FPT.csv",
            "GAS": "GAS.csv",
            "GVR": "GVR.csv",
            "HDB": "HDB.csv",
            "HPG": "HPG.csv",
            "MBB": "MBB.csv",
            "MSN": "MSN.csv",
            "MWG": "MWG.csv",
            "PLX": "PLX.csv",
            "POW": "POW.csv",
            "SAB": "SAB.csv",
            "SHB": "SHB.csv",
            "SSB": "SSB.csv",
            "SSI": "SSI.csv",
            "STB": "STB.csv",
            "TCB": "TCB.csv",
            "TPB": "TPB.csv",
            "VCB": "VCB.csv",
            "VHM": "VHM.csv",
            "VIB": "VIB.csv",
            "VIC": "VIC.csv",
            "VJC": "VJC.csv",
            "VNM": "VNM.csv",
            "VPB": "VPB.csv",
            "VRE": "VRE.csv",
            "E1VFVN30": "E1VFVN30.csv",
        }
    )

    at.add_strategy("long_ema_crossover")
    # at.add_strategy("ema_crossover")fachù chứ
    # at.add_strategy("macd")
    # at.backtest(start="1/6/2023", end="1/2/2024", localize_to_utc=True)
    # "2020-01-01", "2024-04-02"
    at.backtest(start="1/1/2018", end="7/10/2024", localize_to_utc=True)
    at.virtual_account_config(initial_balance=10000, leverage=30)
    at.run()


def get_stock_id():
    return [
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


def get_report_file_name(stock_id) -> str:
    return f"{stock_id}-backtest-chart.html"


def main():
    # Read the YAML file
    with open('config/long_ema_crossover_template.yaml', 'r') as file:
        data = yaml.safe_load(file)

    stock_ids = get_stock_id()
    for stock_id in stock_ids:
        data['WATCHLIST'] = [stock_id]
        with open('src/config/long_ema_crossover.yaml', 'w') as file:
            yaml.dump(data, file)
        print("Start trading for", stock_id, "----------------------------------------------")

        trade()

        # os.rename(get_report_file_name(stock_id), f"output/{stock_id}.csv")

        print("End trading for", stock_id, "----------------------------------------------")


if __name__ == "__main__":
    main()
