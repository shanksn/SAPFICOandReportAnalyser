"""
Test if Claude can now see the Statement of Comprehensive Income
"""

import json
from interactive_qa import SAPDataQA

# Load data
with open('annual_report_parsed.json', 'r') as f:
    document_data = json.load(f)

with open('annual_report_analysis.json', 'r') as f:
    analysis_results = json.load(f)

# Initialize Q&A (with fixed context limit)
qa = SAPDataQA(document_data, analysis_results)

print("="*80)
print("🧪 Testing Statement of Comprehensive Income Access")
print("="*80)
print()

# Test question - very specific about the income statement
question = """
Look for the "Statement of comprehensive income" section in the document.

Extract the following line items for Q3 (Three months ended December 31, 2025 vs 2024):

1. Revenues (in ₹ crore)
2. Cost of Sales
3. Gross profit
4. Selling and marketing expenses
5. General and administration expenses
6. Operating profit
7. Profit before income taxes
8. Income tax expense
9. Net profit
10. Basic EPS

Show me the values for both quarters and calculate growth rates.
"""

print(f"❓ Question:\n{question}\n")
print("-" * 80)

result = qa.ask(question)

if result['success']:
    print("\n💡 Answer:")
    print(result['answer'])
    print()
    print(f"📊 Tokens used: {result['usage']['total_tokens']:,}")
    print(f"💰 Cost: ${result['usage']['total_tokens'] * 0.000003:.4f}")
else:
    print(f"\n❌ Error: {result['error']}")

print("\n" + "="*80)
