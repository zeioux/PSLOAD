from core import checks, listeners, msfvenom_gen, menu, payloads
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    while True:
        menu.display_menu()
        choice = menu.get_user_choice()

        if choice == "1":
            os_type = input("OS (linux/windows/macos): ").strip().lower()
            lang = input("Language (bash/python/perl/ruby/nc/powershell): ").strip().lower()
            ip = input("Target IP: ").strip()
            try:
                port = int(input("Target Port: ").strip())
            except ValueError:
                print("Invalid port number.")
                continue
            protocol = input("Protocol (tcp/udp): ").strip().lower()
            encode = input("Encode payload? (y/n): ").strip().lower() == "y"
            obfuscate = input("Obfuscate payload (powershell only)? (y/n): ").strip().lower() == "y"
            key = "key"

            try:
                payload = payloads.generate_payload(os_type, lang, ip, port, protocol, encode, obfuscate, key)
                print(f"\nGenerated payload:\n{payload}\n")
            except Exception as e:
                logger.error(f"Payload generation error: {e}")

        elif choice == "2":
            try:
                port = int(input("Port to listen on: ").strip())
            except ValueError:
                print("Invalid port number.")
                continue
            protocol = input("Protocol (tcp/udp): ").strip().lower()
            listener_type = input("Listener type (nc/python): ").strip().lower()

            if listener_type == "nc":
                listeners.launch_listener_nc(port, protocol)
            elif listener_type == "python":
                listeners.launch_listener_python(port, protocol)
            else:
                print("Unsupported listener type.")

        elif choice == "3":
            if not checks.check_msfvenom():
                print("msfvenom not found! Please install Metasploit or add msfvenom to PATH.")
                continue
            lhost = input("LHOST: ").strip()
            lport = input("LPORT: ").strip()
            payload_type = input("msfvenom payload (e.g. windows/meterpreter/reverse_tcp): ").strip()
            format = input("Output format (e.g. exe): ").strip()
            msfvenom_gen.generate_msfvenom_payload(lhost, lport, payload_type, format)

        elif choice == "4":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
