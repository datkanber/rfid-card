# RFID Reader with Flask and Sound Alerts

This project is a simple RFID card reader application that uses a USB HID device to read RFID cards, validate their authorization, and respond with appropriate actions. The application also integrates a Flask web server and plays sound alerts for authorized and unauthorized access.

---

## Features

- **RFID Card Reading**: Reads RFID cards via a USB HID device.
- **Card Authorization**: Compares card data against a predefined authorized card number.
- **Sound Alerts**: Plays a sound for authorized or unauthorized card reads.
- **Flask Web Server**: Redirects to a specific URL for authorized cards, shows an unauthorized message for others.
- **Debounce Mechanism**: Prevents repeated reads of the same card within a short period.

---

## Prerequisites

- **Python**: Version 3.8 or higher.
- **pip**: Python package manager.
- **Dependencies**: Install the following Python packages:
  - `Flask`
  - `pygame`
  - `hidapi`

---

## Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-repository/rfid-reader.git
   cd rfid-reader
   pip install -r requirements.txt
   python app.py

## Dependencies

- Flask: Web framework for serving the app.
- pygame: Plays audio feedback for card reads.
- hidapi: Handles communication with the RFID USB device.

2. **Install them via:**
   ```bash
   git clone https://github.com/your-repository/rfid-reader.git
