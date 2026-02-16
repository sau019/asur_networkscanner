"""
Asur script: http_headers
Extracts HTTP headers from web services
"""
import socket


def run(target, port, service):
    """Extract HTTP headers from web services"""
    http_ports = (80, 8080, 8000, 3000, 5000, 8888, 8081, 9000)
    if port not in http_ports:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Send HTTP HEAD request for headers only
        request = b"HEAD / HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n"
        s.sendall(request)
        
        response = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                response += chunk
        except socket.timeout:
            pass
        finally:
            s.close()
        
        if not response:
            return None
        
        response_str = response.decode(errors='ignore')
        lines = response_str.split('\r\n')
        
        results = []
        important_headers = ['Server', 'X-Powered-By', 'X-AspNet-Version', 'X-Runtime', 'Via']
        
        for line in lines:
            for header in important_headers:
                if line.lower().startswith(header.lower()):
                    results.append(f"http_header_{header.lower()}: {line.split(':', 1)[1].strip()[:60]}")
        
        # Detect server type
        if 'Apache' in response_str:
            results.append("http_server: Apache detected")
        elif 'nginx' in response_str:
            results.append("http_server: Nginx detected")
        elif 'IIS' in response_str or 'Microsoft' in response_str:
            results.append("http_server: Microsoft IIS detected")
        elif 'Express' in response_str:
            results.append("http_server: Node.js/Express detected")
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "http_timeout: connection timed out"
    except Exception:
        return None
