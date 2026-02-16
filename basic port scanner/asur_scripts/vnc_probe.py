"""
Asur script: vnc_probe
Probes VNC services for version and capabilities
"""
import socket


def run(target, port, service):
    """Probe VNC (Virtual Network Computing) services"""
    vnc_ports = (5900, 5901, 5902, 5903, 5904, 5905)
    if port not in vnc_ports:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # VNC sends a protocol version string on connection
        banner = s.recv(1024).decode(errors='ignore').strip()
        
        results = []
        if banner and "RFB" in banner:
            results.append(f"vnc_banner: {banner[:60]}")
            
            # Parse VNC version
            if "3.3" in banner:
                results.append("vnc_version: 3.3 (legacy)")
            elif "3.7" in banner:
                results.append("vnc_version: 3.7")
            elif "3.8" in banner:
                results.append("vnc_version: 3.8 (TightVNC)")
            
            # Send client protocol version to get server info
            s.sendall(b"RFB 003.003\n")
            response = s.recv(1024)
            
            if response:
                results.append("vnc_security: authentication available")
        
        s.close()
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "vnc_timeout: connection timed out"
    except Exception:
        return None
