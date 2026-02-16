"""
Simple Asur script: http_title
Exports `run(target, port, service)` which returns title or banner info.
"""
import socket


def run(target, port, service):
    """Extract HTTP title/banner from HTTP services"""
    out = []
    try:
        # Only attempt for likely HTTP ports
        http_ports = (80, 8080, 8000, 3000, 5000, 8888)
        if port not in http_ports:
            return None
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)  # Increased timeout
        s.connect((target, port))
        
        # Send HTTP GET request
        request = b"GET / HTTP/1.0\r\nHost: localhost\r\nConnection: close\r\n\r\n"
        s.sendall(request)
        
        # Receive response
        data = b""
        try:
            while True:
                chunk = s.recv(4096)
                if not chunk:
                    break
                data += chunk
        except socket.timeout:
            pass  # Timeout is ok, we have some data
        finally:
            s.close()
        
        if not data:
            return None
        
        text = data.decode(errors='ignore')
        lines = text.splitlines()
        
        # Extract status line
        if lines:
            status_line = lines[0]
            if 'HTTP' in status_line:
                return f"http_status: {status_line.strip()}"
        
        # Try to extract title
        start = text.lower().find("<title>")
        end = text.lower().find("</title>")
        if start != -1 and end != -1 and end > start:
            title = text[start+7:end].strip()
            if title:
                return f"http_title: {title}"
        
        return f"http_detected: port {port} responds to HTTP"
        
    except socket.timeout:
        return f"http_timeout: connection timed out on port {port}"
    except ConnectionRefusedError:
        return None  # Port closed
    except Exception as e:
        return f"http_error: {str(e)[:50]}"
