from analyzer import analyze_code

# Test code
test_code = """
def calculate(a,b):
    return a+b

x=calculate(5,3)
print(x)
print(x)
print(x)
"""

result = analyze_code(test_code)
print("Score:", result['score'])
print("Issues:", result['issues'])
print("Suggestions:", result['suggestions'])