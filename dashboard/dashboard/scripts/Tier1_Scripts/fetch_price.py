#!/usr/bin/env python3
"""
Universal Price Oracle
Fetches live closing price for any tradable asset using yfinance
Outputs strictly the float value or "ERROR"
"""

import yfinance as yf
import sys

def fetch_live_price(ticker):
    """
    Fetch live closing price for a ticker symbol.
    Returns float price or raises exception on error.
    """
    try:
        # Get latest daily data
        ticker_obj = yf.Ticker(ticker)
        history = ticker_obj.history(period="1d")
        
        if history.empty:
            raise ValueError(f"No data available for {ticker}")
        
        # Get the most recent closing price
        price = history['Close'].iloc[-1]
        return round(float(price), 5)
        
    except Exception as e:
        raise RuntimeError(f"Failed to fetch price for {ticker}: {e}")

def main():
    """Main execution function."""
    if len(sys.argv) != 2:
        print("ERROR")
        sys.exit(1)
    
    ticker = sys.argv[1].strip()
    
    # Validate ticker format
    if not ticker or len(ticker) < 2:
        print("ERROR")
        sys.exit(1)
    
    try:
        price = fetch_live_price(ticker)
        print(price)
        sys.exit(0)
    except Exception:
        print("ERROR")
        sys.exit(1)

if __name__ == "__main__":
    main()