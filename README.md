# Florence: Plant-Human Interface

An interactive art installation that enables communication between humans and plants through light and text.

## Hardware Requirements

* Raspberry Pi 5
* 24-LED RGB Adafruit NeoPixel Ring
* USB Thermal Printer
* Display for web interface

## Software Requirements

* Raspberry Pi OS (Bullseye or newer)
* Python 3.9+
* Web browser

## Hardware Setup

1. Connect the NeoPixel Ring:
   * Data pin to GPIO18
   * Power to 5V
   * Ground to GND

2. Connect the thermal printer via USB

## Software Installation

1. Clone this repository:
   ```bash
   git clone <repository-url>
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
   * Check if audio is disabled in /boot/config.txt
   * Verify GPIO18 is properly connected
   * Check power connections

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