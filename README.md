# Network Monitoring System

A Zabbix-like network monitoring tool for monitoring switches via SSH. Built with Python Flask.

## Features

- SSH-based monitoring of network switches
- Real-time metrics collection (CPU, Memory, Uptime, Interface stats)
- Web-based dashboard
- Alert system with configurable thresholds
- Support for multiple switch vendors (Cisco IOS, NX-OS, Arista, Juniper)
- Historical data tracking and visualization

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Initialize the database:
```bash
python app.py
```

The application will create a SQLite database and start the monitoring service.

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:5000
```

3. Add your switches:
   - Click "Switches" in the navigation
   - Click "+ Add Switch"
   - Enter switch details (name, IP, SSH credentials)
   - Click "Add Switch"

4. The system will automatically start monitoring your switches every 60 seconds.

## Configuration

Edit `config.py` to customize:

- `POLLING_INTERVAL`: How often to poll switches (default: 60 seconds)
- `SSH_TIMEOUT`: SSH connection timeout (default: 10 seconds)
- `CPU_THRESHOLD`: CPU usage alert threshold (default: 80%)
- `MEMORY_THRESHOLD`: Memory usage alert threshold (default: 80%)
- `INTERFACE_ERROR_THRESHOLD`: Interface error count threshold (default: 100)

## Architecture

- **Flask**: Web framework
- **SQLAlchemy**: Database ORM
- **Paramiko**: SSH connections
- **APScheduler**: Background task scheduling
- **Chart.js**: Data visualization

## Security Notes

- Passwords are stored in the database (consider encrypting in production)
- Use strong SSH credentials
- Run behind a reverse proxy (nginx/Apache) in production
- Consider using SSH keys instead of passwords

## Requirements

- Python 3.7+
- SSH access to network switches
- Network switches must support standard show commands
