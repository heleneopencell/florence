#!/bin/bash

# Make script exit on error
set -e

echo "Setting up Florence Plant-Human Interface..."

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Configure audio settings for NeoPixel
echo "Configuring audio settings for NeoPixel..."
sudo sed -i 's/^dtparam=audio=on/#dtparam=audio=on/' /boot/config.txt
echo "dtoverlay=pwm" | sudo tee -a /boot/config.txt

# Create desktop shortcut
echo "Creating desktop shortcut..."
cat > ~/Desktop/florence.desktop << EOL
[Desktop Entry]
Name=Florence
Comment=Plant-Human Interface
Exec=/usr/bin/python3 $(pwd)/florence/app.py
Type=Application
Terminal=false
Categories=Application;
Icon=$(pwd)/florence/static/icon.png
EOL

chmod +x ~/Desktop/florence.desktop

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/florence.service << EOL
[Unit]
Description=Florence Plant-Human Interface
After=network.target

[Service]
ExecStart=$(pwd)/venv/bin/python $(pwd)/florence/app.py
WorkingDirectory=$(pwd)
StandardOutput=inherit
StandardError=inherit
Restart=always
User=$USER

[Install]
WantedBy=multi-user.target
EOL

# Enable and start service
sudo systemctl enable florence.service
sudo systemctl start florence.service

echo "Setup complete! Please reboot your Raspberry Pi for all changes to take effect."
echo "After reboot, you can start Florence by:"
echo "1. Double-clicking the Florence icon on the desktop"
echo "2. The service will also start automatically on boot"
echo ""
echo "To view logs: sudo journalctl -u florence.service -f" 