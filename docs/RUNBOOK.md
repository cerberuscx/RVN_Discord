# Runbook

Operational steps for the Ravencoin bot.

## Verify Bot Is Running

```bash
systemctl status ravencoin-bot.service --no-pager
ps -eo pid,etime,%cpu,%mem,cmd | grep "RAVENCOIN/main.py" | grep -v grep
```

## Check Live Log Activity

```bash
tail -n 50 /home/ubuntu/RAVENCOIN/bot.log
```

Healthy patterns:
- `HTTP/1.1 200 OK`
- `Successfully fetched RVN price`
- `Editing existing message`

## Restart (systemd mode)

```bash
sudo systemctl restart ravencoin-bot.service
```

Optional live logs:

```bash
journalctl -u ravencoin-bot.service -f
```

## Post-Restart Validation

1. Confirm service state is `active (running)`.
2. Confirm one bot process with `venv/bin/python`.
2. Confirm log shows startup lines (`logged in`, `online`, `Bot ID`).
3. Confirm first successful update cycle.

## Common Warnings

- `PyNaCl is not installed, voice will NOT be supported`
  - Safe to ignore unless voice features are needed.

- `The bot has been disconnected`
  - Temporary network/Discord gateway event; verify resume and subsequent successful updates.

## Recovery Checklist

1. Confirm internet and DNS from VPS.
2. Confirm bot token and channel IDs in `.env`.
3. Confirm Discord permissions for embed channel.
4. Restart bot and verify first successful cycle.
