import subprocess
import socket
from typing import Literal

def launch_listener_nc(port: int, protocol: Literal["tcp", "udp"] = "tcp") -> None:
    args = ["nc"]
    if protocol == "tcp":
        args += ["-lvnp", str(port)]
    elif protocol == "udp":
        args += ["-ulnp", str(port)]
    else:
        raise ValueError("Unsupported protocol. Use 'tcp' or 'udp'.")
    try:
        subprocess.run(args, check=True)
    except FileNotFoundError:
        print("Error: 'nc' (netcat) not found. Please install it.")
    except subprocess.CalledProcessError as e:
        print(f"nc exited with error: {e}")

def launch_listener_python(port: int, protocol: Literal["tcp", "udp"] = "tcp") -> None:
    if protocol != "tcp":
        print("Python listener currently supports only TCP.")
        return
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("", port))
            s.listen(1)
            print(f"Listening on port {port} TCP...")
            conn, addr = s.accept()
            with conn:
                print(f"Connection from {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    print(data.decode(errors='ignore'), end='')
        except Exception as e:
            print(f"Socket error: {e}")
