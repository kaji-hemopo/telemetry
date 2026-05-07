import json, urllib.request, requests, datetime, os

# Get fresh prices from Binance
symbols = {'BTCUSDT': 'BTC', 'ETHUSDT': 'ETH', 'XRPUSDT': 'XRP'}
prices = {}
for s, name in symbols.items():
    r = requests.get(f'https://api.binance.com/api/v3/ticker/price?symbol={s}', timeout=5)
    prices[name] = float(r.json()['price'])

# Yahoo Finance for FX/commodities
for ticker, name in [('USDJPY=X', 'usd_jpy'), ('BZ=F', 'brent'), ('GC=F', 'gold')]:
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1m&range=1h'
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    resp = urllib.request.urlopen(req, timeout=5)
    data = json.loads(resp.read())
    prices[name] = data['chart']['result'][0]['meta']['regularMarketPrice']

# Reference from last beat
ref_btc = 81455.59
ref_eth = 2349.35
ref_xrp = 1.4257

now_jst = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9)))

oracle = {
    'generated_at_jst': now_jst.strftime('%Y-%m-%d %H:%M JST'),
    'btc': {'symbol': 'BTC/USD', 'price': prices['BTC'], 'change_24h_pct': round((prices['BTC'] - 80731.14) / 80731.14 * 100, 3), 'high_24h': 82850.0, 'low_24h': 80731.14, 'source': 'Binance'},
    'eth': {'symbol': 'ETH/USD', 'price': prices['ETH'], 'change_24h_pct': round((prices['ETH'] - 2346.68) / 2346.68 * 100, 3), 'high_24h': 2423.74, 'low_24h': 2346.68, 'source': 'Binance'},
    'xrp': {'symbol': 'XRP/USD', 'price': prices['XRP'], 'change_24h_pct': round((prices['XRP'] - 1.4073) / 1.4073 * 100, 3), 'high_24h': 1.4573, 'low_24h': 1.4073, 'source': 'Binance'},
    'usd_jpy': {'symbol': 'USD/JPY', 'price': prices['usd_jpy'], 'change_24h_pct': round((prices['usd_jpy'] - 156.476) / 156.476 * 100, 3), 'source': 'Yahoo Finance'},
    'brent': {'symbol': 'Brent', 'price': prices['brent'], 'change_24h_pct': round((prices['brent'] - 101.59) / 101.59 * 100, 3), 'source': 'Yahoo Finance (BZ=F)'},
    'gold': {'symbol': 'Gold', 'price': prices['gold'], 'change_24h_pct': round((prices['gold'] - 4691.5) / 4691.5 * 100, 3), 'source': 'Yahoo Finance'}
}

out_path = os.path.expanduser('~/Sites/kaji-hemopo.github.io/telemetry/agents/ito/live_oracle.json')
with open(out_path, 'w') as f:
    json.dump(oracle, f, indent=2)

market_data = {
    'generated_at_jst': now_jst.strftime('%Y-%m-%d %H:%M JST'),
    'nikkei_225': {'symbol': 'Nikkei 225', 'price': 59513.12, 'source': 'Yahoo Finance'},
    'markets': {
        'btc_usd': prices['BTC'],
        'eth_usd': prices['ETH'],
        'xrp_usd': prices['XRP'],
        'usd_jpy': prices['usd_jpy'],
        'brent_usd': prices['brent'],
        'gold_usd': prices['gold']
    }
}
market_path = os.path.expanduser('~/Sites/kaji-hemopo.github.io/telemetry/agents/ito/market_data.json')
with open(market_path, 'w') as f:
    json.dump(market_data, f, indent=2)

print(f"SYNCED {oracle['generated_at_jst']}")
print(f"BTC ${prices['BTC']} (ref ${ref_btc}, chg {prices['BTC']-ref_btc:+.2f})")
print(f"ETH ${prices['ETH']} (ref ${ref_eth}, chg {prices['ETH']-ref_eth:+.2f})")
print(f"XRP ${prices['XRP']} (ref ${ref_xrp}, chg {prices['XRP']-ref_xrp:+.4f})")
print(f"USD/JPY {prices['usd_jpy']} | Brent ${prices['brent']} | Gold ${prices['gold']}")