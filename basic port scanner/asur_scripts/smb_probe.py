"""
Asur script: smb_probe
Probes SMB (Samba) services for OS and version information
"""
import socket


def run(target, port, service):
    """Probe SMB services for system information"""
    smb_ports = (139, 445)
    if port not in smb_ports:
        return None
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect((target, port))
        
        # Send SMB negotiation request
        smb_request = b'\x00\x00\x00\x4c\xff\x53\x4d\x42\x72\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x02\x4c\x4d\x31\x2e\x32'
        
        s.sendall(smb_request)
        response = s.recv(1024)
        s.close()
        
        results = []
        if response and len(response) > 36:
            results.append("smb_detected: SMB service active")
            
            # Check for SMB signatures in response
            if b'Windows' in response:
                results.append("smb_os: Windows detected")
            elif b'Samba' in response:
                results.append("smb_os: Samba (Linux) detected")
            
            # Try to extract version info
            response_str = response.decode(errors='ignore')
            
            if "Windows 5.0" in response_str:
                results.append("smb_version: Windows 2000")
            elif "Windows 5.1" in response_str:
                results.append("smb_version: Windows XP")
            elif "Windows 5.2" in response_str:
                results.append("smb_version: Windows Server 2003")
            elif "Windows 6.0" in response_str:
                results.append("smb_version: Windows Vista")
            elif "Windows 6.1" in response_str:
                results.append("smb_version: Windows 7 / Server 2008")
            elif "Windows 10" in response_str:
                results.append("smb_version: Windows 10")
        
        if results:
            return results
        
        return None
    except socket.timeout:
        return "smb_timeout: connection timed out"
    except Exception:
        return None
