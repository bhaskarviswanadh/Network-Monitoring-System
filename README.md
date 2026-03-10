# Network Monitoring System

A production-ready network monitoring solution built with Python Flask that provides real-time visibility into network infrastructure health. This system monitors network switches via SSH, collects performance metrics, and displays them through an intuitive web dashboard with automated alerting capabilities.

##  Project Overview

This Network Monitoring System was developed to address the challenge of monitoring network infrastructure across a college campus with 18+ network switches. Traditional monitoring solutions like Zabbix require extensive setup and SNMP configuration on all devices. This lightweight alternative uses SSH connections to collect metrics directly from switches, making it faster to deploy and easier to maintain.

The system provides network administrators with:
- Real-time visibility into switch performance (CPU, memory, uptime)
- Automated alert generation for critical issues
- Historical data tracking for trend analysis
- Support for multiple switch vendors without additional configuration

**Real-world deployment:** Initially deployed on a campus VM to monitor production switches, now containerized and deployed on AWS EC2 with full CI/CD automation.

##  Key Features

- **SSH-Based Monitoring** - No SNMP configuration required; works with existing SSH access
- **Multi-Vendor Support** - Compatible with Cisco IOS/NX-OS, Aruba, TP-Link, D-Link, and Cambium switches
- **Real-Time Metrics** - Collects CPU usage, memory usage, uptime, and interface statistics
- **Automated Alerting** - Email notifications for critical events (switch down, high CPU/memory)
- **Web Dashboard** - Modern, responsive UI with real-time data visualization using Chart.js
- **Historical Data** - SQLite database stores metrics for trend analysis and troubleshooting
- **Configurable Thresholds** - Customizable alert thresholds for CPU, memory, and interface errors
- **Background Monitoring** - APScheduler runs automated polling every 120 seconds
- **Docker Support** - Fully containerized for consistent deployment across environments
- **CI/CD Pipeline** - Automated testing and validation using GitHub Actions

##  System Architecture

```
<!-- Architecture diagram will be added here -->
```

##  Technology Stack

### Backend
- **Python 3.10** - Core programming language
- **Flask 3.0+** - Web framework for API and dashboard
- **Flask-SQLAlchemy 3.1+** - ORM for database operations
- **APScheduler 3.10+** - Background task scheduling for automated polling

### Network Automation
- **Paramiko 3.4+** - SSH client for connecting to network switches
- **Custom SSH Collector** - Vendor-specific command parsing logic

### Database
- **SQLite** - Lightweight database for development and small deployments
- **SQLAlchemy ORM** - Database abstraction layer (supports PostgreSQL/MySQL for production)

### Containerization
- **Docker** - Application containerization
- **Docker Compose** - Multi-container orchestration
- **Gunicorn** - Production WSGI server (in production Dockerfile)

### CI/CD
- **GitHub Actions** - Automated CI pipeline
- **Docker Build** - Automated image building and testing

### Cloud Infrastructure
- **AWS EC2** - Cloud VM for deployment (demonstrated)
- **Compatible with** - Any cloud provider (Azure, GCP, DigitalOcean)

##  Project Structure

```
Network-Monitoring-System/
 .github/
    workflows/
        ci.yml                 # GitHub Actions CI pipeline
 .kiro/
    steering/                  # Project documentation
 instance/
    network_monitor.db         # SQLite database (created at runtime)
 static/
    script.js                  # Frontend JavaScript
    style.css                  # Custom styling
 templates/
    base.html                  # Base template
    index.html                 # Dashboard
    switches.html              # Device management
    switch_detail.html         # Individual switch view
    alerts.html                # Alert management
    analytics.html             # Analytics dashboard
    logs.html                  # System logs
    settings.html              # Configuration
    add_switch.html            # Add device form
 app.py                         # Main Flask application
 models.py                      # Database models (Switch, Metric, Alert)
 monitor.py                     # Background monitoring service
 ssh_collector.py               # SSH connection and data collection
 email_notifier.py              # Email alert system
 config.py                      # Configuration settings
 import_switches.py             # Bulk import utility
 migrate_database.py            # Database migration script
 requirements.txt               # Python dependencies
 Dockerfile                     # Development Docker image
 Dockerfile.prod                # Production Docker image (with Gunicorn)
 docker-compose.yml             # Docker Compose configuration
 .dockerignore                  # Docker build exclusions
 DOCKER.md                      # Docker deployment guide
 README.md                      # Project documentation
```

##  CI Pipeline

This project implements a continuous integration pipeline using **GitHub Actions** that automatically validates every code change.

### Pipeline Workflow

**Trigger Events:**
- Push to `main` branch
- Pull requests to `main` branch

**Pipeline Steps:**
1. **Checkout Code** - Clones the repository
2. **Build Docker Image** - Builds the application container using the Dockerfile
3. **Run Container Test** - Starts the container and verifies the application launches successfully
4. **Log Validation** - Captures container logs to ensure no startup errors
5. **Cleanup** - Stops and removes test container

**Benefits:**
- Catches build failures before deployment
- Ensures Docker configuration is always valid
- Validates application startup process
- Provides confidence for production deployments

##  Deployment

### Cloud Deployment (AWS EC2 / Any Cloud VM)

The application is deployed using Docker Compose for easy management and scalability.

**Prerequisites:**
- Cloud VM with Docker and Docker Compose installed
- Open port 5000 (or configure reverse proxy)
- SSH access to network switches from the VM

**Deployment Steps:**

1. **Clone the repository:**
```bash
git clone https://github.com/bhaskarviswa/Network-Monitoring-System.git
cd Network-Monitoring-System
```

2. **Deploy using Docker Compose:**
```bash
docker-compose up -d --build
```

3. **Verify deployment:**
```bash
docker-compose ps
docker-compose logs -f
```

4. **Access the dashboard:**
```
http://YOUR_VM_IP:5000
```

##  Run Locally

### Using Docker (Recommended)

**Quick Start:**
```bash
# Clone the repository
git clone https://github.com/bhaskarviswa/Network-Monitoring-System.git
cd Network-Monitoring-System

# Build and run with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Access the application
open http://localhost:5000
```

**Using Docker CLI:**
```bash
# Build the image
docker build -t network-monitoring-system .

# Run the container
docker run -d -p 5000:5000 --name network-monitor network-monitoring-system

# View logs
docker logs -f network-monitor

# Stop the container
docker stop network-monitor
docker rm network-monitor
```

### Manual Installation (Without Docker)

**Prerequisites:**
- Python 3.7+
- pip package manager

**Steps:**
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py

# Access the dashboard
open http://localhost:5000
```

##  Screenshots

### Dashboard UI
```
<!-- Screenshot of the main dashboard showing device status, metrics, and alerts will be added here -->
```

### Docker Container Running
```
<!-- Screenshot of docker ps output showing running container will be added here -->
```

### AWS Deployment
```
<!-- Screenshot of the application running on AWS EC2 will be added here -->
```

### GitHub Actions Pipeline
```
<!-- Screenshot of successful GitHub Actions workflow execution will be added here -->
```

##  Future Improvements

- [ ] **Enhanced Alert Notifications**
  - Slack integration for team notifications
  - SMS alerts for critical issues
  - Webhook support for custom integrations

- [ ] **Extended Vendor Support**
  - HP/HPE switches
  - Juniper EX series
  - Mikrotik devices
  - Ubiquiti UniFi switches

- [ ] **Advanced Metrics Integration**
  - SNMP integration for additional metrics
  - Bandwidth utilization tracking
  - Port-level statistics
  - Temperature monitoring

- [ ] **Authentication for Dashboard**
  - User authentication system
  - Role-based access control (RBAC)
  - SSH key-based authentication
  - Password encryption in database

##  Author

**Bhaskar Viswanath**
- GitHub: [@bhaskarviswa](https://github.com/bhaskarviswa)
- Project: [Network-Monitoring-System](https://github.com/bhaskarviswa/Network-Monitoring-System)

---

**Note:** This project was initially deployed on a campus VM to monitor production network switches and has been enhanced with modern DevOps practices including containerization, CI/CD pipelines, and cloud deployment capabilities.
