# Changelog

All notable changes to this project should be documented in this file.

## [Unreleased]

### Added
- `docs/` documentation structure and top-priority tracker.
- `matplotlib` added to `requirements.txt`.
- Startup/runtime guards for missing token/client and safer channel/guild handling.
- `scripts/healthcheck.sh` watchdog script for process/log freshness checks.
- `ravencoin-healthcheck.service` and `ravencoin-healthcheck.timer` for scheduled health monitoring.
- Retry jitter to `fetch_with_retry` for smoother API backoff (RVN-009).
- `embed_state.json` persistence for embed `message_id` across restarts (RVN-011).
- `load_message_id()` / `save_message_id()` helpers in `utils.py`.

### Changed
- Command prefix set to `!` to align behavior with README and bot messaging.
- `on_ready` now avoids creating duplicate background tasks.
- Bot runtime migrated from tmux to `ravencoin-bot.service` using `venv/bin/python`.
- Python dependencies pinned to exact versions in `requirements.txt`.
- Guild detection uses `bot.get_guild(GUILD_ID)` instead of `bot.guilds[0]`.
- Signal handler now calls `loop.stop()` instead of `sys.exit(0)` for clean shutdown.
- `httpx` logger suppressed to WARNING level to reduce log noise.
- Removed unused config (`ansi_colors`, `ansi_background_colors`, `ansi_styles`, `ALERTS_ID`, `TRACKER_ID`, `IMAGE_URL`, `SLEEP_INTERVAL`).
- Data fetching now uses a 3-tier fallback chain: CoinGecko → CoinMarketCap → Binance.
- `fetch_rvn_data_fallback()` returns a normalized `RVNData` object from any working source.
- Embed fields gracefully show `N/A` when fallback sources lack certain data (ATH, block time).

### Security
- `.env` file permissions tightened to `600`.

### Operations
- Added and validated `/etc/logrotate.d/ravencoin-bot` policy.
- Installed `logrotate` package.
