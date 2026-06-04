import logging
import config
import datetime
import discord
import asyncio
import io
import matplotlib.pyplot as plt
from utils import fetch_rvn_data, fetch_rvn_data_fallback, RVNData, update_bot_activity, send_embed, fetch_with_retry, load_message_id, save_message_id

logger = logging.getLogger(__name__)

async def fetch_price_history(client):
    data = await fetch_with_retry(client, config.RVN_HISTORY_URL)
    if data and 'prices' in data:
        return data['prices']
    logger.error("Failed to fetch price history")
    return None

def generate_chart(price_history):
    dates = [datetime.datetime.fromtimestamp(price[0]/1000) for price in price_history]
    prices = [price[1] for price in price_history]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, prices, color='orange')
    plt.title('RVN Price Last 30 Days')
    plt.xlabel('Date')
    plt.ylabel('Price (USD)')
    plt.grid(True, linestyle='--', alpha=0.7)

    # Rotate and align the tick labels so they look better
    plt.gcf().autofmt_xdate()

    # Use a tight layout
    plt.tight_layout()

    # Save the plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    return buf

async def update_statistics(bot):
    thumbnail_url = config.THUMBNAIL_URL
    description = config.DESCRIPTION
    author_url = config.AUTHOR_URL
    website_link = config.WEBSITE_LINK
    update_interval = config.UPDATE_INTERVAL

    embed_id_raw = config.EMBED_ID
    try:
        embed_channel_id = int(embed_id_raw) if embed_id_raw is not None else 0
    except (TypeError, ValueError):
        logger.error("EMBED_ID is not configured correctly. Expected a numeric Discord channel ID.")
        return
    if embed_channel_id == 0:
        logger.error("EMBED_ID is not configured correctly. Expected a non-zero Discord channel ID.")
        return

    message_id = load_message_id()

    while not bot.is_closed():
        if not bot.is_ready():
            logger.warning("Bot is not ready. Waiting before updating statistics.")
            await asyncio.sleep(60)
            continue

        guild = bot.get_guild(int(config.GUILD_ID)) if config.GUILD_ID else None
        if guild is None:
            logger.warning("Bot is ready but not connected to configured guild. Retrying in 60 seconds.")
            await asyncio.sleep(60)
            continue

        embed_channel = bot.get_channel(embed_channel_id)
        if embed_channel is None:
            logger.error("Embed channel not found. Check EMBED_ID and bot channel access.")
            await asyncio.sleep(60)
            continue

        if not message_id:
            async for msg in embed_channel.history(limit=1):
                if msg.author == bot.user:
                    message_id = msg.id
                    save_message_id(message_id)
                    break

        try:
            if bot.client is None:
                logger.warning("HTTP client not initialized yet. Retrying in 10 seconds.")
                await asyncio.sleep(10)
                continue

            now = datetime.datetime.now()
            rvn = await fetch_rvn_data_fallback(bot.client)
            if rvn is None:
                logger.error("All data sources failed")
                await asyncio.sleep(60)
                continue

            await update_bot_activity(bot, rvn.price)

            chart_buffer = None
            if rvn.source == 'CoinGecko':
                price_history = await fetch_price_history(bot.client)
                chart_buffer = generate_chart(price_history) if price_history else None

            fmt_price = f'${rvn.price:,.5f}'
            fmt_change_24h = f'{rvn.change_24h:,.2f}%' if rvn.change_24h is not None else 'N/A'
            fmt_change_7d = f'{rvn.change_7d:,.2f}%' if rvn.change_7d is not None else 'N/A'
            fmt_change_30d = f'{rvn.change_30d:,.2f}%' if rvn.change_30d is not None else 'N/A'
            fmt_volume = f'${rvn.volume:,.0f}' if rvn.volume else 'N/A'
            fmt_mcap = f'${rvn.mcap:,.0f}' if rvn.mcap else 'N/A'
            fmt_supply = f'{rvn.supply:,.0f} RVN' if rvn.supply else 'N/A'
            fmt_block_time = f'{rvn.block_time}' if rvn.block_time is not None else 'N/A'
            fmt_ath = f'${rvn.ath:,.5f}' if rvn.ath is not None else 'N/A'
            fmt_ath_change = f'{rvn.ath_change:,.2f}%' if rvn.ath_change is not None else 'N/A'
            fmt_ath_date = datetime.datetime.fromisoformat(rvn.ath_date.replace('Z', '+00:00')).strftime('%Y-%m-%d') if rvn.ath_date else 'N/A'

            embed = discord.Embed(
                title='Ravencoin Price & Statistics',
                description=description,
                colour=discord.Colour.orange()
            )
            chart_file = None
            embed.set_thumbnail(url=thumbnail_url)
            embed.set_author(name='', icon_url=thumbnail_url)
            if chart_buffer:
                chart_file = discord.File(chart_buffer, filename="rvn_chart.png")
                embed.set_image(url="attachment://rvn_chart.png")
            embed.add_field(name='Price', value=fmt_price)
            embed.add_field(name='24 Hour Change', value=fmt_change_24h)
            embed.add_field(name='7 Day Change', value=fmt_change_7d)
            embed.add_field(name='30 Day Change', value=fmt_change_30d)
            embed.add_field(name='24 Hour Volume', value=fmt_volume)
            embed.add_field(name='Market Cap', value=fmt_mcap)
            embed.add_field(name='Circulating Supply', value=fmt_supply)
            embed.add_field(name='Block Time (minutes)', value=fmt_block_time)
            embed.add_field(name='All-Time High', value=fmt_ath)
            embed.add_field(name='ATH Change %', value=fmt_ath_change)
            embed.add_field(name='ATH Date', value=fmt_ath_date)
            embed.add_field(name=f'{guild.name} Website', value=f'[Visit Website]({website_link})\n\n'
                                        '[Asset Explorer](https://ravencoin.asset-explorer.net/)\n'
                                        '[RVN Dashboard](https://www.rvn-dashboard.com/)\n'
                                        '[Whitepaper](https://ravencoin.org/assets/documents/Ravencoin.pdf)',
                                        inline=False)
            source_label = rvn.source.replace('CoinGecko', 'Coingecko')
            embed.add_field(name='Source', value=f'[{source_label}](https://www.coingecko.com/en/coins/ravencoin)')
            embed.set_footer(text=f'Last updated on {now.strftime("%B %d, %Y at %H:%M")}', icon_url=author_url)

            if message_id:
                try:
                    message = await embed_channel.fetch_message(message_id)
                    if chart_buffer and chart_file:
                        await message.edit(embed=embed, attachments=[chart_file])
                    else:
                        await message.edit(embed=embed)
                    logger.info("Editing existing message")
                except discord.NotFound:
                    logger.warning("Message not found, creating a new one")
                    if chart_buffer and chart_file:
                        message = await embed_channel.send(file=chart_file, embed=embed)
                    else:
                        message = await send_embed(embed_channel, embed)
                    if message:
                        message_id = message.id
                        save_message_id(message_id)
                    else:
                        logger.error("Failed to send embed after message-not-found fallback")
            else:
                if chart_buffer and chart_file:
                    message = await embed_channel.send(file=chart_file, embed=embed)
                else:
                    message = await send_embed(embed_channel, embed)
                if message:
                    message_id = message.id
                    save_message_id(message_id)
                else:
                    logger.error("Failed to send new embed message")
            
            await asyncio.sleep(update_interval)

        except discord.errors.Forbidden as e:
            logger.error(f"Permission error: {e}", exc_info=True)
            await asyncio.sleep(300)  # Wait 5 minutes before retrying
        except discord.errors.HTTPException as e:
            logger.error(f"Discord HTTP error: {e}", exc_info=True)
            await asyncio.sleep(60)  # Wait 1 minute before retrying
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}", exc_info=True)
            await asyncio.sleep(30)
        else:
            logger.info("RVN stats were successfully updated.")
