from google import genai
import os
import json

def setup_ai(api_key):
    """Setup Gemini AI client"""
    client = genai.Client(api_key=api_key)
    return client

def get_ai_review(code, api_key):
    """Get AI-powered code review"""
    try:
        client = setup_ai(api_key)


        prompt = f"""You are an expert code reviewer. Analyze this code and provide feedback.

IMPORTANT: Respond with ONLY valid JSON, no markdown formatting, no code blocks, no additional text.

Your JSON response must have this exact structure:
{{
  "ai_score": <number 0-100>,
  "issues": [
    {{"severity": "high/medium/low", "description": "issue description", "line": <line_number or null>}}
  ],
  "security": [
    {{"severity": "critical/high/medium/low", "description": "security issue"}}
  ],
  "performance": [
    {{"impact": "high/medium/low", "suggestion": "performance improvement"}}
  ],
  "best_practices": [
    "violation description"
  ],
  "refactored_code": "<improved version of the code or null if no major improvements needed>"
}}

Code to review:
```
{code}
```

Remember: Return ONLY the JSON object, nothing else."""


        response = client.models.generate_content(
            model="models/gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception as e:
        print(f"Full error details: {e}")
        # Return valid JSON even on error
        error_response = {
            "ai_score": 0,
            "issues": [{"severity": "high", "description": f"AI Error: {str(e)}", "line": None}],
            "security": [],
            "performance": [],
            "best_practices": [],
            "refactored_code": None
        }
        return json.dumps(error_response)