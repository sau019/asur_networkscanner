"""
Asur script: cve_database_extended
Extended CVE database with more detailed vulnerability information
"""

# Comprehensive CVE Database
EXTENDED_CVE_DB = {
    # Apache HTTP Server
    'Apache/2.4.49': {
        'cves': [
            {
                'id': 'CVE-2021-41773',
                'severity': 'CRITICAL',
                'cvss': 9.8,
                'description': 'Path traversal via crafted requests',
                'exploit': 'Remote code execution possible',
                'remediation': 'Update to 2.4.50 or later'
            }
        ]
    },
    'Apache/2.4.50': {
        'cves': [
            {
                'id': 'CVE-2021-42013',
                'severity': 'CRITICAL',
                'cvss': 9.8,
                'description': 'Further exploitation of path traversal',
                'exploit': 'Remote code execution',
                'remediation': 'Update to 2.4.51 or later'
            }
        ]
    },
    'Apache/2.2': {
        'cves': [
            {
                'id': 'CVE-2017-9798',
                'severity': 'HIGH',
                'cvss': 7.5,
                'description': 'Optionsbleed - HTTP OPTIONS method information leak',
                'exploit': 'Information disclosure',
                'remediation': 'Update Apache 2.2 to latest version'
            },
            {
                'id': 'CVE-2011-3192',
                'severity': 'MEDIUM',
                'cvss': 5.0,
                'description': 'DoS via Range header crafting',
                'exploit': 'Denial of Service',
                'remediation': 'Disable Range requests or patch'
            }
        ]
    },
    
    # OpenSSH
    'OpenSSH_6': {
        'cves': [
            {
                'id': 'CVE-2018-15473',
                'severity': 'MEDIUM',
                'cvss': 5.3,
                'description': 'Username enumeration via timing attacks',
                'exploit': 'Enumerate valid usernames',
                'remediation': 'Update to OpenSSH 7.7 or later'
            },
            {
                'id': 'CVE-2016-10012',
                'severity': 'MEDIUM',
                'cvss': 6.5,
                'description': 'Shared memory region writable by other processes',
                'exploit': 'DoS or information disclosure',
                'remediation': 'Update to OpenSSH 7.2 or later'
            }
        ]
    },
    'OpenSSH_7.0': {
        'cves': [
            {
                'id': 'CVE-2018-15473',
                'severity': 'MEDIUM',
                'cvss': 5.3,
                'description': 'Username enumeration',
                'exploit': 'User enumeration',
                'remediation': 'Update to OpenSSH 7.7 or later'
            }
        ]
    },
    
    # Samba
    'Samba_3': {
        'cves': [
            {
                'id': 'CVE-2017-7494',
                'severity': 'CRITICAL',
                'cvss': 9.8,
                'description': 'Remote code execution via out-of-bounds pointer dereference',
                'exploit': 'Arbitrary code execution',
                'remediation': 'Update to Samba 4.6.15, 4.7.9, or 4.8.4+'
            },
            {
                'id': 'CVE-2012-1182',
                'severity': 'HIGH',
                'cvss': 7.2,
                'description': 'Symlink verification bypass',
                'exploit': 'Path traversal and arbitrary file access',
                'remediation': 'Update Samba 3 to latest'
            }
        ]
    },
    'Samba_4.0': {
        'cves': [
            {
                'id': 'CVE-2017-7494',
                'severity': 'CRITICAL',
                'cvss': 9.8,
                'description': 'Remote code execution',
                'exploit': 'Arbitrary code execution',
                'remediation': 'Update to patched version'
            }
        ]
    },
    
    # MySQL
    'MySQL_5.5': {
        'cves': [
            {
                'id': 'CVE-2012-2122',
                'severity': 'HIGH',
                'cvss': 7.5,
                'description': 'Authentication bypass with multiple connections',
                'exploit': 'Authenticate without valid password',
                'remediation': 'Update to MySQL 5.5.25 or later'
            }
        ]
    },
    'MySQL_5.6': {
        'cves': [
            {
                'id': 'CVE-2015-3152',
                'severity': 'MEDIUM',
                'cvss': 5.8,
                'description': 'SSL negotiation timing attacks',
                'exploit': 'Connection downgrade',
                'remediation': 'Update MySQL and use TLS 1.2+'
            }
        ]
    },
    
    # MongoDB
    'MongoDB_2': {
        'cves': [
            {
                'id': 'CVE-2014-3971',
                'severity': 'CRITICAL',
                'cvss': 9.1,
                'description': 'Authentication bypass',
                'exploit': 'Access without credentials',
                'remediation': 'Update to MongoDB 2.6 or enable authentication'
            }
        ]
    },
    'MongoDB_3.0': {
        'cves': [
            {
                'id': 'CVE-2015-7882',
                'severity': 'HIGH',
                'cvss': 7.5,
                'description': 'Write concern authentication bypass',
                'exploit': 'Execute operations without auth',
                'remediation': 'Update to MongoDB 3.0.7 or later'
            }
        ]
    },
    
    # Redis
    'Redis_4': {
        'cves': [
            {
                'id': 'CVE-2021-29477',
                'severity': 'HIGH',
                'cvss': 7.5,
                'description': 'Acl bypass via AUTH command',
                'exploit': 'Bypass access controls',
                'remediation': 'Update to Redis 6.2.3 or later'
            }
        ]
    },
    
    # PostgreSQL
    'PostgreSQL_9.4': {
        'cves': [
            {
                'id': 'CVE-2015-3165',
                'severity': 'HIGH',
                'cvss': 7.5,
                'description': 'SSL certificate verification bypass',
                'exploit': 'MITM attacks',
                'remediation': 'Update to PostgreSQL 9.4.3 or later'
            }
        ]
    },
    
    # IIS
    'IIS_10': {
        'cves': [
            {
                'id': 'CVE-2021-31166',
                'severity': 'CRITICAL',
                'cvss': 9.8,
                'description': 'HTTP Protocol Stack remote code execution',
                'exploit': 'Arbitrary code execution',
                'remediation': 'Apply Windows security patches'
            }
        ]
    },
    
    # Nginx
    'nginx/1.16': {
        'cves': [
            {
                'id': 'CVE-2019-9511',
                'severity': 'MEDIUM',
                'cvss': 5.3,
                'description': 'HTTP/2 rapid reset DoS',
                'exploit': 'Denial of Service',
                'remediation': 'Update to nginx 1.17.3 or later'
            }
        ]
    },
    
    # Windows RDP
    'RDP': {
        'cves': [
            {
                'id': 'CVE-2019-0708',
                'severity': 'CRITICAL',
                'cvss': 9.8,
                'description': 'Remote code execution without authentication (BlueKeep)',
                'exploit': 'Wormable RCE',
                'remediation': 'Apply Windows security patch KB4500331'
            }
        ]
    },
}


def lookup_cve(service_string):
    """Lookup CVEs for a given service string"""
    results = []
    
    service_lower = service_string.lower()
    
    for service, vuln_data in EXTENDED_CVE_DB.items():
        if service.lower() in service_lower or service.split('/')[0].lower() in service_lower:
            if 'cves' in vuln_data:
                results.extend(vuln_data['cves'])
    
    return results


def run(target, port, service):
    """
    Main Asur script entry point for CVE lookup
    """
    results = []
    
    # Build service string from available data
    service_string = f"{service}_{port}" if service else str(port)
    
    # Lookup CVEs
    cves = lookup_cve(service_string)
    
    for cve in cves:
        severity_icon = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        icon = severity_icon.get(cve.get('severity', 'UNKNOWN'), '⚪')
        
        cvss = cve.get('cvss', 'N/A')
        cve_id = cve.get('id', 'UNKNOWN')
        severity = cve.get('severity', 'UNKNOWN')
        desc = cve.get('description', '')
        
        results.append(f"cve_lookup: {icon} {cve_id} [CVSS:{cvss} {severity}] {desc[:50]}")
    
    if results:
        return results
    
    return None
