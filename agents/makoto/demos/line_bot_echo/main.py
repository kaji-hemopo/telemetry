"""
LINE Bot Echo + Keyword Responder Demo
======================================
Minimal FastAPI app demonstrating LINE Messaging API webhook handling.
Responses:
  - "help"    → usage instructions
  - " services" → list of services (web scraping, FastAPI, LINE bots, LP制作)
  - "price"  → pricing tier overview
  - Default  → echo back with confirmation

Deploy: Railway (free) or ngrok for local dev.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os
import sys

app = FastAPI(title="LINE Bot Echo Demo — Jackson")

# LINE Channel credentials from environment
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "YOUR_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "YOUR_CHANNEL_SECRET")

if LINE_CHANNEL_ACCESS_TOKEN == "YOUR_ACCESS_TOKEN":
    print("WARNING: Set LINE_CHANNEL_ACCESS_TOKEN and LINE_CHANNEL_SECRET env vars before production.", file=sys.stderr)

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


# ─── Keyword Routing ────────────────────────────────────────────

RESPONSES = {
    "help": (
        "⚡ Jackson's LINE Bot Demo\n\n"
        "Available keywords:\n"
        "  help     → Show this message\n"
        "  services → What I build\n"
        "  price    → Pricing overview\n"
        "  anything else → Echo reply"
    ),
    "services": (
        "🛠️ Services I build:\n\n"
        "• LINE Bot開発 — AI photo, オプトイン, 自動返信\n"
        "• FastAPIバックエンド — REST API, データパイプライン\n"
        "• Webスクレイピング — 価格監視, データ収集\n"
        "• LP制作 —  WordPress, LP制作 (JP/EN対応)\n\n"
        "対応エリア: 東京・神奈川"
    ),
    "price": (
        "💰 Pricing (参考例):\n\n"
        "• LINE Bot開発: ¥80,000〜¥300,000\n"
        "• FastAPI API: ¥50,000〜¥200,000\n"
        "• スクレイピング: ¥30,000〜¥100,000\n"
        "• LP制作: ¥50,000〜¥150,000\n\n"
        "※ PROJECTごとにcustom quote対応"
    ),
}


def get_response(text: str) -> str:
    """Route incoming message to appropriate response handler."""
    t = text.strip().lower()
    for keyword, response in RESPONSES.items():
        if keyword in t:
            return response
    return f"✅ Received: {text}\n\nText 'help' for options, 'services' for what I build, 'price' for rates."


# ─── LINE Webhook ───────────────────────────────────────────────

@app.post("/callback")
async def callback(request: Request):
    """LINE Messaging API webhook endpoint."""
    signature = request.headers.get("X-Line-Signature", "")
    body = await request.body()

    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return JSONResponse(content={"status": "ok"})


@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    """Echo + keyword routing for text messages."""
    user_text = event.message.text
    reply_text = get_response(user_text)
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_text))


# ─── Health Check ───────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "status": "live",
        "bot": "Jackson LINE Bot Demo",
        "endpoints": {
            "callback": "POST /callback (LINE webhook)",
            "health": "GET /",
        }
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


# ─── Local Dev ─────────────────────────────────────────────────
# Run: uvicorn main:app --reload --port 8000
# Then: ngrok http 8000 → set webhook URL in LINE Console
