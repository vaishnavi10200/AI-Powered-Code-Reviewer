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
        
        if len(code) > 10000:
            return jsonify({"error": "Code too long (max 10,000 characters)"}), 400
        
        # Basic analysis
        basic_analysis = analyze_code(code)
        
        # AI analysis
        ai_response = get_ai_review(code, GEMINI_API_KEY)

        # Parse AI response as JSON
        ai_analysis = None
        try:
            # Remove markdown code blocks if present
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
        
        # Calculate final score (average of basic and AI scores)
        final_score = (basic_analysis['score'] + ai_analysis.get('ai_score', 0)) // 2

        # Convert basic issues to frontend format
        formatted_issues = []
        for issue in basic_analysis.get('issues', []):
            formatted_issues.append({
                'type': 'warning',
                'title': 'Code Style Issue',
                'description': issue,
                'line': None
            })

        # Convert AI issues to frontend format
        for issue in ai_analysis.get('issues', []):
            severity = issue.get('severity', 'warning')
            # Map severity to frontend types
            issue_type = 'error' if severity in ['critical', 'high'] else 'warning' if severity == 'medium' else 'info'
            formatted_issues.append({
                'type': issue_type,
                'title': 'AI Detected Issue',
                'description': issue.get('description', ''),
                'line': issue.get('line')
            })
            
        # Extract security issues
        security_list = []
        for item in ai_analysis.get('security', []):
            if isinstance(item, dict):
                security_list.append(item.get('description', str(item)))
            else:
                security_list.append(str(item))

        # Extract performance tips
        performance_list = []
        for item in ai_analysis.get('performance', []):
            if isinstance(item, dict):
                performance_list.append(item.get('suggestion', str(item)))
            else:
                performance_list.append(str(item))

        # Combine suggestions
        all_suggestions = basic_analysis.get('suggestions', []) + ai_analysis.get('best_practices', [])

        # Format response exactly as frontend expects
        result = {
            'score': final_score,
            'issues': formatted_issues,
            'ai_review': {
                'suggestions': all_suggestions,
                'security': security_list,
                'performance': performance_list
            }
        }                

        print(f"Returning result with score: {final_score}")  # Debug log
        return jsonify(result)
    
    except Exception as e:
        print(f"Error in review_code: {e}")
        return jsonify({
            "status": "error",
            "error": f"Internal server error: {str(e)}"
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)

