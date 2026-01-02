from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_code

app = Flask(__name__)
CORS(app)

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message":"Backend is working!"})

@app.route("/review", methods=["POST"])
def review_code():
    data = request.json
    code = data.get("code","")

    if not code:
        return jsonify({"error": "No code provided"}), 400
    
    # Analyze the Code
    analysis = analyze_code(code)

    return jsonify({
        "status" : "success",
        "analysis": analysis
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)

