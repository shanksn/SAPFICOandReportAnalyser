"""
Deep dive into Infosys Statement of Comprehensive Income
Uses the actual line item data from the document
"""

import json
from interactive_qa import SAPDataQA

# Load data
with open('annual_report_parsed.json', 'r') as f:
    document_data = json.load(f)

with open('annual_report_analysis.json', 'r') as f:
    analysis_results = json.load(f)

qa = SAPDataQA(document_data, analysis_results)

print("="*80)
print("📊 Infosys Q3 Statement of Comprehensive Income - Detailed Analysis")
print("="*80)
print()

# Focused questions based on actual data in the document
questions = [
    # First, get the full table
    """Look at the Statement of Comprehensive Income table in the document.
    Extract ALL line items with their values for:
    - Three months ended December 31, 2025
    - Three months ended December 31, 2024
    - Calculate the Growth % for each line

    Show it in a clear table format with amounts in ₹ crore.""",

    # Revenue analysis
    """From the Statement of Comprehensive Income:
    1. What was Revenues for Q3 2025 vs Q3 2024 (in ₹ crore)?
    2. What was the growth rate?
    3. What was it in USD terms and growth rate?""",

    # Cost of Sales deep dive
    """Analyze Cost of Sales in detail:
    1. Q3 2025 amount: ₹32,652 crore
    2. Q3 2024 amount: ₹29,120 crore
    3. Growth rate: 12.1%

    Why did Cost of Sales grow at 12.1% when Revenue only grew at 8.9%?
    What does this mean for margins?""",

    # Operating expenses breakdown
    """Compare ALL Operating Expenses line items:
    1. Selling and marketing expenses: Q3 2025 vs Q3 2024
    2. General and administration expenses: Q3 2025 vs Q3 2024
    3. Total operating expenses: Q3 2025 vs Q3 2024

    Which category grew the most in absolute terms and percentage?""",

    # Operating profit analysis
    """Analyze Operating Profit:
    - Q3 2025: ₹8,355 crore
    - Q3 2024: ₹8,912 crore
    - Growth: -6.3%

    Why did Operating Profit DECLINE by 6.3% when Revenue GREW by 8.9%?
    Break down the bridge from Revenue to Operating Profit.""",

    # Bottom line
    """Analyze the complete profit flow:
    - Operating profit: ₹8,355 → ₹8,912 (declined)
    - Profit before tax: ₹9,229 → ₹9,670 (declined)
    - Net profit: ₹6,654 → ₹6,806 (declined)

    What happened at each stage? Why is every profit line declining?""",

    # EPS impact
    """EPS Analysis:
    - Basic EPS Q3 2025: ₹16.17
    - Basic EPS Q3 2024: ₹16.43
    - Change: -1.6%

    Why did EPS decline less than Net Profit declined? What explains the difference?""",

    # Margin compression summary
    """Calculate and explain the margin compression:
    1. Gross Profit Margin: Q3 2025 vs Q3 2024
    2. Operating Profit Margin: Q3 2025 vs Q3 2024
    3. Net Profit Margin: Q3 2025 vs Q3 2024

    What are the top 3 root causes of this margin compression?""",
]

for i, question in enumerate(questions, 1):
    print(f"\n{'='*80}")
    print(f"📊 Analysis {i}/{len(questions)}")
    print(f"{'='*80}")
    print(f"\n{question}\n")
    print("-" * 80)

    result = qa.ask(question)

    if result['success']:
        print(result['answer'])
        print()
        print(f"💰 Cost: ${result['usage']['total_tokens'] * 0.000003:.4f} ({result['usage']['total_tokens']:,} tokens)")
    else:
        print(f"❌ Error: {result['error']}")

    print("\n" + "="*80)

print("\n✅ Deep Dive Analysis Complete!")
print("\nKey Files Generated:")
print("  - annual_report_summary.txt (high-level summary)")
print("  - annual_report_analysis.json (structured data)")
print("\n💡 For interactive Q&A:")
print("  python3 analyze_annual_report.py samples/q3-2026-inf.pdf --interactive")
