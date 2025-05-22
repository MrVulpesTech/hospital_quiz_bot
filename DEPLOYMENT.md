# Hospital Quiz Bot Deployment Guide

This guide provides step-by-step instructions for deploying the Hospital Quiz Bot on an Ubuntu server.

## Preparation

1. Create a dedicated user for the bot:
```bash
sudo adduser hospital_bot --disabled-password
```

2. Create the application directory:
```bash
sudo mkdir -p /opt/hospital_quiz_bot
```

## File Transfer

1. Transfer the project files to the server using one of these methods:
   
   Option 1: Using SCP (from your local machine):
   ```bash
   scp -r hospital_quiz_bot requirements.txt config.yaml quizes.yaml quizes_de.yaml prompts.md user@server:/tmp/
   ```
   
   Option 2: Using Git:
   ```bash
   git clone https://your-repository-url.git /tmp/hospital_quiz_bot
   ```

2. Move files to the application directory:
```bash
sudo cp -r /tmp/hospital_quiz_bot/* /opt/hospital_quiz_bot/
sudo cp config.yaml /opt/hospital_quiz_bot/
```

3. Ensure data files are in the correct location:
```bash
sudo mkdir -p /opt/hospital_quiz_bot/hospital_quiz_bot/data
sudo cp quizes.yaml quizes_de.yaml /opt/hospital_quiz_bot/hospital_quiz_bot/data/
sudo cp prompts.md /opt/hospital_quiz_bot/hospital_quiz_bot/data/
```

## Configuration

1. Create and set up log directory:
```bash
sudo mkdir -p /var/log/hospital_quiz_bot
sudo chown hospital_bot:hospital_bot /var/log/hospital_quiz_bot
```

2. Set proper ownership for application files:
```bash
sudo chown hospital_bot:hospital_bot -R /opt/hospital_quiz_bot
```

3. Set up the virtual environment:
```bash
cd /opt/hospital_quiz_bot
sudo -u hospital_bot python3 -m venv venv
sudo -u hospital_bot venv/bin/pip install --upgrade pip
sudo -u hospital_bot venv/bin/pip install -r requirements.txt
```

4. Edit the configuration file with your credentials:
```bash
sudo -u hospital_bot nano /opt/hospital_quiz_bot/config.yaml
```
   - Add your Telegram Bot Token (`telegram.token`)
   - Add your OpenAI API Key (`openai.api_key`)
   - Adjust other settings if needed

## Systemd Service Setup

1. Copy the service file to systemd:
```bash
sudo cp hospital-quiz-bot.service /etc/systemd/system/
```

2. Reload systemd to recognize the new service:
```bash
sudo systemctl daemon-reload
```

3. Start the service:
```bash
sudo systemctl start hospital-quiz-bot
```

4. Enable the service to start on boot:
```bash
sudo systemctl enable hospital-quiz-bot
```

## Monitoring and Maintenance

1. Check service status:
```bash
sudo systemctl status hospital-quiz-bot
```

2. View logs:
```bash
sudo journalctl -u hospital-quiz-bot -f
```

3. Restart the service after changes:
```bash
sudo systemctl restart hospital-quiz-bot
```

## Troubleshooting

- If the bot fails to start, check logs for errors:
```bash
sudo journalctl -u hospital-quiz-bot -e
```

- Verify file permissions:
```bash
ls -la /opt/hospital_quiz_bot
ls -la /var/log/hospital_quiz_bot
```

- Check configuration file format:
```bash
sudo -u hospital_bot cat /opt/hospital_quiz_bot/config.yaml
```

- Test the bot manually:
```bash
cd /opt/hospital_quiz_bot
sudo -u hospital_bot venv/bin/python -m hospital_quiz_bot.bot
```

- If you encounter YAML parsing errors, verify the syntax:
```bash
sudo -u hospital_bot python3 -c "import yaml; yaml.safe_load(open('/opt/hospital_quiz_bot/config.yaml'))"
```

## System Requirements

- Python 3.10 or newer
- Ubuntu 20.04 or newer
- At least 1GB RAM
- At least 5GB disk space 