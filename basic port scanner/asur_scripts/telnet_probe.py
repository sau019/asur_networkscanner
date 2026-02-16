"""
Asur script: telnet_probe
Probes Telnet services for banners and system info
"""
import socket


def run(target, port, service):
    """Extract Telnet banner and system information"""
    if port != 23:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Read telnet banner
        banner = s.recv(1024).decode(errors='ignore').strip()
        
        results = []
        if banner:
            # Clean telnet protocol bytes and extract readable text
            clean_banner = ''.join(c if 32 <= ord(c) < 127 else ' ' for c in banner)
            clean_banner = ' '.join(clean_banner.split())
            
            if clean_banner:
                results.append(f"telnet_banner: {clean_banner[:100]}")
        
        # Try to detect OS
        if "Linux" in banner or "linux" in banner:
            results.append("telnet_os: Linux detected")
        elif "Windows" in banner or "windows" in banner:
            results.append("telnet_os: Windows detected")
        elif "Cisco" in banner or "cisco" in banner:
            results.append("telnet_os: Cisco device detected")
        
        s.close()
        
        if results:
            return results
        
        return "telnet_detected: Telnet service active"
    except socket.timeout:
        return "telnet_timeout: connection timed out"
    except Exception:
        return None
