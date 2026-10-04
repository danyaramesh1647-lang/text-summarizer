from flask import Flask, jsonify, render_template, request
from summarizer import summarize

app = Flask(__name__)
MAX_CHARS = 20000
MIN_WORDS = 15


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/summarize", methods=["POST"])
def summarize_route():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    length = data.get("length", "medium")
    if len(text.split()) < MIN_WORDS:
        return jsonify({"error": f"Enter at least {MIN_WORDS} words to summarize."}), 400
    if len(text) > MAX_CHARS:
        return jsonify({"error": f"Keep the text under {MAX_CHARS} characters."}), 400
    return jsonify(summarize(text, length))


if __name__ == "__main__":
    app.run(debug=True, port=5050)