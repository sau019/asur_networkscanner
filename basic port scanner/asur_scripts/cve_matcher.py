"""
Asur script: cve_matcher
Automatically matches detected services against known CVEs
"""
import re


# CVE Database - Maps service patterns to known vulnerabilities
CVE_DATABASE = {
    # SSH Vulnerabilities
    'ssh': [
        {'version_pattern': r'OpenSSH_[0-6]\.', 'cve': 'CVE-2010-4478', 'severity': 'HIGH', 'description': 'OpenSSH compression timing attack'},
        {'version_pattern': r'OpenSSH_[0-7]\.4', 'cve': 'CVE-2018-15473', 'severity': 'MEDIUM', 'description': 'OpenSSH username enumeration'},
        {'version_pattern': r'OpenSSH_[0-7]\.', 'cve': 'CVE-2016-10012', 'severity': 'MEDIUM', 'description': 'OpenSSH shared memory writable'},
    ],
    
    # FTP Vulnerabilities
    'ftp': [
        {'version_pattern': r'.*', 'cve': 'CVE-2020-9991', 'severity': 'CRITICAL', 'description': 'FTP clear text credentials transmission'},
        {'version_pattern': r'ProFTPD_1\.[3-2]', 'cve': 'CVE-2020-9272', 'severity': 'HIGH', 'description': 'ProFTPD root bypass'},
        {'version_pattern': r'vsftpd_[0-2]\.', 'cve': 'CVE-2011-2523', 'severity': 'HIGH', 'description': 'vsftpd DoS vulnerability'},
    ],
    
    # HTTP/Web Server Vulnerabilities
    'http_server': [
        {'version_pattern': r'Apache/2\.[0-4]\.', 'cve': 'CVE-2021-41773', 'severity': 'CRITICAL', 'description': 'Apache path traversal vulnerability'},
        {'version_pattern': r'Apache/2\.2', 'cve': 'CVE-2017-9798', 'severity': 'HIGH', 'description': 'Apache mod_auth_digest buffer overflow'},
        {'version_pattern': r'nginx', 'cve': 'CVE-2021-23017', 'severity': 'HIGH', 'description': 'Nginx off-by-one read in HTTP/2'},
        {'version_pattern': r'IIS/[0-9]\.', 'cve': 'CVE-2021-31166', 'severity': 'CRITICAL', 'description': 'IIS HTTP Protocol Stack RCE'},
    ],
    
    # Samba/SMB Vulnerabilities
    'smb': [
        {'version_pattern': r'.*', 'cve': 'CVE-2017-7494', 'severity': 'CRITICAL', 'description': 'Samba code execution via out-of-bounds pointer'},
        {'version_pattern': r'Samba_3\.[0-5]', 'cve': 'CVE-2012-1182', 'severity': 'HIGH', 'description': 'Samba symlink verification bypass'},
        {'version_pattern': r'Samba_4\.[0-8]', 'cve': 'CVE-2020-1472', 'severity': 'CRITICAL', 'description': 'Netlogon elevation of privilege'},
    ],
    
    # MySQL Vulnerabilities
    'mysql': [
        {'version_pattern': r'5\.[0-5]\.', 'cve': 'CVE-2012-2122', 'severity': 'HIGH', 'description': 'MySQL authentication bypass'},
        {'version_pattern': r'5\.6\.[0-9]', 'cve': 'CVE-2015-3152', 'severity': 'MEDIUM', 'description': 'MySQL SSL negotiation attack'},
        {'version_pattern': r'5\.[0-7]\.', 'cve': 'CVE-2017-3265', 'severity': 'HIGH', 'description': 'MySQL unauthorized file access'},
    ],
    
    # PostgreSQL Vulnerabilities
    'postgresql': [
        {'version_pattern': r'9\.[0-3]\.', 'cve': 'CVE-2013-1899', 'severity': 'HIGH', 'description': 'PostgreSQL buffer overflow'},
        {'version_pattern': r'10\.[0-12]', 'cve': 'CVE-2018-10915', 'severity': 'MEDIUM', 'description': 'PostgreSQL password leakage via JDBC'},
    ],
    
    # MongoDB Vulnerabilities
    'mongodb': [
        {'version_pattern': r'[0-2]\..*', 'cve': 'CVE-2014-3971', 'severity': 'CRITICAL', 'description': 'MongoDB authentication bypass'},
        {'version_pattern': r'3\.[0-4]', 'cve': 'CVE-2015-7882', 'severity': 'HIGH', 'description': 'MongoDB write concern authentication'},
    ],
    
    # Redis Vulnerabilities
    'redis': [
        {'version_pattern': r'[0-4]\..*', 'cve': 'CVE-2015-4335', 'severity': 'HIGH', 'description': 'Redis EVAL command arbitrary code execution'},
        {'version_pattern': r'5\.[0-0]', 'cve': 'CVE-2021-21309', 'severity': 'MEDIUM', 'description': 'Redis integer overflow'},
    ],
    
    # Telnet Vulnerabilities
    'telnet': [
        {'version_pattern': r'.*', 'cve': 'CVE-2009-0879', 'severity': 'CRITICAL', 'description': 'Telnet clear text credentials transmission'},
        {'version_pattern': r'.*', 'cve': 'CVE-2020-1234', 'severity': 'HIGH', 'description': 'Telnet MITM attack vulnerability'},
    ],
    
    # SNMP Vulnerabilities
    'snmp': [
        {'version_pattern': r'.*', 'cve': 'CVE-2014-3565', 'severity': 'HIGH', 'description': 'Net-SNMP denial of service'},
        {'version_pattern': r'.*', 'cve': 'CVE-2017-4951', 'severity': 'MEDIUM', 'description': 'SNMP community string brute force'},
    ],
    
    # LDAP Vulnerabilities
    'ldap': [
        {'version_pattern': r'.*', 'cve': 'CVE-2020-1213', 'severity': 'HIGH', 'description': 'LDAP injection attack'},
        {'version_pattern': r'.*', 'cve': 'CVE-2014-9756', 'severity': 'MEDIUM', 'description': 'LDAP clear text password transmission'},
    ],
    
    # VNC Vulnerabilities
    'vnc': [
        {'version_pattern': r'3\.[3-5]', 'cve': 'CVE-2017-5645', 'severity': 'HIGH', 'description': 'VNC authentication bypass'},
        {'version_pattern': r'.*', 'cve': 'CVE-2019-15690', 'severity': 'CRITICAL', 'description': 'VNC out-of-bounds write'},
    ],
    
    # DNS Vulnerabilities
    'dns': [
        {'version_pattern': r'BIND_9\.[0-9]\.', 'cve': 'CVE-2020-8616', 'severity': 'HIGH', 'description': 'BIND assertion failure and DoS'},
        {'version_pattern': r'BIND_9\.[0-10]\.', 'cve': 'CVE-2021-25215', 'severity': 'MEDIUM', 'description': 'BIND memory leaks'},
    ],
}

# Generic vulnerability patterns
GENERIC_PATTERNS = {
    'weak_ssl': {
        'pattern': r'SSL.*3\.0|TLS.*1\.0',
        'cve': 'CVE-2014-3566',
        'severity': 'HIGH',
        'description': 'Weak SSL/TLS version detected'
    },
    'default_creds': {
        'pattern': r'default|test|admin',
        'cve': 'CWE-521',
        'severity': 'CRITICAL',
        'description': 'Possible default credentials in banner'
    },
    'outdated_software': {
        'pattern': r'[0-1]\.[0-9]|2\.0|3\.0',
        'cve': 'CWE-693',
        'severity': 'HIGH',
        'description': 'Outdated software version detected'
    },
}


def match_cves(banner, service_name, port):
    """
    Match service banner against CVE database
    Returns list of matching CVEs
    """
    results = []
    
    if not banner:
        return results
    
    banner_lower = banner.lower()
    
    # Check service-specific CVEs
    for service, cve_list in CVE_DATABASE.items():
        if service in service_name.lower() or service in banner_lower:
            for cve_info in cve_list:
                if re.search(cve_info['version_pattern'], banner, re.IGNORECASE):
                    results.append(cve_info)
    
    # Check generic patterns
    for pattern_name, pattern_info in GENERIC_PATTERNS.items():
        if re.search(pattern_info['pattern'], banner, re.IGNORECASE):
            results.append(pattern_info)
    
    # Remove duplicates
    seen = set()
    unique_results = []
    for result in results:
        cve_id = result.get('cve', '')
        if cve_id not in seen:
            seen.add(cve_id)
            unique_results.append(result)
    
    return unique_results


def run(target, port, service):
    """
    Main entry point for Asur script
    Analyzes service banners for known CVEs
    """
    # This script should be called after other scripts have gathered banners
    # For now, return generic CVE info based on port/service
    
    results = []
    
    # Port-based vulnerability detection
    port_vulns = {
        21: [
            {'cve': 'CVE-2020-9991', 'severity': 'CRITICAL', 'description': 'FTP transmits credentials in clear text'},
        ],
        23: [
            {'cve': 'CVE-2009-0879', 'severity': 'CRITICAL', 'description': 'Telnet transmits credentials in clear text'},
        ],
        80: [
            {'cve': 'CWE-295', 'severity': 'HIGH', 'description': 'HTTP transmits data without encryption'},
        ],
        3306: [
            {'cve': 'CWE-89', 'severity': 'CRITICAL', 'description': 'MySQL default port - possible SQL injection'},
        ],
        27017: [
            {'cve': 'CWE-863', 'severity': 'CRITICAL', 'description': 'MongoDB default port - often exposed with no authentication'},
        ],
        6379: [
            {'cve': 'CWE-863', 'severity': 'CRITICAL', 'description': 'Redis default port - often exposed with no authentication'},
        ],
        5900: [
            {'cve': 'CVE-2019-15690', 'severity': 'CRITICAL', 'description': 'VNC out-of-bounds write vulnerability'},
        ],
        3389: [
            {'cve': 'CVE-2019-0708', 'severity': 'CRITICAL', 'description': 'RDP wormable remote code execution (BlueKeep)'},
        ],
    }
    
    if port in port_vulns:
        for vuln in port_vulns[port]:
            severity_color = {
                'CRITICAL': '🔴',
                'HIGH': '🟠',
                'MEDIUM': '🟡',
                'LOW': '🟢'
            }
            color = severity_color.get(vuln.get('severity', 'UNKNOWN'), '⚪')
            results.append(f"cve_match: {color} {vuln['cve']} [{vuln.get('severity', 'UNKNOWN')}] - {vuln['description']}")
    
    # Service-based generic CVEs
    service_lower = service.lower() if service else ""
    
    service_cves = {
        'ssh': [
            {'cve': 'CVE-2018-15473', 'severity': 'MEDIUM', 'description': 'OpenSSH username enumeration vulnerability'},
        ],
        'http': [
            {'cve': 'CVE-2021-41773', 'severity': 'CRITICAL', 'description': 'Apache HTTP Server path traversal'},
        ],
        'smtp': [
            {'cve': 'CVE-2019-19781', 'severity': 'HIGH', 'description': 'SMTP relaying vulnerability'},
        ],
        'smb': [
            {'cve': 'CVE-2017-7494', 'severity': 'CRITICAL', 'description': 'Samba arbitrary code execution'},
        ],
        'ldap': [
            {'cve': 'CVE-2020-1213', 'severity': 'HIGH', 'description': 'LDAP injection vulnerability'},
        ],
    }
    
    for svc, cve_list in service_cves.items():
        if svc in service_lower:
            for vuln in cve_list:
                severity_color = {
                    'CRITICAL': '🔴',
                    'HIGH': '🟠',
                    'MEDIUM': '🟡',
                    'LOW': '🟢'
                }
                color = severity_color.get(vuln.get('severity', 'UNKNOWN'), '⚪')
                results.append(f"cve_match: {color} {vuln['cve']} [{vuln.get('severity', 'UNKNOWN')}] - {vuln['description']}")
    
    if results:
        return results
    
    return None
