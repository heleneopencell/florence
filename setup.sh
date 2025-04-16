#!/bin/bash

# Make script exit on error
set -e

echo "Setting up Florence Plant-Human Interface..."

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv libgpiod-dev libgpiod2 python3-libgpiod

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Configure GPIO10 for NeoPixel
echo "Configuring GPIO10 for NeoPixel..."
sudo raspi-config nonint do_spi 0

# Create a Python script to configure GPIO
cat > configure_gpio.py << EOL
import gpiod
import time

# Get the GPIO chip
chip = gpiod.Chip('gpiochip0')

# Get GPIO line 10
line = chip.get_line(10)

# Request the line as output
line.request(consumer="FLORENCE", type=gpiod.LINE_REQ_DIR_OUT)

# Set initial state to low
line.set_value(0)

# Release the line
line.release()
chip.close()
EOL

# Run the GPIO configuration script
echo "Running GPIO configuration..."
sudo python3 configure_gpio.py

# Create desktop shortcut
echo "Creating desktop shortcut..."
cat > ~/Desktop/Florence.desktop << EOL
[Desktop Entry]
Name=Florence
Comment=Plant-Human Interface
Exec=bash -c 'cd ~/Florence_Cursor && source venv/bin/activate && python app.py'
Type=Application
Categories=Utility;
EOL
chmod +x ~/Desktop/Florence.desktop

# Create systemd service
echo "Creating systemd service..."
sudo tee /etc/systemd/system/florence.service << EOL
[Unit]
Description=Florence Plant-Human Interface
After=network.target

[Service]
ExecStart=/bin/bash -c 'cd /home/florence/Florence_Cursor && source venv/bin/activate && python app.py'
WorkingDirectory=/home/florence/Florence_Cursor
StandardOutput=inherit
StandardError=inherit
Restart=always
User=florence

[Install]
WantedBy=multi-user.target
EOL

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable florence.service
sudo systemctl start florence.service

echo "Setup complete! Florence is now running as a service."
echo "You can access the interface at http://localhost:5000"
echo ""
echo "To view logs: sudo journalctl -u florence.service -f" 