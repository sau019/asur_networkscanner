# Auto CVE Matcher Integration Guide

## Overview
The port scanner now includes automatic CVE (Common Vulnerabilities and Exposures) matching that detects known vulnerabilities in identified services.

## New Scripts Added

### 1. **cve_matcher.py**
- Automatically matches detected services against known CVE database
- Pattern-based version detection
- Severity ratings (CRITICAL, HIGH, MEDIUM, LOW)
- Color-coded output with emojis (🔴 CRITICAL, 🟠 HIGH, 🟡 MEDIUM, 🟢 LOW)
- Covers: SSH, FTP, HTTP, SMB, MySQL, PostgreSQL, MongoDB, Redis, DNS, LDAP, VNC, Telnet, SNMP

### 2. **cve_database_extended.py**
- Comprehensive CVE database with detailed information:
  - CVE ID
  - CVSS Score
  - Severity level
  - Description
  - Exploitation details
  - Remediation steps
- Includes vulnerabilities for:
  - Apache HTTP Server
  - OpenSSH
  - Samba
  - MySQL/PostgreSQL
  - MongoDB
  - Redis
  - IIS
  - Nginx
  - Windows RDP

### 3. **vuln_analyzer.py**
- Generates risk assessment based on port and service
- Provides remediation recommendations
- Risk matrix with port-specific vulnerabilities
- Additional checks for critical services

## Usage Examples

### Run with all CVE detection scripts:
```bash
python basicportscanner.py 192.168.1.1 -p 1-1024 --asur-script all
```

### Run with specific CVE scripts:
```bash
python basicportscanner.py localhost -p 1-100 --asur-script cve_matcher,cve_database_extended,vuln_analyzer
```

### Interactive console mode:
```bash
python basicportscanner.py --console
set target 192.168.1.1
set ports 80,443,3306,6379,27017
set asur_script all
run
```

## Output Examples

```
[OPEN] Port    22 - SSH
      [ssh_banner] SSH-2.0-OpenSSH_6.6
      [cve_match] 🟡 CVE-2018-15473 [MEDIUM] - OpenSSH username enumeration vulnerability
      [cve_match] 🟡 CVE-2016-10012 [MEDIUM] - Shared memory region writable by processes
      [risk_assessment] 🟠 [HIGH] SMB - high attack surface
      [remediation] ✓ Update to OpenSSH 7.7 or later

[OPEN] Port  3306 - MySQL
      [mysql_detected] MySQL service active and responding
      [mysql_version] 5.5.50
      [cve_match] 🔴 CVE-2012-2122 [CRITICAL] - MySQL authentication bypass with multiple connections
      [vulnerability_critical] 🔴 Verify authentication is properly configured
      [risk_assessment] 🔴 [CRITICAL] MySQL often exposed with no auth
      [remediation] ✓ Require authentication, restrict network access

[OPEN] Port  6379 - Redis
      [redis_detected] Redis service active and responding
      [redis_version] 4.0.6
      [cve_match] 🟠 CVE-2021-29477 [HIGH] - ACL bypass via AUTH command
      [vulnerability_critical] 🔴 Verify access controls are enforced
      [risk_assessment] 🔴 [CRITICAL] Redis no authentication by default
      [remediation] ✓ Enable authentication, restrict access
```

## Features

✅ **Automatic Detection**: No manual CVE lookup needed
✅ **Multiple Severity Levels**: CRITICAL, HIGH, MEDIUM, LOW with visual indicators
✅ **Detailed Information**: Includes CVSS scores and remediation advice
✅ **Real-time Matching**: CVE matching happens as services are discovered
✅ **Extensible Database**: Easy to add new CVEs
✅ **Risk Assessment**: Comprehensive vulnerability scoring
✅ **Color-coded Output**: Visual severity indication

## Supported Vulnerabilities

### CRITICAL Level Services:
- FTP (Port 21)
- Telnet (Port 23)
- MySQL (Port 3306)
- MongoDB (Port 27017)
- Redis (Port 6379)
- RDP (Port 3389)
- VNC (Port 5900)

### HIGH Level Services:
- SMB (Ports 139, 445)
- LDAP (Port 389)
- PostgreSQL (Port 5432)
- SNMP (Port 161)
- DNS (Port 53)

### MEDIUM Level Services:
- HTTP (Port 80)
- SSH (Port 22) - if outdated
- HTTPS (Port 443) - weak SSL/TLS

## Integration with Other Scripts

CVE matching works alongside other Asur scripts:
- **generic_banner.py** - Collects service banners
- **ssh_banner.py** - Gets SSH version info
- **http_title.py** - HTTP server detection
- **mysql_probe.py** - MySQL version detection
- **redis_probe.py** - Redis version detection
- etc.

All scripts feed information that CVE matcher uses for detection.

## Future Enhancements

- Real-time CVE database updates from NVD API
- CVSS v3.1 scoring
- Exploit availability tracking
- Patch status verification
- Custom CVE database import
- JSON export with detailed reports
