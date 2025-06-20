from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "<h1>🚀 Hello from Render (Flask)!</h1><p>Your Python app is live.</p>"

# Only for local testing; Render will use gunicorn
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
