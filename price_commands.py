from utils import fetch_rvn_data

async def handle_price(ctx, client):
    price = await fetch_rvn_data(client)
    if price is not None:
        await ctx.send(f"Current RVN price: ${price:,.5f} USD")
    else:
        await ctx.send("Failed to fetch RVN price. Please try again later.")
