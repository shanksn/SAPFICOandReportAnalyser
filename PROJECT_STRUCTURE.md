# Project Structure

## Overview

This repository contains two systems for financial document analysis:
1. **Direct Analysis System** - For single-document deep analysis
2. **RAG System** - For multi-document queries and semantic search

## Core Files (Root Directory)

### SAP FI/CO Analysis System
- **`main.py`** - Main entry point for SAP FI/CO report analysis
- **`main_with_qa.py`** - SAP analysis with interactive Q&A mode
- **`agents.py`** - Three specialized AI agents (Anomaly Detector, Variance Analyst, Executive Summarizer)
- **`config.py`** - SAP FI/CO domain context and configuration
- **`document_ingestion.py`** - Basic PDF parser using PyPDF2
- **`output_generator.py`** - HTML dashboard generator with Jinja2

### Annual Report Analyzer
- **`analyze_annual_report.py`** - Universal financial report analyzer (10-K, 10-Q, quarterly reports)
- **`document_ingestion_enhanced.py`** - Enhanced PDF parser with LlamaParse integration
- **`interactive_qa.py`** - Interactive Q&A engine for financial documents

### RAG System (Multi-Document Analysis)
- **`rag_system.py`** - Full RAG with sentence-transformers (requires PyTorch)
- **`rag_system_simple.py`** - Simplified RAG with Voyage embeddings (no PyTorch) ⭐ Recommended
- **`demo_rag.py`** - Quick 30-second demo script

### Documentation
- **`README.md`** - Main project documentation
- **`RAG_QUICKSTART.md`** - Quick start guide for RAG system ⭐ Start here for RAG
- **`RAG_GUIDE.md`** - Complete RAG documentation (400+ lines)
- **`PROJECT_STRUCTURE.md`** - This file

### Configuration
- **`requirements.txt`** - Python dependencies
- **`.gitignore`** - Git ignore rules
- **`.env`** - API keys (not in repo - create from .env.example)

## Directories

### `samples/`
Sample PDF documents for testing:
- `q3-2026-inf.pdf` - Infosys Q3 2026 quarterly report
- `sap_variance_report.pdf` - SAP variance analysis report
- `SAP_Trial_Balance_SYNTHECORP_Q1_FY2526.pdf` - SAP trial balance

### `archive/`
Test files, demos, and extra documentation:
- `archive/demos/` - Test scripts and demo files
- `archive/docs/` - Additional documentation

### `qdrant_storage/` (local, not in repo)
Local vector database storage for RAG system

## Quick Start

### 1. SAP FI/CO Analysis (Single Document)
```bash
python3 main.py
# Follow prompts or use: python3 main_with_qa.py for Q&A mode
```

### 2. Annual Report Analysis (Single Document)
```bash
python3 analyze_annual_report.py --file samples/q3-2026-inf.pdf --interactive
```

### 3. RAG System (Multi-Document)
```bash
# Quick demo
python3 demo_rag.py

# Or see RAG_QUICKSTART.md for full guide
```

## File Count

**Production files:** 16 Python files + 3 docs = 19 files
**Sample PDFs:** 3 files
**Configuration:** 2 files (.gitignore, requirements.txt)

**Total:** 24 essential files in root directory

## When to Use What

### Use Direct Analysis (`main.py`, `analyze_annual_report.py`)
- ✅ Single document analysis
- ✅ Deep dive into one report
- ✅ Documents under 150 pages
- ✅ Quick analysis (2-3 seconds)

### Use RAG System (`rag_system_simple.py`, `demo_rag.py`)
- ✅ Multiple documents (Q1, Q2, Q3, Q4)
- ✅ Historical comparisons (YoY, QoQ)
- ✅ Cross-company analysis
- ✅ Semantic search across documents
- ✅ Hundreds of documents

## Dependencies

### Core (Required)
```
anthropic==0.43.0
pypdf2==3.0.1
python-dotenv==1.0.1
jinja2==3.1.4
tabulate==0.9.0
```

### Enhanced Parsing (Optional)
```
llama-parse
llama-index
llama-index-embeddings-huggingface
```

### RAG System (Optional)
```
qdrant-client==1.7.0
sentence-transformers  # Only for rag_system.py, not needed for rag_system_simple.py
```

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Input: PDF Report                    │
└───────────────────┬─────────────────────────────────────────┘
                    │
        ┌───────────┴───────────┐
        │                       │
┌───────▼────────┐    ┌────────▼────────┐
│ Single Doc     │    │ Multi-Doc       │
│ Analysis       │    │ RAG System      │
│                │    │                 │
│ • main.py      │    │ • rag_system.py │
│ • analyze_     │    │ • demo_rag.py   │
│   annual_      │    │                 │
│   report.py    │    │ Uses Qdrant     │
│                │    │ Vector DB       │
│ Direct Claude  │    │                 │
│ API calls      │    │ Retrieval +     │
│                │    │ Claude API      │
└───────┬────────┘    └────────┬────────┘
        │                      │
        └──────────┬───────────┘
                   │
         ┌─────────▼──────────┐
         │ Claude Sonnet 4.5  │
         │ (API)              │
         └─────────┬──────────┘
                   │
         ┌─────────▼──────────┐
         │ Structured Output  │
         │ • JSON             │
         │ • HTML Dashboard   │
         │ • Q&A Responses    │
         └────────────────────┘
```

## Cost Estimates

### Single Document Analysis
- **SAP FI/CO Report:** ~$0.02-0.05 per analysis
- **Annual Report:** ~$0.05-0.10 per analysis
- **Q&A Session (10 questions):** ~$0.30-0.40

### RAG System
- **Per query:** ~$0.005-0.01
- **100 queries:** ~$0.50-1.00
- **Storage:** Free (local) or Qdrant Cloud free tier

## Development

### Adding New Features
1. Core SAP analysis → Edit `agents.py`, `config.py`
2. Document parsing → Edit `document_ingestion.py` or `document_ingestion_enhanced.py`
3. RAG features → Edit `rag_system_simple.py`
4. Output format → Edit `output_generator.py`

### Testing
- Run demos in `archive/demos/`
- Test with sample PDFs in `samples/`

## Support

- **Issues:** https://github.com/shanksn/SAPFICOandReportAnalyser/issues
- **Documentation:** See README.md and RAG_QUICKSTART.md
