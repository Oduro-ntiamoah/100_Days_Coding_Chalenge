'''
Simple port scanner against localhost (common ports only)
Day 3 of my 100 day coding challenge
I would be building a Python-based Simple port scanner.
'''

import socket
import sys
from datetime import datetime

def scan_port(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return False

def scan_ports(host, start_port, end_port):
    print(f"Scanning ports {start_port} to {end_port} on host {host}...")
    open_ports = []
    for port in range(start_port, end_port + 1):
        if scan_port(host, port):
            open_ports.append(port)
    return open_ports

def main():
    host = 'localhost'
    try:    
        start_port = 1
        end_port = 1024
        open_ports = scan_ports(host, start_port, end_port)
        if open_ports:
            print(f"Open ports on {host}: {', '.join(map(str, open_ports))}")
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        sys.exit(0)
    except socket.gaierror:
        print("\nHostname could not be resolved. Exiting.")
        sys.exit(1)
    except socket.error:
        print("\nCouldn't connect to server. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main()
