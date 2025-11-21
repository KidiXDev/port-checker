# Port Checker

A powerful Python utility for checking port availability, monitoring port status, and diagnosing network services on your local system.

## Features

- Check port availability in ranges or specific ports
- Detailed service information and port status
- Real-time port monitoring
- Common service ports quick check
- Export results to JSON
- Find available ports automatically

## Installation

No external dependencies required! Just Python 3.6+

```bash
git clone https://github.com/KidiXDev/port-checker.git
cd port-checker
chmod +x phck.py
```

## Quick Start

```bash
# Find first available port in default range (8000-9000)
./phck.py

# Check if specific ports are available
./phck.py --check 80,443,8080

# Scan a range and list all ports
./phck.py --range 3000-3100 --list

# Check common service ports
./phck.py --common
```

## Usage

### Basic Commands

**Find first available port:**

```bash
./phck.py --range 8000-9000
```

**Check specific ports:**

```bash
./phck.py --check 80,443,3306,5432
```

**Check port ranges:**

```bash
./phck.py --check 8000-8010,9000-9005
```

### Scanning & Listing

**List all available and used ports:**

```bash
./phck.py --range 3000-3100 --list
```

**Show detailed information (with service names):**

```bash
./phck.py --range 8000-8050 --list --detailed
```

**Find multiple available ports:**

```bash
./phck.py --range 3000-4000 --count 5
```

### Common Ports Check

Check standard service ports (HTTP, HTTPS, SSH, MySQL, PostgreSQL, Redis, etc.):

```bash
./phck.py --common
```

### Monitoring

Monitor ports for changes over time:

```bash
# Monitor ports every 5 seconds for 60 seconds
./phck.py --monitor 8000,8080,3000

# Custom interval and duration
./phck.py --monitor 80,443 --interval 10 --duration 300
```

### Export Results

Save scan results to JSON:

```bash
./phck.py --range 8000-9000 --list --export results.json
./phck.py --common --export common-ports.json
```

## Options

| Option              | Description                                  |
| ------------------- | -------------------------------------------- |
| `--range START-END` | Port range to check (e.g., 8000-9000)        |
| `--check PORTS`     | Check specific ports (comma-separated)       |
| `--common`          | Check common service ports                   |
| `--list`            | List all available and used ports            |
| `--detailed`        | Show detailed information with service names |
| `--count N`         | Find N available ports                       |
| `--monitor PORTS`   | Monitor ports for changes                    |
| `--interval SEC`    | Monitoring check interval (default: 5)       |
| `--duration SEC`    | Monitoring duration (default: 60)            |
| `--host HOST`       | Host address to bind to (default: 0.0.0.0)   |
| `--export FILE`     | Export results to JSON file                  |

## Examples

**DevOps scenario - Find ports for microservices:**

```bash
./phck.py --range 8000-8100 --count 10
```

**Troubleshooting - Check if services are running:**

```bash
./phck.py --common --detailed
```

**Development - Monitor port during deployment:**

```bash
./phck.py --monitor 3000,8080 --interval 5 --duration 120
```

**Security audit - Scan for open ports:**

```bash
./phck.py --range 1-1024 --list --detailed --export scan-results.json
```

**Quick check before starting a server:**

```bash
./phck.py --check 8000,8080,3000
```

## Output Examples

### Simple check:

```
First available port: 8000
```

### Detailed scan:

```
==================================================
Available Ports (45)
==================================================
  8000
  8001
  8002
  ...

==================================================
Used Ports (5)
==================================================
  8080 (http-alt) [listening]
  3306 (mysql) [in use]
  ...

Summary: 45 available, 5 in use
```

### Common ports check:

```
Port     Service              Status          Listening
============================================================
22       SSH                  ✓ available     ○
80       HTTP                 ✗ in use        ●
443      HTTPS                ✓ available     ○
3306     MySQL                ✗ listening     ●
...
```

## Use Cases

- Development: Find available ports for local services
- DevOps: Verify port availability before deployments
- Troubleshooting: Diagnose port conflicts
- Monitoring: Track port status over time
- Security: Audit open ports on systems
- CI/CD: Automated port checking in pipelines

## Requirements

- Python 3.6 or higher
- No external dependencies

## License

MIT License - feel free to use in your projects!

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.

## Support

If you find this tool helpful, please give it a ⭐️ on GitHub!
