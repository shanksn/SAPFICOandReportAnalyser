"""
Quick test of Q&A with Infosys Q3 report
"""

import json
from interactive_qa import SAPDataQA

# Load the parsed Infosys report
with open('annual_report_parsed.json', 'r') as f:
    document_data = json.load(f)

# Load analysis results
with open('annual_report_analysis.json', 'r') as f:
    analysis_results = json.load(f)

# Initialize Q&A
qa = SAPDataQA(document_data, analysis_results)

# Test questions about Infosys Q3
print("="*70)
print("🎯 Testing Q&A with Infosys Q3 2026 Report")
print("="*70)
print()

questions = [
    "What was Infosys's Q3 revenue and how did it compare to last year?",
    "Why did the operating margin decline?",
    "What's the biggest concern for investors?",
]

for i, question in enumerate(questions, 1):
    print(f"\n{'='*70}")
    print(f"Question {i}: {question}")
    print('='*70)

    result = qa.ask(question)

    if result['success']:
        print(f"\n💡 Answer:\n{result['answer']}")
        print(f"\n📊 Tokens used: {result['usage']['total_tokens']:,}")
    else:
        print(f"\n❌ Error: {result['error']}")

print(f"\n{'='*70}")
print("✅ Q&A Test Complete")
print("="*70)
