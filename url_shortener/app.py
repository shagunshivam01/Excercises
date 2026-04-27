from flask import Flask, request, redirect, jsonify
from urllib.parse import urlparse
from db import init_db
from service import get_or_create_short_url, get_long_url

app = Flask(__name__)

def is_valid_url(url):
    parsed = urlparse(url)
    return parsed.scheme in ("http", "https") and parsed.netloc

init_db()

@app.route("/shorten", methods=["POST"])
def shorten():
    data = request.get_json()
    long_url = data.get("url")
    if not long_url or not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400
        
    short_code = get_or_create_short_url(long_url)
    short_url = request.host_url + short_code
    return jsonify({"short_url": short_url})

@app.route("/<short_code>", methods=["GET"])
def redirect_url(short_code):
    long_url = get_long_url(short_code)
    if long_url:
        return redirect(long_url, code=302)
    return jsonify({"error": "URL not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
