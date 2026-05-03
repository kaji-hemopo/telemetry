#!/usr/bin/env python3
"""
Generate Live Oracle JSON
Fetches live BTC, ETH, XRP (Binance), USD/JPY, Brent, Gold (Yahoo Finance)
Outputs to workspace_ito/live_oracle.json
Used by: EPD assembler, Empire Portfolio Dashboard, Kaji Oil Shock Monitor
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


def fetch_brent() -> dict:
    """Fetch Brent Crude (BZ=F) from Yahoo Finance — REST API fallback for delisted/suspended tickers."""
    # Try yfinance first (Ticker.history)
    try:
        ticker = yf.Ticker("BZ=F")
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = float(hist["Close"].iloc[-1])
            prev = float(hist["Open"].iloc[-1]) if len(hist) > 1 else price
            change_pct = ((price - prev) / prev * 100) if prev else 0
            return {
                "symbol": "Brent",
                "price": round(price, 2),
                "change_24h_pct": round(change_pct, 3),
                "source": "Yahoo Finance (BZ=F)",
            }
    except Exception as e:
        print(f"  Brent yfinance error: {e}", file=sys.stderr)
    # Fallback: REST API for BZ=F
    try:
        resp = requests.get(
            "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F",
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        if resp.ok:
            data = resp.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                price = result[0].get("meta", {}).get("regularMarketPrice")
                if price:
                    return {
                        "symbol": "Brent",
                        "price": float(price),
                        "change_24h_pct": None,
                        "source": "Yahoo Finance REST (BZ=F)",
                    }
    except Exception as e:
        print(f"  Brent REST error: {e}", file=sys.stderr)
    return {"symbol": "Brent", "price": None, "change_24h_pct": None, "source": "Yahoo Finance (BZ=F)"}


def fetch_gold() -> dict:
    """Fetch Gold (GC=F) from Yahoo Finance — REST API fallback for delisted/suspended tickers."""
    # Try yfinance first (Ticker.history)
    try:
        ticker = yf.Ticker("GC=F")
        hist = ticker.history(period="1d")
        if not hist.empty:
            price = float(hist["Close"].iloc[-1])
            prev = float(hist["Open"].iloc[-1]) if len(hist) > 1 else price
            change_pct = ((price - prev) / prev * 100) if prev else 0
            return {
                "symbol": "Gold",
                "price": round(price, 2),
                "change_24h_pct": round(change_pct, 3),
                "source": "Yahoo Finance (GC=F)",
            }
    except Exception as e:
        print(f"  Gold yfinance error: {e}", file=sys.stderr)
    # Fallback: REST API for GC=F
    try:
        resp = requests.get(
            "https://query1.finance.yahoo.com/v8/finance/chart/GC=F",
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"},
        )
        if resp.ok:
            data = resp.json()
            result = data.get("chart", {}).get("result", [])
            if result:
                price = result[0].get("meta", {}).get("regularMarketPrice")
                if price:
                    return {
                        "symbol": "Gold",
                        "price": float(price),
                        "change_24h_pct": None,
                        "source": "Yahoo Finance REST (GC=F)",
                    }
    except Exception as e:
        print(f"  Gold REST error: {e}", file=sys.stderr)
    return {"symbol": "Gold", "price": None, "change_24h_pct": None, "source": "Yahoo Finance (GC=F)"}


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

    print("  Brent...", end=" ")
    brent = fetch_brent()
    print(f"${brent['price']}" if brent["price"] else "FAILED")

    print("  Gold...", end=" ")
    gold = fetch_gold()
    print(f"${gold['price']}" if gold["price"] else "FAILED")

    oracle = {
        "generated_at_jst": datetime.now().strftime("%Y-%m-%d %H:%M JST"),
        "btc": btc,
        "eth": eth,
        "xrp": xrp,
        "usd_jpy": jpy,
        "brent": brent,
        "gold": gold,
    }

    with open(OUTPUT_PATH, "w") as f:
        json.dump(oracle, f, indent=2)
    print(f"\nWritten to {OUTPUT_PATH}")
    print(f"Done. BTC=${btc.get('price')}, ETH=${eth.get('price')}, XRP=${xrp.get('price')}, USD/JPY={jpy.get('price')}, Brent=${brent.get('price')}, Gold=${gold.get('price')}")


if __name__ == "__main__":
    main()
    # Post-oracle Brent escalation check
    import subprocess as _subprocess, sys as _sys
    try:
        _r = _subprocess.run(
            ["/opt/homebrew/bin/python3",
             "/Users/jacksonhemopo/.openclaw/workspace_kaji/scripts/brent_escalation_monitor.py"],
            capture_output=True, text=True, timeout=30
        )
        if _r.returncode == 0:
            _lines = _r.stdout.strip().split("\n")
            print("\n[escalation] " + (_lines[-1] if _lines else ""))
        else:
            print(f"\n[escalation] WARNING non-zero exit: {_r.stderr.strip()}")
    except Exception as _e:
        print(f"\n[escalation] skip: {_e}")
