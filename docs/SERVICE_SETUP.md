# systemd Service Setup

Use this to run the bot as a managed service with auto-restart.

## 1) Create Service File

Create `/etc/systemd/system/ravencoin-bot.service`:

```ini
[Unit]
Description=Ravencoin Discord Bot
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/RAVENCOIN
EnvironmentFile=/home/ubuntu/RAVENCOIN/.env
ExecStart=/home/ubuntu/RAVENCOIN/venv/bin/python main.py
Restart=always
RestartSec=5
TimeoutStopSec=30

[Install]
WantedBy=multi-user.target
```

## 2) Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable ravencoin-bot.service
sudo systemctl start ravencoin-bot.service
```

## 3) Verify

```bash
systemctl status ravencoin-bot.service
journalctl -u ravencoin-bot.service -n 100 --no-pager
```

## 4) Disable tmux Runtime

After service is healthy, stop the tmux-run bot to avoid duplicate instances.
