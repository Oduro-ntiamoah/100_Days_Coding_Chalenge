'''
File-type detector using magic bytes
Day 7 of my 100 days coding challenge
I would be building a Python based File-type detector that would detect file types using magic bytes
'''

import os
import struct

class MagicBytesDetector:
    # Common file signatures (magic bytes)
    MAGIC_BYTES = {
        b'\xFF\xD8\xFF': 'image/jpeg',
        b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A': 'image/png',
        b'\x47\x49\x46\x38': 'image/gif',
        b'\x42\x4D': 'image/bmp',
        b'\x25\x50\x44\x46': 'application/pdf',
        b'\x50\x4B\x03\x04': 'application/zip',
        b'\x52\x61\x72\x21\x1A\x07\x00': 'application/x-rar',
        b'\x7F\x45\x4C\x46': 'application/x-elf',
        b'\x4D\x5A': 'application/x-msdos-program',
        b'\x1F\x8B': 'application/gzip',
        b'\x42\x5A\x68': 'application/x-bzip2',
        b'\x37\x7A\xBC\xAF\x27\x1C': 'application/x-7z-compressed',
        b'\xFF\xFB': 'audio/mpeg',
        b'\x49\x44\x33': 'audio/mpeg',
        b'\x4F\x67\x67\x53': 'audio/ogg',
        b'\x66\x4C\x61\x43': 'audio/flac',
        b'\x52\x49\x46\x46': 'audio/wav',
        b'\x00\x00\x00\x20\x66\x74\x79\x70': 'video/mp4',
        b'\x00\x00\x00\x1C\x66\x74\x79\x70': 'video/mp4',
        b'\x1A\x45\xDF\xA3': 'video/webm',
        b'\x00\x00\x00\x18\x66\x74\x79\x70': 'video/quicktime',
        b'\x3C\x3F\x78\x6D\x6C': 'application/xml',
        b'\xEF\xBB\xBF': 'text/plain',
        b'\xFE\xFF': 'text/plain',
        b'\xFF\xFE': 'text/plain',
        b'\x23\x21': 'text/plain',
        b'\x2F\x2A': 'text/plain',
        b'\x3C\x68\x74\x6D\x6C': 'text/html',
        b'\x3C\x21\x44\x4F\x43': 'text/html',
        b'\x3C\x48\x54\x4D\x4C': 'text/html',
        b'\x50\x4B\x03\x04\x14\x00\x06\x00': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        b'\x50\x4B\x03\x04\x14\x00\x08\x00': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        b'\x50\x4B\x03\x04\x14\x00\x10\x00': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    }
    
    def __init__(self):
        self.file_types = {}
        self.unknown_count = 0
        
    def detect_magic_bytes(self, file_path, bytes_to_read=512):
        """Detect file type using magic bytes"""
        try:
            with open(file_path, 'rb') as f:
                header = f.read(bytes_to_read)
                
            # Check against known magic bytes
            for magic, file_type in self.MAGIC_BYTES.items():
                if header.startswith(magic):
                    return file_type
            
            # Try to detect text files
            try:
                header.decode('utf-8')
                if '\n' in header[:1000].decode('utf-8', errors='ignore'):
                    return 'text/plain'
            except:
                pass
            
            return 'application/octet-stream'  # Unknown binary
            
        except Exception as e:
            return f'Error: {str(e)}'
    
    def scan_directory(self, directory_path, recursive=True):
        """Scan directory and detect file types"""
        if not os.path.exists(directory_path):
            return {"Error": f"Directory '{directory_path}' does not exist"}
        
        self.file_types = {}
        self.unknown_count = 0
        
        walk_func = os.walk if recursive else lambda path: [(path, [], os.listdir(path))]
        
        for root, dirs, files in walk_func(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                
                # Skip directories
                if os.path.isdir(file_path):
                    continue
                
                # Detect file type
                file_type = self.detect_magic_bytes(file_path)
                self.file_types[file_path] = file_type
                
                if file_type == 'application/octet-stream':
                    self.unknown_count += 1
        
        return self.file_types
    
    def print_results(self, show_unknown_only=False):
        """Print detected file types"""
        if not self.file_types:
            print("No files found.")
            return
        
        total = len(self.file_types)
        print(f"\n📁 Found {total} files, {self.unknown_count} unknown types")
        print("=" * 60)
        
        for filepath, filetype in self.file_types.items():
            if show_unknown_only and filetype != 'application/octet-stream':
                continue
                
            filename = os.path.basename(filepath)
            print(f"  {filename}: {filetype}")


# Usage
if __name__ == "__main__":
    detector = MagicBytesDetector()
    directory = "C:/Users/HP/Downloads"
    results = detector.scan_directory(directory)
    
    if "Error" in results:
        print(results["Error"])
    else:
        detector.print_results(show_unknown_only=False)