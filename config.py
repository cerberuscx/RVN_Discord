import os
import discord
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
THUMBNAIL_URL = os.getenv('THUMBNAIL_URL', 'https://i.imgur.com/tqLb13l.png')
IMAGE_URL = os.getenv('IMAGE_URL', 'https://i.imgur.com/7OZBPAz.jpg')
AUTHOR_URL = os.getenv('AUTHOR_URL', 'https://i.imgur.com/z1KjbkG.png')
ALERTS_ID = int(os.getenv('ALERTS_ID', 0))
TRACKER_ID = int(os.getenv('TRACKER_ID', 0))
CHANNEL_ID = os.getenv('CHANNEL_ID')
EMBED_ID = os.getenv('EMBED_ID')
SLEEP_INTERVAL = int(os.getenv('SLEEP_INTERVAL', 60))
UPDATE_INTERVAL = int(os.getenv('UPDATE_INTERVAL', 1800))

DESCRIPTION = 'Official Ravencoin Discord bot providing up-to-date market data and statistics.'
WEBSITE_LINK = 'https://ravencoin.org/'

intents = discord.Intents.default()
intents.message_content = True

RVN_PRICE_URL = 'https://api.coingecko.com/api/v3/simple/price?ids=ravencoin&vs_currencies=usd'
RVN_DATA_URL = 'https://api.coingecko.com/api/v3/coins/ravencoin'

# ANSI Constants and Styled Text Function
ansi_colors = {
    "gray": "30", "red": "31", "green": "32", "yellow": "33",
    "blue": "34", "pink": "35", "cyan": "36", "white": "37"
}
ansi_background_colors = {
    "firefly_dark_blue": "40", "orange": "41", "marble_blue": "42", 
    "greyish_turquoise": "43", "gray": "44", "indigo": "45", 
    "light_gray": "46", "white": "47"
}
ansi_styles = {"normal": "0", "bold": "1", "underline": "4"}
