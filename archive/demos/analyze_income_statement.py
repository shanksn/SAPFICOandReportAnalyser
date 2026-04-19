"""
Deep dive into Statement of Comprehensive Income using Q&A
Ask targeted questions to understand variance drivers
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

print("="*80)
print("📊 Statement of Comprehensive Income - Deep Dive Analysis")
print("="*80)
print()

# Series of targeted questions to understand the P&L
questions = [
    # Overview
    "Show me all the line items from the Statement of Comprehensive Income with their Q3 2026 vs Q3 2025 values and growth rates",

    # Revenue analysis
    "What was the revenue in Q3 2026 vs Q3 2025 (both in rupees and dollars)? Break down the growth rate",

    # Cost analysis
    "Analyze the Cost of Sales line item - what changed from Q3 2025 to Q3 2026 and why is it growing faster than revenue?",

    # Operating expenses
    "Break down all Operating Expenses line items - which increased the most and why?",

    # Profitability
    "Compare Operating Profit, PBT, and Net Profit between Q3 2026 and Q3 2025. Why is profit declining despite revenue growth?",

    # Margins
    "Calculate all the key margins (Gross, Operating, Net) for both quarters and explain the margin compression",

    # Root cause
    "What are the top 3 reasons why profitability declined in Q3 2026 vs Q3 2025?",
]

for i, question in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"Question {i}/{len(questions)}")
    print(f"{'='*80}")
    print(f"❓ {question}")
    print()

    result = qa.ask(question)

    if result['success']:
        print(f"💡 Answer:")
        print("-" * 80)
        print(result['answer'])
        print("-" * 80)
        print(f"📊 Tokens: {result['usage']['total_tokens']:,} | Cost: ~${result['usage']['total_tokens'] * 0.000003:.4f}")
    else:
        print(f"❌ Error: {result['error']}")

    print()
    input("Press Enter for next question...")

print("\n" + "="*80)
print("✅ Analysis Complete!")
print("="*80)
print()
print("💡 You can now ask your own follow-up questions interactively:")
print("   python3 analyze_annual_report.py samples/q3-2026-inf.pdf --interactive")
