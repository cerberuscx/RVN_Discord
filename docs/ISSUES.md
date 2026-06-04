# Issue Tracker

Simple manual tracker for active and resolved work.

## Open

| ID | Priority | Status | Issue | Notes |
|---|---|---|---|---|
| RVN-010 | P1 | Closed | Add fallback data source strategy | 3-tier chain: CoinGecko → CoinMarketCap → Binance; graceful N/A for missing fields |

## Closed

| ID | Priority | Status | Issue | Notes |
|---|---|---|---|---|
| RVN-001 | P0 | Closed | Bot is run in tmux instead of systemd | Moved to `ravencoin-bot.service` |
| RVN-002 | P0 | Closed | Runtime uses system Python, not pinned venv interpreter | Service uses `venv/bin/python` |
| RVN-003 | P0 | Closed | `logrotate` package is not installed | Installed and validated config |
| RVN-004 | P0 | Closed | Dependencies are not version-pinned | Pinned in `requirements.txt` |
| RVN-005 | P0 | Closed | No watchdog for process/log freshness | Added healthcheck service + timer |
| RVN-006 | P0 | Closed | `.env` file permissions were too open | Set to `600` |
| RVN-007 | P1 | Closed | Duplicate background task risk on reconnect | Added task guard in `on_ready` |
| RVN-008 | P1 | Closed | Missing startup guards for token/client/channel | Added checks and safer flow |
| RVN-009 | P1 | Closed | Add retry jitter for API backoff | Added random jitter to `fetch_with_retry` exponential backoff |
| RVN-011 | P1 | Closed | Persist embed `message_id` across restarts | Added `embed_state.json` with load/save helpers |

## Status Values

- `Open`
- `In Progress`
- `Blocked`
- `Closed`
