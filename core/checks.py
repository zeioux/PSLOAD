import shutil
from ipaddress import ip_address

def check_msfvenom() -> bool:
    return shutil.which("msfvenom") is not None

def is_valid_ip(ip: str) -> bool:
    try:
        ip_address(ip)
        return True
    except ValueError:
        return False
