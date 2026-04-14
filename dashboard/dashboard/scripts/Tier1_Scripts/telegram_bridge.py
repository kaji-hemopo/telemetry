#!/usr/bin/env python3
"""
Telegram Webhook Bridge
Pushes Agent 7's output to Telegram for real-time notifications
"""

import sys
import requests

def send_to_telegram(message):
    """
    Send message to Telegram using bot API.
    
    Args:
        message (str): Message text to send
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Telegram credentials for Gold-Shield notifications
    # Updated with actual credentials from system override
    BOT_TOKEN = "8620301983:AAFSqN6eV2ZBPfEIvV_zAhwIqIIX8hJThCs"
    CHAT_ID = "6050367808"
    
    # Validate credentials are present
    if not BOT_TOKEN or not CHAT_ID:
        print("ERROR: Telegram credentials missing.")
        return False
    
    # Construct API URL
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    
    # Prepare payload
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",  # Enable Markdown formatting
        "disable_web_page_preview": True  # Cleaner presentation
    }
    
    try:
        # Send request with timeout
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        # Check Telegram API response
        result = response.json()
        if result.get("ok"):
            print(f"Telegram message delivered successfully (message_id: {result['result']['message_id']})")
            return True
        else:
            print(f"Telegram API error: {result.get('description', 'Unknown error')}")
            return False
            
    except requests.exceptions.Timeout:
        print("Telegram delivery failed: Request timeout")
        return False
    except requests.exceptions.ConnectionError:
        print("Telegram delivery failed: Connection error")
        return False
    except requests.exceptions.HTTPError as e:
        print(f"Telegram delivery failed: HTTP error {e.response.status_code}")
        return False
    except Exception as e:
        print(f"Telegram delivery failed: {str(e)}")
        return False

def main():
    """Main execution function."""
    # Read all input from stdin
    message = sys.stdin.read().strip()
    
    # Check if message is empty
    if not message:
        print("ERROR: No input received from stdin")
        sys.exit(1)
    
    # Truncate very long messages (Telegram limit is 4096 characters)
    if len(message) > 4000:
        message = message[:4000] + "\n\n[Message truncated due to Telegram length limits]"
    
    # Send to Telegram
    success = send_to_telegram(message)
    
    # Exit with appropriate code
    if success:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
