"""
Annual Report Analyzer
Specialized tool for analyzing company annual reports (10-K, 10-Q, etc.)
Uses LlamaParse for superior parsing + Claude for analysis
"""

import sys
import os
import json
from dotenv import load_dotenv

load_dotenv()

# Check if enhanced dependencies are available
try:
    from document_ingestion_enhanced import EnhancedDocumentParser
    ENHANCED_AVAILABLE = True
except ImportError:
    ENHANCED_AVAILABLE = False
    print("⚠️  Enhanced parsing not available. Install: pip install llama-parse llama-index")

from agents import SAPAnalysisAgent
from interactive_qa import SAPDataQA
from output_generator import OutputGenerator


class AnnualReportAgent(SAPAnalysisAgent):
    """Specialized agent for annual report analysis"""

    AGENT_PROMPT = """
## Your Role: Annual Report Analyst

Analyze this company annual report (10-K, 10-Q, or annual filing) and provide comprehensive insights.

Focus on:

1. **Financial Performance**
   - Revenue, profit, margins
   - Year-over-year growth rates
   - Segment performance
   - Key metrics and KPIs

2. **Business Strategy**
   - Strategic initiatives
   - Competitive positioning
   - Market opportunities
   - Future outlook

3. **Risk Assessment**
   - Major risk factors
   - Operational risks
   - Market risks
   - Financial risks

4. **Management Discussion**
   - Key management commentary
   - Forward-looking statements
   - Capital allocation priorities

5. **Red Flags & Concerns**
   - Declining metrics
   - Unusual items
   - Going concern issues
   - Litigation or regulatory issues

Return comprehensive analysis in this JSON structure:
```json
{
  "company_overview": {
    "name": "Company name",
    "fiscal_year": "2024",
    "report_type": "10-K / Annual Report",
    "industry": "Industry/sector"
  },
  "financial_highlights": {
    "revenue": "Total revenue with YoY change",
    "net_income": "Net income with YoY change",
    "eps": "Earnings per share",
    "gross_margin": "Percentage",
    "operating_margin": "Percentage",
    "net_margin": "Percentage"
  },
  "business_segments": [
    {
      "segment_name": "Segment name",
      "revenue": "Revenue amount",
      "performance": "How it performed"
    }
  ],
  "key_strengths": [
    "Strength 1",
    "Strength 2",
    "Strength 3"
  ],
  "key_risks": [
    "Risk 1",
    "Risk 2",
    "Risk 3"
  ],
  "management_outlook": "Summary of management's forward-looking statements",
  "investment_perspective": "Is this a good/bad investment opportunity and why?",
  "red_flags": [
    "Any concerning items"
  ],
  "overall_assessment": "2-3 sentence overall company health assessment"
}
```
"""

    def analyze_annual_report(self, document_data: dict) -> dict:
        """Analyze annual report"""
        print("📊 Analyzing annual report...")
        result = self.analyze(document_data, self.AGENT_PROMPT)

        if result["success"]:
            try:
                content = result["content"]
                # Extract JSON from markdown code blocks
                if "```json" in content:
                    json_start = content.find("```json") + 7
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                elif "```" in content:
                    json_start = content.find("```") + 3
                    json_end = content.find("```", json_start)
                    json_str = content[json_start:json_end].strip()
                else:
                    json_str = content

                parsed = json.loads(json_str)
                result["parsed_output"] = parsed
                print("✓ Annual report analysis complete")
            except json.JSONDecodeError:
                result["parsed_output"] = {"raw_response": content}
                print("⚠ Could not parse JSON response")

        return result


def analyze_annual_report(pdf_path: str, interactive: bool = False):
    """
    Main analysis function for annual reports

    Args:
        pdf_path: Path to annual report PDF
        interactive: Enable Q&A mode after analysis
    """
    print("="*70)
    print("📈 Annual Report Analyzer")
    print("="*70)
    print()

    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"❌ Error: File not found: {pdf_path}")
        return

    # Step 1: Enhanced Document Parsing
    print("📥 STEP 1: Document Parsing (Enhanced)")
    print("-" * 70)

    if ENHANCED_AVAILABLE:
        parser = EnhancedDocumentParser(pdf_path, use_llamaparse=True)
        document_data = parser.parse(return_index=True)
    else:
        print("⚠️  Falling back to basic parsing (install llama-parse for better results)")
        from document_ingestion import SAPDocumentParser
        parser = SAPDocumentParser(pdf_path)
        document_data = parser.parse()

    # Save parsed document
    parser.to_json("annual_report_parsed.json")
    print()

    # Step 2: AI Analysis
    print("🤖 STEP 2: AI-Powered Analysis")
    print("-" * 70)

    agent = AnnualReportAgent()
    analysis_result = agent.analyze_annual_report(document_data)

    # Combine results
    results = {
        "annual_report_analysis": analysis_result,
        "metadata": {
            "document_type": document_data.get("document_type"),
            "parser_used": document_data.get("parser_used", "unknown"),
            "pages": document_data.get("metadata", {}).get("pages"),
        }
    }

    if analysis_result.get("usage"):
        results["total_usage"] = analysis_result["usage"]

    print()

    # Step 3: Generate Output
    print("📤 STEP 3: Output Generation")
    print("-" * 70)

    # Save JSON
    with open("annual_report_analysis.json", 'w') as f:
        json.dump(results, f, indent=2)
    print("✓ Analysis saved to: annual_report_analysis.json")

    # Generate summary report
    generate_summary_report(results, "annual_report_summary.txt")
    print("✓ Summary saved to: annual_report_summary.txt")

    print()

    # Print key findings
    print("="*70)
    print("📊 KEY FINDINGS")
    print("="*70)

    if analysis_result.get("parsed_output"):
        output = analysis_result["parsed_output"]

        if output.get("company_overview"):
            overview = output["company_overview"]
            print(f"\n🏢 Company: {overview.get('name', 'N/A')}")
            print(f"📅 Fiscal Year: {overview.get('fiscal_year', 'N/A')}")
            print(f"📄 Report Type: {overview.get('report_type', 'N/A')}")

        if output.get("financial_highlights"):
            print("\n💰 Financial Highlights:")
            for key, value in output["financial_highlights"].items():
                print(f"  • {key.replace('_', ' ').title()}: {value}")

        if output.get("key_strengths"):
            print("\n✅ Key Strengths:")
            for strength in output["key_strengths"][:3]:
                print(f"  • {strength}")

        if output.get("key_risks"):
            print("\n⚠️  Key Risks:")
            for risk in output["key_risks"][:3]:
                print(f"  • {risk}")

        if output.get("overall_assessment"):
            print(f"\n📝 Overall Assessment:")
            print(f"  {output['overall_assessment']}")

    print()
    print("="*70)

    # Step 4: Interactive Q&A
    if interactive:
        print()
        print("💬 STEP 4: Interactive Q&A Mode")
        print("-" * 70)
        print("Ask questions about the annual report.")
        print("Type 'exit' to quit, 'reset' to clear history.")
        print()

        qa_system = SAPDataQA(document_data, results)

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
                    print("-" * 70)
                    print(result['answer'])
                    print("-" * 70)
                    print(f"📊 Tokens: {result['usage']['total_tokens']:,}")
                else:
                    print(f"❌ Error: {result['error']}")

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def generate_summary_report(results: dict, output_path: str):
    """Generate human-readable summary report"""

    output = results.get("annual_report_analysis", {}).get("parsed_output", {})

    report = []
    report.append("="*70)
    report.append("ANNUAL REPORT ANALYSIS SUMMARY")
    report.append("="*70)
    report.append("")

    # Company Overview
    if output.get("company_overview"):
        overview = output["company_overview"]
        report.append("COMPANY OVERVIEW")
        report.append("-"*70)
        report.append(f"Company:      {overview.get('name', 'N/A')}")
        report.append(f"Fiscal Year:  {overview.get('fiscal_year', 'N/A')}")
        report.append(f"Report Type:  {overview.get('report_type', 'N/A')}")
        report.append(f"Industry:     {overview.get('industry', 'N/A')}")
        report.append("")

    # Financial Highlights
    if output.get("financial_highlights"):
        report.append("FINANCIAL HIGHLIGHTS")
        report.append("-"*70)
        for key, value in output["financial_highlights"].items():
            report.append(f"{key.replace('_', ' ').title():20} {value}")
        report.append("")

    # Business Segments
    if output.get("business_segments"):
        report.append("BUSINESS SEGMENTS")
        report.append("-"*70)
        for segment in output["business_segments"]:
            report.append(f"\n{segment.get('segment_name', 'N/A')}")
            report.append(f"  Revenue: {segment.get('revenue', 'N/A')}")
            report.append(f"  Performance: {segment.get('performance', 'N/A')}")
        report.append("")

    # Key Strengths
    if output.get("key_strengths"):
        report.append("KEY STRENGTHS")
        report.append("-"*70)
        for i, strength in enumerate(output["key_strengths"], 1):
            report.append(f"{i}. {strength}")
        report.append("")

    # Key Risks
    if output.get("key_risks"):
        report.append("KEY RISKS")
        report.append("-"*70)
        for i, risk in enumerate(output["key_risks"], 1):
            report.append(f"{i}. {risk}")
        report.append("")

    # Management Outlook
    if output.get("management_outlook"):
        report.append("MANAGEMENT OUTLOOK")
        report.append("-"*70)
        report.append(output["management_outlook"])
        report.append("")

    # Investment Perspective
    if output.get("investment_perspective"):
        report.append("INVESTMENT PERSPECTIVE")
        report.append("-"*70)
        report.append(output["investment_perspective"])
        report.append("")

    # Red Flags
    if output.get("red_flags") and len(output["red_flags"]) > 0:
        report.append("RED FLAGS / CONCERNS")
        report.append("-"*70)
        for i, flag in enumerate(output["red_flags"], 1):
            report.append(f"{i}. {flag}")
        report.append("")

    # Overall Assessment
    if output.get("overall_assessment"):
        report.append("OVERALL ASSESSMENT")
        report.append("-"*70)
        report.append(output["overall_assessment"])
        report.append("")

    report.append("="*70)
    report.append("End of Report")
    report.append("="*70)

    # Write to file
    with open(output_path, 'w') as f:
        f.write("\n".join(report))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Annual Report Analyzer")
        print()
        print("Usage:")
        print("  python3 analyze_annual_report.py <annual_report.pdf> [--interactive]")
        print()
        print("Options:")
        print("  --interactive, -i    Enable Q&A mode after analysis")
        print()
        print("Examples:")
        print("  python3 analyze_annual_report.py apple_10k_2024.pdf")
        print("  python3 analyze_annual_report.py tesla_10k.pdf --interactive")
        print()
        print("Requirements:")
        print("  pip install llama-parse llama-index anthropic python-dotenv")
        print()
        print("Get annual reports from:")
        print("  • SEC EDGAR: https://www.sec.gov/edgar")
        print("  • Company investor relations pages")
        sys.exit(1)

    pdf_path = sys.argv[1]
    interactive = '--interactive' in sys.argv or '-i' in sys.argv

    analyze_annual_report(pdf_path, interactive)
