"""
Simple RAG test - works without PyTorch
Uses Voyage embeddings or keyword fallback
"""

from rag_system_simple import SimpleFinancialRAGSystem
from document_ingestion import SAPDocumentParser


def test_rag():
    """Test RAG system with sample documents"""
    print("=" * 80)
    print("Testing Simple RAG System")
    print("=" * 80)

    # Initialize RAG
    rag = SimpleFinancialRAGSystem(
        collection_name="financial_reports_test",
        qdrant_path="./qdrant_storage"
    )

    # Clear any existing data
    print("\n🗑️  Clearing existing data...")
    try:
        rag.clear_collection()
    except:
        pass

    # Parse and add Infosys Q3 report
    print("\n" + "=" * 80)
    print("Adding Infosys Q3 2026 Report")
    print("=" * 80)

    try:
        parser = SAPDocumentParser('samples/q3-2026-inf.pdf')
        parsed = parser.parse()
        num_chunks = rag.add_document(
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
        print(f"✅ Added {num_chunks} chunks")
    except Exception as e:
        print(f"❌ Error adding Infosys report: {e}")
        return

    # Add SAP variance report
    print("\n" + "=" * 80)
    print("Adding SAP Variance Report")
    print("=" * 80)

    try:
        parser = SAPDocumentParser('samples/sap_variance_report.pdf')
        parsed = parser.parse()
        num_chunks = rag.add_document(
            text=parsed['raw_text'],
            metadata={
                'company': 'SYNTHECORP',
                'period': 'Q1 FY2526',
                'document_type': 'SAP Variance Report',
                'fiscal_year': '2526'
            },
            chunk_size=1000,
            overlap=200
        )
        print(f"✅ Added {num_chunks} chunks")
    except Exception as e:
        print(f"❌ Error adding SAP report: {e}")

    # Show stats
    stats = rag.get_collection_stats()
    print(f"\n📊 Collection Stats:")
    print(f"   Total chunks: {stats['total_chunks']}")
    print(f"   Vector dimension: {stats['vector_dimension']}")

    # Test semantic search
    print("\n" + "=" * 80)
    print("Testing Semantic Search")
    print("=" * 80)

    queries = [
        "What is the revenue?",
        "Any cost overruns or variances?",
    ]

    for query in queries:
        print(f"\n🔍 Query: {query}")
        try:
            results = rag.search(query=query, top_k=2)
            for i, result in enumerate(results, 1):
                metadata = result['metadata']
                print(f"\n  [{i}] {metadata.get('company')} - {metadata.get('period')}")
                print(f"      Score: {result['score']:.3f}")
                print(f"      Text: {result['text'][:150]}...")
        except Exception as e:
            print(f"   ❌ Search failed: {e}")

    # Test RAG Q&A
    print("\n" + "=" * 80)
    print("Testing RAG Q&A with Claude")
    print("=" * 80)

    questions = [
        "What was Infosys revenue in Q3 2026?",
        "What are the key financial highlights?"
    ]

    for question in questions:
        print(f"\n❓ Question: {question}")
        print("-" * 80)

        try:
            result = rag.ask_with_rag(question=question, top_k=3)
            print(f"\n💡 Answer:\n{result['answer']}")
            print(f"\n📊 Stats:")
            print(f"   Tokens: {result['tokens_used']}")
            print(f"   Cost: ${result['cost_estimate']:.4f}")
            print(f"   Sources: {len(result['sources'])}")
        except Exception as e:
            print(f"   ❌ Q&A failed: {e}")
            import traceback
            traceback.print_exc()

    # Test filtered search
    print("\n" + "=" * 80)
    print("Testing Filtered Search (Infosys only)")
    print("=" * 80)

    try:
        results = rag.search(
            query="revenue",
            top_k=2,
            filters={'company': 'Infosys'}
        )
        print(f"Found {len(results)} results from Infosys")
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] Score: {result['score']:.3f}")
            print(f"    {result['text'][:150]}...")
    except Exception as e:
        print(f"❌ Filtered search failed: {e}")

    print("\n" + "=" * 80)
    print("✅ RAG System Test Complete!")
    print("=" * 80)


if __name__ == '__main__':
    test_rag()
