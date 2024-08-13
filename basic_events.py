import logging
import config
import utils
import datetime
import discord
import asyncio
import httpx
from utils import fetch_rvn_data, update_bot_activity, send_embed

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

message_id = None

async def on_ready(bot):
    logger.info(f'We have logged in as {bot.user}')
    logger.info(f'{bot.user.name} is online!')
    logger.info(f'Bot ID: {bot.user.id}')
    logger.info('----------------------------')
    bot.loop.create_task(update_statistics(bot))

async def on_disconnect():
    logger.warning("The bot has been disconnected")

async def update_statistics(bot):
    global message_id

    guild = bot.guilds[0]
    channel = bot.get_channel(int(config.CHANNEL_ID))
    embed_channel = bot.get_channel(int(config.EMBED_ID))
    thumbnail_url = config.THUMBNAIL_URL
    description = config.DESCRIPTION
    image_url = config.IMAGE_URL
    author_url = config.AUTHOR_URL
    website_link = config.WEBSITE_LINK
    update_interval = config.UPDATE_INTERVAL

    if not message_id:
        async for msg in embed_channel.history(limit=1):
            if msg.author == bot.user:
                message_id = msg.id
                break

    async with httpx.AsyncClient() as client:
        while True:
            try:
                now = datetime.datetime.now()
                price = await fetch_rvn_data(client)
                if price is not None:
                    await update_bot_activity(bot, price)
                    channel_name = f'RVN - ${price:,.5f} USD'
                    await channel.edit(name=channel_name)

                r = await client.get(config.RVN_DATA_URL, timeout=120)
                r.raise_for_status()
                data = r.json()
                price = data['market_data']['current_price']['usd']
                mcap = data['market_data']['market_cap']['usd']
                supply = data['market_data']['circulating_supply']
                volume = data['market_data']['total_volume']['usd']
                change = data['market_data']['price_change_percentage_24h']
                block_time = data['block_time_in_minutes']

                embed = discord.Embed(
                    title = 'Ravencoin Price & Statistics',
                    description = description,
                    colour = discord.Colour.orange()
                )
                embed.set_thumbnail(url=thumbnail_url)
                embed.set_author(name='', icon_url=thumbnail_url)
                embed.set_image(url=image_url)
                embed.add_field(name = 'Price', value = f'${price:,.5f}')
                embed.add_field(name = '24 Hour Change', value = f'{change:,.2f}%')
                embed.add_field(name = '24 Hour Volume', value = f'${volume:,.0f}')
                embed.add_field(name = 'Market Cap', value = f'${mcap:,.0f}')
                embed.add_field(name = 'Circulating Supply', value = f'{supply:,.0f} RVN')
                embed.add_field(name = 'Block Time (minutes)', value = f'{block_time}')
                embed.add_field(name = f'{guild.name} Website', value = f'[Visit Website]({website_link})\n\n'
                                            '[Asset Explorer](https://ravencoin.asset-explorer.net/)\n'
                                            '[RVN Dashboard](https://www.rvn-dashboard.com/)\n'
                                            '[Whitepaper](https://ravencoin.org/assets/documents/Ravencoin.pdf)',
                                            inline=False)
                embed.add_field(name='Source', value=f'[Coingecko](https://www.coingecko.com/en/coins/ravencoin)')
                embed.set_footer(text=f'Last updated on {now.strftime("%B %d, %Y at %H:%M")}', icon_url=author_url)

                if message_id:
                    try:
                        message = await embed_channel.fetch_message(message_id)
                        await message.edit(embed=embed)
                        logger.info("Editing existing message")
                    except discord.NotFound:
                        logger.warning("Message not found, creating a new one")
                        message = await send_embed(embed_channel, embed)
                        message_id = message.id
                else:
                    message = await send_embed(embed_channel, embed)
                    message_id = message.id
                
                await asyncio.sleep(update_interval)

            except Exception as e:
                logger.error("An error occurred while updating RVN stats", exc_info=True)
                await asyncio.sleep(30)
            else:
                logger.info("RVN stats were successfully updated.")
