"""
Asur script: ssh_banner
Grabs SSH banner/version from port 22
"""
import socket


def run(target, port, service):
    """Extract SSH banner from SSH services"""
    if port != 22:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Read SSH banner (first line should be the version)
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        
        if banner and banner.startswith('SSH-'):
            return f"ssh_banner: {banner}"
        
        return None
    except socket.timeout:
        return "ssh_timeout: connection timed out"
    except ConnectionRefusedError:
        return None
    except Exception as e:
        return f"ssh_error: {str(e)[:40]}"
