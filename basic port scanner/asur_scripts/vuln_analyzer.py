"""
Asur script: vuln_analyzer
Aggregates vulnerability findings and generates risk assessment
"""


def run(target, port, service):
    """
    Vulnerability risk assessment based on port and service
    """
    results = []
    
    # Risk assessment matrix
    risk_matrix = {
        # Critical Risk Services
        21: {'risk': 'CRITICAL', 'reason': 'FTP transmits credentials in clear text', 'recommendation': 'Use SFTP or disable FTP'},
        23: {'risk': 'CRITICAL', 'reason': 'Telnet transmits all data in clear text', 'recommendation': 'Disable Telnet, use SSH'},
        80: {'risk': 'MEDIUM', 'reason': 'HTTP without encryption', 'recommendation': 'Use HTTPS (port 443)'},
        135: {'risk': 'HIGH', 'reason': 'RPC endpoint mapper - possible access point', 'recommendation': 'Restrict access to RPC'},
        139: {'risk': 'HIGH', 'reason': 'NetBIOS - outdated protocol', 'recommendation': 'Disable NetBIOS'},
        445: {'risk': 'HIGH', 'reason': 'SMB - high attack surface', 'recommendation': 'Use SMB signing and encryption'},
        1433: {'risk': 'HIGH', 'reason': 'MSSQL exposed - default port', 'recommendation': 'Use authentication and restrict access'},
        3306: {'risk': 'CRITICAL', 'reason': 'MySQL often exposed with no auth', 'recommendation': 'Require authentication, restrict network access'},
        3389: {'risk': 'CRITICAL', 'reason': 'RDP - wormable vulnerabilities', 'recommendation': 'Apply security patches, restrict access'},
        5432: {'risk': 'HIGH', 'reason': 'PostgreSQL exposed', 'recommendation': 'Use authentication and restrict access'},
        5900: {'risk': 'CRITICAL', 'reason': 'VNC - remote access vulnerability', 'recommendation': 'Use VPN, strong passwords, update'},
        6379: {'risk': 'CRITICAL', 'reason': 'Redis no authentication by default', 'recommendation': 'Enable authentication, restrict access'},
        27017: {'risk': 'CRITICAL', 'reason': 'MongoDB no auth by default', 'recommendation': 'Enable authentication, restrict access'},
        50070: {'risk': 'HIGH', 'reason': 'Hadoop NameNode console exposed', 'recommendation': 'Restrict access, use authentication'},
    }
    
    # Port-specific findings
    findings = {
        21: 'FTP service detected - vulnerable to credential interception',
        22: 'SSH service detected - generally secure if patched',
        23: 'Telnet service detected - CRITICAL: no encryption',
        25: 'SMTP service detected - check for open relay',
        53: 'DNS service detected - check for zone transfer',
        80: 'HTTP service detected - consider HTTPS migration',
        110: 'POP3 service detected - no encryption',
        139: 'NetBIOS service detected - outdated protocol',
        143: 'IMAP service detected - enable TLS',
        389: 'LDAP service detected - check for proper authentication',
        445: 'SMB service detected - high attack surface',
        1433: 'MSSQL service detected - check default credentials',
        3306: 'MySQL service detected - verify authentication is enabled',
        3389: 'RDP service detected - ensure patches applied',
        5432: 'PostgreSQL service detected - check access controls',
        5900: 'VNC service detected - consider disabling if not needed',
        6379: 'Redis service detected - CRITICAL if accessible',
        27017: 'MongoDB service detected - CRITICAL if no auth',
    }
    
    if port in risk_matrix:
        risk_info = risk_matrix[port]
        
        # Severity icon
        risk_icon = {
            'CRITICAL': '🔴',
            'HIGH': '🟠',
            'MEDIUM': '🟡',
            'LOW': '🟢'
        }
        icon = risk_icon.get(risk_info['risk'], '⚪')
        
        results.append(f"risk_assessment: {icon} [{risk_info['risk']}] {risk_info['reason']}")
        results.append(f"remediation: ✓ {risk_info['recommendation']}")
    
    if port in findings:
        results.append(f"vulnerability_note: {findings[port]}")
    
    # Additional checks based on service name
    if service:
        service_lower = service.lower()
        
        if 'apache' in service_lower and '2.4.49' in service_lower:
            results.append("vulnerability_critical: 🔴 CVE-2021-41773 - Path traversal RCE detected!")
        
        if 'samba' in service_lower:
            results.append("vulnerability_high: 🟠 CVE-2017-7494 - Code execution possible")
        
        if 'openssh' in service_lower:
            results.append("vulnerability_medium: 🟡 Check for outdated OpenSSH versions")
        
        if 'mysql' in service_lower:
            results.append("vulnerability_critical: 🔴 Verify authentication is properly configured")
        
        if 'mongodb' in service_lower or 'mongo' in service_lower:
            results.append("vulnerability_critical: 🔴 Ensure authentication is enabled")
        
        if 'redis' in service_lower:
            results.append("vulnerability_critical: 🔴 Verify access controls are enforced")
    
    if results:
        return results
    
    return None
