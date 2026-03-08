from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Switch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    ip_address = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    device_type = db.Column(db.String(50), default='cisco_ios')
    status = db.Column(db.String(20), default='unknown')
    last_seen = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    metrics = db.relationship('Metric', backref='switch', lazy=True, cascade='all, delete-orphan')
    alerts = db.relationship('Alert', backref='switch_ref', lazy=True, foreign_keys='Alert.switch_id')

class Metric(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    cpu_usage = db.Column(db.Float)
    memory_usage = db.Column(db.Float)
    uptime = db.Column(db.String(100))
    interface_data = db.Column(db.Text)  # JSON string of interface stats
    
class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    switch_id = db.Column(db.Integer, db.ForeignKey('switch.id', ondelete='SET NULL'), nullable=True)
    switch_name = db.Column(db.String(100))  # Store switch name for historical reference
    switch_ip = db.Column(db.String(50))  # Store IP for historical reference
    alert_type = db.Column(db.String(50), nullable=False)
    severity = db.Column(db.String(20), nullable=False)  # info, warning, critical
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    acknowledged = db.Column(db.Boolean, default=False)
