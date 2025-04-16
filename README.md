# Florence: Plant-Human Interface

An interactive art installation that enables communication between humans and plants through light and text.

## Hardware Requirements

* Raspberry Pi 5
* 24-LED RGB Adafruit NeoPixel Ring
* USB Thermal Printer
* Display for web interface

## Hardware Setup

1. Connect the NeoPixel Ring:
   * Data pin to GPIO10 (MOSI)
   * Power to 5V
   * Ground to GND

2. Connect the thermal printer via USB

## Software Requirements

* Raspberry Pi OS (Bullseye or newer)
* Python 3.9+
* Web browser

## Software Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/heleneopencell/florence.git
   cd florence
   ```

2. Run the setup script:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. Reboot the Raspberry Pi:
   ```bash
   sudo reboot
   ```

## Usage

1. After reboot, the Florence interface will automatically start
2. Double-click the Florence icon on the desktop to open the web interface
3. The interface will be available at: http://localhost:5000

## LED Patterns

The LED ring uses different patterns to represent different types of communication:

* 🔴 Red Blink x3: Greeting
* 🔵 Blue Slow Pulse x5: Appreciation
* 🔴 Red Fade in/out x5: Connection
* 🔵 Blue Blink-pulse x5: Question
* 🟢 Green Flash x1: Time reference

## Troubleshooting

1. If the NeoPixel ring doesn't work:
   * Check if SPI is enabled: `sudo raspi-config nonint get_spi`
   * Verify GPIO10 is properly connected
   * Check power connections
   * Verify GPIO10 is set as output: `cat /sys/class/gpio/gpio10/direction`

2. If the thermal printer doesn't work:
   * Check USB connection
   * Verify printer is powered on
   * Check printer permissions

3. If the web interface doesn't load:
   * Check if the Florence service is running: `sudo systemctl status florence`
   * Check logs: `sudo journalctl -u florence.service -f`

## Service Management

* Start the service: `sudo systemctl start florence`
* Stop the service: `sudo systemctl stop florence`
* Restart the service: `sudo systemctl restart florence`
* View logs: `sudo journalctl -u florence.service -f`

## Project Structure

```
florence/
├── app.py                 # Main Flask application
├── hardware/
│   ├── led_controller.py  # NeoPixel control
│   └── printer_controller.py # Thermal printer control
├── static/
│   ├── css/
│   │   └── style.css     # Retro interface styling
│   └── js/
│       └── main.js       # Interface interactions
└── templates/
    └── index.html        # Main interface template
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 