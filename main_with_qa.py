"""
SAP FI/CO Agent - Main Pipeline with Interactive Q&A
End-to-end orchestration + optional interactive mode
"""

import sys
import os
from document_ingestion import SAPDocumentParser
from agents import ParallelAgentOrchestrator
from output_generator import OutputGenerator
from interactive_qa import SAPDataQA


def main(pdf_path: str, interactive: bool = False):
    """
    Main pipeline execution with optional Q&A mode

    Args:
        pdf_path: Path to SAP FI/CO PDF document
        interactive: Enable interactive Q&A after analysis
    """
    print("="*60)
    print("🤖 SAP FI/CO Analysis Agent - POC")
    print("="*60)
    print()

    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return

    # Step 1: Document Ingestion
    print("📥 STEP 1: Document Ingestion")
    print("-" * 60)
    parser = SAPDocumentParser(pdf_path)
    document_data = parser.parse()
    print()

    # Save intermediate JSON
    json_path = "parsed_document.json"
    parser.to_json(json_path)
    print()

    # Step 2: Agent Analysis
    print("🧠 STEP 2: Agent Analysis")
    print("-" * 60)
    orchestrator = ParallelAgentOrchestrator()
    analysis_results = orchestrator.run_all_agents(document_data)
    print()

    # Step 3: Output Generation
    print("📤 STEP 3: Output Generation")
    print("-" * 60)
    generator = OutputGenerator(analysis_results)

    json_output = generator.save_json("analysis_results.json")
    html_output = generator.generate_html_dashboard("dashboard.html")
    print()

    # Summary
    print("="*60)
    print("✅ PIPELINE COMPLETE")
    print("="*60)
    print(f"📄 Parsed Document: {json_path}")
    print(f"📊 Analysis Results: {json_output}")
    print(f"🌐 Dashboard: {html_output}")
    print()
    print(f"💡 Open {html_output} in your browser to view the results")
    print("="*60)

    # Step 4: Interactive Q&A (optional)
    if interactive:
        print()
        print("="*60)
        print("🎯 STEP 4: Interactive Q&A Mode")
        print("="*60)
        print()

        qa_system = SAPDataQA(document_data, analysis_results)

        print("Ask questions about your SAP data.")
        print("Type 'exit' to quit, 'reset' to clear history.")
        print()

        while True:
            try:
                question = input("\n💬 Your question: ").strip()

                if not question:
                    continue

                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Exiting Q&A mode. Goodbye!")
                    break

                if question.lower() == 'reset':
                    qa_system.reset_conversation()
                    print("🔄 Conversation history cleared.")
                    continue

                # Ask the question
                print("\n🔍 Analyzing...\n")
                result = qa_system.ask(question)

                if result['success']:
                    print("💡 Answer:")
                    print("-" * 60)
                    print(result['answer'])
                    print("-" * 60)
                    print(f"📊 Tokens used: {result['usage']['total_tokens']:,}")
                else:
                    print(f"❌ Error: {result['error']}")

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main_with_qa.py <path_to_sap_pdf> [--interactive]")
        print()
        print("Options:")
        print("  --interactive, -i    Enable Q&A mode after analysis")
        print()
        print("Examples:")
        print("  python3 main_with_qa.py samples/sap_variance_report.pdf")
        print("  python3 main_with_qa.py samples/sap_variance_report.pdf --interactive")
        sys.exit(1)

    pdf_path = sys.argv[1]
    interactive = '--interactive' in sys.argv or '-i' in sys.argv

    main(pdf_path, interactive)
