def display_menu():
    print(r"""
╔════════════════════════════════╗
║        Payload Generator       ║
╠════════════════════════════════╣
║  1) Generate payload           ║
║  2) Launch listener            ║
║  3) Generate msfvenom payload  ║
║  4) Quit                       ║
╚════════════════════════════════╝
""")

def get_user_choice():
    choice = input("Your choice: ")
    return choice.strip()
