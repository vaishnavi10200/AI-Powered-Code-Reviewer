import re

def analyze_code(code):
    """Analyze code and return feedback"""
    issues = []
    suggestions = []
    
    # Check 1: Line length
    lines = code.split('\n')
    for i, line in enumerate(lines, 1):
        if len(line) > 80:
            issues.append(f"Line {i}: Line too long ({len(line)} chars). Keep under 80.")
    
    # Check 2: Variable naming (single letter variables)
    single_letter_vars = re.findall(r'\b[a-z]\s*=', code)
    if single_letter_vars:
        suggestions.append("Use descriptive variable names instead of single letters")
    
    # Check 3: Missing whitespace around operators
    if re.search(r'\w+\+\w+', code) or re.search(r'\w+-\w+', code):
        issues.append("Add spaces around operators (e.g., a + b instead of a+b)")
    
    # Check 4: Function without docstring
    if 'def ' in code and '"""' not in code and "'''" not in code:
        suggestions.append("Add docstrings to your functions")
    
    # Check 5: Print statements (might be debug code)
    print_count = code.count('print(')
    if print_count > 2:
        suggestions.append(f"Found {print_count} print statements. Consider using logging.")
    
    # Calculate a simple score
    score = 100 - (len(issues) * 10) - (len(suggestions) * 5)
    score = max(0, min(100, score))
    
    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "total_lines": len(lines)
    }