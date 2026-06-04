# Top Priorities

This file tracks the highest-priority work for stability on a small VPS.

## P0 - Reliability and Operations

- [x] Run the bot as a `systemd` service (not tmux)
- [x] Use project venv Python in service unit
- [x] Install and validate `logrotate`
- [x] Pin dependency versions in `requirements.txt`
- [x] Add healthcheck watchdog and schedule it

## P1 - Follow-up Hardening

- [x] Improve shutdown handling for clean signal behavior
- [ ] Add strict env validation with clear startup errors
- [x] Add retry jitter for API backoff
- [x] Add fallback data source strategy
- [x] Persist embed `message_id` across restarts

## Notes

- P0 is complete as of 2026-03-01.
- Any completed item should also be recorded in `docs/CHANGELOG.md`.
