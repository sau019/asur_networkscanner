"""
Asur script: ssl_info
Grabs SSL/TLS certificate info from HTTPS ports
"""
import socket
import ssl


def run(target, port, service):
    """Extract SSL certificate information from HTTPS services"""
    https_ports = (443, 8443, 9443)
    if port not in https_ports:
        return None
    
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        
        with context.wrap_socket(s, server_hostname=target) as ssock:
            ssock.connect((target, port))
            cert = ssock.getpeercert()
        
        if cert:
            # Extract subject CN
            subject = dict(x[0] for x in cert['subject'])
            cn = subject.get('commonName', 'Unknown')
            return f"ssl_cert: CN={cn}"
        
        return None
    except ssl.SSLError as e:
        return f"ssl_error: {str(e)[:40]}"
    except socket.timeout:
        return "ssl_timeout: connection timed out"
    except ConnectionRefusedError:
        return None
    except Exception as e:
        return f"ssl_error: {str(e)[:40]}"
