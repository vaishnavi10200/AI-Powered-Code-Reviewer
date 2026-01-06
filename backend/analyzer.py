import re

def analyze_code(code):
    """Analyze code and return feedback"""
    issues = []
    suggestions = []
    
    lines = code.split('\n')

    # Check 1: Line length
    for i, line in enumerate(lines, 1):
        if len(line) > 80:
            issues.append(f"Line {i}: Line too long ({len(line)} chars). Keep under 80.")
    
    # Check 2: Variable naming (single letter variables)
    single_letter_vars = re.findall(r'\b[a-z]\s*=', code)
    if single_letter_vars:
        suggestions.append("Use descriptive variable names instead of single letters")

    # Check 2b: Single letter function parameters
    param_pattern = r'def\s+\w+\(([^)]+)\)'
    matches = re.findall(param_pattern, code)
    for params in matches:
        param_list = [p.strip().split('=')[0].strip() for p in params.split(',')]
        single_letter_params = [p for p in param_list if len(p) == 1 and p.isalpha()]
        if single_letter_params:
            issues.append(f"Use descriptive parameter names instead of: {', '.join(single_letter_params)}")

    # Check 3: Missing whitespace around operators
    if re.search(r'\w+\+\w+', code) or re.search(r'\w+-\w+', code):
        issues.append("Add spaces around operators (e.g., a + b instead of a+b)")
    
    # Check 4: Function without docstring
    if 'def ' in code and '"""' not in code and "'''" not in code:
        suggestions.append("Add docstrings to your functions")
    
    # Check 5: Print statements 
    print_count = code.count('print(')
    if print_count > 2:
        suggestions.append(f"Found {print_count} print statements. Consider using logging.")
    
    # Check 6: Short function names 
    short_func_names = re.findall(r'def\s+([a-z]{1,4})\s*\(', code)
    if short_func_names:
        issues.append(f"Use descriptive function names instead of: {', '.join(short_func_names)}")
    
    # Check 7: Common security issues 
    if 'eval(' in code:
        issues.append("CRITICAL: Never use eval() - major security risk")
    if 'exec(' in code:
        issues.append("CRITICAL: Never use exec() - major security risk")
    if 'os.system(' in code:
        issues.append("Security risk: os.system() can execute arbitrary commands")
    
    # Check 8: Inefficient patterns 
    nested_loops = len(re.findall(r'for\s+\w+\s+in.*:\s*\n\s+for\s+\w+\s+in', code))
    if nested_loops > 0:
        suggestions.append("Nested loops detected - consider optimizing for better performance")
    

    # Calculate score 
    score = 100
    score -= len(issues) * 8        # Each issue: -8 points 
    score -= len(suggestions) * 5   # Each suggestion: -5 points
    
    # Extra penalties
    if 'eval(' in code or 'exec(' in code:
        score -= 20  # Extra penalty for dangerous functions
    if 'os.system(' in code:
        score -= 15  # Extra penalty for security risk
    
    score = max(0, min(100, score))
    
    
    return {
        "score": score,
        "issues": issues,
        "suggestions": suggestions,
        "total_lines": len(lines)
    }