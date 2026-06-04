import logging
from utils import fetch_rvn_data

logger = logging.getLogger(__name__)

async def handle_price(ctx, client):
    try:
        price = await fetch_rvn_data(client)
        if price is not None:
            await ctx.send(f"Current RVN price: ${price:,.5f} USD")
        else:
            await ctx.send("Failed to fetch RVN price. Please try again later.")
    except Exception as e:
        logger.error(f"An error occurred while handling price command: {e}")
        await ctx.send("An unexpected error occurred. Please try again later.")