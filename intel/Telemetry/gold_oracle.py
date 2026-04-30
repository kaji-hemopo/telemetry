#!/usr/bin/env python3
"""Gold Oracle - Fetches XAU/USD (Gold) price data and saves to raw_gold_oracle.json"""

import json
import urllib.request
import ssl
from datetime import datetime, timezone, timedelta

RAW_PATH = "/Users/jacksonhemopo/.openclaw/workspace_ito/intel/Telemetry/raw/raw_gold_oracle.json"

JST = timezone(timedelta(hours=9))

def fetch_gold_price():
    """Fetch gold price from Yahoo Finance via API."""
    url = "https://query1.finance.yahoo.com/v8/finance/chart/GC%3DF?interval=1d&range=2d"
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json",
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
    except Exception as e:
        # Fallback: try alternative approach or raise
        raise Exception(f"Failed to fetch gold data: {e}")
    
    chart = data["chart"]["result"][0]
    meta = chart["meta"]
    
    current_price = meta.get("regularMarketPrice", meta.get("previousClose"))
    prev_close = meta.get("previousClose")
    
    # Get high/low from current day
    high = meta.get("regularMarketDayHigh", current_price)
    low = meta.get("regularMarketDayLow", current_price)
    
    # Try to get previous close for change calculation
    result = chart.get("result", [{}])
    if result:
        indicators = result[0].get("indicators", {})
        quote = indicators.get("quote", [{}])[0]
        closes = quote.get("close", [])
        if len(closes) >= 2:
            prev_close = closes[-2]
            current_price = closes[-1] if closes[-1] else current_price
    
    if not current_price:
        raise Exception("Could not determine current price")
    
    if not prev_close:
        prev_close = current_price
    
    change_pct = ((current_price - prev_close) / prev_close) * 100 if prev_close else 0
    
    return {
        "symbol": "XAU/USD",
        "price": round(float(current_price), 2),
        "change_24h_pct": round(float(change_pct), 3),
        "high_24h": round(float(high), 2),
        "low_24h": round(float(low), 2),
        "source": "Yahoo Finance (GC=F)"
    }

def main():
    timestamp_jst = datetime.now(JST).strftime("%Y-%m-%d %H:%M JST")
    
    try:
        gold_data = fetch_gold_price()
        
        output = {
            "generated_at_jst": timestamp_jst,
            "gold": gold_data
        }
        
        with open(RAW_PATH, "w") as f:
            json.dump(output, f, indent=2)
        
        print(f"[Gold Oracle] Updated at {timestamp_jst}")
        print(f"  Price: ${gold_data['price']} | Change: {gold_data['change_24h_pct']}%")
        
    except Exception as e:
        print(f"[Gold Oracle] Error: {e}")
        raise

if __name__ == "__main__":
    main()
