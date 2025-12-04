import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
from config import Config

class EmailNotifier:
    def __init__(self):
        self.enabled = Config.ENABLE_EMAIL_ALERTS
        self.smtp_server = Config.SMTP_SERVER
        self.smtp_port = Config.SMTP_PORT
        self.username = Config.SMTP_USERNAME
        self.password = Config.SMTP_PASSWORD
        self.recipients = Config.ALERT_EMAIL_TO
    
    def send_alert(self, switch_name, switch_ip, alert_type, severity, message):
        """Send email alert for a switch issue"""
        if not self.enabled:
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'[{severity.upper()}] Network Alert: {switch_name}'
            msg['From'] = self.username
            msg['To'] = ', '.join(self.recipients)
            
            # Create HTML body
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: {'#e74c3c' if severity == 'critical' else '#f39c12'};">
                    Network Monitoring Alert
                </h2>
                <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
                    <tr>
                        <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Switch Name:</td>
                        <td style="padding: 10px;">{switch_name}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">IP Address:</td>
                        <td style="padding: 10px;">{switch_ip}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Alert Type:</td>
                        <td style="padding: 10px;">{alert_type}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Severity:</td>
                        <td style="padding: 10px;">
                            <span style="background-color: {'#f8d7da' if severity == 'critical' else '#fff3cd'}; 
                                         color: {'#721c24' if severity == 'critical' else '#856404'}; 
                                         padding: 5px 10px; border-radius: 4px;">
                                {severity.upper()}
                            </span>
                        </td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Message:</td>
                        <td style="padding: 10px;">{message}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Time:</td>
                        <td style="padding: 10px;">{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</td>
                    </tr>
                </table>
                <p style="margin-top: 20px; color: #7f8c8d;">
                    This is an automated alert from the Network Monitoring System.
                </p>
            </body>
            </html>
            """
            
            # Attach HTML
            msg.attach(MIMEText(html, 'html'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"✉ Email alert sent for {switch_name}")
            return True
            
        except Exception as e:
            print(f"Failed to send email alert: {str(e)}")
            return False
    
    def send_summary_report(self, total_switches, up_switches, down_switches, critical_alerts):
        """Send daily summary report"""
        if not self.enabled:
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = f'Network Monitoring Daily Report - {datetime.now().strftime("%Y-%m-%d")}'
            msg['From'] = self.username
            msg['To'] = ', '.join(self.recipients)
            
            html = f"""
            <html>
            <body style="font-family: Arial, sans-serif;">
                <h2 style="color: #2c3e50;">Daily Network Monitoring Report</h2>
                <p>Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                
                <h3>Summary</h3>
                <table style="border-collapse: collapse; width: 100%; max-width: 600px;">
                    <tr>
                        <td style="padding: 10px; background-color: #f8f9fa; font-weight: bold;">Total Switches:</td>
                        <td style="padding: 10px;">{total_switches}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #d4edda; font-weight: bold;">Online:</td>
                        <td style="padding: 10px; color: #155724;">{up_switches}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #f8d7da; font-weight: bold;">Offline:</td>
                        <td style="padding: 10px; color: #721c24;">{down_switches}</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px; background-color: #fff3cd; font-weight: bold;">Critical Alerts:</td>
                        <td style="padding: 10px; color: #856404;">{critical_alerts}</td>
                    </tr>
                </table>
                
                <p style="margin-top: 20px; color: #7f8c8d;">
                    This is an automated report from the Network Monitoring System.
                </p>
            </body>
            </html>
            """
            
            msg.attach(MIMEText(html, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"✉ Daily summary report sent")
            return True
            
        except Exception as e:
            print(f"Failed to send summary report: {str(e)}")
            return False
