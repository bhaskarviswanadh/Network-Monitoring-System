# Technology Stack

## Language
- Python 3.7+

## Framework & Libraries
- Flask: Web framework
- Flask-SQLAlchemy: Database ORM
- Paramiko: SSH connections to switches
- APScheduler: Background task scheduling
- Chart.js: Frontend data visualization

## Database
- SQLite (development)
- Can be switched to PostgreSQL/MySQL for production

## Development Environment
- VSCode with Kiro AI assistant

## Common Commands

### Setup
```bash
pip install -r requirements.txt
```

### Initialize Database
```bash
python app.py
```

### Running
```bash
python app.py
```

The application runs on http://localhost:5000

### Configuration
Edit `config.py` to adjust:
- Polling intervals
- Alert thresholds
- SSH timeouts
