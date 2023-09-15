import requests
from datetime import datetime
from pe_ratio import retrieve_pe_ratios
import numpy as np


def retrieve_historical(ticker: str) -> dict:
    path_params = {
        "assetclass": "etf",
        "fromdate": "2013-06-20",
        "todate": "2023-09-03",
        "limit": "9999",
    }

    headers = {
        "Accept": "application/json,text/plain,*/*",
        "Cache-Control": "no-cache",
        "Dnt": "1",
        "Origin": "https://www.nasdaq.com",
        "Referer": "https://www.nasdaq.com",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.51",
    }

    return requests.get(
        f"https://api.nasdaq.com/api/quote/{ticker}/historical",
        params=path_params,
        headers=headers,
        timeout=5,
    ).json()


def retrieve_spy_historical_data() -> list:
    pe_history = retrieve_pe_ratios()

    history = retrieve_historical("SPY")
    if (
        history is not None
        and history["data"] is not None
        and history["data"]["tradesTable"] is not None
        and history["data"]["tradesTable"]["rows"]
    ):
        history = history["data"]["tradesTable"]["rows"]

        pe_cursor = 0
        history.reverse()
        for i in range(0, len(history)):
            history[i]["date"] = datetime.strptime(
                history[i]["date"], "%m/%d/%Y"
            ).timestamp()
            history[i]["open"] = float(history[i]["open"].replace(",", ""))
            history[i]["close"] = float(history[i]["close"].replace(",", ""))
            history[i]["high"] = float(history[i]["high"].replace(",", ""))
            history[i]["low"] = float(history[i]["low"].replace(",", ""))
            if history[i]["volume"] != "N/A":
                history[i]["volume"] = int(history[i]["volume"].replace(",", ""))
            else:
                history[i]["volume"] = None
            while (
                pe_cursor < (len(pe_history) - 1)
                and history[i]["date"] > pe_history[pe_cursor + 1][0]
            ):
                pe_cursor += 1
            history[i]["pe"] = float(pe_history[pe_cursor][1])

        print("History download complete!!!")
    else:
        raise Exception("Ticker was not readable")

    return history


"""
 0 - 90 day gain
 1 - 60 day gain
 2 - 30 day gain
 3 - 15 day gain
 4 - 12 day gain
 5 - 10 day gain
 6 - 7 day gain
 7 - 3 day gain
 8 - Previous day close
 9 - Previous day open
 10 - Previous day high
 11 - Previous day low
 12 - Current day open
 13 - P/E ratio
"""


def gain(history, index, days):
    return (history[index]["open"] - history[index - days]["close"]) / history[
        index - days
    ]["close"]


def retrieve_ticker_data() -> (list, list):
    history = retrieve_spy_historical_data()
    symbol_data = []
    for i in range(90, len(history)):
        _90_day_gain = gain(history, i, 90)
        _60_day_gain = gain(history, i, 60)
        _30_day_gain = gain(history, i, 30)
        _15_day_gain = gain(history, i, 15)
        _12_day_gain = gain(history, i, 12)
        _10_day_gain = gain(history, i, 10)
        _7_day_gain = gain(history, i, 7)
        _3_day_gain = gain(history, i, 3)
        previous_close = history[i - 1]["close"]
        previous_open = history[i - 1]["open"]
        previous_high = history[i - 1]["high"]
        previous_low = history[i - 1]["low"]
        current_open = history[i]["open"]
        pe_ratio = history[i]["pe"]

        symbol_data.append(
            np.array(
                [
                    _90_day_gain,
                    _60_day_gain,
                    _30_day_gain,
                    _15_day_gain,
                    _12_day_gain,
                    _10_day_gain,
                    _7_day_gain,
                    _3_day_gain,
                    previous_close,
                    previous_open,
                    previous_high,
                    previous_low,
                    current_open,
                    pe_ratio,
                ],
                dtype=np.single,
            )
        )
    return symbol_data, history


def price_change(current, history, days):
    return (current - history[-days]["close"]) / history[-days]["close"]


def prepare_price(current: float, pe: float, history: list[list[float]]) -> list[float]:
    _90_day_gain = price_change(current, history, 90)
    _60_day_gain = price_change(current, history, 60)
    _30_day_gain = price_change(current, history, 30)
    _15_day_gain = price_change(current, history, 15)
    _12_day_gain = price_change(current, history, 12)
    _10_day_gain = price_change(current, history, 10)
    _7_day_gain = price_change(current, history, 7)
    _3_day_gain = price_change(current, history, 3)
    previous_close = history[-1]["close"]
    previous_open = history[-1]["open"]
    previous_high = history[-1]["high"]
    previous_low = history[-1]["low"]

    return np.array(
        [
            _90_day_gain,
            _60_day_gain,
            _30_day_gain,
            _15_day_gain,
            _12_day_gain,
            _10_day_gain,
            _7_day_gain,
            _3_day_gain,
            previous_close,
            previous_open,
            previous_high,
            previous_low,
            current,
            pe,
        ],
        dtype=np.single,
    )
