"""
Asur script: dns_probe
Probes DNS services for version and information
"""
import socket


def run(target, port, service):
    """Probe DNS services for information"""
    if port != 53:
        return None
    
    try:
        # DNS query for version.bind (TXT record query)
        # DNS header + query for version.bind
        dns_query = b'\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x07version\x04bind\x00\x00\x10\x00\x03'
        
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(2.0)
        s.sendto(dns_query, (target, port))
        
        response, _ = s.recvfrom(1024)
        s.close()
        
        results = []
        if response and len(response) > 12:
            results.append("dns_detected: DNS service active")
            
            # Try to extract version info from response
            # Look for version string patterns
            response_str = response.decode(errors='ignore')
            if "BIND" in response_str or "bind" in response_str:
                results.append("dns_server: BIND detected")
            
            # Check response code for zone transfer possibility
            if len(response) > 3:
                # DNS response code in bytes 3-4
                response_code = response[3] & 0x0f
                if response_code == 0:
                    results.append("dns_response: query successful")
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "dns_timeout: query timed out"
    except Exception:
        return None
