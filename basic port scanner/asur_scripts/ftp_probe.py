"""
Asur script: ftp_probe
Probes FTP services for information
"""
import socket


def run(target, port, service):
    """Extract FTP banner and probe for info"""
    if port != 21:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Read FTP banner (server sends it on connection)
        banner = s.recv(1024).decode(errors='ignore').strip()
        
        # Try HELP command to get more info
        s.sendall(b"HELP\r\n")
        response = s.recv(1024).decode(errors='ignore').strip()
        
        s.close()
        
        results = []
        if banner:
            results.append(f"ftp_banner: {banner[:80]}")
        
        # Check for anonymous FTP
        if "anonymous" in banner.lower() or "anon" in banner.lower():
            results.append("ftp_anonymous: possibly enabled")
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "ftp_timeout: connection timed out"
    except Exception:
        return None
