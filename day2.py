'''
Today I will be making a Hash calculator (MD5/SHA1/SHA256) for any input string or file
'''

import hashlib
import argparse
import os
import sys
import base64
from pathlib import Path

# Available algorithms
SUPPORTED_ALGORITHMS = {
    'md5': hashlib.md5,
    'sha1': hashlib.sha1,
    'sha224': hashlib.sha224,
    'sha256': hashlib.sha256,
    'sha384': hashlib.sha384,
    'sha512': hashlib.sha512,
    'sha3_256': hashlib.sha3_256,
    'sha3_512': hashlib.sha3_512,
    'blake2b': hashlib.blake2b,
    'blake2s': hashlib.blake2s
}

def calculate_hash(data, algorithm='sha256'):
    """Calculate hash of string data"""
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hash_obj = SUPPORTED_ALGORITHMS[algorithm]()
    hash_obj.update(data.encode('utf-8'))
    return hash_obj.hexdigest()

def hash_file(filepath, algorithm='sha256', chunk_size=8192):
    """Hash a file using chunked reading for memory efficiency"""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")
    
    if algorithm not in SUPPORTED_ALGORITHMS:
        raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    hash_obj = SUPPORTED_ALGORITHMS[algorithm]()
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_obj.update(chunk)
    
    return hash_obj.hexdigest()

def setup_parser():
    parser = argparse.ArgumentParser(
        description='Hash Calculator - Compute hashes for strings or files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
        Examples:
        python hashcalc.py "Hello World"
        python hashcalc.py -a sha256 "Hello World"
        python hashcalc.py -f document.pdf
        python hashcalc.py -f image.jpg -a md5
        python hashcalc.py -f data.bin --all
        '''
    )
    
    parser.add_argument(
        'input',
        nargs='?',
        help='Input string to hash'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Path to file to hash'
    )
    
    parser.add_argument(
        '-a', '--algorithm',
        default='sha256',
        choices=list(SUPPORTED_ALGORITHMS.keys()),
        help='Hash algorithm (default: sha256)'
    )
    
    parser.add_argument(
        '--all',
        action='store_true',
        help='Calculate all supported hashes'
    )
    
    parser.add_argument(
        '-b', '--base64',
        action='store_true',
        help='Output in base64 instead of hex'
    )
    
    return parser

def display_hash(algorithm, hash_value, base64_output=False):
    """Display hash with optional base64 encoding"""
    if base64_output:
        # Convert hex to bytes then to base64
        hash_bytes = bytes.fromhex(hash_value)
        hash_value = base64.b64encode(hash_bytes).decode('utf-8')
    
    print(f"{algorithm.upper()}: {hash_value}")

def display_all_hashes(data, is_file=False, base64_output=False):
    """Calculate and display all supported hashes"""
    print(f"{'File' if is_file else 'String'}: {data}")
    print("-" * 50)
    
    for algo in SUPPORTED_ALGORITHMS:
        try:
            if is_file:
                result = hash_file(data, algo)
            else:
                result = calculate_hash(data, algo)
            
            display_hash(algo, result, base64_output)
        except Exception as e:
            print(f"{algo.upper()}: Error - {e}")

def hash_file_with_progress(filepath, algorithm='sha256', chunk_size=8192):
    """Hash file with progress bar for large files"""
    file_size = os.path.getsize(filepath)
    processed = 0
    hash_obj = SUPPORTED_ALGORITHMS[algorithm]()
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(chunk_size):
            hash_obj.update(chunk)
            processed += len(chunk)
            progress = (processed / file_size) * 100
            print(f"\rProgress: {progress:.1f}%", end='', file=sys.stderr)
    
    print("\r" + " " * 20 + "\r", end='', file=sys.stderr)  # Clear line
    return hash_obj.hexdigest()

def main():
    parser = setup_parser()
    args = parser.parse_args()
    
    # Validate input
    if not args.input and not args.file:
        parser.error("Either input string or --file is required")
    
    if args.input and args.file:
        parser.error("Please provide either a string OR a file, not both")
    
    try:
        # Handle file input
        if args.file:
            if not os.path.exists(args.file):
                print(f"Error: File '{args.file}' not found", file=sys.stderr)
                sys.exit(1)
            
            if args.all:
                display_all_hashes(args.file, is_file=True, base64_output=args.base64)
            else:
                result = hash_file(args.file, args.algorithm)
                display_hash(args.algorithm, result, args.base64)
        
        # Handle string input
        else:
            if args.all:
                display_all_hashes(args.input, is_file=False, base64_output=args.base64)
            else:
                result = calculate_hash(args.input, args.algorithm)
                display_hash(args.algorithm, result, args.base64)
    
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()