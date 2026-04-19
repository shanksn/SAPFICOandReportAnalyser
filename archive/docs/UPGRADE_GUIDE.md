# Upgrade Guide: LlamaParse + LlamaIndex

## Why Upgrade?

Your current POC uses **PyPDF2** (basic text extraction). Upgrading to **LlamaParse + LlamaIndex** lets you analyze:

✅ **Annual Reports** - Complex multi-column layouts
✅ **10-K/10-Q Filings** - SEC documents
✅ **Investor Presentations** - Multi-format content
✅ **Scanned PDFs** - Built-in OCR
✅ **Any Company Report** - Not just SAP!

## What You Have

- ✅ Free tier LlamaIndex key
- ✅ Working SAP FI/CO agent (PyPDF2)
- ✅ Anthropic API key

## Installation (5 minutes)

### Step 1: Install Additional Dependencies

```bash
cd "/Users/shankar/Documents/SAP FICO Agent"

# Install LlamaParse and LlamaIndex
pip install llama-parse llama-index llama-index-embeddings-openai
```

### Step 2: Add LlamaIndex API Key to .env

```bash
# Edit your .env file
nano .env

# Add this line (replace with your actual key):
LLAMA_CLOUD_API_KEY=llx-your-llamaindex-key-here

# Your .env should now have:
ANTHROPIC_API_KEY=sk-ant-...
LLAMA_CLOUD_API_KEY=llx-...
```

### Step 3: Test the Enhanced Parser

```bash
# Test with your existing SAP sample
python3 document_ingestion_enhanced.py samples/sap_variance_report.pdf
```

## Usage Examples

### Example 1: Analyze Any Annual Report

```bash
# Download any company's annual report (e.g., Apple, Tesla, Microsoft)
# Then analyze it:

python3 analyze_annual_report.py apple_10k_2024.pdf
```

This will:
- Parse the complex PDF layout (LlamaParse)
- Extract financial highlights automatically
- Create searchable index (LlamaIndex)
- Allow Q&A about the report

### Example 2: Compare Multiple Companies

```bash
# Analyze multiple annual reports
python3 analyze_annual_report.py tesla_10k.pdf
python3 analyze_annual_report.py ford_10k.pdf

# Then use Q&A to compare:
"Compare Tesla vs Ford revenue growth"
"Which company has better margins?"
"What are the risk differences?"
```

### Example 3: Any PDF with Q&A

```bash
# Works with ANY financial document
python3 main_with_qa_enhanced.py any_document.pdf --interactive

# Then ask:
"Summarize this document"
"What are the key financial metrics?"
"What are the main risks?"
```

## What's Different?

### PyPDF2 (Current) vs LlamaParse (Upgraded)

| Feature | PyPDF2 | LlamaParse |
|---------|--------|------------|
| Simple text PDFs | ✅ Good | ✅ Excellent |
| Complex layouts | ❌ Poor | ✅ Excellent |
| Multi-column | ❌ Scrambles | ✅ Preserves |
| Tables | ⚠️ Basic | ✅ Perfect |
| Scanned PDFs | ❌ No OCR | ✅ Built-in OCR |
| Charts/Images | ❌ Ignored | ✅ Can describe |
| Annual reports | ❌ Struggles | ✅ Designed for this |
| Speed | Fast (local) | Slower (API call) |
| Cost | Free | $0.003/page (~$0.30/100pg) |

## Free Tier Limits

**LlamaIndex Free Tier:**
- 1,000 pages per day
- 7,000 pages per week

**That's enough for:**
- ~10 annual reports per day (100 pages each)
- ~70 annual reports per week
- Perfect for testing and moderate usage!

## New Capabilities

### 1. Annual Report Analysis

```python
from analyze_annual_report import AnnualReportAnalyzer

analyzer = AnnualReportAnalyzer("apple_10k.pdf")
analysis = analyzer.analyze()

# Auto-extracted sections:
print(analysis['financial_highlights'])
print(analysis['revenue_analysis'])
print(analysis['risks'])
print(analysis['outlook'])

# Ask anything:
print(analyzer.ask("What's the revenue growth rate?"))
print(analyzer.ask("Who are the main competitors?"))
print(analyzer.ask("What's the R&D spending?"))
```

### 2. Multi-Document Search

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Load all PDFs in a folder
documents = SimpleDirectoryReader("annual_reports/").load_data()
index = VectorStoreIndex.from_documents(documents)

# Search across ALL documents
query_engine = index.as_query_engine()
response = query_engine.query("Which company has the highest profit margin?")
```

### 3. Semantic Search

Unlike PyPDF2 which just extracts text, LlamaIndex understands **meaning**:

```python
# Semantic search finds relevant info even if exact words don't match
query = "How much money did they make?"
# Will find: "Net income", "Profit", "Earnings", "Revenue", etc.

query = "Is the company doing well?"
# Will analyze: profitability, growth, margins, outlook
```

## Integration with Your Existing Agent

You can keep BOTH versions:

### Option 1: Auto-detect (Recommended)

```python
# Automatically use best parser based on document complexity
if is_complex_document(pdf_path):
    parser = EnhancedDocumentParser(pdf_path, use_llamaparse=True)
else:
    parser = SAPDocumentParser(pdf_path)  # Original PyPDF2
```

### Option 2: User Choice

```bash
# Basic mode (free, fast)
python3 main.py report.pdf

# Enhanced mode (better parsing, costs $)
python3 main_enhanced.py report.pdf
```

### Option 3: Hybrid

```python
# Use PyPDF2 for SAP reports (they're simple, text-based)
# Use LlamaParse for annual reports (complex layouts)

if "SAP" in document_type or "Trial Balance" in document_type:
    use_pypdf2()
else:
    use_llamaparse()
```

## Cost Optimization Tips

### 1. Cache Parsed Results

```python
# Don't re-parse the same document
cache_file = f"{pdf_path}.llamaparse_cache.json"

if os.path.exists(cache_file):
    with open(cache_file) as f:
        parsed_data = json.load(f)
else:
    parsed_data = parser.parse()
    with open(cache_file, 'w') as f:
        json.dump(parsed_data, f)
```

### 2. Use PyPDF2 for Simple Docs

```python
# Try PyPDF2 first
basic_parser = SAPDocumentParser(pdf_path)
result = basic_parser.parse()

# Only use LlamaParse if PyPDF2 failed or quality is poor
if len(result['tables']) == 0 or text_quality_is_poor(result):
    enhanced_parser = EnhancedDocumentParser(pdf_path)
    result = enhanced_parser.parse()
```

### 3. Batch Processing

```python
# Process multiple documents in one go to amortize setup costs
documents = ["report1.pdf", "report2.pdf", "report3.pdf"]
parser = LlamaParse(api_key=...)

results = []
for doc in documents:
    results.append(parser.parse(doc))
```

## Real-World Examples

### Example 1: Analyze Tesla's Annual Report

```bash
# Download Tesla's 10-K from SEC website
wget https://www.sec.gov/Archives/edgar/data/.../tsla-20231231.pdf

# Analyze it
python3 analyze_annual_report.py tsla-20231231.pdf

# Ask questions:
💬 "What was Tesla's total revenue in 2023?"
💬 "How many vehicles did they deliver?"
💬 "What are their main risk factors?"
💬 "What's the outlook for 2024?"
💬 "Compare automotive vs energy segment revenues"
```

### Example 2: Competitive Analysis

```bash
# Download multiple automaker reports
# Analyze each one
python3 analyze_annual_report.py tesla_10k.pdf
python3 analyze_annual_report.py ford_10k.pdf
python3 analyze_annual_report.py gm_10k.pdf

# Then use multi-document search:
from compare_companies import CompanyComparator

comparator = CompanyComparator([
    "tesla_10k.pdf",
    "ford_10k.pdf",
    "gm_10k.pdf"
])

comparator.ask("Which company has the highest R&D spending?")
comparator.ask("Compare profit margins across all three")
comparator.ask("Who mentions AI/autonomous driving most?")
```

### Example 3: Due Diligence

```bash
# Analyzing a target company for M&A or investment

python3 analyze_annual_report.py target_company_10k.pdf --interactive

# Key questions for due diligence:
"What's the revenue growth rate over 3 years?"
"Are there any pending lawsuits or legal issues?"
"What are the main customer concentrations?"
"How leveraged is the balance sheet?"
"What are the major risk factors?"
"Who are the key executives and what's their compensation?"
```

## Troubleshooting

### "LLAMA_CLOUD_API_KEY not found"

```bash
# Make sure .env file has your key
cat .env
# Should show: LLAMA_CLOUD_API_KEY=llx-...

# If not, add it:
echo "LLAMA_CLOUD_API_KEY=llx-your-key-here" >> .env
```

### "Rate limit exceeded"

You've hit the free tier limit (1,000 pages/day). Either:
- Wait until tomorrow
- Upgrade to paid tier
- Use PyPDF2 fallback for simpler docs

### "LlamaParse returned empty text"

The PDF might be:
- Heavily encrypted
- Corrupted
- Image-only with no OCR capability

Try:
```bash
# Force OCR mode
parser = LlamaParse(api_key=..., use_ocr=True)
```

### Parser is slow

LlamaParse is cloud-based and slower than PyPDF2:
- PyPDF2: <1 second (local)
- LlamaParse: 5-30 seconds (API + processing)

For speed-critical apps, use PyPDF2 when possible.

## Next Steps

1. ✅ Install dependencies: `pip install llama-parse llama-index`
2. ✅ Add API key to `.env`
3. ✅ Test with sample: `python3 document_ingestion_enhanced.py samples/sap_variance_report.pdf`
4. ✅ Download an annual report and test
5. ✅ Try the interactive Q&A with a real annual report

## Getting Annual Reports

### SEC EDGAR (US Companies)
```
https://www.sec.gov/edgar/searchedgar/companysearch.html

Search for any public company → View filings → Find "10-K" (annual) or "10-Q" (quarterly)
```

### Company Investor Relations
```
Most companies have investor relations sections:
- Apple: https://investor.apple.com
- Microsoft: https://www.microsoft.com/en-us/investor
- Tesla: https://ir.tesla.com
```

### Examples to Try:
- **Tech**: Apple, Microsoft, Google (Alphabet), Meta, Amazon
- **Auto**: Tesla, Ford, GM, Toyota
- **Finance**: JPMorgan, Bank of America, Goldman Sachs
- **Retail**: Walmart, Target, Costco
- **Energy**: ExxonMobil, Chevron, BP

## Summary: When to Use What

| Document Type | Parser | Reason |
|---------------|--------|--------|
| SAP FI/CO reports | PyPDF2 | Simple text, fast, free |
| Annual reports (10-K) | LlamaParse | Complex layout, tables |
| Investor presentations | LlamaParse | Multi-column, images |
| Trial balance | PyPDF2 | Simple tables |
| Scanned documents | LlamaParse | Needs OCR |
| 100+ page reports | LlamaParse + Index | Better search |
| Real-time analysis | PyPDF2 | Speed critical |
| High-accuracy needed | LlamaParse | Better quality |

---

**Ready to analyze any company's annual report!** 🚀

Just add your LlamaIndex key and you're good to go.
