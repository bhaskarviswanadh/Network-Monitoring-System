from flask import Flask, render_template, request, jsonify, redirect, url_for
from models import db, Switch, Metric, Alert
from monitor import NetworkMonitor
from config import Config
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

# Initialize monitor
monitor = NetworkMonitor(app)

@app.route('/')
def index():
    """Dashboard view"""
    switches = Switch.query.all()
    total_switches = len(switches)
    up_switches = len([s for s in switches if s.status == 'up'])
    down_switches = len([s for s in switches if s.status == 'down'])
    
    recent_alerts = Alert.query.filter_by(acknowledged=False).order_by(Alert.timestamp.desc()).limit(10).all()
    
    return render_template('index.html',
                         switches=switches,
                         total_switches=total_switches,
                         up_switches=up_switches,
                         down_switches=down_switches,
                         alerts=recent_alerts)

@app.route('/switches')
def switches():
    """List all switches"""
    all_switches = Switch.query.all()
    return render_template('switches.html', switches=all_switches)

@app.route('/switch/<int:switch_id>')
def switch_detail(switch_id):
    """Detailed view of a single switch"""
    switch = Switch.query.get_or_404(switch_id)
    
    # Get recent metrics (last 24 hours)
    since = datetime.utcnow() - timedelta(hours=24)
    metrics = Metric.query.filter(
        Metric.switch_id == switch_id,
        Metric.timestamp >= since
    ).order_by(Metric.timestamp.desc()).all()
    
    # Get alerts for this switch
    alerts = Alert.query.filter_by(switch_id=switch_id).order_by(Alert.timestamp.desc()).limit(20).all()
    
    return render_template('switch_detail.html', switch=switch, metrics=metrics, alerts=alerts)

@app.route('/switch/add', methods=['GET', 'POST'])
def add_switch():
    """Add a new switch"""
    if request.method == 'POST':
        switch = Switch(
            name=request.form['name'],
            ip_address=request.form['ip_address'],
            username=request.form['username'],
            password=request.form['password'],
            device_type=request.form.get('device_type', 'cisco_ios')
        )
        db.session.add(switch)
        db.session.commit()
        return redirect(url_for('switches'))
    
    return render_template('add_switch.html')

@app.route('/switch/<int:switch_id>/delete', methods=['POST'])
def delete_switch(switch_id):
    """Delete a switch"""
    switch = Switch.query.get_or_404(switch_id)
    db.session.delete(switch)
    db.session.commit()
    return redirect(url_for('switches'))

@app.route('/alerts')
def alerts():
    """View all alerts"""
    all_alerts = Alert.query.order_by(Alert.timestamp.desc()).all()
    return render_template('alerts.html', alerts=all_alerts)

@app.route('/alert/<int:alert_id>/acknowledge', methods=['POST'])
def acknowledge_alert(alert_id):
    """Acknowledge an alert"""
    alert = Alert.query.get_or_404(alert_id)
    alert.acknowledged = True
    db.session.commit()
    return jsonify({'status': 'success'})

@app.route('/api/metrics/<int:switch_id>')
def api_metrics(switch_id):
    """API endpoint for switch metrics"""
    hours = request.args.get('hours', 24, type=int)
    since = datetime.utcnow() - timedelta(hours=hours)
    
    metrics = Metric.query.filter(
        Metric.switch_id == switch_id,
        Metric.timestamp >= since
    ).order_by(Metric.timestamp.asc()).all()
    
    data = {
        'timestamps': [m.timestamp.isoformat() for m in metrics],
        'cpu': [m.cpu_usage for m in metrics],
        'memory': [m.memory_usage for m in metrics]
    }
    
    return jsonify(data)

def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized.")

if __name__ == '__main__':
    init_db()
    monitor.start()
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    finally:
        monitor.stop()
