#!/bin/bash
set -e

echo "🚀 Starting Installation for Debian RTMP Bot..."

# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install Dependencies
sudo apt install -y python3-pip python3-venv ffmpeg mongodb-server screen curl

# 3. Create Environment
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 4. Setup Directories
mkdir -p videos logs

# 5. Check FFmpeg version
ffmpeg -version | head -n 1

echo "✅ Environment Ready."
echo "Please configure .env file before starting."
