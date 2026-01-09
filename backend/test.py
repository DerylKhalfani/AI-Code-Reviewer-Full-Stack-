from tools.tools import analyze_security_tool
import os
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("OPENAI_API_KEY")

if key:
    print('yes')

# Sample code with a security issue
test_code = """
  def login():
      api_key = "sk-abc123secretkey456"
      password = "hardcoded_password"
      return api_key
  """

  # Test the function
print("Testing security tool...")
results = analyze_security_tool(test_code, "python")

print(f"\nFound {len(results)} issues:")
for issue in results:
    print(f"- {issue.severity}: {issue.message}")
    print(f"  Line: {issue.line_number}")
    print(f"  Suggestion: {issue.suggestion}\n")