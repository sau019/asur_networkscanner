"""
Asur script: ldap_probe
Probes LDAP services for directory information
"""
import socket


def run(target, port, service):
    """Probe LDAP (Lightweight Directory Access Protocol) services"""
    ldap_ports = (389, 636, 3268, 3269)
    if port not in ldap_ports:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # LDAP search request for rootDSE (empty base)
        ldap_bind = b'\x30\x0c\x02\x01\x01\x60\x07\x02\x01\x03\x04\x00\x04\x00'
        s.sendall(ldap_bind)
        
        response = s.recv(1024)
        s.close()
        
        results = []
        if response and len(response) > 10:
            results.append("ldap_detected: LDAP service active")
            
            # Check for secure LDAP (port 636)
            if port in (636, 3269):
                results.append("ldap_tls: LDAPS (LDAP over TLS) detected")
            
            # Try to extract domain info
            response_str = response.decode(errors='ignore')
            
            # Look for domain components (dc=)
            if "dc=" in response_str.lower():
                results.append("ldap_structure: Active Directory structure detected")
            
            # Check for Microsoft AD
            if port in (3268, 3269):
                results.append("ldap_ad: Microsoft Active Directory detected")
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "ldap_timeout: connection timed out"
    except Exception:
        return None
