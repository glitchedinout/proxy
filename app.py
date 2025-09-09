from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Referer": "https://www.nseindia.com/"
}

BASE_URL = "https://www.nseindia.com/api"

@app.route("/quote", methods=["GET"])
def get_quote():
    symbol = request.args.get("symbol")
    series = request.args.get("series", "EQ")
    if not symbol:
        return jsonify({"error": "symbol parameter is required"}), 400
    
    url = f"{BASE_URL}/quote-equity?symbol={symbol}&series={series}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    try:
        data = resp.json()
    except Exception:
        return jsonify({"error": "Invalid response from NSE", "text": resp.text}), 500
    return jsonify(data)

@app.route("/chart", methods=["GET"])
def get_chart():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "symbol parameter is required"}), 400
    
    url = f"{BASE_URL}/chart-databyindex?index={symbol}"
    resp = requests.get(url, headers=HEADERS, timeout=10)
    try:
        data = resp.json()
    except Exception:
        return jsonify({"error": "Invalid response from NSE", "text": resp.text}), 500
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
