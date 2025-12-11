"""
System Information Monitor for Qwerich Desktop Application
Collects and displays system metrics using psutil
"""

import psutil
import platform
from datetime import datetime


class SystemMonitor:
    def __init__(self):
        pass
    
    def get_cpu_info(self):
        """Get CPU information and usage statistics"""
        cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
        cpu_count_logical = psutil.cpu_count(logical=True)
        cpu_count_physical = psutil.cpu_count(logical=False)
        cpu_freq = psutil.cpu_freq()
        
        # Get average CPU frequency if available
        freq_current = cpu_freq.current if cpu_freq else 0
        freq_max = cpu_freq.max if cpu_freq else 0
        
        # Try to get CPU temperature (not available on all systems)
        try:
            temps = psutil.sensors_temperatures()
            cpu_temp = temps.get('coretemp', temps.get('cpu_thermal', []))
            if cpu_temp:
                cpu_temp = cpu_temp[0].current
            else:
                cpu_temp = "N/A"
        except AttributeError:
            cpu_temp = "N/A"
        
        return {
            'percentages': cpu_percent,
            'count_logical': cpu_count_logical,
            'count_physical': cpu_count_physical,
            'freq_current': freq_current,
            'freq_max': freq_max,
            'temperature': cpu_temp
        }
    
    def get_memory_info(self):
        """Get memory (RAM) information"""
        memory = psutil.virtual_memory()
        
        # Convert bytes to GB
        total_gb = round(memory.total / (1024**3), 2)
        available_gb = round(memory.available / (1024**3), 2)
        used_gb = round(memory.used / (1024**3), 2)
        
        return {
            'total': total_gb,
            'available': available_gb,
            'used': used_gb,
            'percent': memory.percent,
            'free': round(memory.free / (1024**3), 2)
        }
    
    def get_disk_info(self):
        """Get disk information for all partitions"""
        disk_info = []
        
        partitions = psutil.disk_partitions()
        for partition in partitions:
            try:
                partition_usage = psutil.disk_usage(partition.mountpoint)
                
                # Convert bytes to GB
                total_gb = round(partition_usage.total / (1024**3), 2)
                used_gb = round(partition_usage.used / (1024**3), 2)
                free_gb = round(partition_usage.free / (1024**3), 2)
                
                disk_info.append({
                    'device': partition.device,
                    'mountpoint': partition.mountpoint,
                    'file_system': partition.fstype,
                    'total': total_gb,
                    'used': used_gb,
                    'free': free_gb,
                    'percent': round((used_gb / total_gb) * 100, 2) if total_gb > 0 else 0
                })
            except PermissionError:
                # This can happen on Windows for certain drives
                continue
        
        return disk_info
    
    def get_network_info(self):
        """Get network interface information"""
        net_io = psutil.net_io_counters(pernic=True)
        net_addrs = psutil.net_if_addrs()
        
        network_info = {}
        
        for interface, addresses in net_addrs.items():
            if interface in net_io:
                stats = net_io[interface]
                
                # Convert bytes to MB
                bytes_sent_mb = round(stats.bytes_sent / (1024**2), 2)
                bytes_recv_mb = round(stats.bytes_recv / (1024**2), 2)
                
                network_info[interface] = {
                    'addresses': [],
                    'bytes_sent': bytes_sent_mb,
                    'bytes_recv': bytes_recv_mb,
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv
                }
                
                for addr in addresses:
                    if addr.family.name == 'AF_INET':  # IPv4
                        network_info[interface]['addresses'].append({
                            'family': addr.family.name,
                            'address': addr.address,
                            'netmask': addr.netmask
                        })
                    elif addr.family.name == 'AF_INET6':  # IPv6
                        network_info[interface]['addresses'].append({
                            'family': addr.family.name,
                            'address': addr.address,
                            'netmask': addr.netmask
                        })
        
        # Get primary IP address
        try:
            primary_ip = [(net_io[name]['addresses'][0]['address']) 
                         for name in network_info 
                         if network_info[name]['addresses'] and 
                         not network_info[name]['addresses'][0]['address'].startswith('127.')][0]
        except IndexError:
            primary_ip = "N/A"
        
        return {
            'interfaces': network_info,
            'primary_ip': primary_ip
        }
    
    def get_system_info(self):
        """Get general system information"""
        uname = platform.uname()
        
        boot_time = datetime.fromtimestamp(psutil.boot_time())
        
        return {
            'system': uname.system,
            'node_name': uname.node,
            'release': uname.release,
            'version': uname.version,
            'machine': uname.machine,
            'processor': uname.processor,
            'boot_time': boot_time.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_all_info(self):
        """Get all system information at once"""
        return {
            'cpu': self.get_cpu_info(),
            'memory': self.get_memory_info(),
            'disk': self.get_disk_info(),
            'network': self.get_network_info(),
            'system': self.get_system_info()
        }
    
    def format_bytes(self, bytes_value):
        """Format bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.2f} PB"


# Example usage
if __name__ == "__main__":
    monitor = SystemMonitor()
    
    print("=== CPU Info ===")
    cpu_info = monitor.get_cpu_info()
    print(f"CPU Cores (Logical): {cpu_info['count_logical']}")
    print(f"CPU Cores (Physical): {cpu_info['count_physical']}")
    print(f"CPU Usage (%): {cpu_info['percentages']}")
    print(f"CPU Temperature: {cpu_info['temperature']}°C")
    
    print("\n=== Memory Info ===")
    mem_info = monitor.get_memory_info()
    print(f"Total Memory: {mem_info['total']} GB")
    print(f"Used Memory: {mem_info['used']} GB")
    print(f"Available Memory: {mem_info['available']} GB")
    print(f"Memory Usage: {mem_info['percent']}%")
    
    print("\n=== Disk Info ===")
    disk_info = monitor.get_disk_info()
    for disk in disk_info:
        print(f"Device: {disk['device']}")
        print(f"Mount Point: {disk['mountpoint']}")
        print(f"File System: {disk['file_system']}")
        print(f"Total: {disk['total']} GB")
        print(f"Used: {disk['used']} GB")
        print(f"Free: {disk['free']} GB")
        print(f"Usage: {disk['percent']}%")
        print("---")
    
    print("\n=== Network Info ===")
    net_info = monitor.get_network_info()
    print(f"Primary IP: {net_info['primary_ip']}")
    
    print("\n=== System Info ===")
    sys_info = monitor.get_system_info()
    print(f"System: {sys_info['system']}")
    print(f"Node Name: {sys_info['node_name']}")
    print(f"Release: {sys_info['release']}")
    print(f"Boot Time: {sys_info['boot_time']}")