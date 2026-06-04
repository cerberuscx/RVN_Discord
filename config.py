import os
import discord
from dotenv import load_dotenv

load_dotenv()

# Bot Token and Guild ID
TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')

# URLs — Primary (CoinGecko)
THUMBNAIL_URL = os.getenv('THUMBNAIL_URL', 'https://i.imgur.com/tqLb13l.png')
AUTHOR_URL = os.getenv('AUTHOR_URL', 'https://i.imgur.com/z1KjbkG.png')
WEBSITE_LINK = 'https://ravencoin.org/'
RVN_PRICE_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ravencoin&vs_currencies=usd'
RVN_HISTORY_URL = "https://api.coingecko.com/api/v3/coins/ravencoin/market_chart?vs_currency=usd&days=30"
RVN_DATA_URL = 'https://api.coingecko.com/api/v3/coins/ravencoin'

# URLs — Fallback (CoinMarketCap keyless, no API key required)
CMC_QUOTE_URL = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/quote/latest?slug=ravencoin'
CMC_DETAIL_URL = 'https://api.coinmarketcap.com/data-api/v3/cryptocurrency/detail?slug=ravencoin'

# URLs — Last-resort fallback (Binance public, no key required)
BINANCE_TICKER_URL = 'https://api.binance.com/api/v3/ticker/24hr?symbol=RVNUSDT'

# Channel IDs
CHANNEL_ID = os.getenv('CHANNEL_ID')
EMBED_ID = os.getenv('EMBED_ID')

# Intervals
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 1800))

# Bot Description
DESCRIPTION = 'Official Ravencoin Discord bot providing up-to-date market data and statistics.'

# Discord Intents
intents = discord.Intents.default()
intents.message_content = True

# State persistence
EMBED_STATE_FILE = 'embed_state.json'
