#!/usr/bin/env python3
"""
Port Checker - A utility to check port availability on the local system.
"""

import argparse
import socket
import sys
import json
import time
from typing import Tuple, List, Optional, Dict
from datetime import datetime


class PortChecker:
    """Handles port availability checking operations."""
    
    def __init__(self, host: str = "0.0.0.0"):
        self.host = host
    
    def is_port_available(self, port: int) -> bool:
        """
        Check if a port is available for binding.
        
        Args:
            port: Port number to check
            
        Returns:
            True if port is available, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                sock.bind((self.host, port))
                return True
        except (OSError, PermissionError):
            return False
    
    def get_service_name(self, port: int) -> Optional[str]:
        """
        Get the service name associated with a port.
        
        Args:
            port: Port number
            
        Returns:
            Service name or None
        """
        try:
            return socket.getservbyport(port)
        except OSError:
            return None
    
    def check_port_connection(self, port: int, timeout: float = 1.0) -> bool:
        """
        Check if a service is actively listening on a port.
        
        Args:
            port: Port number to check
            timeout: Connection timeout in seconds
            
        Returns:
            True if service is listening, False otherwise
        """
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                result = sock.connect_ex((self.host if self.host != "0.0.0.0" else "127.0.0.1", port))
                return result == 0
        except Exception:
            return False
    
    def get_port_info(self, port: int) -> Dict[str, any]:
        """
        Get comprehensive information about a port.
        
        Args:
            port: Port number
            
        Returns:
            Dictionary with port information
        """
        available = self.is_port_available(port)
        service = self.get_service_name(port)
        listening = self.check_port_connection(port) if not available else False
        
        return {
            "port": port,
            "available": available,
            "service": service,
            "listening": listening,
            "status": "available" if available else ("listening" if listening else "in use")
        }
    
    def find_first_available(self, start: int, end: int) -> Optional[int]:
        """
        Find the first available port in a range.
        
        Args:
            start: Starting port number
            end: Ending port number
            
        Returns:
            First available port number, or None if no ports available
        """
        for port in range(start, end + 1):
            if self.is_port_available(port):
                return port
        return None
    
    def scan_range(self, start: int, end: int, detailed: bool = False) -> Tuple[List, List]:
        """
        Scan a range of ports and categorize them.
        
        Args:
            start: Starting port number
            end: Ending port number
            detailed: Include detailed port information
            
        Returns:
            Tuple of (available_ports, used_ports)
        """
        available = []
        used = []
        
        total = end - start + 1
        for i, port in enumerate(range(start, end + 1), 1):
            if detailed:
                info = self.get_port_info(port)
                if info["available"]:
                    available.append(info)
                else:
                    used.append(info)
            else:
                if self.is_port_available(port):
                    available.append(port)
                else:
                    used.append(port)
            
            # Progress indicator for large ranges
            if total > 100 and i % 50 == 0:
                print(f"Scanning... {i}/{total} ports checked", end='\r')
        
        if total > 100:
            print(" " * 50, end='\r')  # Clear progress line
        
        return available, used
    
    def monitor_ports(self, ports: List[int], interval: int = 5, duration: int = 60):
        """
        Monitor ports for changes over time.
        
        Args:
            ports: List of ports to monitor
            interval: Check interval in seconds
            duration: Total monitoring duration in seconds
        """
        print(f"Monitoring {len(ports)} port(s) every {interval} seconds for {duration} seconds...")
        print("Press Ctrl+C to stop early\n")
        
        start_time = time.time()
        iteration = 0
        
        try:
            while time.time() - start_time < duration:
                iteration += 1
                timestamp = datetime.now().strftime("%H:%M:%S")
                print(f"[{timestamp}] Check #{iteration}")
                
                for port in ports:
                    info = self.get_port_info(port)
                    status_icon = "✓" if info["available"] else "✗"
                    service_info = f" ({info['service']})" if info['service'] else ""
                    print(f"  Port {port}: {status_icon} {info['status']}{service_info}")
                
                print()
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")


def validate_port_range(range_str: str) -> Tuple[int, int]:
    """
    Validate and parse port range string.
    
    Args:
        range_str: Range in format "start-end"
        
    Returns:
        Tuple of (start_port, end_port)
        
    Raises:
        ValueError: If range format is invalid
    """
    try:
        parts = range_str.split("-")
        if len(parts) != 2:
            raise ValueError("Range must be in format 'start-end'")
        
        start, end = int(parts[0]), int(parts[1])
        
        if start < 1 or end > 65535:
            raise ValueError("Ports must be between 1 and 65535")
        
        if start > end:
            raise ValueError("Start port must be less than or equal to end port")
        
        return start, end
    
    except ValueError as e:
        raise ValueError(f"Invalid port range: {e}")


def parse_port_list(port_str: str) -> List[int]:
    """
    Parse comma-separated port list.
    
    Args:
        port_str: Comma-separated port numbers
        
    Returns:
        List of port numbers
    """
    ports = []
    for part in port_str.split(","):
        part = part.strip()
        if "-" in part:
            start, end = validate_port_range(part)
            ports.extend(range(start, end + 1))
        else:
            port = int(part)
            if port < 1 or port > 65535:
                raise ValueError(f"Port {port} out of valid range (1-65535)")
            ports.append(port)
    return ports


def export_results(data: Dict, filename: str):
    """Export scan results to JSON file."""
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"\nResults exported to {filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Check port availability on the local system",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --range 8000-9000
  %(prog)s --range 3000-3010 --list
  %(prog)s --check 80,443,8080
  %(prog)s --range 8000-8100 --detailed
  %(prog)s --monitor 8000,8080 --interval 10
  %(prog)s --range 3000-3100 --export results.json
  %(prog)s --common
        """
    )
    
    parser.add_argument(
        "--range",
        type=str,
        help="Port range to check (format: start-end, e.g., 8000-9000)"
    )
    
    parser.add_argument(
        "--check",
        type=str,
        metavar="PORTS",
        help="Check specific ports (comma-separated, e.g., 80,443,8080)"
    )
    
    parser.add_argument(
        "--common",
        action="store_true",
        help="Check common service ports (HTTP, HTTPS, SSH, etc.)"
    )
    
    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available and used ports in the range"
    )
    
    parser.add_argument(
        "--detailed",
        action="store_true",
        help="Show detailed information including service names"
    )
    
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host address to bind to (default: 0.0.0.0)"
    )
    
    parser.add_argument(
        "--count",
        type=int,
        metavar="N",
        help="Find N available ports"
    )
    
    parser.add_argument(
        "--monitor",
        type=str,
        metavar="PORTS",
        help="Monitor specific ports for changes (comma-separated)"
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Monitoring interval in seconds (default: 5)"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        default=60,
        help="Monitoring duration in seconds (default: 60)"
    )
    
    parser.add_argument(
        "--export",
        type=str,
        metavar="FILE",
        help="Export results to JSON file"
    )
    
    args = parser.parse_args()
    
    checker = PortChecker(host=args.host)
    
    # Monitor mode
    if args.monitor:
        try:
            ports = parse_port_list(args.monitor)
            checker.monitor_ports(ports, args.interval, args.duration)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return
    
    # Common ports check
    if args.common:
        common_ports = {
            20: "FTP Data", 21: "FTP Control", 22: "SSH", 23: "Telnet",
            25: "SMTP", 53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
            443: "HTTPS", 465: "SMTPS", 587: "SMTP (submission)",
            993: "IMAPS", 995: "POP3S", 3306: "MySQL", 5432: "PostgreSQL",
            6379: "Redis", 8080: "HTTP Alt", 27017: "MongoDB"
        }
        
        print("Checking common service ports...\n")
        print(f"{'Port':<8} {'Service':<20} {'Status':<15} {'Listening'}")
        print("=" * 60)
        
        results = []
        for port, service in sorted(common_ports.items()):
            info = checker.get_port_info(port)
            status_icon = "✓" if info["available"] else "✗"
            listen_icon = "●" if info["listening"] else "○"
            print(f"{port:<8} {service:<20} {status_icon} {info['status']:<13} {listen_icon}")
            results.append(info)
        
        if args.export:
            export_results({"common_ports": results, "timestamp": datetime.now().isoformat()}, args.export)
        return
    
    # Specific ports check
    if args.check:
        try:
            ports = parse_port_list(args.check)
            print(f"Checking {len(ports)} port(s)...\n")
            
            results = []
            for port in ports:
                info = checker.get_port_info(port)
                status_icon = "✓" if info["available"] else "✗"
                service_info = f" ({info['service']})" if info['service'] else ""
                print(f"Port {port}: {status_icon} {info['status']}{service_info}")
                results.append(info)
            
            if args.export:
                export_results({"checked_ports": results, "timestamp": datetime.now().isoformat()}, args.export)
            
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return
    
    # Range-based operations
    if not args.range:
        args.range = "8000-9000"
    
    try:
        start, end = validate_port_range(args.range)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    
    if args.list:
        print(f"Scanning ports {start}-{end}...\n")
        available, used = checker.scan_range(start, end, args.detailed)
        
        print("=" * 50)
        print(f"Available Ports ({len(available)})")
        print("=" * 50)
        if available:
            for item in available:
                if args.detailed:
                    service = f" ({item['service']})" if item['service'] else ""
                    print(f"  {item['port']}{service}")
                else:
                    print(f"  {item}")
        else:
            print("  None")
        
        print(f"\n{'=' * 50}")
        print(f"Used Ports ({len(used)})")
        print("=" * 50)
        if used:
            for item in used:
                if args.detailed:
                    service = f" ({item['service']})" if item['service'] else ""
                    status = f" [{item['status']}]"
                    print(f"  {item['port']}{service}{status}")
                else:
                    print(f"  {item}")
        else:
            print("  None")
        
        print(f"\nSummary: {len(available)} available, {len(used)} in use")
        
        if args.export:
            export_results({
                "range": f"{start}-{end}",
                "available": available,
                "used": used,
                "timestamp": datetime.now().isoformat()
            }, args.export)
    
    elif args.count:
        print(f"Finding {args.count} available ports in range {start}-{end}...")
        found = []
        for port in range(start, end + 1):
            if checker.is_port_available(port):
                found.append(port)
                if len(found) >= args.count:
                    break
        
        if found:
            print(f"\nFound {len(found)} available port(s):")
            for port in found:
                print(f"  {port}")
            
            if args.export:
                export_results({
                    "available_ports": found,
                    "count": len(found),
                    "timestamp": datetime.now().isoformat()
                }, args.export)
        else:
            print(f"\nNo available ports found in range {start}-{end}")
            sys.exit(1)
    
    else:
        port = checker.find_first_available(start, end)
        if port is None:
            print(f"No available ports in range {start}-{end}")
            sys.exit(1)
        else:
            print(f"First available port: {port}")


if __name__ == "__main__":
    main()