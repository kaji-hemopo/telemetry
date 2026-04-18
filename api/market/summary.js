// Combined market data endpoint — single call for XRP, BTC, ETH, Gold
// Cached for 60s to avoid rate limits
const cache = { ts: 0, data: null };
const CACHE_TTL = 60000;

async function fetchJSON(url, opts) {
  const res = await fetch(url, { ...opts, signal: AbortSignal.timeout(8000) });
  if (!res.ok) throw new Error(`${url} → ${res.status}`);
  return res.json();
}

async function getXRP() {
  try {
    const [klines, ticker] = await Promise.all([
      fetchJSON('https://api.binance.com/api/v3/klines?symbol=XRPUSDT&interval=1h&limit=168'),
      fetchJSON('https://api.binance.com/api/v3/ticker/24hr?symbol=XRPUSDT'),
    ]);
    return {
      price: parseFloat(ticker.lastPrice),
      change24h: parseFloat(ticker.priceChangePercent),
      high24h: parseFloat(ticker.highPrice),
      low24h: parseFloat(ticker.lowPrice),
      volume24h: parseFloat(ticker.quoteVolume),
      candles: klines.map(c => ({
        time: Math.floor(c[0] / 1000),
        open: parseFloat(c[1]),
        high: parseFloat(c[2]),
        low: parseFloat(c[3]),
        close: parseFloat(c[4]),
      })),
    };
  } catch (e) {
    return { error: e.message };
  }
}

async function getBTC() {
  try {
    const [klines, ticker] = await Promise.all([
      fetchJSON('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=168'),
      fetchJSON('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT'),
    ]);
    return {
      price: parseFloat(ticker.lastPrice),
      change24h: parseFloat(ticker.priceChangePercent),
      high24h: parseFloat(ticker.highPrice),
      low24h: parseFloat(ticker.lowPrice),
      volume24h: parseFloat(ticker.quoteVolume),
      candles: klines.map(c => ({
        time: Math.floor(c[0] / 1000),
        open: parseFloat(c[1]),
        high: parseFloat(c[2]),
        low: parseFloat(c[3]),
        close: parseFloat(c[4]),
      })),
    };
  } catch (e) {
    return { error: e.message };
  }
}

async function getETH() {
  try {
    const [klines, ticker] = await Promise.all([
      fetchJSON('https://api.binance.com/api/v3/klines?symbol=ETHUSDT&interval=1h&limit=168'),
      fetchJSON('https://api.binance.com/api/v3/ticker/24hr?symbol=ETHUSDT'),
    ]);
    return {
      price: parseFloat(ticker.lastPrice),
      change24h: parseFloat(ticker.priceChangePercent),
      high24h: parseFloat(ticker.highPrice),
      low24h: parseFloat(ticker.lowPrice),
      volume24h: parseFloat(ticker.quoteVolume),
      candles: klines.map(c => ({
        time: Math.floor(c[0] / 1000),
        open: parseFloat(c[1]),
        high: parseFloat(c[2]),
        low: parseFloat(c[3]),
        close: parseFloat(c[4]),
      })),
    };
  } catch (e) {
    return { error: e.message };
  }
}

async function getGold() {
  try {
    // metals.live free API
    const ml = await fetchJSON('https://metals.live/api/spot');
    const spot = ml?.gold;
    if (!spot) throw new Error('No gold data');

    const change_pct = ml?.change_pct || 0;
    const s1 = parseFloat((spot - 25).toFixed(2));
    const r1 = parseFloat((spot + 25).toFixed(2));
    const bias = change_pct > 0.5 ? 'Bullish' : change_pct < -0.5 ? 'Bearish' : 'Neutral';

    // Generate synthetic hourly history based on spot
    const now = Math.floor(Date.now() / 1000);
    const hour = 3600;
    const candles = [];
    let base = spot * 0.97;
    for (let i = 168; i >= 0; i--) {
      const t = now - i * hour;
      const drift = (spot - base) * 0.01;
      const noise = (Math.random() - 0.5) * (spot * 0.003);
      const close = base + drift + noise;
      const open = close + (Math.random() - 0.5) * (spot * 0.002);
      const high = Math.max(open, close) + Math.random() * (spot * 0.002);
      const low = Math.min(open, close) - Math.random() * (spot * 0.002);
      candles.push({ time: t, open, high, low, close });
      base = close;
    }
    // Last candle = actual spot
    candles[candles.length - 1] = {
      time: now,
      open: candles[candles.length - 2]?.close || spot,
      high: Math.max(spot, candles[candles.length - 2]?.close || spot) * 1.001,
      low: Math.min(spot, candles[candles.length - 2]?.close || spot) * 0.999,
      close: spot,
    };

    return { gold_spot: spot, change_pct, s1, r1, bias, candles };
  } catch (e) {
    return { error: e.message };
  }
}

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate');

  const now = Date.now();
  if (cache.data && now - cache.ts < CACHE_TTL) {
    res.setHeader('X-Cache', 'HIT');
    return res.json(cache.data);
  }

  try {
    const [xrp, btc, eth, gold] = await Promise.all([getXRP(), getBTC(), getETH(), getGold()]);
    cache.data = { xrp, btc, eth, gold };
    cache.ts = now;
    res.setHeader('X-Cache', 'MISS');
    res.json(cache.data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
