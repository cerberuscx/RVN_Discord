# Ravencoin Discord Bot

This is the official Discord bot for the Ravencoin community. It provides real-time updates on RVN metrics, including price, market cap, volume, and circulating supply.

## Features

- Displays current Ravencoin price and statistics in an embedded message
- Updates a channel name with the current RVN price
- Responds to price inquiries with the current RVN price

## Setup

1. Clone this repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```
3. Create a `.env` file in the root directory and add the following:
```
TOKEN=your_discord_bot_token_here
GUILD_ID=your_guild_id_here
CHANNEL_ID=your_channel_id_here
EMBED_ID=your_embed_channel_id_here
```
(Fill in the appropriate values for your Discord server)

4. Run the bot:
```
python main.py
```
## Commands

- `!price`: Responds with the current RVN price

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Disclaimer

This bot is not financial advice. Always do your own research before making any investment decisions.
