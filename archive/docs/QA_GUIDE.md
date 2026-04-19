# Interactive Q&A Guide

## Overview

The SAP FI/CO Agent now includes **Interactive Q&A** mode, allowing you to ask natural language questions about your financial data and get instant AI-powered answers.

## What You Can Ask

### General Performance Questions
```
- What's the overall financial performance this quarter?
- Is the company profitable?
- What are the biggest issues I should be concerned about?
- Summarize the financial health of the business
```

### Deep Dive Analysis
```
- Why did material costs exceed budget?
- Which operating expenses are over budget and why?
- Explain the revenue variance between actual and budget
- What's driving the margin compression?
- Why is product revenue up but service revenue down?
```

### Actionable Insights
```
- What immediate actions should management take?
- Which cost centers need attention?
- How can we improve profitability next quarter?
- What are the risks if these trends continue?
- What are the top 3 priorities for the CFO?
```

### Calculations & Metrics
```
- What's the gross margin percentage?
- Calculate the operating margin
- What's the variance on COGS as a % of revenue?
- How much do we need to cut costs to hit budget?
- What's our EBITDA?
```

### Comparative Analysis
```
- Which GL accounts have the largest unfavorable variances?
- Is product revenue performing better than services?
- What's the biggest driver of the profit miss?
- Compare actual vs budget across all categories
- Which division is underperforming?
```

### Follow-up Questions
```
- Can you elaborate on that?
- What's the root cause?
- Show me the numbers
- What's the impact on cash flow?
- How does this compare to industry benchmarks?
```

## Three Ways to Use Q&A

### Option 1: Standalone Q&A Session

Run analysis first, then start Q&A:

```bash
# Step 1: Run analysis
python3 main.py samples/sap_variance_report.pdf

# Step 2: Start Q&A session
python3 interactive_qa.py parsed_document.json analysis_results.json
```

### Option 2: Combined Pipeline + Q&A

Run everything in one command with interactive mode:

```bash
python3 main_with_qa.py samples/sap_variance_report.pdf --interactive
```

This will:
1. Parse the PDF
2. Run the 3 agent analyses
3. Generate dashboard
4. Drop you into interactive Q&A mode

### Option 3: Programmatic Q&A

Use the Q&A system in your own Python code:

```python
from interactive_qa import SAPDataQA
import json

# Load your data
with open('parsed_document.json') as f:
    doc_data = json.load(f)

with open('analysis_results.json') as f:
    analysis = json.load(f)

# Initialize Q&A
qa = SAPDataQA(doc_data, analysis.get('results', analysis))

# Ask questions
result = qa.ask("What are the top 3 financial issues?")
print(result['answer'])

# Ask follow-up
result = qa.ask("How can we fix the material cost problem?")
print(result['answer'])

# Multiple questions
questions = [
    "What's the gross margin?",
    "Which expenses are over budget?",
    "What actions should management take?"
]
answers = qa.ask_multiple(questions)
```

## Interactive Commands

When in interactive mode:

| Command | Action |
|---------|--------|
| `exit` or `quit` | End the Q&A session |
| `reset` | Clear conversation history (start fresh) |
| `summary` | Show number of questions asked |
| Just type your question | Get an answer! |

## How It Works

### Context Awareness

The Q&A system has access to:

1. **Raw Document Data**
   - All GL account details
   - Actual vs Budget numbers
   - Metadata (company code, period, etc.)

2. **Agent Analysis Results** (if available)
   - Anomaly detection findings
   - Variance analysis
   - Executive summary

3. **Conversation History**
   - Remembers previous questions in the session
   - Can do follow-up questions
   - Maintains context across questions

### Example Conversation Flow

```
💬 Your question: What are the biggest financial problems?

💡 Answer:
The three biggest financial problems are:

1. Material costs are $130k over budget (+15.3%) - this is the largest
   variance and indicates supplier pricing issues or waste problems

2. Operating profit missed budget by $65k (-11.9%) despite revenue
   growth - showing margin compression

3. Professional fees and marketing both significantly exceeded budget
   (25% and 20% respectively), suggesting cost control weaknesses

These require immediate management attention.
───────────────────────────────────────────────────────────────
📊 Tokens: 2,145

💬 Your question: How can we fix the material cost issue?

💡 Answer:
Here are specific actions to address the $130k material cost overrun:

1. IMMEDIATE (This Week):
   - Review top 5 suppliers by spend and renegotiate contracts
   - Analyze material waste/scrap rates by production line
   - Check for any unauthorized price increases

2. SHORT-TERM (This Month):
   - Implement competitive bidding for materials >$10k
   - Conduct value engineering review to identify lower-cost alternatives
   - Set up cost variance alerts at +5% threshold

3. MEDIUM-TERM (This Quarter):
   - Diversify supplier base to improve negotiating leverage
   - Implement just-in-time inventory to reduce waste
   - Review and optimize bill of materials

Target: Reduce material costs by 5-7% to get back on budget.
───────────────────────────────────────────────────────────────
📊 Tokens: 2,487
```

Notice how the second question builds on the first - the AI remembers the context!

## Use Cases

### 1. Board Meeting Prep
```
Ask: "What are the 5 key points I should present to the board?"
Get: Concise executive summary tailored for board-level discussion
```

### 2. Variance Investigation
```
Ask: "Walk me through why we missed our profit target"
Get: Step-by-step breakdown of variance drivers with specific numbers
```

### 3. Action Planning
```
Ask: "Give me a priority-ranked action plan to fix these issues"
Get: Concrete steps with urgency levels and expected impact
```

### 4. Trend Analysis
```
Ask: "If these trends continue, what's our Q2 outlook?"
Get: Forward-looking projection based on current variances
```

### 5. Educational
```
Ask: "Explain what's happening with our gross margin"
Get: Clear explanation of margin compression with specific drivers
```

## Advanced Features

### Multi-Turn Conversations

The system maintains conversation history, so you can:

```
Q1: "What's our biggest cost problem?"
A1: "Material costs are $130k over budget..."

Q2: "Why is that happening?"
A2: "The material cost overrun is likely due to..."

Q3: "What should we do about it?"
A3: "Here's a 3-step action plan..."

Q4: "How much will that save?"
A4: "Based on the variance, you could save..."
```

### Reset for New Topics

```
> What's the revenue variance?
[Answer about revenue...]

> reset
🔄 Conversation history cleared.

> What's the cost variance?
[Fresh analysis of costs, no revenue context]
```

### Combining with Dashboard

**Workflow:**
1. Open `dashboard.html` in browser
2. Run Q&A session in terminal
3. See visual data in browser, ask questions in terminal
4. Best of both worlds!

## Cost & Performance

**Per Question:**
- Input tokens: ~1,500-3,000 (context + question)
- Output tokens: ~500-1,500 (answer)
- Total: ~2,000-4,500 tokens per Q&A
- Cost: ~$0.02-0.05 per question

**Interactive Session (10 questions):**
- Total: ~20,000-45,000 tokens
- Cost: ~$0.20-0.45
- Time: 2-3 seconds per answer

**Value:**
- Replaces 30+ minutes of analyst research
- Instant answers vs waiting for reports
- Can explore multiple hypotheses quickly

## Tips for Better Questions

### ✅ Good Questions

- **Specific**: "Why did GL 5000 exceed budget by 15%?"
- **Action-oriented**: "What should we do about the marketing overspend?"
- **Comparative**: "Which division performed better, products or services?"
- **Quantitative**: "What's the gross margin percentage?"

### ❌ Less Effective Questions

- **Too vague**: "Tell me about the numbers"
- **Outside scope**: "What's our stock price?" (not in SAP data)
- **Hypothetical without context**: "What if we doubled revenue?"
- **Yes/no when you want analysis**: "Is revenue good?" (ask "How's revenue performance?")

### 🎯 Pro Tips

1. **Start broad, then drill down**
   - "What are the key issues?" → "Tell me more about the COGS problem"

2. **Ask "why" and "how"**
   - Gets deeper analysis vs just numbers

3. **Request specific formats**
   - "Give me a 3-point action plan"
   - "Explain in bullet points"
   - "Show me a before/after comparison"

4. **Use follow-ups**
   - "Can you elaborate?"
   - "What's the root cause?"
   - "What else should I know?"

## Integration Examples

### Export Q&A to Report

```python
from interactive_qa import SAPDataQA
import json

qa = SAPDataQA(doc_data, analysis_data)

# Ask multiple questions
questions = [
    "What are the top 3 financial issues?",
    "What actions should management take?",
    "What's the risk assessment?"
]

report = []
for q in questions:
    result = qa.ask(q)
    report.append({
        'question': q,
        'answer': result['answer']
    })

# Save to file
with open('qa_report.json', 'w') as f:
    json.dump(report, f, indent=2)
```

### Slack Bot Integration

```python
# Pseudo-code for Slack integration
@app.command("/sap-ask")
def handle_question(command):
    question = command['text']

    # Load latest analysis
    qa = SAPDataQA(latest_doc_data, latest_analysis)

    # Get answer
    result = qa.ask(question)

    # Post to Slack
    respond(result['answer'])
```

### Dashboard Integration

```python
# Add Q&A widget to HTML dashboard
# User types question in web form
# Backend calls qa.ask(question)
# Display answer in dashboard
```

## Troubleshooting

**"API key not found"**
- Check `.env` file exists and has `ANTHROPIC_API_KEY=...`

**"No document data provided"**
- Run analysis first: `python3 main.py your_report.pdf`
- This creates `parsed_document.json` and `analysis_results.json`

**"Credit balance too low"**
- Add credits at https://console.anthropic.com/settings/plans

**Answers seem generic**
- Make sure you passed `analysis_results.json` to get full context
- Try more specific questions with GL account numbers

**Conversation loses context**
- Don't type `reset` unless you want to clear history
- Each session maintains context until exit

## Demo Mode

Try the demo to see examples without using API credits:

```bash
python3 demo_qa.py
```

This shows:
- Example questions across all categories
- Sample Q&A exchange (if API available)
- How to use the Q&A features

## What's Next

Potential enhancements:
- **Voice input**: Ask questions by speaking
- **Multi-document Q&A**: Compare across periods
- **Scheduled Q&A**: Daily/weekly automated insights
- **Export to PowerPoint**: Turn Q&A into presentations
- **Custom knowledge base**: Add company-specific context

---

## Quick Reference

```bash
# View example questions
python3 demo_qa.py

# Run analysis + interactive Q&A
python3 main_with_qa.py your_report.pdf --interactive

# Standalone Q&A session
python3 interactive_qa.py parsed_document.json analysis_results.json

# Programmatic usage
from interactive_qa import SAPDataQA
qa = SAPDataQA(doc_data, analysis_data)
result = qa.ask("Your question here")
```

---

**Ready to ask questions about your SAP data!** 🎯
