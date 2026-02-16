# PRACTICAL EXAMPLES - Module Usage Guide

## 📌 ADDED MODULES OVERVIEW

**Total Modules Added: 20**

### Service Detection Modules (17):
✅ generic_banner, http_title, ssh_banner, ssl_info, ftp_probe, smtp_probe, rdp_probe, telnet_probe, dns_probe, vnc_probe, mysql_probe, mongodb_probe, snmp_probe, ldap_probe, http_headers, smb_probe, redis_probe

### CVE/Vulnerability Modules (3):
✅ cve_matcher, cve_database_extended, vuln_analyzer

---

## 🎯 EXAMPLE 1: Scan Your Local Network

```bash
python basicportscanner.py 192.168.1.1 -p 22,80,443,3306,6379,27017 --asur-script all
```

**What it does:**
- Scans 6 common ports
- Detects SSH, HTTP, MySQL, Redis, MongoDB
- Checks for known CVEs
- Shows results immediately

**Expected Output:**
```
[OPEN] Port    22 - SSH
      [ssh_banner] SSH-2.0-OpenSSH_7.4
      [cve_match] 🟡 CVE-2018-15473 [MEDIUM] - Username enumeration

[OPEN] Port    80 - HTTP
      [http_status] HTTP/1.1 200 OK
      [http_server] Apache detected
      [http_header_server] Apache/2.4.49

[OPEN] Port  3306 - MySQL
      [mysql_detected] MySQL service active
      [mysql_version] 5.7.30
      [cve_match] 🔴 CVE-2012-2122 [CRITICAL] - Authentication bypass
      [vulnerability_critical] 🔴 Verify authentication is configured
```

---

## 🎯 EXAMPLE 2: Find Exposed Databases

```bash
python basicportscanner.py 10.0.0.0 -p 3306,5432,27017,6379,9200 --asur-script all -o database_scan.txt
```

**What it does:**
- Scans for common database ports
- Checks MySQL, PostgreSQL, MongoDB, Redis, Elasticsearch
- Detects versions and vulnerabilities
- Saves report to file

**Output file contents:**
```
[OPEN] Port  3306 - MySQL
      [mysql_detected] MySQL service active
      [mysql_version] 5.5.50
      [cve_match] 🔴 CVE-2012-2122 [CRITICAL]
      [risk_assessment] 🔴 [CRITICAL] MySQL often exposed with no auth

[OPEN] Port  6379 - Redis
      [redis_detected] Redis service active
      [redis_version] 4.0.6
      [cve_match] 🟠 CVE-2021-29477 [HIGH]
      [risk_assessment] 🔴 [CRITICAL] Redis no authentication by default
      [remediation] ✓ Enable authentication, restrict access
```

---

## 🎯 EXAMPLE 3: Web Server Security Audit

```bash
python basicportscanner.py www.example.com -p 80,443,8080,8443,8000,3000 --asur-script http_title,http_headers,cve_matcher
```

**What it does:**
- Scans all common web service ports
- Extracts HTTP headers (Server, X-Powered-By, etc)
- Detects web server type and version
- Checks for web server CVEs

**Output:**
```
[OPEN] Port    80 - HTTP
      [http_status] HTTP/1.1 301 Moved Permanently
      [http_header_server] nginx/1.19.0
      [http_server] Nginx detected

[OPEN] Port   443 - HTTPS
      [http_status] HTTP/1.1 200 OK
      [http_header_server] nginx/1.19.0
      [http_header_x-powered-by] Express
      [http_server] Node.js/Express detected
      [cve_match] 🟡 CVE-2021-23017 [MEDIUM] - Nginx off-by-one read
```

---

## 🎯 EXAMPLE 4: Full Network Vulnerability Assessment

```bash
python basicportscanner.py 192.168.1.1 -p 1-65535 --aggressive --asur-script all --concurrency 500 -o full_audit.txt
```

**What it does:**
- Scans ALL 65535 ports
- Uses aggressive mode (very fast)
- Runs ALL detection modules
- Checks ALL CVEs
- Saves complete report

**Time: ~30-60 seconds**

---

## 🎯 EXAMPLE 5: Check Specific Service

### Check if FTP is enabled and vulnerable:
```bash
python basicportscanner.py 192.168.1.1 -p 21 --asur-script ftp_probe
```

Output:
```
[OPEN] Port    21 - FTP
      [ftp_banner] 220 ProFTPD 1.3.5 Server Ready
      [ftp_anonymous] possibly enabled
      [risk_assessment] 🔴 [CRITICAL] FTP transmits credentials in clear text
      [remediation] ✓ Use SFTP or disable FTP
```

### Check if Telnet is running (VERY BAD):
```bash
python basicportscanner.py 192.168.1.1 -p 23 --asur-script telnet_probe
```

Output:
```
[OPEN] Port    23 - Telnet
      [telnet_detected] Telnet service active
      [risk_assessment] 🔴 [CRITICAL] Telnet transmits all data in clear text
      [remediation] ✓ Disable Telnet, use SSH
```

### Check Active Directory/LDAP:
```bash
python basicportscanner.py 192.168.1.1 -p 389,636 --asur-script ldap_probe
```

Output:
```
[OPEN] Port   389 - LDAP
      [ldap_detected] LDAP service active
      [ldap_structure] Active Directory structure detected
      [ldap_ad] Microsoft Active Directory detected
```

---

## 🎯 EXAMPLE 6: Docker/Kubernetes Security Check

```bash
python basicportscanner.py 10.0.0.1 -p 2375,2376,10250,6379,27017 --asur-script all
```

**Detects:**
- Docker daemon (2375/2376) - unencrypted/encrypted
- Kubernetes kubelet (10250) - unencrypted API
- Redis (6379) - often used by containers
- MongoDB (27017) - database exposure

---

## 🎯 EXAMPLE 7: Mobile/IoT Device Scan

```bash
python basicportscanner.py 192.168.1.100 -p 22,80,443,8080,8888,9000 --asur-script all
```

**Common ports on IoT:**
- 22: SSH for management
- 80/443: Web interface
- 8080/8888: Alternative web ports
- 9000: Admin panels

---

## 🎯 EXAMPLE 8: Stealth Scanning (Avoid Detection)

```bash
python basicportscanner.py target.com -p 1-1024 --stealth --asur-script cve_matcher,vuln_analyzer
```

**Characteristics:**
- Very slow (1-2 hours for 1024 ports)
- Random delays between ports
- Less likely to trigger IDS/firewall
- Still gets CVE information

---

## 🎯 EXAMPLE 9: Quick Vulnerability Check

```bash
python basicportscanner.py 192.168.1.1 -p 1-1024 --asur-script cve_matcher,vuln_analyzer
```

**Output focus:**
- Only CVEs and vulnerabilities
- Risk assessment
- Remediation steps
- No banner grabbing

---

## 🎯 EXAMPLE 10: Interactive Console Workflow

```bash
# Start console
python basicportscanner.py --console

# In console, run these commands:
asur -a 192.168.1.1 -p 22,80,443
asur -a 192.168.1.1 -p 1-1024 --aggressive --asur-script all
set target 192.168.1.1
set ports 3306,6379,27017
set asur_script cve_matcher
run

# Save to file
set output_file results.txt
run

# Show config
show

# Exit
exit
```

---

## 📊 WHICH SCRIPT TO USE?

### I want to detect...

| Service | Script | Command |
|---------|--------|---------|
| Web servers | http_title, http_headers | `-p 80,443,8080 --asur-script http_title,http_headers` |
| SSH servers | ssh_banner | `-p 22 --asur-script ssh_banner` |
| Mail servers | smtp_probe | `-p 25,587 --asur-script smtp_probe` |
| Databases | mysql_probe, redis_probe, mongodb_probe | `-p 3306,6379,27017 --asur-script all` |
| Directory services | ldap_probe | `-p 389,636 --asur-script ldap_probe` |
| File sharing | smb_probe, ftp_probe | `-p 139,445,21 --asur-script all` |
| VNC/RDP | vnc_probe, rdp_probe | `-p 5900,3389 --asur-script all` |
| Everything | all | `--asur-script all` |

---

## 🔧 COMBINING MODULES

### Use multiple scripts together:
```bash
# HTTP + CVE
python basicportscanner.py target -p 80,443 --asur-script http_title,http_headers,cve_matcher

# Databases + CVE + Vuln Analysis
python basicportscanner.py target -p 3306,6379,27017 --asur-script mysql_probe,redis_probe,mongodb_probe,cve_matcher,vuln_analyzer

# Everything + Performance
python basicportscanner.py target -p 1-65535 --aggressive --asur-script all --concurrency 500
```

---

## 🎓 LEARNING PATH

**Day 1: Basics**
```bash
# Just scan
python basicportscanner.py 192.168.1.1 -p 22,80,443

# Add SSH detection
python basicportscanner.py 192.168.1.1 -p 22 --asur-script ssh_banner

# Add HTTP detection
python basicportscanner.py 192.168.1.1 -p 80,443 --asur-script http_title
```

**Day 2: Service Detection**
```bash
# Multiple services
python basicportscanner.py 192.168.1.1 -p 22,80,443,3306,6379 --asur-script all

# With CVE checking
python basicportscanner.py 192.168.1.1 -p 1-1024 --asur-script cve_matcher
```

**Day 3: Advanced**
```bash
# Full audit with performance
python basicportscanner.py 192.168.1.1 -p 1-65535 --aggressive --asur-script all -o audit.txt

# Risk assessment
python basicportscanner.py 192.168.1.1 -p 1-1024 --asur-script vuln_analyzer
```

---

## 📋 TROUBLESHOOTING MODULES

**Problem: Module not loading**
```bash
# Check if module exists
ls asur_scripts/

# Try with explicit module name
python basicportscanner.py target -p 80 --asur-script http_title
```

**Problem: CVE not showing**
```bash
# Make sure CVE script is enabled
python basicportscanner.py target -p 1-1024 --asur-script cve_matcher

# Or use all
python basicportscanner.py target -p 1-1024 --asur-script all
```

**Problem: Slow scanning**
```bash
# Increase concurrency
python basicportscanner.py target -p 1-10000 --aggressive --concurrency 500

# Or use aggressive mode
python basicportscanner.py target -p 1-10000 --aggressive
```

---

## ✅ BEST PRACTICES

1. **Always use CVE matcher for vulnerabilities:**
   ```bash
   --asur-script cve_matcher
   ```

2. **Save important scans:**
   ```bash
   -o filename.txt
   ```

3. **Use aggressive for speed:**
   ```bash
   --aggressive
   ```

4. **Use stealth for evasion:**
   ```bash
   --stealth
   ```

5. **Test before full deployment:**
   ```bash
   # Test with small port range first
   -p 80,443,22
   ```

---

That's everything! Use these examples as templates for your own scans. Happy scanning! 🔱⚔️
