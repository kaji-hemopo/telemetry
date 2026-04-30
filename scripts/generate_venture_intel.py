#!/usr/bin/env python3
"""
Generate Venture Intelligence Report
Fetches live Brent Crude (CoinGecko) + Gold (yfinance GC=F)
Reads curated venture ideas (hardcoded from Ito's vetted database)
Outputs to agents/ito/venture_intel.md
"""

import requests
import yfinance as yf
import os
import sys
from datetime import datetime

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_PATH = os.path.join(WORKSPACE, "outputs", "venture_intel.md")

# ---------------------------------------------------------------------------
# Venture Ideas — Ito's vetted micro-SaaS database (curated for Jackson)
# ---------------------------------------------------------------------------
VENTURE_IDEAS = [
    {
        "score": 90,
        "name": "SaaS Integration Health Monitor & Alerting System",
        "summary": "A monitoring service that tracks the health and latency of critical B2B SaaS API integrations (e.g., Stripe -> QuickBooks, Salesforce -> HubSpot). Detects failures, schema changes, or rate limit issues before they cascade.",
        "tags": "Integration, API, Monitoring, DevOps, Automation",
        "empire_score": "$900000",
        "capital": "$25,000",
        "status": "Idea",
    },
    {
        "score": 88,
        "name": "Legacy ERP to Modern SaaS Data Migration Bridge",
        "summary": "A specialized ETL tool focused on migrating specific, complex data objects (customer records, inventory items, bills of materials) from legacy on-premise ERP systems to modern SaaS platforms with zero data loss guarantees.",
        "tags": "Integration, Data Migration, Legacy Systems, ETL, B2B",
        "empire_score": "$880000",
        "capital": "$25,000",
        "status": "Idea",
    },
    {
        "score": 85,
        "name": "Remote Work Hour Tracker API for Cross-Border Tax Compliance",
        "summary": "A micro-SaaS providing a standardized API for remote workers to log billable hours with geolocation and activity tagging, generating audit-ready reports formatted for international tax jurisdictions.",
        "tags": "Compliance, Remote Work, API, Reporting, Automation",
        "empire_score": "$850000",
        "capital": "$25,000",
        "status": "Idea",
    },
    {
        "score": 82,
        "name": "Multi-Currency Expense Reconciliation Engine for Nomadic Teams",
        "summary": "A backend service that automates reconciliation of expenses submitted in multiple currencies (AUD, USD, NZD, JPY) against company budgets and bank feeds, handling volatile exchange rates and calculating true-cost-per-transaction.",
        "tags": "Workflow, Finance, Multi-Currency, Automation, SaaS",
        "empire_score": "$820000",
        "capital": "$25,000",
        "status": "Idea",
    },
    {
        "score": 80,
        "name": "Fuel Cost Attribution & Reconciliation Tool for Distributed Teams",
        "summary": "A tool that ingests fuel price APIs, commute distance data (from Google Maps), and payroll/expense systems to automatically calculate and allocate fuel cost impacts or support allowances for distributed remote teams.",
        "tags": "Administrative, API Integration, Payroll, Automation, Data",
        "empire_score": "$800000",
        "capital": "$25,000",
        "status": "Idea",
    },
]

# ---------------------------------------------------------------------------
# Data fetchers
# ---------------------------------------------------------------------------

def fetch_brent() -> tuple[float, float]:
    """Fetch Brent Crude — primary: CoinGecko spot, fallback: yfinance BZ=F futures.
    Sanity check: CoinGecko Brent below $80/bbl is considered stale/rate-limited.
    """
    # Primary: CoinGecko (spot Brent)
    try:
        resp = requests.get(
            "https://api.coingecko.com/api/v3/simple/price",
            params={"ids": "crude-oil-brent", "vs_currencies": "usd"},
            headers={"Accept": "application/json"},
            timeout=10,
        )
        if resp.ok:
            data = resp.json()
            price = float(data["crude-oil-brent"]["usd"])
            # Sanity: Brent rarely drops below $40; $80 is a safe floor to detect stale/rate-limited responses
            if price and price >= 80:
                return price, 0.0
            else:
                print(f"    CoinGecko returned suspicious Brent ${price} — treating as stale, trying fallbacks", file=sys.stderr)
    except Exception as e:
        print(f"    CoinGecko error: {e}", file=sys.stderr)
    # Fallback 1: yfinance BZ=F (Brent Crude Jun 2026 futures — approximate spot)
    try:
        bz = yf.Ticker("BZ=F")
        hist = bz.history(period="1d")
        if not hist.empty:
            futures_price = float(hist["Close"].iloc[-1])
            print(f"    yfinance BZ=F (futures): ${futures_price:.2f}")
            return futures_price, 0.0
    except Exception as e:
        print(f"    yfinance BZ=F error: {e}", file=sys.stderr)
    return None, None


def fetch_gold() -> tuple[float, float]:
    """Fetch Gold spot price — primary: yfinance GC=F (gold futures), fallback: GLD ETF."""
    for ticker_sym in ["GC=F", "GLD"]:
        try:
            ticker = yf.Ticker(ticker_sym)
            hist = ticker.history(period="1d")
            if not hist.empty:
                price = float(hist["Close"].iloc[-1])
                # GLD is 1/10 the price of spot gold
                if ticker_sym == "GLD":
                    price = price * 10
                return round(price, 2), 0.0
        except Exception:
            pass
    return None, None


def generate_bar(score: int) -> str:
    filled = score // 10
    empty = 10 - filled
    return "█" * filled + "░" * empty


def format_idea(idea: dict) -> str:
    score = idea["score"]
    bar = generate_bar(score)
    return f"""### {score} — {idea['name']}
{'█' * (score // 10)}{'░' * (10 - score // 10)} `{score}/100`
{'⭐ High score' if score >= 85 else ''}
- **Summary:** {idea['summary']}
- **Tags:** {idea['tags']}
- **Empire Score:** {idea['empire_score']} · **Capital:** {idea['capital']}
- **Status:** {idea['status']}
"""


def generate_report(brent_price, gold_price) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    brent_str = f"${brent_price:.2f}" if brent_price else "N/A"
    gold_str = f"${gold_price:,.2f}" if gold_price else "N/A"

    body = "# Venture Intelligence\n\n"
    body += f"**Generated:** {now}\n\n"
    body += "## Market Oracles\n\n"
    body += f"- 🛢️ **Brent Crude:** {brent_str}\n"
    body += f"- 🥇 **Gold:** {gold_str}\n"
    body += "\n## Top Venture Opportunities\n\n"

    for idea in VENTURE_IDEAS:
        body += format_idea(idea) + "\n"

    return body


def main():
    print("Fetching Brent Crude from CoinGecko...")
    brent_price, _ = fetch_brent()
    print(f"  Brent: ${brent_price}" if brent_price else "  Brent: FAILED — using N/A")

    print("Fetching Gold from yfinance (GC=F)...")
    gold_price, _ = fetch_gold()
    print(f"  Gold: ${gold_price:,.2f}" if gold_price else "  Gold: FAILED — using N/A")

    print("Generating report...")
    report = generate_report(brent_price, gold_price)

    with open(OUTPUT_PATH, "w") as f:
        f.write(report)
    print(f"  Written to {OUTPUT_PATH}")

    print(f"\nDone. Brent=${brent_price}, Gold=${gold_price}, Ideas={len(VENTURE_IDEAS)}")


if __name__ == "__main__":
    main()
