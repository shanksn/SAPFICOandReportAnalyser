# SAP FI/CO Agent - File Organization

## ✅ ESSENTIAL FILES (Keep in Root)

### Core Pipeline
- `main.py` - Basic analysis pipeline (SAP reports)
- `main_with_qa.py` - Analysis + Interactive Q&A mode
- `config.py` - SAP FI/CO context & settings
- `agents.py` - 3 Claude agents (Anomaly, Variance, Executive)
- `document_ingestion.py` - PDF parser (PyPDF2)
- `interactive_qa.py` - Q&A engine
- `output_generator.py` - Dashboard generator
- `requirements.txt` - Dependencies

### Enhanced Features (Optional)
- `analyze_annual_report.py` - For annual reports (10-K, etc.)
- `document_ingestion_enhanced.py` - LlamaParse integration

### Configuration
- `.env` - API keys (ANTHROPIC_API_KEY, LLAMA_CLOUD_API_KEY)
- `.env.example` - Template

### Sample Data
- `samples/sap_variance_report.pdf` - Test document

### Quick Start
- `START_HERE.md` - **Read this first!**

---

## 📁 ARCHIVED FILES

### Archive: Demos (./archive/demos/)
- `demo_qa.py` - Q&A demo script
- `create_demo_output.py` - Demo data generator
- `create_sample_pdf.py` - Sample PDF generator
- `demo_dashboard.html` - Example output
- `demo_analysis_results.json` - Example results

### Archive: Documentation (./archive/docs/)
- `README.md` - Full technical docs (now in archive)
- `QUICKSTART.md` - Quick start guide
- `QA_GUIDE.md` - Detailed Q&A guide
- `UPGRADE_GUIDE.md` - LlamaParse upgrade guide
- `EMBEDDING_GUIDE.md` - Embedding model guide
- `SUMMARY.md` - Feature summary
- `QUICK_REFERENCE.txt` - Command reference
- `setup_enhanced.sh` - Setup script

### Archive: Generated Output (automatically archived)
- `analysis_results.json` - Generated each run
- `parsed_document.json` - Generated each run
- `dashboard.html` - Generated each run

---

## 🗂️ Recommended Structure

```
SAP FICO Agent/
├── START_HERE.md              ← Read this first!
├── .env                        ← Your API keys
│
├── Core Files (8 files)
│   ├── main.py
│   ├── main_with_qa.py
│   ├── config.py
│   ├── agents.py
│   ├── document_ingestion.py
│   ├── interactive_qa.py
│   ├── output_generator.py
│   └── requirements.txt
│
├── Enhanced (2 files)
│   ├── analyze_annual_report.py
│   └── document_ingestion_enhanced.py
│
├── samples/
│   └── sap_variance_report.pdf
│
└── archive/
    ├── demos/                  ← Demo scripts
    └── docs/                   ← Full documentation
```

---

## Daily Usage - Only Need These:

**For SAP Reports:**
```bash
python3 main_with_qa.py your_report.pdf --interactive
```

**For Annual Reports:**
```bash
python3 analyze_annual_report.py company_10k.pdf --interactive
```

**Files generated (auto-archived):**
- `analysis_results.json`
- `dashboard.html`
- `parsed_document.json`

That's it! Only 12 files in root directory, everything else archived.
