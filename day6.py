'''
File integrity checker using SHA-256 (detect changed files in a folder)
Day 6 of my 100 days coding challenge
I would be building a Python based File integrity checker that would detect changed files
in a folder using SHA-256 hashing algorithm
'''

import hashlib
import json
import datetime
import argparse
from pathlib import Path

class FileIntegrityChecker:
    def __init__(self, folder_path, hash_file='file_hashes.json'):
        self.folder_path = Path(folder_path)
        self.hash_file = Path(hash_file)
        self.hash_db = {}

    def calculate_sha256(self, file_path):
        """Calculate SHA-256 hash of a file"""
        sha256_hash = hashlib.sha256()
        try:    
            with open(file_path, 'rb') as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except Exception as e:
            print(f"Error calculating hash for {file_path}: {e}")
            return None

    def scan_folder(self):
        """Scan the folder and update the hash database"""
        hashes = {}
        for file_path in self.folder_path.rglob('*'):
            if file_path.is_file():
                relative_path = str(file_path.relative_to(self.folder_path))
                print(f"Scanning file: {relative_path}")
                file_hash = self.calculate_sha256(file_path)
                if file_hash:
                    hashes[relative_path] = file_hash
        return hashes

    def save_database(self):
        """Save the hash database to a JSON file"""
        try:    
            with open(self.hash_file, 'w') as f:
                json.dump(self.hash_db, f, indent=4)
            print(f"Hash database saved to {self.hash_file}")
        except Exception as e:
            print(f"Error saving hash database: {e}")

    def load_database(self):
        """Load the hash database from a JSON file"""
        if self.hash_file.exists():
            try:    
                with open(self.hash_file, 'r') as f:
                    self.hash_db = json.load(f)
                print(f"Hash database loaded from {self.hash_file}")
            except Exception as e:
                print(f"Error loading hash database: {e}")
        else:
            print(f"No existing hash database found at {self.hash_file}. Starting fresh.")

    def check_integrity(self):
        """Check the integrity of files in the folder"""
        current_hashes = self.scan_folder()

        changes = {
            'new_files': [],
            'modified_files': [],
            'deleted_files': [],
            'unchanged_files': []
        }

        # Check for new and modified files
        for file_path, current_hash in current_hashes.items():
            if file_path not in self.hash_db:
                changes['new_files'].append(file_path)
            elif self.hash_db[file_path] != current_hash:
                changes['modified_files'].append(file_path)
            else:
                changes['unchanged_files'].append(file_path)

        # Check for deleted files
        for file_path in self.hash_db:
            if file_path not in current_hashes:
                changes['deleted_files'].append(file_path)

        return changes

    def update_database(self, current_hashes):
        """Update the hash database with current hashes"""
        self.hash_db = current_hashes
        self.save_database()
        print("Hash database updated.")

    def print_report(self, changes):
        '''Integrity check report'''
        total_files = len(changes['new_files']) + len(changes['modified_files']) + len(changes['deleted_files']) + len(changes['unchanged_files'])
        print("\nIntegrity Check Report")

        print(f'Total files scanned: {total_files}')
        print(f'Files scanned: {len(changes["unchanged_files"]) + len(changes["modified_files"]) + len(changes["new_files"])}')

        if changes['unchanged_files']:
            print(f'Unchanged files: {len(changes["unchanged_files"])}')

        if changes['new_files']:
            print(f'New files: {len(changes["new_files"])}')
            for file in changes['new_files']:
                print(f'  - {file}')

        if changes['modified_files']:
            print(f'Modified files: {len(changes["modified_files"])}')
            for file in changes['modified_files']:
                print(f'  - {file}')

        if changes['deleted_files']:
            print(f'Deleted files: {len(changes["deleted_files"])}')
            for file in changes['deleted_files']:
                print(f'  - {file}')

        if not any([changes['new_files'], changes['modified_files'], changes['deleted_files']]):
            print("No changes detected. All files are intact.")


def main():
    parser = argparse.ArgumentParser(description="File Integrity Checker using SHA-256")
    parser.add_argument("folder", help="Path to the folder to check integrity")
    parser.add_argument("--hash-file", default="file_hashes.json", help="Path to the hash database file (default: file_hashes.json)")
    parser.add_argument('--action', choices=['init', 'check', 'update'], default='check', help='Action to perform')
    
    args = parser.parse_args()

    checker = FileIntegrityChecker(args.folder, args.hash_file)

    if args.action == 'init':
        print(f"Initializing database for folder: {args.folder}")
        checker.hash_db = checker.scan_folder()
        checker.save_database()
    elif args.action == 'check':
        print(f"Checking integrity for folder: {args.folder}")
        checker.load_database()
        changes = checker.check_integrity()
        checker.print_report(changes)
    elif args.action == 'update':
        print(f"Updating database for folder: {args.folder}")
        checker.load_database()
        current_hashes = checker.scan_folder()
        checker.update_database(current_hashes)
    else:
        print("Invalid action. Use 'init', 'check', or 'update'.")

if __name__ == "__main__":
    main()

'''How to use:'''
# 1. Initialize the database (first time)
# python integrity_checker.py /path/to/folder --action init

# 2. Check for changes
# python integrity_checker.py /path/to/folder --action check

# 3. Update database after changes
# python integrity_checker.py /path/to/folder --action update

# 4. Use custom database file
# python integrity_checker.py /path/to/folder --db custom_db.json --action check