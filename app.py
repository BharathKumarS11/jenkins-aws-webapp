from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Jenkins AWS DevOps</title>
        </head>
        <body>
            <h1>Hello from Jenkins + Docker + AWS!</h1>
            <p>Application deployed successfully.</p>
        </body>
    </html>
    """

@app.route("/health")
def health():
    return "healthy", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)