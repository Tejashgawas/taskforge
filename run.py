from app import create_app
from flask import send_from_directory
import os

app = create_app()
# Absolute path to your frontend folder
FRONTEND_DIR = os.path.join(os.getcwd(), "frontend")


@app.route("/")
def index():
    return send_from_directory(FRONTEND_DIR, "index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(FRONTEND_DIR, filename)

if __name__ == "__main__" :
    app.run(debug = True)