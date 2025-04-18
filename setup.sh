#!/bin/bash

# Make script exit on error
set -e

echo "Setting up Florence Plant-Human Interface..."

# Install system dependencies
echo "Installing system dependencies..."
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Enable SPI interface
echo "Enabling SPI interface..."
sudo raspi-config nonint do_spi 0

# Create desktop shortcut
echo "Creating desktop shortcut..."
cat > ~/Desktop/Florence.desktop << EOL
[Desktop Entry]
Name=Florence
Comment=Plant-Human Interface
Exec=bash -c 'cd ~/Florence_Cursor && source venv/bin/activate && sudo python app.py'
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
Type=simple
ExecStart=/bin/bash -c "cd /home/florence/Florence_Cursor && source venv/bin/activate && python app.py"
WorkingDirectory=/home/florence/Florence_Cursor
StandardOutput=inherit
StandardError=inherit
Restart=always
User=root
Environment=PYTHONUNBUFFERED=1
Environment=FLASK_APP=app.py
Environment=FLASK_ENV=development

[Install]
WantedBy=multi-user.target
EOL

# Stop the service if it's running
sudo systemctl stop florence.service || true

# Reload systemd configuration
sudo systemctl daemon-reload

# Start the service
sudo systemctl start florence.service

# Enable the service to start on boot
sudo systemctl enable florence.service

echo "Setup complete! Florence is now running as a service."
echo "You can access the interface at http://localhost:5000"
echo ""
echo "To view logs: sudo journalctl -u florence.service -f" 