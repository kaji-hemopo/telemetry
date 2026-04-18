const fetchCache = new Map();
const CACHE_TTL = 60000;

export default async function handler(req, res) {
  const cacheKey = 'gold';
  const now = Date.now();
  const cached = fetchCache.get(cacheKey);

  if (cached && now - cached.ts < CACHE_TTL) {
    res.setHeader('X-Cache', 'HIT');
    return res.json(cached.data);
  }

  try {
    // Try metals.live free API first
    let gold_spot = null;
    let change_pct = 0;

    try {
      const mlRes = await fetch('https://metals.live/api/spot', {
        headers: { 'Accept': 'application/json' },
        signal: AbortSignal.timeout(5000),
      });
      if (mlRes.ok) {
        const ml = await mlRes.json();
        gold_spot = ml?.gold?.toFixed(2);
        change_pct = ml?.change_pct || 0;
      }
    } catch (_) {}

    // Fallback: GoldAPI.io free tier
    if (!gold_spot) {
      try {
        const gpRes = await fetch('https://www.goldapi.io/api/XAU/USD', {
          headers: { 'x-access-token': 'goldapi-demo', 'Accept': 'application/json' },
          signal: AbortSignal.timeout(5000),
        });
        if (gpRes.ok) {
          const gp = await gpRes.json();
          gold_spot = gp?.price?.toFixed(2) || null;
          change_pct = gp?.price_change_pct || 0;
        }
      } catch (_) {}
    }

    // Final fallback: worldgovernmentbonds.com
    if (!gold_spot) {
      try {
        const wgbRes = await fetch('https://www.worldgovernmentbonds.com/country/united-states/', {
          headers: { 'Accept': 'application/json' },
          signal: AbortSignal.timeout(5000),
        });
        if (wgbRes.ok) {
          const text = await wgbRes.text();
          const m = text.match(/Gold\s*\$\s*([0-9,.]+)/i);
          if (m) gold_spot = parseFloat(m[1].replace(/,/g, '')).toFixed(2);
        }
      } catch (_) {}
    }

    if (!gold_spot) {
      return res.status(500).json({ error: 'All gold APIs failed' });
    }

    const spot = parseFloat(gold_spot);
    const s1 = spot - 25;
    const r1 = spot + 25;
    const bias = change_pct > 0.5 ? 'Bullish' : change_pct < -0.5 ? 'Bearish' : 'Neutral';

    const data = {
      symbol: 'XAU/USD',
      gold_spot: spot,
      change_pct,
      s1: parseFloat(s1.toFixed(2)),
      r1: parseFloat(r1.toFixed(2)),
      bias,
    };

    fetchCache.set(cacheKey, { data, ts: now });
    res.setHeader('X-Cache', 'MISS');
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
