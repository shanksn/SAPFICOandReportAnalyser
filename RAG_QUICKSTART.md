# RAG System - Quick Start

## What is This?

The RAG (Retrieval Augmented Generation) system lets you **analyze multiple financial documents at once** using semantic search and AI.

Instead of analyzing one report at a time, you can:
- Query across Q1, Q2, Q3, Q4 reports simultaneously
- Compare companies (Infosys vs TCS vs Wipro)
- Find trends across time periods
- Ask questions that span multiple documents

## Installation

```bash
# Install the one required dependency
pip3 install qdrant-client

# That's it! (python-dotenv and anthropic should already be installed)
```

## Quick Demo (30 seconds)

```bash
python3 demo_rag.py
```

This will:
1. Initialize the RAG system
2. Add the Infosys Q3 report to the vector store
3. Ask 2 example questions using Claude
4. Show you the results

**Expected output:**
- Document added with ~20 chunks
- Questions answered with citations
- Cost: ~$0.01 total

## How It Works

```
Your PDFs → Split into chunks → Generate embeddings → Store in Qdrant
                                                              ↓
Your Question → Find relevant chunks ← Semantic Search ←─────┘
                       ↓
              Send to Claude with context → Get answer with citations
```

## Two Versions

### 1. **rag_system_simple.py** (Recommended - No PyTorch)
- Uses Voyage embeddings API (optional, free tier available)
- Falls back to keyword matching if no API key
- Simpler installation
- **Use this version!**

### 2. **rag_system.py** (Advanced - Requires PyTorch)
- Uses local sentence-transformers models
- No external API calls for embeddings
- Requires PyTorch installation (~2GB)
- Slower installation

## Basic Usage

```python
from rag_system_simple import SimpleFinancialRAGSystem
from document_ingestion import SAPDocumentParser

# 1. Initialize RAG
rag = SimpleFinancialRAGSystem()

# 2. Add a document
parser = SAPDocumentParser('path/to/report.pdf')
parsed = parser.parse()

rag.add_document(
    text=parsed['raw_text'],
    metadata={
        'company': 'Infosys',
        'period': 'Q3 2026',
        'document_type': 'Quarterly Report'
    }
)

# 3. Ask questions
result = rag.ask_with_rag(
    "What was the revenue in Q3?",
    top_k=5
)

print(result['answer'])
print(f"Cost: ${result['cost_estimate']:.4f}")
```

## Common Use Cases

### Use Case 1: Add Multiple Quarters

```python
rag = SimpleFinancialRAGSystem()

for quarter in ['Q1', 'Q2', 'Q3']:
    parser = SAPDocumentParser(f'reports/{quarter}_2026.pdf')
    parsed = parser.parse()
    rag.add_document(
        text=parsed['raw_text'],
        metadata={'period': quarter, 'year': '2026'}
    )

# Now ask questions across all quarters
result = rag.ask_with_rag("How did revenue trend from Q1 to Q3?")
```

### Use Case 2: Compare Companies

```python
# Add reports from multiple companies
companies = ['Infosys', 'TCS', 'Wipro']
for company in companies:
    # Add their Q3 reports...
    rag.add_document(text=..., metadata={'company': company})

# Compare them
comparison = rag.compare_documents(
    "Compare profit margins across companies",
    doc_filters=[{'company': c} for c in companies]
)
```

### Use Case 3: Filtered Search

```python
# Search only within Infosys documents
results = rag.search(
    query="revenue growth",
    filters={'company': 'Infosys'}
)
```

## Optional: Voyage API Key (Better Search Quality)

By default, the system works in fallback mode (keyword matching). For better semantic search:

1. Get free API key at https://www.voyageai.com/
2. Add to `.env`:
   ```
   VOYAGE_API_KEY=your_key_here
   ```
3. Run again - now with semantic search!

## Configuration

### Chunk Size
```python
rag.add_document(
    text=doc_text,
    metadata=metadata,
    chunk_size=1000,  # Characters per chunk (default: 1000)
    overlap=200       # Overlap (default: 200)
)
```

- **Smaller chunks (500)**: More precise search, more chunks
- **Larger chunks (2000)**: More context, fewer chunks
- **Recommended**: 1000 (balanced)

### Retrieval Count
```python
result = rag.ask_with_rag(
    question="...",
    top_k=5  # Number of chunks to retrieve (default: 5)
)
```

- **top_k=3**: Quick single answers
- **top_k=5**: Balanced (recommended)
- **top_k=10+**: Multi-document comparisons

### Storage Location

```python
# Local storage (default)
rag = SimpleFinancialRAGSystem(
    qdrant_path="./qdrant_storage"
)

# Qdrant Cloud (for production)
rag = SimpleFinancialRAGSystem(
    use_cloud=True,
    qdrant_url=os.getenv('QDRANT_URL'),
    qdrant_api_key=os.getenv('QDRANT_API_KEY')
)
```

## Cost

- **Storage**: Free (local) or Qdrant Cloud free tier (1GB)
- **Embeddings**: Free (Voyage free tier or fallback mode)
- **Claude API**: ~$0.005-0.01 per query
  - Example: 10 questions = ~$0.10

## Examples

Run the included examples:

```bash
# Run the quick demo
python3 demo_rag.py

# Run full test suite
python3 test_rag_simple.py

# Run specific examples
python3 example_rag_usage.py 1  # Add documents
python3 example_rag_usage.py 2  # Semantic search
python3 example_rag_usage.py 3  # Q&A demo
python3 example_rag_usage.py all  # All examples
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'qdrant_client'"
```bash
pip3 install qdrant-client
```

### "VOYAGE_API_KEY not found"
This is just a warning! The system works fine in fallback mode (keyword matching). For better semantic search, get a free key at https://www.voyageai.com/

### "No relevant information found"
- Make sure you added documents first: `rag.add_document(...)`
- Check that your query matches the document content
- Try broader search terms

### Search results have score 0.000
This is normal in fallback mode (without Voyage API key). The system still works, just using keyword matching instead of semantic search.

## RAG vs Direct Analysis

| Feature | Direct Analysis (existing) | RAG System (new) |
|---------|---------------------------|------------------|
| Best for | Single document deep dive | Multi-document queries |
| Speed | ⚡ Fast (2-3 sec) | 🐢 Moderate (5-10 sec) |
| Documents | One at a time | Unlimited |
| Setup | ✅ Simple | ⚠️ Moderate |
| Semantic search | ❌ No | ✅ Yes |
| Comparisons | ❌ Manual | ✅ Automatic |

**Recommendation**: Use both!
- RAG for multi-document queries
- Direct analysis for single-document deep dives

## Full Documentation

See **[RAG_GUIDE.md](RAG_GUIDE.md)** for:
- Detailed architecture
- Advanced use cases
- Performance optimization
- Production deployment
- Complete API reference

## Next Steps

1. ✅ Run `python3 demo_rag.py` to see it in action
2. 📚 Add your own documents
3. 🔍 Experiment with different queries
4. 📖 Read [RAG_GUIDE.md](RAG_GUIDE.md) for advanced features
5. 🚀 Deploy to production (local or Qdrant Cloud)

## Support

- **Issues**: https://github.com/shanksn/SAPFICOandReportAnalyser/issues
- **Qdrant Docs**: https://qdrant.tech/documentation/
- **Claude API**: https://docs.anthropic.com/
