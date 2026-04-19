"""
SAP FI/CO Agent - Main Pipeline
End-to-end orchestration of document ingestion → agent analysis → output generation
"""

import sys
import os
from document_ingestion import SAPDocumentParser
from agents import ParallelAgentOrchestrator
from output_generator import OutputGenerator


def main(pdf_path: str):
    """
    Main pipeline execution

    Args:
        pdf_path: Path to SAP FI/CO PDF document
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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_sap_pdf>")
        print()
        print("Example:")
        print("  python main.py samples/sap_trial_balance.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    main(pdf_path)
