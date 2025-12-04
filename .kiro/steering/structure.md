# Project Structure

## Root Directory
```
.
├── .kiro/              # Kiro AI configuration and steering rules
├── .vscode/            # VSCode settings
├── templates/          # HTML templates (Jinja2)
├── static/             # CSS, JS, images
├── app.py              # Main Flask application
├── models.py           # Database models
├── monitor.py          # Background monitoring service
├── ssh_collector.py    # SSH connection and data collection
├── config.py           # Configuration settings
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## Key Components

### Backend
- `app.py`: Flask routes and web interface
- `models.py`: SQLAlchemy models (Switch, Metric, Alert)
- `monitor.py`: Scheduled polling and alert checking
- `ssh_collector.py`: SSH commands and parsing logic
- `config.py`: Centralized configuration

### Frontend
- `templates/`: Jinja2 HTML templates
- `static/`: CSS styling and JavaScript

## Conventions
- Follow Python PEP 8 style guidelines
- Use descriptive file and variable names
- Database models use singular names
- Routes follow RESTful patterns where applicable
