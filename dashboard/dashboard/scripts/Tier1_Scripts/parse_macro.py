#!/usr/bin/env python3
"""
Regex Parser for Agent 6 Output
Extracts target_ticker and conviction_score regardless of JSON nesting or markdown formatting
"""

import sys
import re

def extract_ticker_and_score(text):
    """
    Extract target_ticker and conviction_score using regex patterns.
    Handles nested JSON, markdown code blocks, and various formatting.
    
    Args:
        text (str): Raw output from Agent 6
        
    Returns:
        tuple: (ticker, score) where ticker is string, score is int
    """
    # Pattern for target_ticker: "target_ticker": "VALUE"
    ticker_pattern = r'"target_ticker"\s*:\s*"([^"]+)"'
    ticker_match = re.search(ticker_pattern, text)
    
    # Pattern for conviction_score: "conviction_score": NUMBER
    score_pattern = r'"conviction_score"\s*:\s*(\d+)'
    score_match = re.search(score_pattern, text)
    
    # Extract values with defaults
    ticker = ticker_match.group(1) if ticker_match else "NONE"
    score = int(score_match.group(1)) if score_match else 0
    
    return ticker, score

def main():
    """Main execution function."""
    # Read all input from stdin
    text = sys.stdin.read()
    
    # Extract ticker and score
    ticker, score = extract_ticker_and_score(text)
    
    # Output as comma-separated string for bash parsing
    print(f"{ticker},{score}")
    
    # Exit with success
    sys.exit(0)

if __name__ == "__main__":
    main()