# LINE Bot Echo Demo — Jackson

**Purpose:** Demo for freelance LINE Bot development. Proves competency in:
- LINE Messaging API webhook handling
- FastAPI server
- Keyword routing + auto-response logic

**Live demo:** Add Jackson as LINE friend (QR/deploy link coming once Railway deployment is live)

**Tech stack:** Python 3.11+ · FastAPI · LINE Bot SDK · ngrok (local dev)

---

## Quick Start (Local)

```bash
cd demos/line_bot_echo
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt

# Configure .env (copy .env.example → .env and fill in LINE credentials)
cp .env.example .env

# Run dev server
uvicorn main:app --reload --port 8000
```

Then set up ngrok for local webhook testing:
```bash
ngrok http 8000
# Copy https URL → paste into LINE Console webhook URL field
```

---

## LINE Console Setup

1. Create LINE Channel at https://console.line.biz/
2. Go to **Messaging API** tab
3. Set Webhook URL: `https://your-domain.com/callback`
4. Disable auto-reply (we handle replies programmatically)
5. Copy **Channel Access Token** and **Channel Secret** → `.env`

---

## Deploy to Railway (Free)

```bash
# 1. Push to GitHub (repo with this demo)
git init && git add . && git commit -m "LINE Bot Echo Demo"
gh repo create line-bot-echo-demo --public --push

# 2. Connect repo to Railway
#    railway init → select repo → deploys automatically
#    Add env vars: LINE_CHANNEL_ACCESS_TOKEN, LINE_CHANNEL_SECRET

# 3. Set LINE webhook URL to Railway domain:
#    https://line-bot-echo-demo.up.railway.app/callback
```

Or use the **Deploy to Railway** button (coming once Railway account is connected).

---

## How It Works

| Message | Response |
|---------|----------|
| `help` | Shows all available commands |
| `services` | Lists what Jackson builds |
| `price` | Pricing reference |
| Anything else | Echoes back with confirmation |

Webhook flow:
```
[User sends message]
    ↓
[LINE Server POSTs to /callback]
    ↓
[FastAPI receives, validates signature]
    ↓
[Handler routes keyword → appropriate response]
    ↓
[LINE Bot SDK replies to user]
```

---

## What This Demo Proves

✅ Can handle LINE webhooks with FastAPI  
✅ Can implement keyword routing logic  
✅ Can deploy a Python app to production (Railway)  
✅ Understands LINE Messaging API (reply vs push, webhook verification)

**Used to bid on:** ¥80-300k LINE Bot jobs on Lancers, Upwork

---

## Files

```
line_bot_echo/
├── main.py           ← FastAPI app + LINE webhook handler
├── requirements.txt   ← Python dependencies
├── .env.example      ← Env var template (copy → .env)
└── README.md         ← This file
```
