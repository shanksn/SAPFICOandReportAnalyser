"""
Example usage of RAG system with Qdrant for multi-document financial analysis

This demonstrates:
1. Adding multiple documents to the vector store
2. Semantic search across documents
3. Q&A with retrieval augmented generation
4. Multi-document comparison
"""

import os
from rag_system import FinancialRAGSystem
from document_ingestion import DocumentParser


def example_1_add_documents():
    """Add multiple financial documents to the RAG system"""
    print("=" * 80)
    print("EXAMPLE 1: Adding Documents to Vector Store")
    print("=" * 80)

    # Initialize RAG system (uses local Qdrant storage)
    rag = FinancialRAGSystem(
        collection_name="financial_reports",
        embedding_model="sentence-transformers/all-MiniLM-L6-v2",
        qdrant_path="./qdrant_storage"
    )

    # Parse and add documents
    parser = DocumentParser()
    documents = [
        {
            'path': 'samples/q3-2026-inf.pdf',
            'metadata': {
                'company': 'Infosys',
                'period': 'Q3 2026',
                'document_type': 'Quarterly Report',
                'fiscal_year': '2026'
            }
        },
        {
            'path': 'samples/sap_variance_report.pdf',
            'metadata': {
                'company': 'SYNTHECORP',
                'period': 'Q1 FY2526',
                'document_type': 'SAP Variance Report',
                'fiscal_year': '2526'
            }
        }
    ]

    for doc in documents:
        print(f"\nProcessing: {doc['path']}")
        parsed = parser.parse_document(doc['path'])

        # Add to vector store
        num_chunks = rag.add_document(
            text=parsed['raw_text'],
            metadata=doc['metadata'],
            chunk_size=1000,
            overlap=200
        )
        print(f"✅ Added {num_chunks} chunks for {doc['metadata']['company']}")

    # Show stats
    stats = rag.get_collection_stats()
    print(f"\n📊 Collection Stats:")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Vector dimension: {stats['vector_dimension']}")


def example_2_semantic_search():
    """Perform semantic search across all documents"""
    print("\n" + "=" * 80)
    print("EXAMPLE 2: Semantic Search")
    print("=" * 80)

    rag = FinancialRAGSystem()

    queries = [
        "What is the revenue for the quarter?",
        "Are there any cost overruns or budget variances?",
        "What are the key financial metrics?"
    ]

    for query in queries:
        print(f"\n🔍 Query: {query}")
        results = rag.search(query=query, top_k=3)

        for i, result in enumerate(results, 1):
            metadata = result['metadata']
            print(f"\n  [{i}] {metadata.get('company')} - {metadata.get('period')}")
            print(f"      Score: {result['score']:.3f}")
            print(f"      Text: {result['text'][:200]}...")


def example_3_rag_qa():
    """Ask questions using RAG with Claude"""
    print("\n" + "=" * 80)
    print("EXAMPLE 3: Q&A with RAG")
    print("=" * 80)

    rag = FinancialRAGSystem()

    questions = [
        "What was Infosys revenue in Q3 2026?",
        "Which cost centers have budget variances in SYNTHECORP?",
        "What are the key financial highlights across all companies?"
    ]

    for question in questions:
        print(f"\n❓ Question: {question}")
        print("-" * 80)

        result = rag.ask_with_rag(question=question, top_k=5)

        print(f"\n💡 Answer:\n{result['answer']}")
        print(f"\n📊 Stats:")
        print(f"   Tokens used: {result['tokens_used']}")
        print(f"   Cost: ${result['cost_estimate']:.4f}")
        print(f"   Sources used: {len(result['sources'])}")


def example_4_filtered_search():
    """Search with metadata filters"""
    print("\n" + "=" * 80)
    print("EXAMPLE 4: Filtered Search")
    print("=" * 80)

    rag = FinancialRAGSystem()

    # Search only Infosys documents
    print("\n🔍 Searching only Infosys documents...")
    results = rag.search(
        query="revenue growth",
        top_k=3,
        filters={'company': 'Infosys'}
    )

    for i, result in enumerate(results, 1):
        print(f"\n[{i}] Score: {result['score']:.3f}")
        print(f"    {result['text'][:200]}...")


def example_5_compare_documents():
    """Compare metrics across multiple documents"""
    print("\n" + "=" * 80)
    print("EXAMPLE 5: Multi-Document Comparison")
    print("=" * 80)

    rag = FinancialRAGSystem()

    comparison = rag.compare_documents(
        question="Compare the revenue and profitability across different periods",
        doc_filters=[
            {'company': 'Infosys'},
            {'company': 'SYNTHECORP'}
        ]
    )

    print(f"\n📊 Comparison Analysis:\n{comparison['analysis']}")
    print(f"\nTokens used: {comparison['tokens_used']}")


def example_6_multi_document_trend():
    """Analyze trends across multiple quarterly reports"""
    print("\n" + "=" * 80)
    print("EXAMPLE 6: Trend Analysis")
    print("=" * 80)

    rag = FinancialRAGSystem()

    # If you have Q1, Q2, Q3 reports, you can analyze trends
    question = """
    Analyze the trend in key financial metrics across quarters.
    What patterns or changes do you observe?
    """

    result = rag.ask_with_rag(question=question, top_k=10)

    print(f"\n📈 Trend Analysis:\n{result['answer']}")


def example_7_cloud_qdrant():
    """Use Qdrant Cloud instead of local storage"""
    print("\n" + "=" * 80)
    print("EXAMPLE 7: Using Qdrant Cloud")
    print("=" * 80)

    # To use Qdrant Cloud:
    # 1. Sign up at https://cloud.qdrant.io/
    # 2. Create a cluster
    # 3. Get your URL and API key
    # 4. Add to .env file:
    #    QDRANT_URL=https://your-cluster.qdrant.io
    #    QDRANT_API_KEY=your_api_key

    qdrant_url = os.getenv('QDRANT_URL')
    qdrant_api_key = os.getenv('QDRANT_API_KEY')

    if qdrant_url and qdrant_api_key:
        rag = FinancialRAGSystem(
            use_cloud=True,
            qdrant_url=qdrant_url,
            qdrant_api_key=qdrant_api_key
        )
        print("✅ Connected to Qdrant Cloud")
        stats = rag.get_collection_stats()
        print(f"   Total chunks: {stats['total_chunks']}")
    else:
        print("ℹ️  Qdrant Cloud credentials not found in .env")
        print("   Using local storage instead")


if __name__ == '__main__':
    import sys

    examples = {
        '1': ('Add documents to vector store', example_1_add_documents),
        '2': ('Semantic search', example_2_semantic_search),
        '3': ('Q&A with RAG', example_3_rag_qa),
        '4': ('Filtered search', example_4_filtered_search),
        '5': ('Multi-document comparison', example_5_compare_documents),
        '6': ('Trend analysis', example_6_multi_document_trend),
        '7': ('Qdrant Cloud setup', example_7_cloud_qdrant),
        'all': ('Run all examples', None)
    }

    if len(sys.argv) > 1:
        choice = sys.argv[1]
    else:
        print("\n📚 RAG System Examples:")
        print("=" * 80)
        for key, (desc, _) in examples.items():
            if key != 'all':
                print(f"  {key}. {desc}")
        print(f"  all. Run all examples")
        print("\nUsage: python example_rag_usage.py [example_number]")
        print("Example: python example_rag_usage.py 1")
        sys.exit(0)

    if choice == 'all':
        for key, (desc, func) in examples.items():
            if key != 'all' and func:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ Error in example {key}: {e}")
    elif choice in examples and examples[choice][1]:
        examples[choice][1]()
    else:
        print(f"Invalid choice: {choice}")
        sys.exit(1)

    print("\n" + "=" * 80)
    print("✅ Examples completed!")
    print("=" * 80)
