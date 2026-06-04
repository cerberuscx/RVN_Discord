import discord
import asyncio
import config
import logging
import httpx
import random
import json

logger = logging.getLogger(__name__)

async def fetch_with_retry(client, url, max_retries=5, initial_delay=1):
    for attempt in range(max_retries):
        try:
            r = await client.get(url, timeout=120)
            if r.status_code == 429:
                retry_after = int(r.headers.get('Retry-After', str(initial_delay * (2 ** attempt))))
                jitter = random.uniform(0, 0.1 * retry_after)
                logger.warning(f'Rate limit exceeded. Retrying after {retry_after + jitter:.1f} seconds.')
                await asyncio.sleep(retry_after + jitter)
                continue
            r.raise_for_status()
            return r.json()
        except httpx.RequestError as e:
            delay = initial_delay * (2 ** attempt)
            jitter = random.uniform(0, 0.1 * delay)
            logger.error(f"Network error occurred: {e}")
            await asyncio.sleep(delay + jitter)
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            return None
    logger.error("Max retries reached. Unable to fetch data.")
    return None

async def fetch_rvn_data(client):
    data = await fetch_with_retry(client, config.RVN_PRICE_URL)
    if data:
        try:
            price = data['ravencoin']['usd']
            logger.info(f"Successfully fetched RVN price: ${price:,.5f}")
            return price
        except KeyError as e:
            logger.error(f"Unexpected data format: {e}")
    return None

async def update_bot_activity(bot, price):
    try:
        activity = discord.Activity(name=f'RVN: ${price:,.5f} USD', type=discord.ActivityType.watching)
        await bot.change_presence(activity=activity)
    except Exception as e:
        logger.error(f"Failed to update bot activity: {e}")

async def send_embed(embed_channel, embed):
    try:
        message = await embed_channel.send(embed=embed)
        return message
    except discord.HTTPException as e:
        logger.error(f"Failed to send embed: {e}")
        return None

class RVNData:
    def __init__(self, price, mcap, supply, volume, change_24h, change_7d, change_30d,
                 ath=None, ath_change=None, ath_date=None, block_time=None, source='unknown'):
        self.price = price
        self.mcap = mcap
        self.supply = supply
        self.volume = volume
        self.change_24h = change_24h
        self.change_7d = change_7d
        self.change_30d = change_30d
        self.ath = ath
        self.ath_change = ath_change
        self.ath_date = ath_date
        self.block_time = block_time
        self.source = source

async def fetch_from_coingecko(client):
    data = await fetch_with_retry(client, config.RVN_DATA_URL)
    if not data:
        return None
    try:
        md = data['market_data']
        return RVNData(
            price=md['current_price']['usd'],
            mcap=md['market_cap']['usd'],
            supply=md['circulating_supply'],
            volume=md['total_volume']['usd'],
            change_24h=md['price_change_percentage_24h'],
            change_7d=md['price_change_percentage_7d'],
            change_30d=md['price_change_percentage_30d'],
            ath=md['ath']['usd'],
            ath_change=md['ath_change_percentage']['usd'],
            ath_date=md['ath_date']['usd'],
            block_time=data.get('block_time_in_minutes'),
            source='CoinGecko',
        )
    except (KeyError, TypeError) as e:
        logger.warning(f"CoinGecko data parse failed: {e}")
        return None

async def fetch_from_cmc(client):
    quote = await fetch_with_retry(client, config.CMC_QUOTE_URL)
    if not quote:
        return None
    try:
        coin = quote['data'][0]
        q = coin['quotes'][0]
        detail = await fetch_with_retry(client, config.CMC_DETAIL_URL)
        supply = None
        if detail and 'data' in detail:
            stats = detail['data'].get('statistics') or {}
            supply = stats.get('circulatingSupply')
        return RVNData(
            price=q['price'],
            mcap=q.get('marketCap') or 0,
            supply=supply or 0,
            volume=q.get('volume24h') or 0,
            change_24h=q.get('percentChange24h') or 0,
            change_7d=q.get('percentChange7d') or 0,
            change_30d=q.get('percentChange30d') or 0,
            source='CoinMarketCap',
        )
    except (KeyError, IndexError, TypeError) as e:
        logger.warning(f"CoinMarketCap data parse failed: {e}")
        return None

async def fetch_from_binance(client):
    ticker = await fetch_with_retry(client, config.BINANCE_TICKER_URL, max_retries=2, initial_delay=0.5)
    if not ticker:
        return None
    try:
        price = float(ticker['lastPrice'])
        change_24h = float(ticker['priceChangePercent'])
        volume = float(ticker['quoteVolume'])
        return RVNData(
            price=price,
            mcap=0,
            supply=0,
            volume=volume,
            change_24h=change_24h,
            change_7d=None,
            change_30d=None,
            source='Binance',
        )
    except (KeyError, TypeError, ValueError) as e:
        logger.warning(f"Binance data parse failed: {e}")
        return None

async def fetch_rvn_data_fallback(client):
    sources = [
        ('CoinGecko', fetch_from_coingecko),
        ('CoinMarketCap', fetch_from_cmc),
        ('Binance', fetch_from_binance),
    ]
    for name, fetcher in sources:
        result = await fetcher(client)
        if result is not None:
            logger.info(f"RVN data fetched from {name}")
            return result
        logger.warning(f"{name} unavailable, trying next source...")
    logger.error("All data sources failed")
    return None

def load_message_id():
    try:
        with open(config.EMBED_STATE_FILE) as f:
            state = json.load(f)
            return state.get('message_id')
    except (FileNotFoundError, json.JSONDecodeError, ValueError):
        return None

def save_message_id(message_id):
    try:
        with open(config.EMBED_STATE_FILE, 'w') as f:
            json.dump({'message_id': message_id}, f)
    except OSError as e:
        logger.error(f"Failed to save embed message_id: {e}")