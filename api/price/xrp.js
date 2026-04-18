const fetchCache = new Map();
const CACHE_TTL = 60000;

export default async function handler(req, res) {
  const cacheKey = 'xrp';
  const now = Date.now();
  const cached = fetchCache.get(cacheKey);

  if (cached && now - cached.ts < CACHE_TTL) {
    res.setHeader('X-Cache', 'HIT');
    return res.json(cached.data);
  }

  try {
    const [binanceRes, huobiRes] = await Promise.all([
      fetch('https://api.binance.com/api/v3/klines?symbol=XRPUSDT&interval=1h&limit=168', { headers: { 'Accept': 'application/json' } }),
      fetch('https://api.huobi.com/market/history/kline?symbol=xrpusdt&period=60min&size=168', { headers: { 'Accept': 'application/json' } }),
    ]);

    const binance = binanceRes.ok ? await binanceRes.json() : [];
    const huobi = huobiRes.ok ? await huobiRes.json() : [];

    const candles = binance.length
      ? binance.map(c => ({ time: Math.floor(c[0] / 1000), open: parseFloat(c[1]), high: parseFloat(c[2]), low: parseFloat(c[3]), close: parseFloat(c[4]) }))
      : huobi.data?.map(c => ({ time: c.id, open: c.open, high: c.high, low: c.low, close: c.close })) || [];

    const priceRes = await fetch('https://api.binance.com/api/v3/ticker/24hr?symbol=XRPUSDT');
    const ticker = priceRes.ok ? await priceRes.json() : null;

    const data = {
      symbol: 'XRP/USDT',
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
