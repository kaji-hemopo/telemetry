"""
FastAPI Data Scraper API — Demo 2
Input: URL → returns structured JSON (title, price, key data)
Use: FastAPI + Pydantic + requests + BeautifulSoup
"""
import httpx
from bs4 import BeautifulSoup
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, HttpUrl
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI Data Scraper API",
    description="Input a URL → returns structured JSON with title, price, and key data",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ScrapeResponse(BaseModel):
    url: str
    title: str | None = None
    price: str | None = None
    description: str | None = None
    image_url: str | None = None
    key_data: dict = {}
    success: bool = True
    error: str | None = None


class ScrapeRequest(BaseModel):
    url: HttpUrl


def extract_price(soup: BeautifulSoup, text: str) -> str | None:
    """Try to extract price from common JP/E-commerce patterns."""
    import re
    patterns = [
        r'¥[\d,]+',
        r'[\d,]+円',
        r'\$\d+\.\d{2}',
        r'[\d,]+\s*円',
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(0)
    # Try meta tags
    meta_price = soup.find("meta", property="product:price:amount")
    if meta_price:
        return f"¥{meta_price.get('content', '')}"
    return None


def scrape_url(url: str) -> ScrapeResponse:
    """Fetch and parse a URL, extracting structured data."""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
    }

    try:
        response = httpx.get(url, headers=headers, timeout=15.0, follow_redirects=True)
        response.raise_for_status()
    except httpx.HTTPError as e:
        logger.error(f"HTTP error fetching {url}: {e}")
        return ScrapeResponse(url=url, success=False, error=str(e))

    soup = BeautifulSoup(response.text, "lxml")

    # Title
    title = (
        soup.find("meta", property="og:title")
        or soup.find("meta", attrs={"name": "title"})
        or soup.find("title")
    )
    title_text = title.get("content", title.text.strip()) if title else None

    # Description
    desc = (
        soup.find("meta", property="og:description")
        or soup.find("meta", attrs={"name": "description"})
    )
    desc_text = desc.get("content", "").strip() if desc else None

    # Image
    img = soup.find("meta", property="og:image") or soup.find("meta", attrs={"name": "image"})
    img_url = img.get("content", "") if img else None

    # Price — scan page text + meta
    page_text = soup.get_text()[:5000]  # first 5000 chars
    price = extract_price(soup, page_text)

    # Key data dict — gather common structured fields
    key_data = {}
    og_site = soup.find("meta", property="og:site_name")
    if og_site:
        key_data["site_name"] = og_site.get("content", "")

    h1 = soup.find("h1")
    if h1:
        key_data["h1"] = h1.get_text(strip=True)[:200]

    # Product-specific meta (common e-com patterns)
    for attr in ["product:price:currency", "product:price:amount"]:
        meta = soup.find("meta", property=attr)
        if meta:
            key_data[attr] = meta.get("content", "")

    return ScrapeResponse(
        url=url,
        title=title_text,
        price=price,
        description=desc_text,
        image_url=img_url,
        key_data=key_data,
        success=True,
    )


@app.post("/scrape", response_model=ScrapeResponse)
async def scrape(req: ScrapeRequest):
    """Scrape a URL and return structured data."""
    return scrape_url(str(req.url))


@app.get("/scrape", response_model=ScrapeResponse)
async def scrape_get(url: str):
    """Scrape a URL (GET with query param)."""
    if not url:
        raise HTTPException(status_code=400, detail="url query param required")
    return scrape_url(url)


@app.get("/health")
async def health():
    return {"status": "ok", "service": "fastapi-scraper-demo"}


@app.get("/")
async def root():
    return {
        "service": "FastAPI Data Scraper API",
        "version": "1.0.0",
        "endpoints": {
            "POST /scrape": {"body": {"url": "https://example.com"}, "returns": "ScrapeResponse"},
            "GET /scrape?url=...": {"returns": "ScrapeResponse"},
            "GET /health": {"returns": "health check"},
        },
    }
