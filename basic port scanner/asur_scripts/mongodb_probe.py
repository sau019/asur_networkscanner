"""
Asur script: mongodb_probe
Probes MongoDB database services for information
"""
import socket


def run(target, port, service):
    """Probe MongoDB database services"""
    mongodb_ports = (27017, 27018, 27019, 27020)
    if port not in mongodb_ports:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Send MongoDB OP_COMMAND for server info
        # Minimal MongoDB wire protocol command
        s.sendall(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        
        response = s.recv(1024)
        s.close()
        
        results = []
        if response and len(response) > 0:
            results.append("mongodb_detected: MongoDB service active")
            
            # Check response for common patterns
            response_str = response.decode(errors='ignore')
            if "ismaster" in response_str.lower() or "version" in response_str.lower():
                results.append("mongodb_responding: server responding to queries")
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "mongodb_timeout: connection timed out"
    except Exception:
        return None
