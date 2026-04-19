# Archive Folder

This folder contains demos, documentation, and generated outputs that aren't needed for daily use.

## What's Here

### `/demos` - Demo Scripts & Examples
- `demo_qa.py` - Shows Q&A examples (run without API credits)
- `create_demo_output.py` - Generates sample analysis output
- `create_sample_pdf.py` - Creates sample SAP variance report
- `demo_dashboard.html` - Example of what dashboard output looks like
- `demo_analysis_results.json` - Example analysis results

**Use these to:**
- See what the output looks like without running analysis
- Generate test data
- Learn how the system works

### `/docs` - Complete Documentation
- `README.md` - Full technical documentation
- `QUICKSTART.md` - Quick start guide
- `QA_GUIDE.md` - 70+ example questions you can ask
- `UPGRADE_GUIDE.md` - How to use LlamaParse for complex PDFs
- `EMBEDDING_GUIDE.md` - When/how to use embedding models
- `SUMMARY.md` - Complete feature summary
- `QUICK_REFERENCE.txt` - Command reference card
- `setup_enhanced.sh` - Automated setup script

**Use these when:**
- You want detailed technical information
- You need specific examples
- You're setting up advanced features
- You want to understand how everything works

### Root Level - Generated Output Files

When you run analyses, output files are automatically moved here:
- `analysis_results.json` - Full analysis data
- `dashboard.html` - Visual dashboard
- `parsed_document.json` - Parsed PDF data

## Quick Access

**Want to see what output looks like?**
```bash
open archive/demos/demo_dashboard.html
```

**Need detailed Q&A examples?**
```bash
cat archive/docs/QA_GUIDE.md
```

**Want complete technical docs?**
```bash
cat archive/docs/README.md
```

**Run a demo (no API needed)?**
```bash
python3 archive/demos/demo_qa.py
```

## Back to Main

Go back to root directory and read `START_HERE.md` for daily usage.

```bash
cd ..
cat START_HERE.md
```
