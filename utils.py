import discord
import asyncio
import config
import logging

logger = logging.getLogger(__name__)

async def fetch_rvn_data(client):
    r = await client.get(config.RVN_PRICE_URL, timeout=120)
    if r.status_code == 429:
        retry_after = int(r.headers.get('Retry-After', '1'))
        logger.warning(f'Rate limit exceeded. Retrying after {retry_after} seconds.')
        await asyncio.sleep(retry_after)
        return None
    r.raise_for_status()
    data = r.json()
    price = data['ravencoin']['usd']
    return price

async def update_bot_activity(bot, price):
    activity = discord.Activity(name=f'RVN: ${price:,.5f} USD', type=discord.ActivityType.watching)
    await bot.change_presence(activity=activity)

async def send_embed(embed_channel, embed):
    message = await embed_channel.send(embed=embed)
    return message
