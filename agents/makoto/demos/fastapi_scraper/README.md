# Demo 2: FastAPI Data Scraper API

**Purpose:** Wins freelance bids on Lancers/Upwork — shows ability to build data extraction backends.

**What it does:** Accept a URL → return structured JSON with title, price, description, image, and key metadata.

**Stack:** FastAPI · Pydantic · requests · BeautifulSoup4 · lxml

---

## Run Locally

```bash
cd fastapi_scraper
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

## Endpoints

| Method | Path | Body / Params |
|--------|------|---------------|
| `POST` | `/scrape` | `{"url": "https://..."}` |
| `GET`  | `/scrape?url=...` | query param |
| `GET`  | `/health` | — |
| `GET`  | `/` | — |

## Example Response

```json
{
  "url": "https://example.com/product",
  "title": "Product Name",
  "price": "¥3,280",
  "description": "Product description...",
  "image_url": "https://...",
  "key_data": {
    "site_name": "Amazon",
    "h1": "Product Name"
  },
  "success": true,
  "error": null
}
```

## Deploy to Railway

1. Push to GitHub repo
2. Connect repo to [Railway](https://railway.app)
3. Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. Railway auto-detects FastAPI, installs from requirements.txt

**URL for proposals:** `https://your-railway-app.up.railway.app/scrape`

## Use in Lancers Proposals

> 「URLを与えるとタイトル・価格・ descripción を JSON で返す FastAPI API を作れます。デモ: [URL]」

Pattern matches high-volume JP requests:
- データ収集 / スクレイピング
- API 開発
- サーバーサイド開発

## Files

```
fastapi_scraper/
├── main.py          # FastAPI app + scraping logic
├── requirements.txt # Dependencies
└── README.md        # This file
```
