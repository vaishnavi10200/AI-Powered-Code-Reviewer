from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message":"Backend is working!"})

@app.route("/review", methods=["POST"])
def review_code():
    data = request.json
    code = data.get("code","")

    return jsonify({
        "status" : "success",
        "original_code" : code,
        "feedback" : "Analysis coming soon!"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000)

