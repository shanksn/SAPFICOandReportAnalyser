# RAG System with Qdrant - Complete Guide

## Overview

The RAG (Retrieval Augmented Generation) system enables **semantic search and multi-document analysis** for your financial reports. Instead of analyzing one document at a time, you can:

- **Query across multiple documents** (Q1, Q2, Q3 reports from different companies)
- **Compare trends** across time periods
- **Find similar patterns** using semantic search
- **Scale to hundreds of documents** without hitting Claude's context limits

## When to Use RAG vs Direct Analysis

### Use Direct Analysis (existing system) when:
- Analyzing a **single document**
- Document is **under 150 pages**
- Need deep analysis of **one specific report**

### Use RAG system when:
- Analyzing **multiple documents** (e.g., all quarterly reports for 2025)
- Need to **compare across time periods** (Q1 vs Q2 vs Q3)
- Working with **many companies** (compare Infosys vs TCS vs Wipro)
- Need **semantic search** ("find all mentions of revenue decline")
- Documents **exceed 500 pages total**

## Architecture

```
┌─────────────────┐
│  PDF Documents  │
└────────┬────────┘
         │ Parse & Chunk
         ▼
┌─────────────────┐
│  Sentence       │  Generate embeddings
│  Transformers   │  (384-dim vectors)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Qdrant Vector  │  Store chunks + metadata
│  Database       │  (local or cloud)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  User Query     │
└────────┬────────┘
         │ Semantic Search
         ▼
┌─────────────────┐
│  Top K Chunks   │  Retrieve relevant context
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Claude Sonnet  │  Generate answer
│  4.5            │  with retrieved context
└─────────────────┘
```

## Installation

### 1. Install Dependencies

```bash
pip install qdrant-client sentence-transformers
```

Or use the updated requirements.txt:
```bash
pip install -r requirements.txt
```

### 2. Choose Storage Mode

**Option A: Local Storage (Default)**
- Data stored in `./qdrant_storage/` folder
- No external dependencies
- Free and fast
- Good for development and small-scale use

**Option B: Qdrant Cloud**
- Managed cloud database
- Better for production
- Handles larger scale
- Free tier: 1GB storage

To use Qdrant Cloud:
1. Sign up at https://cloud.qdrant.io/
2. Create a cluster
3. Add to `.env`:
```
QDRANT_URL=https://your-cluster.qdrant.io
QDRANT_API_KEY=your_api_key
```

## Quick Start

### Step 1: Add Documents to Vector Store

```python
from rag_system import FinancialRAGSystem
from document_ingestion import DocumentParser

# Initialize RAG system
rag = FinancialRAGSystem(
    collection_name="financial_reports",
    qdrant_path="./qdrant_storage"  # Local storage
)

# Parse and add a document
parser = DocumentParser()
parsed = parser.parse_document('samples/q3-2026-inf.pdf')

rag.add_document(
    text=parsed['raw_text'],
    metadata={
        'company': 'Infosys',
        'period': 'Q3 2026',
        'document_type': 'Quarterly Report',
        'fiscal_year': '2026'
    },
    chunk_size=1000,
    overlap=200
)
```

### Step 2: Ask Questions

```python
# Simple Q&A
result = rag.ask_with_rag(
    question="What was the revenue in Q3 2026?",
    top_k=5
)

print(result['answer'])
print(f"Cost: ${result['cost_estimate']:.4f}")
```

### Step 3: Compare Documents

```python
# Compare across time periods
comparison = rag.compare_documents(
    question="How did revenue change from Q1 to Q3?",
    doc_filters=[
        {'period': 'Q1 2026'},
        {'period': 'Q2 2026'},
        {'period': 'Q3 2026'}
    ]
)

print(comparison['analysis'])
```

## Examples

Run the included examples:

```bash
# Add documents
python example_rag_usage.py 1

# Semantic search
python example_rag_usage.py 2

# Q&A with RAG
python example_rag_usage.py 3

# Run all examples
python example_rag_usage.py all
```

## Key Features

### 1. Semantic Search

Find relevant information without exact keyword matching:

```python
# These queries understand financial context
results = rag.search("revenue growth")
results = rag.search("cost overruns")
results = rag.search("profitability trends")
```

### 2. Filtered Search

Search within specific documents:

```python
# Only search Infosys documents
results = rag.search(
    query="revenue",
    filters={'company': 'Infosys'}
)

# Only Q3 reports
results = rag.search(
    query="expenses",
    filters={'period': 'Q3 2026'}
)
```

### 3. Multi-Document Q&A

Ask questions that span multiple documents:

```python
result = rag.ask_with_rag(
    question="Compare revenue across all quarters",
    top_k=10  # Retrieve from more documents
)
```

### 4. Trend Analysis

Analyze patterns across time:

```python
result = rag.ask_with_rag(
    question="What trends do you see in operating expenses from Q1 to Q3?",
    top_k=15
)
```

## Configuration Options

### Chunking Strategy

```python
rag.add_document(
    text=document_text,
    metadata=metadata,
    chunk_size=1000,    # Characters per chunk (default: 1000)
    overlap=200         # Overlap between chunks (default: 200)
)
```

**Guidelines:**
- **chunk_size=500**: Very granular, more chunks, slower
- **chunk_size=1000**: Balanced (recommended)
- **chunk_size=2000**: Broader context, fewer chunks
- **overlap=200**: Prevents information loss at boundaries

### Embedding Model

```python
# Default: Fast and efficient (384 dimensions)
rag = FinancialRAGSystem(
    embedding_model="sentence-transformers/all-MiniLM-L6-v2"
)

# Better quality, slower (768 dimensions)
rag = FinancialRAGSystem(
    embedding_model="sentence-transformers/all-mpnet-base-v2"
)
```

### Retrieval Parameters

```python
result = rag.ask_with_rag(
    question="...",
    top_k=5,          # Number of chunks to retrieve
    filters={...},    # Metadata filters
    model="claude-sonnet-4-20250514"  # Claude model
)
```

**top_k guidelines:**
- **top_k=3**: Quick answers, narrow context
- **top_k=5**: Balanced (recommended)
- **top_k=10+**: Multi-document comparison

## Cost Analysis

### Storage Costs
- **Local**: Free (uses disk space)
- **Qdrant Cloud Free Tier**: 1GB storage, ~1M chunks
- **Embeddings**: One-time cost (free with local model)

### Query Costs
Each RAG query costs:
- **Embedding**: Free (local model)
- **Qdrant search**: Free
- **Claude API**: $0.003/1K input tokens, $0.015/1K output tokens

Example: "What was revenue?" with top_k=5
- Input: ~2K tokens (5 chunks × ~400 tokens each)
- Output: ~200 tokens
- Cost: ~$0.009 per query

## Performance

### Speed
- **Adding documents**: 2-5 seconds per document (depends on size)
- **Semantic search**: 10-50ms
- **RAG query**: 2-4 seconds (mostly Claude API call)

### Scalability
- **Local Qdrant**: 100K+ chunks, ~1GB RAM
- **Qdrant Cloud**: Millions of chunks

### Accuracy
- Semantic search works well for financial terms
- Claude with RAG provides sourced, accurate answers
- Retrieval quality depends on chunking strategy

## Workflow Examples

### Use Case 1: Quarterly Report Analysis

```python
# 1. Add all quarterly reports
for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
    parsed = parser.parse_document(f'reports/{quarter}_2026.pdf')
    rag.add_document(
        text=parsed['raw_text'],
        metadata={'period': quarter, 'year': '2026'}
    )

# 2. Analyze trends
result = rag.ask_with_rag(
    "How did operating margins change from Q1 to Q4?",
    top_k=10
)
```

### Use Case 2: Competitive Analysis

```python
# Add reports from multiple companies
companies = ['Infosys', 'TCS', 'Wipro', 'HCL']
for company in companies:
    # Add their Q3 reports
    ...

# Compare
comparison = rag.compare_documents(
    "Compare revenue growth and profit margins across companies",
    doc_filters=[{'company': c} for c in companies]
)
```

### Use Case 3: Anomaly Detection Across Time

```python
result = rag.ask_with_rag(
    """Analyze all quarterly reports and identify:
    1. Unusual expense patterns
    2. Significant revenue fluctuations
    3. Any anomalies in cost structures""",
    top_k=20
)
```

## Troubleshooting

### Issue: "No relevant information found"
- **Cause**: Documents not added to vector store
- **Fix**: Run `example_rag_usage.py 1` to add documents

### Issue: Low search scores (<0.5)
- **Cause**: Query doesn't match document content
- **Fix**: Rephrase query, use domain-specific terms

### Issue: Slow performance
- **Cause**: Too many chunks, large documents
- **Fix**: Increase chunk_size, use Qdrant Cloud

### Issue: Out of memory
- **Cause**: Embedding model too large
- **Fix**: Use "all-MiniLM-L6-v2" (smaller model)

## Best Practices

1. **Metadata**: Always include company, period, document_type
2. **Chunking**: Start with 1000/200, adjust based on results
3. **top_k**: Use 5 for single questions, 10+ for comparisons
4. **Filters**: Use when you know which documents to search
5. **Cost**: Monitor Claude API costs for large-scale use

## Comparison: RAG vs Direct Analysis

| Feature | Direct Analysis | RAG System |
|---------|----------------|------------|
| Single document | ✅ Excellent | ⚠️ Overkill |
| Multiple documents | ❌ Manual | ✅ Automatic |
| Context limit | 200K tokens | ♾️ Unlimited |
| Speed (single doc) | ⚡ 2-3 sec | 🐢 5-10 sec |
| Speed (10 docs) | 🐢 30+ sec | ⚡ 5-10 sec |
| Semantic search | ❌ No | ✅ Yes |
| Setup complexity | ✅ Simple | ⚠️ Moderate |
| Cost per query | $0.01-0.05 | $0.005-0.02 |

## Next Steps

1. **Start simple**: Test with 2-3 documents using `example_rag_usage.py`
2. **Add your data**: Parse and add your company's reports
3. **Experiment**: Try different chunk sizes and top_k values
4. **Scale up**: Move to Qdrant Cloud if you have 50+ documents
5. **Integrate**: Combine RAG queries with your existing analysis pipeline

## Support

- Issues: https://github.com/shanksn/SAPFICOandReportAnalyser/issues
- Qdrant Docs: https://qdrant.tech/documentation/
- Claude API: https://docs.anthropic.com/
