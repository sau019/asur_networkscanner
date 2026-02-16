"""
Asur script: smtp_probe
Probes SMTP services for mail server information
"""
import socket


def run(target, port, service):
    """Extract SMTP banner and mail server info"""
    smtp_ports = (25, 587, 465, 2525)
    if port not in smtp_ports:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Read SMTP banner (server sends it on connection)
        banner = s.recv(1024).decode(errors='ignore').strip()
        
        results = []
        if banner:
            results.append(f"smtp_banner: {banner[:80]}")
            
            # Extract mail server name from banner
            if "ESMTP" in banner:
                results.append("smtp_supports: ESMTP")
            if "Sendmail" in banner:
                results.append("smtp_server: Sendmail detected")
            if "Postfix" in banner:
                results.append("smtp_server: Postfix detected")
            if "Exim" in banner:
                results.append("smtp_server: Exim detected")
            if "Exchange" in banner or "Microsoft" in banner:
                results.append("smtp_server: Microsoft Exchange detected")
        
        # Try EHLO to get capabilities
        s.sendall(b"EHLO test\r\n")
        response = s.recv(1024).decode(errors='ignore').strip()
        
        if "AUTH" in response:
            results.append("smtp_auth: authentication available")
        if "TLS" in response or "STARTTLS" in response:
            results.append("smtp_tls: TLS/STARTTLS available")
        
        s.close()
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "smtp_timeout: connection timed out"
    except Exception:
        return None
