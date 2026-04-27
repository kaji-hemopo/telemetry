#!/usr/bin/env python3
"""
Generate Live Oracle JSON
Fetches live BTC, ETH, XRP (Binance) and USD/JPY (Yahoo Finance)
Outputs to workspace_ito/live_oracle.json
Used by: EPD assembler, Empire Portfolio Dashboard
"""

import requests
import yfinance as yf
import json
import os
import sys
from datetime import datetime

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(WORKSPACE, "live_oracle.json")


def fetch_btc() -> dict:
    """Fetch BTC/USDT from Binance."""
    try:
        resp = requests.get(
            "https://api.binance.com/api/v3/ticker/24hr",
            params={"symbol": "BTCUSDT"},
            headers={"Accept": "application/json"},
            timeout=10,
        )
        if resp.ok:
            d = resp.json()
            return {
                "symbol": "BTC/USD",
                "price": float(d["lastPrice"]),
                "change_24h_pct": float(d["priceChangePercent"]),
                "high_24h": float(d["highPrice"]),
                "low_24h": float(d["lowPrice"]),
                "source": "Binance",
            }
    except Exception as e:
        print(f"  BTC fetch error: {e}", file=sys.stderr)
    return {"symbol": "BTC/USD", "price": None, "change_24h_pct": None, "source": "Binance"}


def fetch_eth() -> dict:
    """Fetch ETH/USDT from Binance."""
    try:
        resp = requests.get(
            "https://api.binance.com/api/v3/ticker/24hr",
            params={"symbol": "ETHUSDT"},
            headers={"Accept": "application/json"},
            timeout=10,
        )
        if resp.ok:
            d = resp.json()
            return {
                "symbol": "ETH/USD",
                "price": float(d["lastPrice"]),
                "change_24h_pct": float(d["priceChangePercent"]),
                "high_24h": float(d["highPrice"]),
                "low_24h": float(d["lowPrice"]),
                "source": "Binance",
            }
    except Exception as e:
        print(f"  ETH fetch error: {e}", file=sys.stderr)
    return {"symbol": "ETH/USD", "price": None, "change_24h_pct": None, "source": "Binance"}


def fetch_xrp() -> dict:
    """Fetch XRP/USDT from Binance."""
    try:
        resp = requests.get(
            "https://api.binance.com/api/v3/ticker/24hr",
            params={"symbol": "XRPUSDT"},
            headers={"Accept": "application/json"},
            timeout=10,
        )
        if resp.ok:
            d = resp.json()
            return {
                "symbol": "XRP/USD",
                "price": float(d["lastPrice"]),
                "change_24h_pct": float(d["priceChangePercent"]),
                "high_24h": float(d["highPrice"]),
                "low_24h": float(d["lowPrice"]),
                "source": "Binance",
            }
    except Exception as e:
        print(f"  XRP fetch error: {e}", file=sys.stderr)
    return {"symbol": "XRP/USD", "price": None, "change_24h_pct": None, "source": "Binance"}


def fetch_usd_jpy() -> dict:
    """Fetch USD/JPY from Yahoo Finance."""
    try:
        ticker = yf.Ticker("USDJPY=X")
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = float(hist["Close"].iloc[-1])
            prev = float(hist["Open"].iloc[-1]) if len(hist) > 1 else price
            change_pct = ((price - prev) / prev * 100) if prev else 0
            return {
                "symbol": "USD/JPY",
                "price": round(price, 3),
                "change_24h_pct": round(change_pct, 3),
                "source": "Yahoo Finance",
            }
    except Exception as e:
        print(f"  USD/JPY fetch error: {e}", file=sys.stderr)
    return {"symbol": "USD/JPY", "price": None, "change_24h_pct": None, "source": "Yahoo Finance"}


def main():
    print("Fetching live oracle data...")
    print("  BTC...", end=" ")
    btc = fetch_btc()
    print(f"${btc['price']}" if btc["price"] else "FAILED")

    print("  ETH...", end=" ")
    eth = fetch_eth()
    print(f"${eth['price']}" if eth["price"] else "FAILED")

    print("  XRP...", end=" ")
    xrp = fetch_xrp()
    print(f"${xrp['price']}" if xrp["price"] else "FAILED")

    print("  USD/JPY...", end=" ")
    jpy = fetch_usd_jpy()
    print(f"{jpy['price']}" if jpy["price"] else "FAILED")

    oracle = {
        "generated_at_jst": datetime.now().strftime("%Y-%m-%d %H:%M JST"),
        "btc": btc,
        "eth": eth,
        "xrp": xrp,
        "usd_jpy": jpy,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(oracle, f, indent=2)
    print(f"\nWritten to {OUTPUT_PATH}")
    print(f"Done. BTC=${btc.get('price')}, ETH=${eth.get('price')}, XRP=${xrp.get('price')}, USD/JPY={jpy.get('price')}")


if __name__ == "__main__":
    main()
