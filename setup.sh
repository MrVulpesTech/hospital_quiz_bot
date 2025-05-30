#!/bin/bash
# Hospital Quiz Bot Setup Script

# Exit on error
set -e

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

echo "=== Hospital Quiz Bot Setup ==="
echo "Setting up the Hospital Quiz Bot..."

# Create directories and user
echo "Creating user and directories..."
adduser hospital_bot --disabled-password --gecos "" || echo "User already exists"
mkdir -p /opt/hospital_quiz_bot
mkdir -p /var/log/hospital_quiz_bot

# Clone the repository
echo "Cloning the repository..."
if [ -d "/opt/hospital_quiz_bot/.git" ]; then
    cd /opt/hospital_quiz_bot
    git pull
else
    rm -rf /opt/hospital_quiz_bot/*
    git clone https://github.com/MrVulpesTech/hospital_quiz_bot.git /opt/hospital_quiz_bot
fi

# Copy service file
echo "Setting up systemd service..."
cp /opt/hospital_quiz_bot/hospital-quiz-bot.service /etc/systemd/system/

# Set up Python virtual environment
echo "Setting up Python environment..."
cd /opt/hospital_quiz_bot
python3 -m venv venv
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt
venv/bin/pip install redis aiosqlite

# Update ownership
echo "Setting permissions..."
chown -R hospital_bot:hospital_bot /opt/hospital_quiz_bot
chown -R hospital_bot:hospital_bot /var/log/hospital_quiz_bot

# Edit config file
if [ ! -f "/opt/hospital_quiz_bot/config.yaml" ]; then
    echo "Creating config file..."
    cp /opt/hospital_quiz_bot/config.yaml.example /opt/hospital_quiz_bot/config.yaml 2>/dev/null || echo "Config example not found, creating new config..."
    # If no example, the updated config.yaml should be present in the repo
fi

echo "Please edit the config file with your Telegram token and OpenAI API key:"
echo "sudo nano /opt/hospital_quiz_bot/config.yaml"

# Set up and start the service
echo "Setting up systemd service..."
systemctl daemon-reload
systemctl enable hospital-quiz-bot
systemctl restart hospital-quiz-bot

echo "=== Setup Complete ==="
echo "Check service status with: systemctl status hospital-quiz-bot"
echo "View logs with: journalctl -u hospital-quiz-bot -f" 