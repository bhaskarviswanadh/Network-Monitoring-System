import paramiko
import re
import json
from datetime import datetime
from config import Config

class SSHCollector:
    def __init__(self, host, username, password, device_type='cisco_ios'):
        self.host = host
        self.username = username
        self.password = password
        self.device_type = device_type
        self.client = None
        
    def connect(self):
        """Establish SSH connection to the switch"""
        try:
            self.client = paramiko.SSHClient()
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(
                self.host,
                username=self.username,
                password=self.password,
                timeout=Config.SSH_TIMEOUT,
                look_for_keys=False,
                allow_agent=False
            )
            return True
        except Exception as e:
            print(f"Connection failed to {self.host}: {str(e)}")
            return False
    
    def execute_command(self, command):
        """Execute a command on the switch"""
        if not self.client:
            return None
        try:
            stdin, stdout, stderr = self.client.exec_command(command, timeout=Config.SSH_TIMEOUT)
            output = stdout.read().decode('utf-8', errors='ignore')
            return output
        except Exception as e:
            print(f"Command execution failed: {str(e)}")
            return None
    
    def collect_metrics(self):
        """Collect various metrics from the switch"""
        metrics = {
            'cpu_usage': None,
            'memory_usage': None,
            'uptime': None,
            'interfaces': []
        }
        
        if not self.connect():
            return None
        
        try:
            # Get commands based on device type
            commands = self._get_commands_for_device()
            
            # Collect CPU usage
            cpu_output = self.execute_command(commands['cpu'])
            if cpu_output:
                metrics['cpu_usage'] = self._parse_cpu(cpu_output)
            
            # Collect memory usage
            mem_output = self.execute_command(commands['memory'])
            if mem_output:
                metrics['memory_usage'] = self._parse_memory(mem_output)
            
            # Collect uptime
            version_output = self.execute_command(commands['version'])
            if version_output:
                metrics['uptime'] = self._parse_uptime(version_output)
            
            # Collect interface statistics
            int_output = self.execute_command(commands['interfaces'])
            if int_output:
                metrics['interfaces'] = self._parse_interfaces(int_output)
                
        finally:
            self.disconnect()
        
        return metrics
    
    def _get_commands_for_device(self):
        """Get appropriate commands based on device type"""
        # Default Cisco commands
        commands = {
            'cpu': 'show processes cpu',
            'memory': 'show memory statistics',
            'version': 'show version',
            'interfaces': 'show interfaces'
        }
        
        # Aruba/HP specific commands
        if self.device_type in ['aruba_os', 'hp_procurve']:
            commands = {
                'cpu': 'show system',
                'memory': 'show system',
                'version': 'show version',
                'interfaces': 'show interfaces brief'
            }
        
        # TP-Link specific commands
        elif self.device_type == 'tplink':
            commands = {
                'cpu': 'show cpu',
                'memory': 'show memory',
                'version': 'show system-info',
                'interfaces': 'show interface status'
            }
        
        # D-Link specific commands
        elif self.device_type == 'dlink':
            commands = {
                'cpu': 'show cpu utilization',
                'memory': 'show memory',
                'version': 'show switch',
                'interfaces': 'show ports'
            }
        
        # Cambium - may vary by model
        elif self.device_type == 'cambium':
            commands = {
                'cpu': 'show system',
                'memory': 'show system',
                'version': 'show version',
                'interfaces': 'show interfaces'
            }
        
        return commands
    
    def _parse_cpu(self, output):
        """Parse CPU usage from show processes cpu"""
        # Cisco pattern
        match = re.search(r'CPU utilization.*?(\d+)%', output)
        if match:
            return float(match.group(1))
        
        # Aruba/HP pattern
        match = re.search(r'CPU\s+utilization\s+:\s+(\d+)%', output, re.IGNORECASE)
        if match:
            return float(match.group(1))
        
        # Generic percentage pattern
        match = re.search(r'(\d+)%', output)
        if match:
            return float(match.group(1))
        
        return None
    
    def _parse_memory(self, output):
        """Parse memory usage"""
        # Cisco pattern
        match = re.search(r'Processor\s+(\d+)\s+(\d+)\s+(\d+)', output)
        if match:
            total = int(match.group(1))
            used = int(match.group(2))
            return round((used / total) * 100, 2) if total > 0 else None
        
        # Aruba/HP pattern
        match = re.search(r'Memory\s+utilization\s+:\s+(\d+)%', output, re.IGNORECASE)
        if match:
            return float(match.group(1))
        
        # Generic used/total pattern
        match = re.search(r'(\d+)\s*[KMG]?B?\s+used.*?(\d+)\s*[KMG]?B?\s+total', output, re.IGNORECASE)
        if match:
            used = int(match.group(1))
            total = int(match.group(2))
            return round((used / total) * 100, 2) if total > 0 else None
        
        return None
    
    def _parse_uptime(self, output):
        """Parse system uptime"""
        match = re.search(r'uptime is (.+)', output, re.IGNORECASE)
        return match.group(1).strip() if match else None
    
    def _parse_interfaces(self, output):
        """Parse interface statistics"""
        interfaces = []
        current_interface = None
        
        for line in output.split('\n'):
            # Match interface name
            if_match = re.match(r'^(\S+)\s+is\s+(up|down|administratively down)', line)
            if if_match:
                if current_interface:
                    interfaces.append(current_interface)
                current_interface = {
                    'name': if_match.group(1),
                    'status': if_match.group(2),
                    'input_errors': 0,
                    'output_errors': 0
                }
            
            # Parse error counts
            if current_interface:
                error_match = re.search(r'(\d+)\s+input errors', line)
                if error_match:
                    current_interface['input_errors'] = int(error_match.group(1))
                
                error_match = re.search(r'(\d+)\s+output errors', line)
                if error_match:
                    current_interface['output_errors'] = int(error_match.group(1))
        
        if current_interface:
            interfaces.append(current_interface)
        
        return interfaces
    
    def disconnect(self):
        """Close SSH connection"""
        if self.client:
            self.client.close()
            self.client = None
