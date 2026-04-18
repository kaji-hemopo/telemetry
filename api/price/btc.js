const fetchCache = new Map();
const CACHE_TTL = 60000;

export default async function handler(req, res) {
  const cacheKey = 'btc';
  const now = Date.now();
  const cached = fetchCache.get(cacheKey);

  if (cached && now - cached.ts < CACHE_TTL) {
    res.setHeader('X-Cache', 'HIT');
    return res.json(cached.data);
  }

  try {
    const [binanceRes, cbRes] = await Promise.all([
      fetch('https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1h&limit=168', { headers: { 'Accept': 'application/json' } }),
      fetch('https://api.coinbase.com/v2/prices/BTC-USD/historic?hours=168', { headers: { 'Accept': 'application/json' } }),
    ]);

    const binance = binanceRes.ok ? await binanceRes.json() : [];
    const candles = binance.length
      ? binance.map(c => ({ time: Math.floor(c[0] / 1000), open: parseFloat(c[1]), high: parseFloat(c[2]), low: parseFloat(c[3]), close: parseFloat(c[4]) }))
      : [];

    const tickerRes = await fetch('https://api.binance.com/api/v3/ticker/24hr?symbol=BTCUSDT');
    const ticker = tickerRes.ok ? await tickerRes.json() : null;

    const data = {
      symbol: 'BTC/USDT',
      price: parseFloat(ticker?.lastPrice || 0),
      change24h: parseFloat(ticker?.priceChangePercent || 0),
      high24h: parseFloat(ticker?.highPrice || 0),
      low24h: parseFloat(ticker?.lowPrice || 0),
      volume24h: parseFloat(ticker?.quoteVolume || 0),
      candles,
    };

    fetchCache.set(cacheKey, { data, ts: now });
    res.setHeader('X-Cache', 'MISS');
    res.json(data);
  } catch (e) {
    res.status(500).json({ error: e.message });
  }
}
