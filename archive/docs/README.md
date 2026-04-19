# SAP FI/CO Analysis Agent - POC

AI-powered financial analysis agent that automatically analyzes SAP FI/CO reports using Claude Sonnet 4.5.

## Architecture

```
SAP FI/CO PDF Report
        ↓
   PyPDF2 Document Ingestion
   (preserves table structure)
        ↓
   Structured JSON
        ↓
   Claude (claude-sonnet-4-5)
   "SAP FI Analyst" system prompt
        ↓
   3 Specialized Agents:
   1. Anomaly Detector
   2. Variance Analyst
   3. Executive Summariser
        ↓
   Structured JSON + HTML Dashboard
```

## Features

### 1. Document Ingestion Layer
- Parses SAP FI/CO PDF reports (P&L, Trial Balance, Cost Center Reports)
- Extracts tables, metadata (company code, period, currency)
- Identifies document type automatically

### 2. Three Parallel Analysis Agents

**Anomaly Detector:**
- Duplicate postings detection
- Outlier transaction identification
- Control violation checks
- Unusual posting patterns

**Variance Analyst:**
- Actual vs Budget/Plan comparison
- Root cause analysis for material variances
- Natural language variance explanations
- Actionable recommendations

**Executive Summariser:**
- CFO-ready 5-bullet summary
- Key metrics with trends
- Critical issues highlight
- Overall financial health assessment

### 3. Structured Output
- JSON export of all analysis results
- Beautiful HTML dashboard with color-coded insights
- Token usage tracking

### 4. Interactive Q&A (NEW!)
- Ask natural language questions about your financial data
- Conversational interface with context awareness
- Get instant answers to:
  - "What are the top 3 financial issues?"
  - "Why did material costs exceed budget?"
  - "What actions should management take?"
  - "What's the gross margin percentage?"
- See [QA_GUIDE.md](QA_GUIDE.md) for complete guide

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your Anthropic API key:**
```bash
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

3. **Create a sample SAP report (optional):**
```bash
python create_sample_pdf.py
```

## Usage

### Basic Analysis

```bash
python main.py samples/sap_variance_report.pdf
```

### Analysis + Interactive Q&A

```bash
python3 main_with_qa.py samples/sap_variance_report.pdf --interactive
```

This will run the full analysis and then drop you into Q&A mode where you can ask questions about the data.

### Standalone Q&A Session

```bash
# After running analysis
python3 interactive_qa.py parsed_document.json analysis_results.json
```

### Expected Output

```
📥 STEP 1: Document Ingestion
📄 Parsing document: samples/sap_variance_report.pdf
✓ Extracted 3,421 characters
✓ Document type: Profit & Loss
✓ Found 2 table sections

🧠 STEP 2: Agent Analysis
🚀 Running SAP FI/CO Analysis - 3 Agents in Parallel

🔍 Running anomaly detection...
✓ Anomaly detection complete - Found 3 issues

📊 Running variance analysis...
✓ Variance analysis complete - Found 8 variances

📋 Creating executive summary...
✓ Executive summary complete

📤 STEP 3: Output Generation
✓ JSON results saved to: analysis_results.json
✓ HTML dashboard saved to: dashboard.html

✅ PIPELINE COMPLETE
💡 Open dashboard.html in your browser to view the results
```

### View Results

Open `dashboard.html` in your browser to see:
- Executive summary with headline and key metrics
- Anomaly detection results with severity levels
- Variance analysis with favorable/unfavorable highlighting
- Actionable recommendations

## Project Structure

```
SAP FICO Agent/
├── main.py                      # Main pipeline orchestrator
├── config.py                    # SAP FI/CO context & thresholds
├── document_ingestion.py        # PDF parsing layer
├── agents.py                    # 3 Claude-powered agents
├── output_generator.py          # JSON + HTML dashboard generator
├── create_sample_pdf.py         # Sample report generator
├── requirements.txt             # Python dependencies
├── .env.example                 # API key template
├── samples/                     # Sample SAP reports
│   └── sap_variance_report.pdf
└── README.md                    # This file
```

## Configuration

Edit [config.py](config.py) to customize:

- **Claude Model**: Default is `claude-sonnet-4-20250514`
- **Chart of Accounts**: Modify GL account ranges
- **Company Codes**: Add your company structure
- **Cost Centers**: Define your cost center hierarchy
- **Thresholds**: Adjust anomaly detection sensitivity

## SAP FI/CO Context

The agents are pre-configured with SAP FI/CO domain knowledge:

- Chart of Accounts structure (Assets, Liabilities, Revenue, Expenses)
- Company Code and Cost Center hierarchies
- Financial control rules (balanced entries, posting period checks)
- Materiality thresholds for variance flagging

## Sample Output

### Anomaly Detection
- Detects material cost overruns (15.3% over budget)
- Flags excessive marketing spend (20% variance)
- Identifies professional fees spike (25% over)

### Variance Analysis
- Revenue: +6.1% favorable ($195k)
- COGS: -11.4% unfavorable ($165k)
- Operating Profit: -11.9% unfavorable ($65k)

### Executive Summary
- One-line headline: "Q1 revenue beat by 6%, but margin compression from COGS overruns"
- 3-5 key metrics with trends
- Critical issues requiring CFO attention
- 2-3 actionable recommendations

## Future Enhancements (Not in POC)

- [ ] **SAP OData Connector**: Direct API integration with S/4HANA Cloud
- [ ] **True Parallel Processing**: Async execution of 3 agents using asyncio
- [ ] **LiteParse Integration**: More sophisticated table extraction
- [ ] **Multi-period Trending**: YoY and QoQ analysis
- [ ] **Slack/Email Alerts**: Automatic notification of critical issues
- [ ] **PDF Report Export**: Generate PDF summary using ReportLab

## Token Usage

Typical analysis uses ~8,000-12,000 tokens depending on document size:
- Input: ~6,000-8,000 tokens (document + context)
- Output: ~2,000-4,000 tokens (3 agent responses)
- Cost: ~$0.10-0.15 per analysis (Claude Sonnet 4.5 pricing)

## Testing

To test with the sample document:

```bash
# Generate sample PDF
python create_sample_pdf.py

# Run analysis
python main.py samples/sap_variance_report.pdf

# Open dashboard.html in browser
```

## Requirements

- Python 3.8+
- Anthropic API key with Claude access
- Internet connection for API calls
- 10-15MB RAM for PDF processing

## Troubleshooting

**"Module not found" errors:**
```bash
pip install -r requirements.txt
```

**"API key not found":**
```bash
# Make sure .env file exists with:
ANTHROPIC_API_KEY=sk-ant-...
```

**PDF parsing issues:**
- Ensure PDF is text-based (not scanned image)
- For scanned PDFs, add OCR preprocessing

**No anomalies/variances detected:**
- Check that sample PDF has sufficient data
- Adjust thresholds in config.py

## License

POC - For demonstration purposes

## Contact

For questions or improvements, please open an issue.
