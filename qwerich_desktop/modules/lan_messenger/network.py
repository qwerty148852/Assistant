"""
LAN Messenger Network Module for Qwerich Desktop Application
Handles peer-to-peer communication over local network using UDP/TCP
"""

import socket
import threading
import json
import time
from datetime import datetime


class LANMessenger:
    def __init__(self, nickname="Anonymous", port=12345):
        self.nickname = nickname
        self.port = port
        self.broadcast_port = 12344  # Port for discovery broadcasts
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.tcp_socket = None
        self.clients = {}  # Dictionary to store discovered clients
        self.message_handlers = []  # List of functions to handle received messages
        self.running = False
        self.listen_thread = None
        self.broadcast_thread = None
    
    def start(self):
        """Start the messenger service"""
        self.running = True
        
        # Start listening for broadcasts
        self.listen_thread = threading.Thread(target=self.listen_for_broadcasts, daemon=True)
        self.listen_thread.start()
        
        # Start broadcasting presence
        self.broadcast_thread = threading.Thread(target=self.broadcast_presence, daemon=True)
        self.broadcast_thread.start()
        
        # Start TCP server for direct messaging
        self.start_tcp_server()
        
        print(f"LAN Messenger started. Nickname: {self.nickname}, Port: {self.port}")
    
    def stop(self):
        """Stop the messenger service"""
        self.running = False
        if self.tcp_socket:
            self.tcp_socket.close()
        if self.socket:
            self.socket.close()
    
    def broadcast_presence(self):
        """Broadcast presence to local network"""
        while self.running:
            try:
                message = {
                    "type": "presence",
                    "nickname": self.nickname,
                    "port": self.port,
                    "timestamp": datetime.now().isoformat()
                }
                data = json.dumps(message).encode('utf-8')
                
                # Broadcast to local network
                self.socket.sendto(data, ('<broadcast>', self.broadcast_port))
                
                # Also send to localhost
                self.socket.sendto(data, ('127.0.0.1', self.broadcast_port))
                
                time.sleep(5)  # Broadcast every 5 seconds
            except Exception as e:
                print(f"Error broadcasting presence: {e}")
                time.sleep(5)
    
    def listen_for_broadcasts(self):
        """Listen for broadcasts from other peers"""
        listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        listen_socket.bind(('', self.broadcast_port))
        
        while self.running:
            try:
                data, addr = listen_socket.recvfrom(1024)
                try:
                    message = json.loads(data.decode('utf-8'))
                    
                    if message.get('type') == 'presence':
                        client_addr = addr[0]
                        client_port = message['port']
                        client_nickname = message['nickname']
                        
                        # Update client list
                        self.clients[client_addr] = {
                            'nickname': client_nickname,
                            'port': client_port,
                            'last_seen': datetime.now()
                        }
                        
                        print(f"Discovered peer: {client_nickname} at {client_addr}:{client_port}")
                        
                except json.JSONDecodeError:
                    pass  # Ignore invalid JSON messages
            except Exception as e:
                if self.running:  # Only print error if we're still running
                    print(f"Error receiving broadcast: {e}")
        
        listen_socket.close()
    
    def start_tcp_server(self):
        """Start TCP server for receiving direct messages"""
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.tcp_socket.bind(('0.0.0.0', self.port))
            self.tcp_socket.listen(5)
            
            server_thread = threading.Thread(target=self.handle_incoming_connections, daemon=True)
            server_thread.start()
        except Exception as e:
            print(f"Error starting TCP server: {e}")
    
    def handle_incoming_connections(self):
        """Handle incoming TCP connections"""
        while self.running:
            try:
                conn, addr = self.tcp_socket.accept()
                
                client_thread = threading.Thread(
                    target=self.handle_client_connection,
                    args=(conn, addr),
                    daemon=True
                )
                client_thread.start()
            except Exception as e:
                if self.running:
                    print(f"Error accepting connection: {e}")
    
    def handle_client_connection(self, conn, addr):
        """Handle a client connection"""
        try:
            data = conn.recv(1024)
            if data:
                try:
                    message = json.loads(data.decode('utf-8'))
                    
                    # Process the message
                    if message.get('type') == 'chat':
                        sender = message.get('sender', 'Unknown')
                        content = message.get('content', '')
                        timestamp = message.get('timestamp', datetime.now().isoformat())
                        
                        # Notify message handlers
                        for handler in self.message_handlers:
                            handler(sender, content, timestamp)
                        
                        print(f"[{timestamp}] {sender}: {content}")
                    
                except json.JSONDecodeError:
                    pass
        except Exception as e:
            print(f"Error handling client connection: {e}")
        finally:
            conn.close()
    
    def send_message(self, recipient_ip, recipient_port, message):
        """Send a message to a specific peer"""
        try:
            tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp_socket.connect((recipient_ip, recipient_port))
            
            message_data = {
                "type": "chat",
                "sender": self.nickname,
                "content": message,
                "timestamp": datetime.now().isoformat()
            }
            
            data = json.dumps(message_data).encode('utf-8')
            tcp_socket.send(data)
            tcp_socket.close()
            
            return True
        except Exception as e:
            print(f"Error sending message: {e}")
            return False
    
    def register_message_handler(self, handler_func):
        """Register a function to handle received messages"""
        self.message_handlers.append(handler_func)
    
    def get_online_clients(self):
        """Get list of currently online clients"""
        # Remove clients that haven't been seen in the last 15 seconds
        current_time = datetime.now()
        active_clients = {}
        
        for ip, info in self.clients.items():
            if (current_time - info['last_seen']).seconds < 15:
                active_clients[ip] = info
        
        self.clients = active_clients
        return self.clients


# Example usage
if __name__ == "__main__":
    def message_handler(sender, content, timestamp):
        print(f"Received message from {sender}: {content}")
    
    messenger = LANMessenger(nickname="TestUser", port=12345)
    messenger.register_message_handler(message_handler)
    messenger.start()
    
    try:
        while True:
            cmd = input("Enter command (send <ip> <msg>, list, quit): ")
            if cmd.startswith("send "):
                parts = cmd.split(" ", 2)
                if len(parts) >= 3:
                    ip = parts[1]
                    msg = parts[2]
                    # Find port for this IP (simplified)
                    port = 12345  # Default port
                    messenger.send_message(ip, port, msg)
            elif cmd == "list":
                clients = messenger.get_online_clients()
                print("Online clients:")
                for ip, info in clients.items():
                    print(f"  {info['nickname']} at {ip}:{info['port']}")
            elif cmd == "quit":
                break
    except KeyboardInterrupt:
        pass
    finally:
        messenger.stop()