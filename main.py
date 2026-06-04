import asyncio
import logging
import signal
import httpx
import config
from discord.ext import commands
import basic_events
import price_commands

# Logging Setup
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    handlers=[
                        logging.FileHandler("bot.log"),
                        logging.StreamHandler()
                    ])
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Bot Initialization
class RavencoinBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = None
        self.bg_task = None

    async def on_ready(self):
        try:
            if self.client is None:
                self.client = httpx.AsyncClient()

            user = self.user
            if user is None:
                logger.warning("on_ready fired but bot user is not available yet")
                return

            logger.info(f'We have logged in as {user}')
            logger.info(f'{user.name} is online!')
            logger.info(f'Bot ID: {user.id}')
            logger.info('----------------------------')

            if self.bg_task is None or self.bg_task.done():
                self.bg_task = self.loop.create_task(basic_events.update_statistics(self))
            else:
                logger.info("Background statistics task already running")
        except Exception as e:
            logger.error(f"Error in on_ready: {e}", exc_info=True)

    async def on_disconnect(self):
        logger.warning("The bot has been disconnected")
    
    async def on_resumed(self):
        logger.info("Bot has resumed connection")
        if self.bg_task and self.bg_task.done():
            self.bg_task = self.loop.create_task(basic_events.update_statistics(self))

    async def close(self):
        if self.client:
            await self.client.aclose()
            self.client = None
            logger.info("httpx client closed.")
        if self.bg_task:
            self.bg_task.cancel()
            try:
                await self.bg_task
            except asyncio.CancelledError:
                pass
        await super().close()

bot = RavencoinBot(command_prefix="!", intents=config.intents)

@bot.command()
async def price(ctx):
    if bot.client is None:
        await ctx.send("Bot client is still initializing. Please try again in a few seconds.")
        return
    await price_commands.handle_price(ctx, bot.client)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Type !help for a list of available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing required argument: {error.param}")
    else:
        logger.error(f"An error occurred: {error}", exc_info=True)
        await ctx.send("An error occurred while processing the command.")

def signal_handler(signum, frame):
    logger.info(f"Received shutdown signal: {signum}")
    asyncio.get_event_loop().stop()

def main():
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    try:
        token = config.TOKEN
        if not token:
            raise RuntimeError("TOKEN is not set in environment")
        bot.run(token)
    except Exception as e:
        logger.error("An unexpected error occurred", exc_info=True)
    finally:
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    main()
