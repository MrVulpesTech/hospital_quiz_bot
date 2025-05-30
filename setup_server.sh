#!/bin/bash
# Hospital Quiz Bot Server Setup Script

# Exit on error
set -e

# Check if running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "This script must be run as root"
    exit 1
fi

echo "=== Hospital Quiz Bot Server Setup ==="
echo "This script will set up the Hospital Quiz Bot on your server."
echo

# Create user
echo "Creating hospital_bot user..."
adduser hospital_bot --disabled-password --gecos "" || echo "User already exists"

# Create directories
echo "Creating directories..."
mkdir -p /opt/hospital_quiz_bot
mkdir -p /var/log/hospital_quiz_bot

# Copy files
echo "Copying files..."
cp -r hospital_quiz_bot /opt/hospital_quiz_bot/
cp requirements.txt /opt/hospital_quiz_bot/
cp config.yaml /opt/hospital_quiz_bot/
cp hospital-quiz-bot.service /etc/systemd/system/

# Create data directory if it doesn't exist
mkdir -p /opt/hospital_quiz_bot/hospital_quiz_bot/data

# Copy data files
echo "Copying data files..."
cp quizes.yaml /opt/hospital_quiz_bot/hospital_quiz_bot/data/
cp quizes_de.yaml /opt/hospital_quiz_bot/hospital_quiz_bot/data/
cp prompts.md /opt/hospital_quiz_bot/hospital_quiz_bot/data/

# Set permissions
echo "Setting permissions..."
chown hospital_bot:hospital_bot -R /opt/hospital_quiz_bot
chown hospital_bot:hospital_bot /var/log/hospital_quiz_bot

# Setup virtual environment
echo "Setting up Python virtual environment..."
cd /opt/hospital_quiz_bot
su -c "python3 -m venv venv" hospital_bot
su -c "venv/bin/pip install --upgrade pip" hospital_bot
su -c "venv/bin/pip install -r requirements.txt" hospital_bot

# Reload systemd
echo "Setting up systemd service..."
systemctl daemon-reload

echo
echo "=== Setup Complete ==="
echo
echo "Next steps:"
echo "1. Edit the configuration file:"
echo "   nano /opt/hospital_quiz_bot/config.yaml"
echo
echo "2. Start the service:"
echo "   systemctl start hospital-quiz-bot"
echo
echo "3. Enable the service to start on boot:"
echo "   systemctl enable hospital-quiz-bot"
echo
echo "4. Check the service status:"
echo "   systemctl status hospital-quiz-bot"
echo 