# tMod-Server-Updater
Script to back up and deploy new versions of tModLoader on an existing installation.

## Requirements
- Python 3.11+
- `tmux`
- A working tModLoader server install under `/root/tModLoader`
- Existing server logs at `/root/tModLoader/tModLoader-Logs/server.log`

Install `tmux`:

```bash
apt-get install tmux
```

Install runtime Python dependencies:

```bash
pip3 install -r requirements.txt
```

Create backup directory:

```bash
mkdir -p /root/backup
```

## Startup scripts
Place these scripts in `/root/tModLoader/` and make them executable.

`boot_start.sh`

```bash
#!/bin/bash
tmux new -d -s tmod
tmux send-keys -t tmod:. "cd /root/tModLoader" C-m
tmux send-keys -t tmod:. "./start.sh boot" C-m
```

`start.sh`

```bash
#!/bin/bash
if [[ $1 == "boot" ]]; then
  sleep 15
fi
while :
do
  cd /root/tModLoader
  chmod 755 *.sh
  ./start-tModLoaderServer.sh -nosteam -noupnp
  echo "Press [CTRL+C] to stop.."
  sleep 5
done
```

Make shell scripts executable:

```bash
chmod +x /root/tModLoader/*.sh
```

To restart automatically on reboot, add this crontab entry:

```cron
@reboot /root/tModLoader/boot_start.sh
```

## Install and run updater
Copy `version_update.py` to your target host (for example `/root/`) and make it executable:

```bash
chmod +x version_update.py
```

Run once with no valid command to confirm installation and create version tracking metadata:

```bash
./version_update.py
```

Commands:

```bash
./version_update.py check
./version_update.py upgrade
```

Behavior:
- `check`: prints installed/latest version and exits `0` (up-to-date) or `42` (update available)
- `upgrade`: backs up executable/data files, installs latest release, restores config files

Exit codes:
- `0`: exit without error, no upgrade available
- `2`: missing/invalid command
- `42`: new version available
- `69`: file move/copy errors detected
- `88`: upgrade complete

## Lint and quality checks
This repo uses `pre-commit` with `uv` and a lint dependency group in `pyproject.toml`.

Run full lint suite:

```bash
uv run --group lint pre-commit run --all-files
```

Run a specific file:

```bash
uv run --group lint pre-commit run --files version_update.py
```

Included checks:
- `ruff`
- `grain`
- basic pre-commit hygiene hooks
- `pytest` (when `tests/` exists)

Manual-stage hooks are also configured for:
- `shellcheck`
- `shfmt`
- `yamllint`
- `sqlfluff`
- `semgrep`
- `codeql`
