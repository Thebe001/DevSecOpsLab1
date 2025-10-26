import subprocess
import requests
from http.server import HTTPServer, SimpleHTTPRequestHandler

# Fonction existante du TP1
def safe_function(cmd):
    allowed_commands = ["ls", "dir", "echo"]
    if cmd.split()[0] not in allowed_commands:
        raise ValueError("Commande non autorisée")
    subprocess.run(cmd.split(), shell=False)

# Nouvelle classe pour personnaliser le serveur HTTP
class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Répond à une requête GET avec un message simple
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        html = """
        <html>
            <body>
                <h1>Bienvenue sur l'application de test !</h1>
                <p>Ceci est une page de test pour le TP2.</p>
                <form method="POST">
                    <input type="text" name="command" placeholder="Entrez une commande">
                    <input type="submit" value="Exécuter">
                </form>
            </body>
        </html>
        """
        self.wfile.write(html.encode("utf-8"))

    def do_POST(self):
        # Gère les requêtes POST pour exécuter la commande
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("utf-8")
        # Extrait la commande du formulaire (format : command=ls)
        cmd = post_data.split("=")[1] if "=" in post_data else ""
        try:
            safe_function(cmd)
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Commande exécutée : {cmd}</h1></body></html>".encode("utf-8"))
        except ValueError as e:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(f"<html><body><h1>Erreur : {str(e)}</h1></body></html>".encode("utf-8"))

# Garde la logique CLI existante pour compatibilité
if __name__ == "__main__":
    try:
        user_input = input("Entrez une commande (ou laissez vide pour lancer le serveur) : ")
        if user_input:
            safe_function(user_input)
        else:
            # Lancer le serveur HTTP
            server_address = ('0.0.0.0', 8000)
            httpd = HTTPServer(server_address, CustomHandler)
            print("Serveur démarré sur http://localhost:8000")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("Arrêt du serveur")
        httpd.server_close()