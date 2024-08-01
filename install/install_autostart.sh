#!/bin/bash

# Get the current directory
CURRENT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"


echo "$BEACHBOT_HOME/Scripts/"
mkdir -p "$BEACHBOT_HOME/Scripts/"
cp "$CURRENT_DIR/../scripts/start_beachbot.sh" "$BEACHBOT_HOME/Scripts/start_beachbot.sh"
chmod +x "$BEACHBOT_HOME/Scripts/start_beachbot.sh"

# Check if start_beachbot_ap.sh exists
if [ ! -f "$BEACHBOT_HOME/Scripts/start_beachbot.sh" ]; then
    echo "Error: start_beachbot.sh not found in the $BEACHBOT_HOME/Scripts."
    exit 1
fi

# Create a new sudoers file for the script
#TODO:
#sudo sh -c "echo '%wheel ALL= NOPASSWD: /usr/bin/systemctl poweroff' >> /etc/sudoers"
#gnome-session-quit --power-off --force --no-prompt
#sudo sh -c "echo '%sudo ALL=NOPASSWD: /usr/sbin/shutdown' | sudo tee /etc/sudoers.d/poweroff_beachbot"
sudo sh -c "echo '%sudo ALL=NOPASSWD: ${BEACHBOT_HOME}/Scripts/start_beachbot.sh' | sudo tee /etc/sudoers.d/start_beachbot"

# Create the systemd service unit file
sudo sh -c "
cat <<EOF > /etc/systemd/system/start_beachbot.service
[Unit]
Description=Start Beachbot Script
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/nohup $BEACHBOT_HOME/Scripts/start_beachbot.sh
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
"

# Reload systemd
sudo systemctl daemon-reload
# Enable and start the service
sudo systemctl enable start_beachbot.service
sudo systemctl start start_beachbot.service
