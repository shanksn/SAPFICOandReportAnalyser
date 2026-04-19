"""
Demo: Interactive Q&A with SAP FI/CO Data
Shows what you can do with the Q&A system
"""

import json
from interactive_qa import SAPDataQA

# Load demo data
with open('parsed_document.json', 'r') as f:
    document_data = json.load(f)

with open('demo_analysis_results.json', 'r') as f:
    analysis_data = json.load(f)
    analysis_results = analysis_data.get('results', analysis_data)

# Initialize Q&A system
qa = SAPDataQA(document_data, analysis_results)

print("="*70)
print("🎯 SAP FI/CO Interactive Q&A - Demo")
print("="*70)
print()
print("This demonstrates the kinds of questions you can ask about your data.")
print("With API credits, you'll get real-time answers from Claude.")
print()

# Example questions
demo_questions = [
    {
        "category": "📊 Overall Performance",
        "questions": [
            "What's the overall financial performance this quarter?",
            "Is the company profitable?",
            "What are the biggest financial issues?",
        ]
    },
    {
        "category": "🔍 Deep Dive Analysis",
        "questions": [
            "Why did material costs exceed budget?",
            "Which operating expenses are over budget and why?",
            "Explain the revenue variance - why is product revenue up but services down?",
            "What's causing the margin compression?",
        ]
    },
    {
        "category": "💡 Actionable Insights",
        "questions": [
            "What immediate actions should management take?",
            "How can we improve profitability next quarter?",
            "What are the top 3 priorities for the CFO?",
            "Which cost centers need attention?",
        ]
    },
    {
        "category": "🧮 Calculations & Metrics",
        "questions": [
            "What's the gross margin percentage?",
            "Calculate the operating margin and compare to budget",
            "What's COGS as a percentage of revenue?",
            "How much do we need to cut costs to hit the profit target?",
        ]
    },
    {
        "category": "📈 Comparative Analysis",
        "questions": [
            "Which GL accounts have the largest unfavorable variances?",
            "Is product revenue performing better than services revenue?",
            "What's the single biggest driver of the profit miss?",
            "Compare actual vs budget across all expense categories",
        ]
    },
    {
        "category": "⚠️ Risk & Forecast",
        "questions": [
            "What are the risks if these trends continue?",
            "Will we meet annual targets at this run rate?",
            "What's the cash flow impact of these variances?",
            "Should we revise our forecast?",
        ]
    },
    {
        "category": "🎓 Educational",
        "questions": [
            "Explain what GL account 5000 represents",
            "What's the difference between gross profit and operating profit?",
            "Why is depreciation not a cash expense?",
            "What does a favorable variance mean?",
        ]
    },
]

# Display categories and questions
for section in demo_questions:
    print(f"\n{section['category']}")
    print("-" * 70)
    for i, q in enumerate(section['questions'], 1):
        print(f"  {i}. {q}")

print("\n" + "="*70)
print("\n💡 How to Use:")
print()
print("1. Run analysis first:")
print("   python3 main.py samples/sap_variance_report.pdf")
print()
print("2. Start interactive Q&A:")
print("   python3 interactive_qa.py parsed_document.json analysis_results.json")
print()
print("3. Or run analysis + Q&A in one command:")
print("   python3 main_with_qa.py samples/sap_variance_report.pdf --interactive")
print()

# Try asking one question (if API is available)
print("="*70)
print("📝 Sample Q&A Exchange")
print("="*70)
print()

sample_question = "What are the top 3 financial issues in this report?"
print(f"❓ Question: {sample_question}")
print()

result = qa.ask(sample_question)

if result['success']:
    print("✅ Answer:")
    print("-" * 70)
    print(result['answer'])
    print("-" * 70)
    print(f"\n💰 Cost: ~{result['usage']['total_tokens']} tokens (~$0.01)")
else:
    print(f"❌ Error: {result['error']}")
    print()
    print("Note: This requires API credits. See demo_analysis_results.json")
    print("for what the full analysis looks like.")

print()
print("="*70)
