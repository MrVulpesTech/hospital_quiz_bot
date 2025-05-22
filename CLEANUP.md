# Hospital Quiz Bot Cleanup and Fresh Installation

If you're experiencing issues with your current installation, follow these steps to clean up and start fresh:

## Step 1: Stop and disable the service

```bash
sudo systemctl stop hospital-quiz-bot
sudo systemctl disable hospital-quiz-bot
```

## Step 2: Remove the existing installation

```bash
# Remove service file
sudo rm /etc/systemd/system/hospital-quiz-bot.service

# Backup your config if needed
sudo cp /opt/hospital_quiz_bot/config.yaml /tmp/config.yaml.backup

# Remove the installation directory
sudo rm -rf /opt/hospital_quiz_bot
```

## Step 3: Create fresh installation

```bash
# Create the directory
sudo mkdir -p /opt/hospital_quiz_bot

# Clone the repository directly
sudo git clone https://github.com/MrVulpesTech/hospital_quiz_bot.git /opt/hospital_quiz_bot
```

## Step 4: Set up the new installation

```bash
# Run the setup script
cd /opt/hospital_quiz_bot
sudo chmod +x setup.sh
sudo ./setup.sh
```

## Step 5: Configure your bot

```bash
# Edit the config file with your API keys
sudo nano /opt/hospital_quiz_bot/config.yaml
```

## Step 6: Start the service

```bash
sudo systemctl daemon-reload
sudo systemctl enable hospital-quiz-bot
sudo systemctl start hospital-quiz-bot
```

## Step 7: Verify it's working

```bash
sudo systemctl status hospital-quiz-bot
sudo journalctl -u hospital-quiz-bot -f
```

If you still encounter issues, check the logs for specific error messages and fix them one by one. 