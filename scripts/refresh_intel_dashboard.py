#!/usr/bin/env python3
"""
Refresh Ito Intel Dashboard — Full Content Refresh
Fetches live news and updates the Oracle Terminal dashboard HTML
Run by: cron every 20min
"""

import os
import sys
import re
import json
import warnings
import requests
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup, Tag

warnings.filterwarnings("ignore")
BeautifulSoup.MARKUP_MENTION_WITH_ATTR_VALUE = False

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TELEMETRY_DIR = "/Users/jacksonhemopo/.openclaw/telemetry-repo/agents/ito"
DASHBOARD_HTML = os.path.join(TELEMETRY_DIR, "index.html")
OUTPUT_NEWS = os.path.join(WORKSPACE, "intel", "Telemetry", "raw", "news_latest.json")
GIT_DIR = "/Users/jacksonhemopo/.openclaw/telemetry-repo"

JST = timezone(timedelta(hours=+9))

# ===== NEWS SOURCES =====
NEWS_SOURCES = [
    ("TechCrunch", "https://techcrunch.com/feed/", "Tech"),
    ("SaaStr", "https://www.saastr.com/feed/", "SaaS"),
    ("The Verge", "https://www.theverge.com/rss/index.xml", "Tech"),
    ("Reuters World", "https://www.reutersagency.com/feed/", "World"),
]

CATEGORY_MAP = {
    "Tech": ("Tech", "#8B5CF6"),
    "AI": ("AI", "#EC4899"),
    "SaaS": ("SaaS", "#10B981"),
    "Finance": ("Finance", "#D4AF37"),
    "Japan": ("日本", "#22d3ee"),
    "World": ("World", "#849396"),
}

CATEGORIES_ORDER = ["AI", "Tech", "SaaS", "Finance", "Japan", "World"]


def fetch_rss(feed_url, max_items=6):
    """Fetch RSS feed items."""
    try:
        resp = requests.get(feed_url, timeout=12, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0"
        })
        if not resp.ok:
            return []
        
        soup = BeautifulSoup(resp.text, "html.parser")
        items = []
        
        for entry in (soup.find_all("item") or soup.find_all("entry"))[:max_items]:
            title_el = entry.find("title")
            guid_el = entry.find("guid") or entry.find("id")
            link_text = ""
            if entry.name == "item":
                link_el = entry.find("link")
                if link_el:
                    link_text = link_el.get_text(strip=True) or link_el.get("href", "")
                if not link_text:
                    link_text = guid_el.get_text(strip=True) if guid_el else ""
            else:
                link_el = entry.find("link")
                if link_el:
                    link_text = link_el.get("href") or link_el.get_text(strip=True) or ""
                if not link_text:
                    link_text = guid_el.get_text(strip=True) if guid_el else ""
            
            desc_el = entry.find("description") or entry.find("summary") or entry.find("content")
            pub_el = entry.find("pubDate") or entry.find("published") or entry.find("updated")
            
            title = title_el.get_text(strip=True) if title_el else ""
            link = link_text.strip() if link_text else "#"
            description = desc_el.get_text(strip=True)[:180] if desc_el else ""
            pub_date = pub_el.get_text(strip=True) if pub_el else ""
            
            if title:
                items.append({"title": title, "link": link or "#", "description": description, "pub_date": pub_date})
        return items
    except Exception as e:
        print(f"  Error {feed_url}: {e}", file=sys.stderr)
        return []


def detect_category(title, description):
    """Detect category from text."""
    text = (title + " " + description).lower()
    if any(w in text for w in ["ai", "llm", "gpt", "chatgpt", "gemini", "openai", "anthropic", "model", "agent", "claude"]):
        return "AI"
    if any(w in text for w in ["saas", "software", "startup", "arr", "revenue", "cloud", "saastr"]):
        return "SaaS"
    if any(w in text for w in ["stock", "market", "fed", "rate", "inflation", "economy", "bond", "yield"]):
        return "Finance"
    if any(w in text for w in ["japan", "japanese", "tokyo", "nikkei", "osaka"]):
        return "Japan"
    if any(w in text for w in ["tech", "apple", "google", "microsoft", "meta", "nvidia", "amazon", "apple"]):
        return "Tech"
    return "World"


def parse_time(pub_date):
    """Convert pubDate to relative time."""
    if not pub_date:
        return "Recent"
    try:
        for fmt in ["%a, %d %b %Y %H:%M:%S %z", "%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S+09:00"]:
            try:
                dt = datetime.strptime(pub_date[:26], fmt).astimezone(JST)
                h = (datetime.now(JST) - dt).total_seconds() / 3600
                if h < 1: return f"{int(h*60)}m"
                elif h < 24: return f"{int(h)}h"
                else: return f"{int(h/24)}d"
            except: pass
    except: pass
    return "Recent"


def build_news_card(item, cat, color):
    """Build a single news card HTML."""
    time_str = parse_time(item["pub_date"])
    desc = item["description"][:150] + "..." if len(item["description"]) > 150 else item["description"]
    title = item["title"].replace("<", "&lt;").replace(">", "&gt;")
    link = item["link"] if item["link"].startswith("http") else "#"
    return f'''<div class="card">
            <div class="flex-between">
                <span class="tag" style="background:{color}22; color:{color};">{cat}</span>
                <span style="font-size:0.8rem; color:var(--text-dim);">{time_str}</span>
            </div>
            <a href="{link}" target="_blank" class="card-title-link">{title}</a>
            <div class="card-summary">{desc}</div>
        </div>'''


def build_category_section(cat_name, cat_color, items):
    """Build a full category section div."""
    cards_html = "".join(build_news_card(it, cat_name, cat_color) for it in items)
    return f'''<div id="subtab-intel-{CATEGORIES_ORDER.index(cat_name)}" class="sub-tab-content active">
        <div style="display:grid; gap:16px;">{cards_html}
        </div>
    </div>''' if items else f'<div id="subtab-intel-{CATEGORIES_ORDER.index(cat_name)}" class="sub-tab-content active"><p style="color:var(--text-dim)">No {cat_name} news yet.</p></div>'


def refresh_news():
    """Fetch all news and organize by category."""
    all_items = []
    for name, url, default_cat in NEWS_SOURCES:
        print(f"  Fetching {name}...")
        items = fetch_rss(url, max_items=6)
        for item in items:
            cat = detect_category(item["title"], item["description"])
            all_items.append((cat, item))
        print(f"    → {len(items)} items")
    
    # Organize by category
    by_category = {cat: [] for cat in CATEGORIES_ORDER}
    for cat, item in all_items:
        if cat in by_category:
            by_category[cat].append(item)
        else:
            by_category.setdefault(cat, []).append(item)
    
    return by_category


def update_dashboard(html_path, by_category, timestamp):
    """Update the dashboard HTML with fresh news content."""
    try:
        with open(html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f.read(), "html.parser")
        
        # Update header timestamp
        ts_el = soup.find("span", class_="timestamp")
        if ts_el:
            ts_el.string = timestamp
        
        # Find the news-wall div
        news_wall = soup.find("div", id="news-wall")
        if not news_wall:
            print("  WARNING: news-wall div not found")
            return False
        
        # Find subtab-intel-0 (Intel Brief) content area
        first_subtab = soup.find("div", id="subtab-intel-0")
        if first_subtab:
            # Clear and rebuild content
            subtab_content = first_subtab.find("div")
            if subtab_content:
                subtab_content.clear()
                
                # Build cards for first category (AI) as default
                ai_items = by_category.get("AI", [])
                for item in ai_items[:8]:
                    color = CATEGORY_MAP.get("AI", ("News", "#849396"))[1]
                    subtab_content.append(BeautifulSoup(build_news_card(item, "AI", color), "html.parser"))
        
        # Save updated HTML
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(str(soup.prettify()))
        
        print(f"  Dashboard HTML updated")
        return True
    except Exception as e:
        print(f"  Dashboard update error: {e}", file=sys.stderr)
        return False


def git_push():
    """Commit and push dashboard changes."""
    try:
        os.chdir(GIT_DIR)
        import subprocess
        subprocess.run(["git", "add", "agents/ito/index.html"], check=True, capture_output=True)
        result = subprocess.run(["git", "diff", "--cached", "--stat"], capture_output=True, text=True)
        if result.stdout.strip():
            subprocess.run(["git", "commit", "-m", f"[ito] Intel refresh {datetime.now(JST).strftime('%Y-%m-%d %H:%M JST')}"], check=True, capture_output=True, text=True)
            push = subprocess.run(["git", "push", "origin", "main"], capture_output=True, text=True)
            if push.returncode == 0:
                print("  ✅ Pushed to GitHub Pages")
            else:
                print(f"  ⚠️ Push failed: {push.stderr[:200]}")
        else:
            print("  No changes to commit")
    except Exception as e:
        print(f"  Git error: {e}", file=sys.stderr)


def main():
    now_jst = datetime.now(JST)
    timestamp = now_jst.strftime("%Y-%m-%d %H:%M JST")
    print(f"=== Ito Intel Refresh [{timestamp}] ===")
    
    # Fetch news
    by_category = refresh_news()
    total = sum(len(v) for v in by_category.values())
    
    if total > 0:
        # Save news JSON
        all_items_flat = [{"category": k, **it} for k, v in by_category.items() for it in v]
        with open(OUTPUT_NEWS, "w") as f:
            json.dump({"timestamp": timestamp, "items": all_items_flat[:20]}, f, indent=2)
        
        # Update dashboard
        success = update_dashboard(DASHBOARD_HTML, by_category, timestamp)
        
        # Git push if updated
        if success:
            git_push()
        
        print(f"\n✅ Done — {total} items across {len(by_category)} categories")
        for cat in CATEGORIES_ORDER:
            count = len(by_category.get(cat, []))
            if count:
                print(f"   {cat}: {count}")
    else:
        print("\n⚠️ No items collected")

    return 0


if __name__ == "__main__":
    sys.exit(main())