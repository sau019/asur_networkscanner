"""
Asur script: mysql_probe
Probes MySQL database services for version information
"""
import socket


def run(target, port, service):
    """Probe MySQL database services"""
    if port != 3306:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # MySQL sends a greeting packet on connection
        response = s.recv(1024)
        s.close()
        
        results = []
        if response and len(response) > 10:
            results.append("mysql_detected: MySQL service active")
            
            # Parse MySQL greeting packet
            # Protocol version is at byte 0
            protocol_version = response[0]
            results.append(f"mysql_protocol: version {protocol_version}")
            
            # Try to extract server version (starts at byte 1)
            try:
                version_end = response.find(b'\x00', 1)
                if version_end > 1:
                    version = response[1:version_end].decode(errors='ignore')
                    if version:
                        results.append(f"mysql_version: {version}")
            except:
                pass
            
            # Check for authentication plugins (MariaDB vs MySQL)
            response_str = response.decode(errors='ignore')
            if "MariaDB" in response_str:
                results.append("mysql_server: MariaDB detected")
            elif "MySQL" in response_str:
                results.append("mysql_server: MySQL detected")
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "mysql_timeout: connection timed out"
    except Exception:
        return None
