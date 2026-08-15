'''
Log file parser — extract IPs and timestamps with regex
Day 8 of my 100 days coding challenge
Today I would be building a Log file parser — extract IPs and timestamps with regex
'''

import re
from datetime import datetime
from collections import defaultdict
import os

class LogParser:
    def __init__(self):
        # Comprehensive IP pattern (validates IPv4)
        self.ip_pattern = re.compile(
            r'\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.'
            r'(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
        )
        
        # Timestamp pattern for common log formats
        self.timestamp_patterns = [
            # Apache/NGINX format: [15/Aug/2026:14:32:11 +0000]
            re.compile(r'\[(\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2} [+-]\d{4})\]'),
            # ISO format: 2026-08-15T14:32:11Z
            re.compile(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}[Z+-]\d{2}:?\d{2}?)'),
            # Simple format: 2026-08-15 14:32:11
            re.compile(r'(\d{4}-\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})')
        ]
    
    def extract_ip(self, text):
        """Extract IP address from text"""
        match = self.ip_pattern.search(text)
        return match.group(0) if match else None
    
    def extract_timestamp(self, text):
        """Extract timestamp from text using multiple patterns"""
        for pattern in self.timestamp_patterns:
            match = pattern.search(text)
            if match:
                return match.group(1)
        return None
    
    def parse_log_file(self, filepath):
        """Parse entire log file and return structured data"""
        results = []
        ip_counts = defaultdict(int)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as file:
            for line_num, line in enumerate(file, 1):
                ip = self.extract_ip(line)
                timestamp = self.extract_timestamp(line)
                
                if ip:
                    ip_counts[ip] += 1
                
                results.append({
                    'line_number': line_num,
                    'ip': ip,
                    'timestamp': timestamp,
                    'raw_line': line.strip()
                })
        
        return results, ip_counts
    
    def parse_string(self, text):
        """Parse a string instead of a file"""
        lines = text.split('\n')
        results = []
        
        for line in lines:
            if line.strip():
                ip = self.extract_ip(line)
                timestamp = self.extract_timestamp(line)
                results.append({
                    'ip': ip,
                    'timestamp': timestamp,
                    'raw_line': line.strip()
                })
        
        return results

def create_sample_log(filepath):
    """Create a sample log file for testing"""
    sample_logs = [
        '192.168.1.1 - - [15/Aug/2026:14:32:11 +0000] "GET /index.html HTTP/1.1" 200 1024',
        '192.168.1.2 - - [15/Aug/2026:14:32:15 +0000] "POST /api/data HTTP/1.1" 404 512',
        '192.168.1.1 - - [15/Aug/2026:14:32:20 +0000] "GET /about.html HTTP/1.1" 200 2048',
        # Add more sample logs as needed
    ]
    
    with open(filepath, 'w') as f:
        for log in sample_logs:
            f.write(log + '\n')

# Usage example
if __name__ == "__main__":
    parser = LogParser()
    
    # Parse from string
    sample_log = """
    192.168.1.100 - - [15/Aug/2026:14:32:11 +0000] "GET /index.html HTTP/1.1" 200 2326
    10.0.0.55 - - [15/Aug/2026:14:32:15 +0000] "POST /api/data HTTP/1.1" 201 1024
    """
    
    results = parser.parse_string(sample_log)
    for entry in results:
        print(f"IP: {entry['ip']}, Timestamp: {entry['timestamp']}")
    
    # Parse from file
    log_file = 'access.log'
    create_sample_log(log_file)
    results, ip_counts = parser.parse_log_file(log_file)
    print("\nIP Frequency:")
    for ip, count in sorted(ip_counts.items(), key=lambda x: x[1], reverse=True):
        print(f"{ip}: {count} occurrences")