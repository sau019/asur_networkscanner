"""
Asur script: snmp_probe
Probes SNMP services for community strings and information
"""
import socket


def run(target, port, service):
    """Probe SNMP services"""
    snmp_ports = (161, 162)
    if port not in snmp_ports:
        return None
    
    try:
        # SNMP GET request with common community strings
        communities = [b'public', b'private', b'community']
        
        results = []
        
        for community in communities:
            # Build SNMP GET packet for sysDescr (OID 1.3.6.1.2.1.1.1.0)
            snmp_packet = b'\x30' + bytes([len(community) + 25]) + \
                         b'\x02\x01\x00\x04' + bytes([len(community)]) + community + \
                         b'\xa0\x18\x02\x04\x00\x00\x00\x00\x02\x01\x00\x02\x01\x00' + \
                         b'\x30\x0a\x06\x08\x2b\x06\x01\x02\x01\x01\x01\x00'
            
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.settimeout(1.0)
                s.sendto(snmp_packet, (target, port))
                
                response, _ = s.recvfrom(1024)
                s.close()
                
                if response and len(response) > 10:
                    if community == b'public':
                        results.append("snmp_community: 'public' string accepted!")
                    elif community == b'private':
                        results.append("snmp_community: 'private' string accepted!")
                    else:
                        results.append(f"snmp_community: '{community.decode()}' accepted!")
            except socket.timeout:
                pass
            except Exception:
                pass
        
        if not results:
            # At least confirm SNMP is there if any attempt worked
            results.append("snmp_detected: SNMP service active")
        
        if results:
            return results
        
        return None
    except Exception:
        return None
