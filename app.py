from http.server import HTTPServer, SimpleHTTPRequestHandler

class CustomHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        # Vulnérabilité XSS intentionnelle
        user_input = self.path.split("?input=")[-1] if "?input=" in self.path else "default"
        html = f"""
        <html><body><h1>Bienvenue sur l'application de test !</h1><p>TP2</p>
        <div>{user_input}</div>
        <form method="POST"><input type="text" name="command"><input type="submit"></form></body></html>
        """
        self.wfile.write(html.encode("utf-8"))
if __name__ == "__main__":
    try:
        server_address = ('0.0.0.0', 8000)
        httpd = HTTPServer(server_address, CustomHandler)
        print("Serveur démarré sur http://0.0.0.0:8000")
        httpd.serve_forever()
    except KeyboardInterrupt:
        httpd.server_close()