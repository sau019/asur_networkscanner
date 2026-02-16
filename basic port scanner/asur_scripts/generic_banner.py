"""
Asur script: generic_banner
Attempts a generic banner grab from any service
Connects and reads the first response without sending anything
"""
import socket


def run(target, port, service):
    """Grab initial server banner/greeting"""
    # Skip if already handled by more specific scripts
    if port in (22, 80, 8080, 8000, 3000, 5000, 8888, 443, 8443, 9443):
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1.0)
        s.connect((target, port))
        
        # Wait for server to send banner without us sending anything
        banner = s.recv(1024).decode(errors='ignore').strip()
        s.close()
        
        if banner and len(banner) > 0 and len(banner) < 200:
            # Clean up banner for display
            banner = banner.replace('\n', ' | ').replace('\r', '')
            return f"service_banner: {banner[:100]}"
        
        return None
    except socket.timeout:
        return None  # No banner sent
    except ConnectionRefusedError:
        return None
    except Exception:
        return None
