from dotenv import load_dotenv
load_dotenv()

from flask import Flask, request, jsonify
from flask_cors import CORS
from analyzer import analyze_code
from ai_analyzer import get_ai_review
import json
import re
import os

app = Flask(__name__)
CORS(app)

# Get API key from environment variable (secure way)
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

@app.route("/test", methods=["GET"])
def test():
    return jsonify({"message":"Backend is working!"})

@app.route("/review", methods=["POST"])
def review_code():
    try:
        data = request.json
        code = data.get("code", "")
        language = data.get('language', 'python')

        if not code:
            return jsonify({"error": "No code provided"}), 400
        
        # Limit code length to prevent abuse
        if len(code) > 10000:
            return jsonify({"error": "Code too long (max 10,000 characters)"}), 400
        
        # Basic analysis
        basic_analysis = analyze_code(code)
        
        # AI analysis
        ai_response = get_ai_review(code, GEMINI_API_KEY)

        # Try to parse AI response as JSON
        ai_analysis = None
        try:
            # First, try to remove markdown code blocks if present
            cleaned_response = re.sub(r'```json\s*|\s*```', '', ai_response).strip()
            
            # Try parsing as JSON
            ai_analysis = json.loads(cleaned_response)
            
        except json.JSONDecodeError as e:
            print(f"JSON parse error: {e}")
            # Fallback: Return error in structured format
            ai_analysis = {
                "ai_score": 0,
                "issues": [{"severity": "high", "description": "Failed to parse AI response", "line": None}],
                "security": [],
                "performance": [],
                "best_practices": [],
                "refactored_code": None,
                "raw_response": ai_response[:500]  # Include partial raw response for debugging
            }
        
        return jsonify({
            "status": "success",
            "basic_analysis": basic_analysis,
            "ai_analysis": ai_analysis,
            "language": language
        })
    
    except Exception as e:
        print(f"Error in review_code: {e}")
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

