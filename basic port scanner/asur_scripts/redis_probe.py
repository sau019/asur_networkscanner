"""
Asur script: redis_probe
Probes Redis cache services for information
"""
import socket


def run(target, port, service):
    """Probe Redis cache services"""
    if port != 6379:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Send Redis PING command
        s.sendall(b"PING\r\n")
        response = s.recv(1024).decode(errors='ignore').strip()
        
        results = []
        if response and "PONG" in response:
            results.append("redis_detected: Redis service active and responding")
        
        # Try INFO command to get version
        s.sendall(b"INFO\r\n")
        try:
            info = s.recv(4096).decode(errors='ignore')
            
            # Extract Redis version
            for line in info.split('\r\n'):
                if 'redis_version' in line.lower():
                    version = line.split(':')[-1].strip()
                    results.append(f"redis_version: {version}")
                if 'os:' in line.lower():
                    results.append(f"redis_os: {line.split(':')[-1].strip()[:40]}")
                if 'role:' in line.lower():
                    role = line.split(':')[-1].strip()
                    results.append(f"redis_role: {role}")
        except:
            pass
        
        s.close()
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "redis_timeout: connection timed out"
    except Exception:
        return None
