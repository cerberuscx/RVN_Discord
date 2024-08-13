import asyncio
import logging
import signal
import sys
import httpx
import config
from discord.ext import commands
import basic_events
import price_commands

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Bot Initialization
bot = commands.Bot(command_prefix="!", intents=config.intents)

# Global httpx client
client = None

@bot.event
async def on_ready():
    global client
    client = httpx.AsyncClient()
    await basic_events.on_ready(bot)

@bot.event
async def on_disconnect():
    await basic_events.on_disconnect()

@bot.command()
async def price(ctx):
    await price_commands.handle_price(ctx, client)

async def on_shutdown():
    global client
    if client:
        await client.aclose()
        client = None
        logger.info("httpx client closed.")
    
    logger.info("Shutting down bot...")
    await bot.close()
    logger.info("Bot has been shut down.")

def signal_handler(signum, frame):
    logger.info(f"Received shutdown signal: {signum}")
    sys.exit(0)

def main():
    # Register the signal handlers
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        bot.run(config.TOKEN)
    except SystemExit:
        logger.info("SystemExit received. Starting graceful shutdown.")
    except Exception as e:
        logger.error("An unexpected error occurred", exc_info=True)
    finally:
        asyncio.run(on_shutdown())
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    main()
