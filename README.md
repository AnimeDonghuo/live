# Telegram RTMP Streamer Bot

A production-ready Telegram bot to manage 24/7 RTMP livestreams from pre-recorded videos, optimized for low-resource VPS (Debian 10/11).

## 🚀 Quick Start (Debian)

1. **Clone & Install:**
   ```bash
   git clone https://github.com/youruser/rtmp-bot.git
   cd rtmp-bot
   chmod +x install.sh
   ./install.sh
   
 ##  1. Configure:
Copy .env.example to .env.
Edit .env and add your BOT_TOKEN and OWNER_ID.

## 2.Deploy with Systemd:

   nano systemd/streamer.service # Check paths
cp systemd/streamer.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable streamer
systemctl start streamer

## Features
FFmpeg Engine: Intelligent -c copy detection to save CPU.
Auto-Re-encoding: Falls back to libx264 720p if format is incompatible.
Persistence: MongoDB stores your RTMP endpoints and video metadata.
Monitoring: Real-time CPU/RAM/Bitrate tracking.
Secure: Only the designated Owner ID can interact with the bot.
📁 Directory Structure
bot/: Telegram logic and command handlers.
services/: FFmpeg process management and system monitoring.
database/: MongoDB connection wrapper.
videos/: Storage for uploaded media.
logs/: Daily rotating logs.
⚠️ Requirements
Debian 10+
Python 3.10+
MongoDB
FFmpeg


### Final Review Checklist (Self-Verification):
1.  **Circular Imports:** Checked. `Config` and `Database` are imported carefully.
2.  **Path Traversal:** Handled in `sanitize_filename`.
3.  **CPU Usage:** Added `-preset veryfast` and `-c copy` logic to ensure a 2vCPU VPS doesn't choke.
4.  **Process Management:** `psutil` is used to cleanly terminate FFmpeg and its children.
5.  **Installation:** `install.sh` covers all Debian-specific dependencies.
6.  **Owner Lock:** `restricted` decorator applied to every command handler.

This repository is now **complete**. Every file mentioned in the structure has a corresponding implementation provided. You can now copy these into your project structure, run the install script, and deploy.
