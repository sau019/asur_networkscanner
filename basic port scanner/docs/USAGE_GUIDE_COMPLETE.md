# ASUR Port Scanner - Complete Usage Guide

## Added Modules Summary

### Service Detection Modules (Asur Scripts):
1. **generic_banner.py** - Generic banner grabbing for any service
2. **http_title.py** - HTTP server title extraction
3. **ssh_banner.py** - SSH version detection
4. **ssl_info.py** - SSL/TLS certificate information
5. **ftp_probe.py** - FTP service probing
6. **smtp_probe.py** - SMTP mail server detection
7. **rdp_probe.py** - RDP (Remote Desktop) detection
8. **telnet_probe.py** - Telnet service detection
9. **dns_probe.py** - DNS service probing
10. **vnc_probe.py** - VNC (Virtual Network Computing) detection
11. **mysql_probe.py** - MySQL database version detection
12. **mongodb_probe.py** - MongoDB detection
13. **snmp_probe.py** - SNMP community string probing
14. **ldap_probe.py** - LDAP/Active Directory detection
15. **http_headers.py** - HTTP headers extraction
16. **smb_probe.py** - SMB/Samba OS detection
17. **redis_probe.py** - Redis cache detection

### CVE/Vulnerability Modules:
18. **cve_matcher.py** - Automatic CVE detection
19. **cve_database_extended.py** - Extended CVE database
20. **vuln_analyzer.py** - Vulnerability risk assessment

---

## Usage Examples

### 1. BASIC SCANNING (Single Port)
```bash
# Scan SSH on port 22
python basicportscanner.py 192.168.1.1 -p 22

# With service detection
python basicportscanner.py 192.168.1.1 -p 22 --asur-script ssh_banner
```

**Output:**
```
[OPEN] Port    22 - SSH
      [ssh_banner] SSH-2.0-OpenSSH_7.4
```

---

### 2. SCAN MULTIPLE PORTS WITH DETECTION
```bash
python basicportscanner.py 192.168.1.1 -p 22,80,443,3306,6379 --asur-script all
```

**Output:**
```
[OPEN] Port    22 - SSH
      [ssh_banner] SSH-2.0-OpenSSH_7.4

[OPEN] Port    80 - HTTP
      [http_status] HTTP/1.1 200 OK
      [http_server] Apache detected
      [http_header_server] Apache/2.4.49

[OPEN] Port   443 - HTTPS
      [ssl_cert] Certificate found

[OPEN] Port  3306 - MySQL
      [mysql_detected] MySQL service active
      [mysql_version] 5.7.30
      [cve_match] 🔴 CVE-2012-2122 [CRITICAL] - Authentication bypass

[OPEN] Port  6379 - Redis
      [redis_detected] Redis service active
      [redis_version] 4.0.6
      [cve_match] 🔴 CVE-2021-29477 [HIGH] - ACL bypass
```

---

### 3. PORT RANGE SCANNING WITH CVE DETECTION
```bash
python basicportscanner.py localhost -p 1-1024 --asur-script cve_matcher,vuln_analyzer
```

**Output:**
```
[OPEN] Port    21 - FTP
      [ftp_banner] 220 ProFTPD 1.3.5 Server Ready
      [ftp_anonymous] possibly enabled
      [risk_assessment] 🔴 [CRITICAL] FTP transmits credentials in clear text
      [remediation] ✓ Use SFTP or disable FTP

[OPEN] Port    23 - Telnet
      [telnet_detected] Telnet service active
      [risk_assessment] 🔴 [CRITICAL] Telnet transmits all data in clear text
      [remediation] ✓ Disable Telnet, use SSH

[OPEN] Port    80 - HTTP
      [http_status] HTTP/1.1 200 OK
      [risk_assessment] 🟡 [MEDIUM] HTTP without encryption
      [remediation] ✓ Use HTTPS (port 443)
```

---

### 4. AGGRESSIVE MODE WITH ALL DETECTION
```bash
python basicportscanner.py 10.0.0.1 -p 1-65535 --aggressive --asur-script all
```

- Fast scanning (timeout: 0.1s)
- Ultra-fast concurrent scanning
- All service detection enabled
- All CVE checking enabled

---

### 5. STEALTH MODE WITH DETECTION
```bash
python basicportscanner.py target.com -p 1-1024 --stealth --asur-script all
```

- Slow evasive scanning (timeout: 3.0s)
- Random delays between ports
- Detection enabled

---

### 6. SAVE RESULTS TO FILE
```bash
python basicportscanner.py 192.168.1.1 -p 80,443,3306 -o scan_results.txt --asur-script all
```

**Output file (scan_results.txt):**
```
============================================================
PORT SCANNER RESULTS
============================================================

Target      : 192.168.1.1
Ports       : 3 port(s)
Timeout     : 1.0 second(s)
Scan Date   : 2026-02-01 14:30:45
Open Ports  : 3

Scan Modes  : 

OPEN SERVICES:
------------------------------------------------------------
Port    80 - HTTP
Port   443 - HTTPS
Port  3306 - MySQL

============================================================
```

---

### 7. SPECIFIC SERVICE DETECTION
```bash
# Detect only HTTP services
python basicportscanner.py 192.168.1.1 -p 80,8080,8000,3000,5000 --asur-script http_title,http_headers

# Detect only databases
python basicportscanner.py 192.168.1.1 -p 3306,5432,27017,6379 --asur-script mysql_probe,mongodb_probe,redis_probe

# Detect only mail servers
python basicportscanner.py 192.168.1.1 -p 25,110,143,587 --asur-script smtp_probe
```

---

### 8. INTERACTIVE CONSOLE MODE
```bash
python basicportscanner.py --console
```

**Console Commands:**

#### Quick Start (Fast way):
```
asur -a 192.168.1.1 -p 22,80,443 --asur-script all
asur -a target.com -p 1-1000 --aggressive --concurrency 500
asur -a 10.0.0.1 -p 80 -o results.txt --asur-script mysql_probe,redis_probe
```

#### Traditional Method:
```
set target 192.168.1.1
set ports 22,80,443,3306,6379
set asur_script all
show
run
```

#### Other Commands:
```
help              - Show help
show              - Display current configuration
history           - Show command history
clear             - Clear screen
exit              - Exit console
```

---

### 9. CONCURRENT SCANNING (PERFORMANCE)
```bash
# Default: 100 workers
python basicportscanner.py 192.168.1.1 -p 1-10000 --asur-script all

# Custom: 500 workers (faster but more resource usage)
python basicportscanner.py 192.168.1.1 -p 1-10000 --concurrency 500 --asur-script all

# Custom: 50 workers (slower but less resource usage)
python basicportscanner.py 192.168.1.1 -p 1-10000 --concurrency 50 --asur-script all
```

---

### 10. ADVANCED MODES COMBINATION
```bash
# Aggressive + CVE Detection + Save Results
python basicportscanner.py 192.168.1.1 -p 1-1024 --aggressive --asur-script all -o results.txt -v

# Stealth + All Detection + High Concurrency
python basicportscanner.py target.com -p 1-65535 --stealth --asur-script all --concurrency 200

# Anonymity Mode + CVE Detection
python basicportscanner.py 10.0.0.0/24 --anonymity --asur-script cve_matcher,vuln_analyzer
```

---

## Script-by-Script Usage

### HTTP Detection:
```bash
python basicportscanner.py 192.168.1.1 -p 80,8080,3000,5000 --asur-script http_title,http_headers
```
Detects: Web server type, version, headers, title

### Database Detection:
```bash
python basicportscanner.py 192.168.1.1 -p 3306,5432,27017,6379 --asur-script mysql_probe,mongodb_probe,redis_probe
```
Detects: Database type, version, role information

### Mail Server Detection:
```bash
python basicportscanner.py 192.168.1.1 -p 25,587,465 --asur-script smtp_probe
```
Detects: Mail server type (Sendmail, Postfix, Exchange), AUTH, TLS support

### Directory Service Detection:
```bash
python basicportscanner.py 192.168.1.1 -p 389,636 --asur-script ldap_probe
```
Detects: LDAP/Active Directory, TLS support

### Remote Access Detection:
```bash
python basicportscanner.py 192.168.1.1 -p 22,3389,5900 --asur-script ssh_banner,rdp_probe,vnc_probe
```
Detects: SSH version, RDP, VNC versions and vulnerabilities

---

## CVE Matcher Output Explained

```
🔴 CRITICAL     - Immediate action required
🟠 HIGH         - Should be fixed soon
🟡 MEDIUM       - Plan to fix
🟢 LOW          - Monitor and fix when possible
```

### Example CVE Output:
```
[cve_match] 🔴 CVE-2012-2122 [CRITICAL] - MySQL authentication bypass
  - Affected: MySQL 5.5.x
  - Fix: Update to MySQL 5.5.25 or later
  - Risk: Attacker can bypass password authentication

[cve_match] 🟠 CVE-2018-15473 [HIGH] - OpenSSH username enumeration
  - Affected: OpenSSH 6.x - 7.7
  - Fix: Update to OpenSSH 7.7 or later
  - Risk: Username enumeration via timing attack

[risk_assessment] 🔴 [CRITICAL] Redis no authentication by default
  - Reason: Redis often exposed without authentication
  - Fix: Enable requirepass, restrict network access
```

---

## Full Command Reference

| Command | Example | Purpose |
|---------|---------|---------|
| Target | `-a 192.168.1.1` | Set target IP/domain |
| Ports | `-p 22,80,443` | Set ports to scan |
| Port Range | `-p 1-1024` | Scan port range |
| Timeout | `-t 2.0` | Set socket timeout |
| Output | `-o results.txt` | Save to file |
| Verbose | `-v` | Show all ports |
| Aggressive | `--aggressive` | Fast scanning (0.1s timeout) |
| Stealth | `-s` or `--stealth` | Slow evasive (3.0s timeout) |
| Anonymity | `--anonymity` | Spoof source IP |
| VPN | `--vpn tun0` | Route through VPN |
| MAC Spoof | `--mac-spoof 00:11:22:33:44:55` | Change MAC |
| Scripts | `--asur-script all` | Load all detection scripts |
| Specific Scripts | `--asur-script mysql_probe,redis_probe` | Load specific scripts |
| CVE Matching | `--asur-script cve_matcher` | Enable CVE detection |
| Concurrency | `--concurrency 500` | Set worker threads |
| Version | `--version` | Show version |

---

## Performance Tips

1. **Fast Scan (1-10K ports):**
   ```bash
   python basicportscanner.py target -p 1-10000 --aggressive --concurrency 500 --asur-script cve_matcher
   ```

2. **Deep Scan with Detection (Full port range):**
   ```bash
   python basicportscanner.py target -p 1-65535 --concurrency 300 --asur-script all
   ```

3. **Stealth Scan (Avoid detection):**
   ```bash
   python basicportscanner.py target -p 1-1024 --stealth --concurrency 50 --asur-script generic_banner
   ```

---

## Real-World Scenarios

### Scenario 1: Quick Network Audit
```bash
python basicportscanner.py 192.168.1.0/24 -p 22,80,443,3306 --asur-script all -o audit_report.txt
```

### Scenario 2: Database Security Check
```bash
python basicportscanner.py 10.0.0.1 -p 3306,5432,27017,6379 --asur-script all
```

### Scenario 3: Web Application Security
```bash
python basicportscanner.py target.com -p 80,443,8080,8443 --asur-script http_title,http_headers,cve_matcher
```

### Scenario 4: Full System Vulnerability Assessment
```bash
python basicportscanner.py 192.168.1.1 -p 1-65535 --aggressive --asur-script all -o full_audit.txt
```

---

## Troubleshooting

**Issue: Script not found**
```bash
# Make sure script is in asur_scripts/ directory
ls asur_scripts/
python basicportscanner.py target -p 80 --asur-script http_title
```

**Issue: CVE matcher not showing results**
```bash
# Use all scripts or specifically enable CVE matcher
python basicportscanner.py target -p 1-1024 --asur-script cve_matcher,vuln_analyzer
```

**Issue: Slow scanning**
```bash
# Increase concurrency or use aggressive mode
python basicportscanner.py target -p 1-1024 --aggressive --concurrency 500
```

---

## Notes
- All scripts are located in `./asur_scripts/` directory
- Scripts are loaded dynamically at runtime
- Use `--asur-script all` to load all available scripts
- CVE matcher works best with service-specific probes enabled
- Results can be saved to file with `-o` option
