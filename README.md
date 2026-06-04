# Ravencoin Discord Bot

This is the official Discord bot for the Ravencoin community. It provides real-time updates on RVN metrics, including price, market cap, volume, and circulating supply.

## Development Entry Point

Use this file as the entry point for development work and fresh LLM conversations.
Before making changes, check the docs index below for current priorities, known issues, and operational notes.

## Docs Index

- `docs/TOP_PRIORITIES.md`: active reliability and operations priorities
- `docs/ISSUES.md`: tracked issues and status
- `docs/CHANGELOG.md`: project change history
- `docs/RUNBOOK.md`: deploy, restart, verify, and recovery steps
- `docs/SERVICE_SETUP.md`: systemd service setup for production runtime

## Features

### Auto-Updating Price Embed
A live embed in the configured channel auto-updates every 30 minutes with:
- Current RVN price, 24h/7d/30d change percentages
- 24h volume, market cap, circulating supply
- All-time high with change % and date
- Block time
- 30-day price chart (when CoinGecko is the active source)
- Data source attribution

The embed survives bot restarts — its message ID is persisted to `embed_state.json`.

### Status Activity Ticker
The bot's Discord "Watching" status displays the current RVN price (e.g. "Watching RVN: $0.04250 USD"), updating every cycle.

### Data Sources (3-Tier Fallback Chain)
The bot tries sources in order until one succeeds:

| Priority | Source | Data | Key Required |
|----------|--------|------|-------------|
| 1° | **CoinGecko** | Full stats + 30d price chart | No |
| 2° | **CoinMarketCap** (keyless API) | Price, market cap, volume, supply, 24h/7d/30d change | No |
| 3° | **Binance** (public ticker) | Price, 24h change, volume only | No |

Fields that are unavailable from a fallback source display as `N/A`.

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

For production on VPS, prefer a systemd service instead of running directly in a terminal.

## Commands

- `!price`: Responds with the current RVN price (fetched from CoinGecko simple price endpoint)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Disclaimer

This bot is not financial advice. Always do your own research before making any investment decisions.
