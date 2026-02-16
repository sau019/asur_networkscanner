"""
Asur script: rdp_probe
Probes RDP services for information
"""
import socket


def run(target, port, service):
    """Probe RDP (Remote Desktop Protocol) services"""
    if port != 3389:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # RDP greeting (X.224 Connection Request)
        # Send initial TPKT packet to probe
        s.sendall(b'\x03\x00\x00\x13\x0eE\x00\x00\x00\x00\x00')
        
        # Try to receive RDP response
        response = s.recv(1024)
        s.close()
        
        if response and len(response) > 0:
            # Check for RDP signatures
            if b'COTP' in response or b'0x06' in response or len(response) > 10:
                return "rdp_detected: RDP service confirmed"
        
        return None
    except socket.timeout:
        return "rdp_timeout: RDP connection timed out"
    except Exception:
        return None
