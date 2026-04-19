"""
Quick RAG Demo - Run this to see RAG in action!
Works without any additional dependencies beyond qdrant-client
"""

import os
import sys

def main():
    print("=" * 80)
    print("SAP FI/CO RAG System Demo")
    print("=" * 80)

    # Check if qdrant-client is installed
    try:
        import qdrant_client
    except ImportError:
        print("\n❌ Missing dependency: qdrant-client")
        print("\nInstall it with:")
        print("  pip3 install qdrant-client")
        sys.exit(1)

    # Check if python-dotenv is installed
    try:
        import dotenv
    except ImportError:
        print("\n❌ Missing dependency: python-dotenv")
        print("\nInstall it with:")
        print("  pip3 install python-dotenv")
        sys.exit(1)

    # Check if anthropic is installed
    try:
        import anthropic
    except ImportError:
        print("\n❌ Missing dependency: anthropic")
        print("\nInstall it with:")
        print("  pip3 install anthropic")
        sys.exit(1)

    # Check ANTHROPIC_API_KEY
    from dotenv import load_dotenv
    load_dotenv()

    if not os.getenv('ANTHROPIC_API_KEY'):
        print("\n❌ ANTHROPIC_API_KEY not found in .env file")
        print("\nPlease add your API key to .env:")
        print("  ANTHROPIC_API_KEY=your_key_here")
        sys.exit(1)

    print("\n✅ All dependencies installed!")
    print("✅ ANTHROPIC_API_KEY found!")

    # Import and run the RAG system
    from rag_system_simple import SimpleFinancialRAGSystem
    from document_ingestion import SAPDocumentParser

    print("\n" + "=" * 80)
    print("Step 1: Initialize RAG System")
    print("=" * 80)

    rag = SimpleFinancialRAGSystem(
        collection_name="financial_demo",
        qdrant_path="./qdrant_storage"
    )

    print("\n" + "=" * 80)
    print("Step 2: Add Infosys Q3 Report")
    print("=" * 80)

    try:
        parser = SAPDocumentParser('samples/q3-2026-inf.pdf')
        parsed = parser.parse()

        num_chunks = rag.add_document(
            text=parsed['raw_text'],
            metadata={
                'company': 'Infosys',
                'period': 'Q3 2026',
                'document_type': 'Quarterly Report'
            }
        )
        print(f"\n✅ Added {num_chunks} chunks from Infosys Q3 report")
    except FileNotFoundError:
        print("⚠️  Sample file not found. Make sure you're in the project directory.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

    print("\n" + "=" * 80)
    print("Step 3: Ask Questions with RAG")
    print("=" * 80)

    questions = [
        "What are the key financial metrics in this report?",
        "What information is available about revenue?",
    ]

    for i, question in enumerate(questions, 1):
        print(f"\n[Question {i}] {question}")
        print("-" * 80)

        try:
            result = rag.ask_with_rag(question, top_k=3)
            print(f"\n{result['answer']}")
            print(f"\n📊 Tokens used: {result['tokens_used']} | Cost: ${result['cost_estimate']:.4f}")
        except Exception as e:
            print(f"❌ Error: {e}")
            import traceback
            traceback.print_exc()

    print("\n" + "=" * 80)
    print("✅ Demo Complete!")
    print("=" * 80)
    print("\nNext steps:")
    print("  1. Add more documents: rag.add_document(...)")
    print("  2. Try semantic search: rag.search('revenue growth')")
    print("  3. Compare documents: rag.compare_documents(...)")
    print("  4. See full examples: python3 example_rag_usage.py")
    print("\nDocumentation: Read RAG_GUIDE.md")


if __name__ == '__main__':
    main()
