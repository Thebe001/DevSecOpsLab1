import subprocess
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler

def safe_function(cmd):
    allowed_commands = ["ls", "dir", "echo"]
    if cmd.split()[0] not in allowed_commands:
        raise ValueError("Commande non autorisée")
    subprocess.run(cmd.split(), shell=False)

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """
        <html><body><h1>Bienvenue sur l'application de test !</h1><p>TP2</p><form method="POST"><input type="text" name="command"><input type="submit"></form></body></html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        cmd = post_data.split("=")[1] if "=" in post_data else ""
        try:
            safe_function(cmd)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Commande : {cmd}</h1></body></html>".encode("utf-8"))
        except ValueError as e:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Erreur : {str(e)}</h1></body></html>".encode("utf-8"))

if __name__ == "__main__":
    try:
        server_address = ('0.0.0.0', 8000)
        httpd = HTTPServer(server_address, CustomHandler)
        print("Serveur démarré sur http://0.0.0.0:8000")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()