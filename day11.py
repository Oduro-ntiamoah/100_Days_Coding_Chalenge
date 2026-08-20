'''
Subnet calculator (CIDR → IP range)
Day 11 of my 100 day coding challenge
I would be building a Subnet calculator (CIDR → IP range)
'''

import sys
import ipaddress
import argparse
from typing import Tuple


def parse_cidr(cidr: str) -> Tuple[str, int]:
    """
    Parse CIDR notation into IP and prefix length
    """
    try:
        if '/' not in cidr:
            raise ValueError("Missing '/' in CIDR notation")
        
        ip_str, prefix_str = cidr.split('/')
        prefix = int(prefix_str)
        
        # Validate prefix length
        if not (0 <= prefix <= 32):
            raise ValueError("Prefix length must be between 0 and 32")
        
        # Validate IP address
        ipaddress.ip_address(ip_str)
        
        return ip_str, prefix
    
    except ValueError as e:
        raise ValueError(f"Invalid CIDR notation: {e}")


def calculate_subnet(cidr: str) -> dict:
    """
    Calculate all subnet information from CIDR
    """
    try:
        network = ipaddress.ip_network(cidr, strict=False)
        
        # Get network info
        network_address = str(network.network_address)
        broadcast_address = str(network.broadcast_address)
        netmask = str(network.netmask)
        wildcard = str(network.hostmask)
        
        # Calculate number of hosts
        num_hosts = network.num_addresses
        if num_hosts >= 2:
            usable_hosts = num_hosts - 2  # Network and broadcast addresses
        else:
            usable_hosts = num_hosts
        
        # Get first and last usable IPs
        hosts = list(network.hosts())
        if hosts:
            first_usable = str(hosts[0])
            last_usable = str(hosts[-1])
        else:
            first_usable = "N/A"
            last_usable = "N/A"
        
        return {
            'network': network_address,
            'broadcast': broadcast_address,
            'netmask': netmask,
            'wildcard': wildcard,
            'total_hosts': num_hosts,
            'usable_hosts': usable_hosts,
            'first_usable': first_usable,
            'last_usable': last_usable,
            'prefix': network.prefixlen,
            'cidr': str(network),
            'is_private': network.is_private,
            'is_global': network.is_global,
            'is_multicast': network.is_multicast,
            'is_unspecified': network.is_unspecified,
            'is_loopback': network.is_loopback,
            'is_link_local': network.is_link_local,
        }
    
    except ValueError as e:
        raise ValueError(f"Invalid network: {e}")


def print_results(results: dict, detailed: bool = False):
    """
    Print subnet information in a formatted way
    """
    print("\n" + "=" * 50)
    print(f"  SUBNET CALCULATOR RESULTS")
    print("=" * 50)
    
    print(f"\n  CIDR Notation:   {results['cidr']}")
    print(f"  Prefix Length:   /{results['prefix']}")
    print(f"  Netmask:         {results['netmask']}")
    print(f"  Wildcard Mask:   {results['wildcard']}")
    
    print(f"\n  Network Address: {results['network']}")
    print(f"  Broadcast:       {results['broadcast']}")
    print(f"  First Usable:    {results['first_usable']}")
    print(f"  Last Usable:     {results['last_usable']}")
    
    print(f"\n  Total Hosts:     {results['total_hosts']:,}")
    print(f"  Usable Hosts:    {results['usable_hosts']:,}")
    
    # Additional details
    if detailed:
        print("\n  Additional Information:")
        print(f"  Private:         {results['is_private']}")
        print(f"  Global:          {results['is_global']}")
        print(f"  Multicast:       {results['is_multicast']}")
        print(f"  Loopback:        {results['is_loopback']}")
        print(f"  Link Local:      {results['is_link_local']}")
        print(f"  Unspecified:     {results['is_unspecified']}")
    
    print("\n" + "=" * 50)


def ip_to_binary(ip_str: str) -> str:
    """
    Convert IP address to binary string
    """
    ip = ipaddress.ip_address(ip_str)
    return '.'.join(f'{octet:08b}' for octet in ip.packed)


def print_binary_details(results: dict):
    """
    Print binary representation of network
    """
    print("\n" + "=" * 50)
    print("  BINARY REPRESENTATION")
    print("=" * 50)
    
    # Calculate network bits and host bits
    prefix = results['prefix']
    network = results['network']
    netmask = results['netmask']
    
    # Display in binary
    print(f"\n  Network Address: {ip_to_binary(network)}")
    print(f"  Netmask:         {ip_to_binary(netmask)}")
    
    # Show network/host bits separation
    net_bits = prefix
    host_bits = 32 - prefix
    
    network_binary = ip_to_binary(network)
    print(f"\n  Network Bits:    {network_binary[:net_bits + (net_bits//8)]}")
    print(f"  Host Bits:       {network_binary[net_bits + (net_bits//8):]}")
    
    print("\n  Bit Breakdown:")
    print(f"  Network Bits:    {net_bits} bits")
    print(f"  Host Bits:       {host_bits} bits")


def main():
    parser = argparse.ArgumentParser(
        description="Subnet Calculator - Convert CIDR notation to IP range",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python subnet_calculator.py 192.168.1.0/24
  python subnet_calculator.py 10.0.0.0/16 --detailed
  python subnet_calculator.py 172.16.0.0/12 --binary
        """
    )
    
    parser.add_argument(
        'cidr',
        help='CIDR notation (e.g., 192.168.1.0/24)'
    )
    
    parser.add_argument(
        '-d', '--detailed',
        action='store_true',
        help='Show detailed information (private, global, etc.)'
    )
    
    parser.add_argument(
        '-b', '--binary',
        action='store_true',
        help='Show binary representation'
    )
    
    args = parser.parse_args()
    
    try:
        # Validate CIDR
        parse_cidr(args.cidr)
        
        # Calculate subnet
        results = calculate_subnet(args.cidr)
        
        # Display results
        print_results(results, args.detailed)
        
        if args.binary:
            print_binary_details(results)
        
        return 0
    
    except ValueError as e:
        print(f"\nError: {e}", file=sys.stderr)
        print("\nUsage: python subnet_calculator.py <CIDR>", file=sys.stderr)
        print("Example: python subnet_calculator.py 192.168.1.0/24", file=sys.stderr)
        return 1
    
    except KeyboardInterrupt:
        print("\n\nOperation cancelled.", file=sys.stderr)
        return 130


if __name__ == "__main__":
    sys.exit(main())