import subprocess
import requests

def safe_function(cmd):
    allowed_commands = ["ls", "dir", "echo"]  # Restrict to safe commands
    if cmd.split()[0] not in allowed_commands:
        raise ValueError("Commande non autorisée")
    subprocess.run(cmd.split(), shell=False)

user_input = input("Entrez une commande : ")
safe_function(user_input)