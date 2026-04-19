# SAP FI/CO Analysis Agent

AI-powered financial analysis agent that analyzes SAP FI/CO reports and company annual reports using Claude Sonnet 4.5.

## Features

- 📊 **Automated Analysis** - Anomaly detection, variance analysis, executive summaries
- 💬 **Interactive Q&A** - Ask natural language questions about financial data
- 📈 **Works with Any Report** - SAP reports, 10-K/10-Q filings, quarterly earnings
- 🎯 **Three Specialized AI Agents** - Anomaly Detector, Variance Analyst, Executive Summarizer
- 🌐 **Beautiful Dashboards** - HTML output with color-coded insights

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Keys

```bash
cp .env.example .env
# Edit .env and add your API keys
```

Required:
- `ANTHROPIC_API_KEY` - Get from https://console.anthropic.com

Optional (for enhanced parsing of complex PDFs):
- `LLAMA_CLOUD_API_KEY` - Get from https://cloud.llamaindex.ai

### 3. Run Analysis

**For Annual Reports / Quarterly Reports:**
```bash
python3 analyze_annual_report.py samples/q3-2026-inf.pdf --interactive
```

**For SAP FI/CO Reports:**
```bash
python3 main_with_qa.py samples/sap_variance_report.pdf --interactive
```

## Usage Examples

### Analyze Any Company's Report

```bash
# Download any 10-K from SEC.gov
python3 analyze_annual_report.py tesla_10k.pdf --interactive
```

### Ask Questions About Financial Data

After running analysis, ask questions like:

```
What was the revenue in Q3 and how did it compare to last year?

Why did operating profit decline when revenue grew?

Show me the Statement of Comprehensive Income with all line items.

What are the top 3 financial issues?

Calculate all margins (Gross, Operating, Net) and explain the compression.
```

### Example Output

```
📊 KEY FINDINGS
═══════════════════════════════════════════════════════════

🏢 Company: Infosys Limited
📅 Fiscal Year: Q3 2026

💰 Financial Highlights:
  • Revenue: ₹45,479 crore (+8.9% YoY)
  • Operating Margin: 18.4% (down from 21.3%)
  • Net Profit: ₹6,654 crore (-2.2% YoY)

⚠️  Key Risks:
  • Margin compression across all levels
  • Employee costs rising faster than revenue
  • Cost inflation outpacing pricing power
```

## Architecture

```
PDF Report
    ↓
Document Parser (PyPDF2 or LlamaParse)
    ↓
Structured JSON
    ↓
Claude Sonnet 4.5 with SAP FI/CO Context
    ↓
3 Parallel AI Agents:
  1. Anomaly Detector
  2. Variance Analyst
  3. Executive Summarizer
    ↓
Structured Output → HTML Dashboard + Interactive Q&A
```

## What You Can Analyze

✅ SAP FI/CO Reports (P&L, Trial Balance, Cost Center, Variance)
✅ Annual Reports (10-K, 10-Q) from any company
✅ Quarterly Earnings Reports
✅ Financial Statements
✅ Management Reports

**Document Size:** Up to 150 pages (~60K tokens) work perfectly

## Project Structure

```
sap-fico-agent/
├── main_with_qa.py              # SAP reports + Q&A
├── analyze_annual_report.py     # Annual/quarterly reports
├── interactive_qa.py            # Q&A engine
├── agents.py                    # 3 AI agents
├── config.py                    # SAP FI/CO context
├── document_ingestion.py        # Basic PDF parser
├── document_ingestion_enhanced.py  # LlamaParse integration
├── output_generator.py          # Dashboard generator
├── requirements.txt             # Dependencies
├── samples/                     # Sample documents
│   ├── q3-2026-inf.pdf
│   └── sap_variance_report.pdf
└── archive/                     # Documentation & demos
    ├── demos/
    └── docs/
```

## Features in Detail

### Anomaly Detection
- Duplicate postings
- Outlier transactions
- Control violations
- Unusual posting patterns
- Missing cost center assignments

### Variance Analysis
- Actual vs Budget/Plan comparison
- Root cause analysis
- Natural language explanations
- Actionable recommendations
- Trend analysis

### Executive Summary
- CFO-ready 5-bullet summary
- Key metrics with trends
- Critical issues highlight
- Investment perspective
- Overall financial health assessment

### Interactive Q&A
- Ask anything about the financial data
- Context-aware conversations
- Cross-references multiple sections
- Provides business reasoning, not just numbers

## Cost

- Document analysis: ~$0.12-0.16
- Per Q&A question: ~$0.02-0.04
- Full session (analysis + 10 questions): ~$0.40

**No chunking or embeddings needed** - documents fit in Claude's 200K token context!

## Configuration

Edit `config.py` to customize:
- Chart of Accounts structure
- Company codes
- Cost center hierarchies
- Anomaly detection thresholds
- Materiality amounts

## Getting Financial Reports

**SEC EDGAR (US Public Companies):**
1. Visit https://www.sec.gov/edgar/searchedgar/companysearch
2. Search for company
3. Find "10-K" (annual) or "10-Q" (quarterly)
4. Download PDF

**Company Investor Relations:**
- Apple: https://investor.apple.com
- Tesla: https://ir.tesla.com
- Microsoft: https://www.microsoft.com/en-us/investor

## Technical Details

**PDF Parsing:**
- Basic: PyPDF2 (fast, free, works for most reports)
- Enhanced: LlamaParse (better for complex layouts, requires API key)

**Context Window:**
- Sends up to 50,000 characters per query
- Claude Sonnet 4.5: 200K token capacity
- Most financial reports: 10-50K tokens
- No need for chunking or vector embeddings!

**AI Model:**
- Claude Sonnet 4.5 (claude-sonnet-4-20250514)
- Specialized system prompt with SAP FI/CO knowledge
- Structured JSON output for programmatic use

## Requirements

- Python 3.8+
- Anthropic API key
- (Optional) LlamaIndex API key for enhanced parsing

## Troubleshooting

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"API key not found"**
```bash
# Make sure .env exists with:
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

**"Credit balance too low"**
- Add credits at https://console.anthropic.com/settings/plans

**Claude can't see specific sections**
- The system sends 50K characters - should capture everything
- For very large docs (>150 pages), consider splitting

## Contributing

This is a proof-of-concept system. For production use:
- Add error handling and retry logic
- Implement batch processing
- Add multi-period comparison
- Create web interface
- Add SAP OData connector for live data

## License

MIT License - Free to use and modify

## Credits

Built with:
- [Anthropic Claude](https://www.anthropic.com/claude) - AI analysis
- [LlamaParse](https://www.llamaindex.ai/) - Enhanced PDF parsing
- [PyPDF2](https://pypdf2.readthedocs.io/) - Basic PDF parsing

---

**Ready to analyze financial reports!** 🚀

Start with:
```bash
python3 analyze_annual_report.py samples/q3-2026-inf.pdf --interactive
```
