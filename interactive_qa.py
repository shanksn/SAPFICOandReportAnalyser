"""
Interactive Q&A Mode for SAP FI/CO Analysis
Ask natural language questions about your analyzed financial data
"""

import anthropic
import json
import os
from dotenv import load_dotenv
from config import CLAUDE_MODEL, SAP_FI_CONTEXT

load_dotenv()


class SAPDataQA:
    """Interactive question-answering for SAP FI/CO data"""

    def __init__(self, document_data: dict, analysis_results: dict = None):
        """
        Initialize QA system with analyzed data

        Args:
            document_data: Parsed document from document_ingestion.py
            analysis_results: Optional pre-computed agent analysis
        """
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = CLAUDE_MODEL
        self.document_data = document_data
        self.analysis_results = analysis_results
        self.conversation_history = []

    def ask(self, question: str) -> dict:
        """
        Ask a question about the SAP data

        Args:
            question: Natural language question

        Returns:
            dict with answer and metadata
        """
        # Build context from document and analysis
        context = self._build_context()

        # Create system prompt
        system_prompt = f"""{SAP_FI_CONTEXT}

## Your Role: SAP FI/CO Data Analyst - Interactive Q&A

You are helping a user understand their SAP financial data. Answer questions clearly and concisely.

**Available Data:**
{context}

**Instructions:**
- Answer questions based on the data provided
- Cite specific numbers and GL accounts when relevant
- If asked about trends, calculations, or root causes, provide detailed analysis
- If data is not available, say so clearly
- Use financial terminology appropriately
- Be direct and actionable in your responses
"""

        # Add question to conversation history
        self.conversation_history.append({
            "role": "user",
            "content": question
        })

        try:
            # Call Claude
            response = self.client.messages.create(
                model=self.model,
                max_tokens=2048,
                system=system_prompt,
                messages=self.conversation_history
            )

            answer_text = response.content[0].text

            # Add response to conversation history
            self.conversation_history.append({
                "role": "assistant",
                "content": answer_text
            })

            return {
                "success": True,
                "question": question,
                "answer": answer_text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens,
                    "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                }
            }

        except Exception as e:
            return {
                "success": False,
                "question": question,
                "error": str(e)
            }

    def ask_multiple(self, questions: list) -> list:
        """
        Ask multiple questions in sequence

        Args:
            questions: List of question strings

        Returns:
            List of answer dicts
        """
        answers = []
        for q in questions:
            result = self.ask(q)
            answers.append(result)
        return answers

    def reset_conversation(self):
        """Clear conversation history to start fresh"""
        self.conversation_history = []

    def _build_context(self) -> str:
        """Build context string from available data"""
        context_parts = []

        # Document metadata
        if self.document_data.get("metadata"):
            meta = self.document_data["metadata"]
            context_parts.append(f"""
**Document Metadata:**
- Company Code: {meta.get('company_code', 'N/A')}
- Period: {meta.get('period', 'N/A')}/{meta.get('fiscal_year', 'N/A')}
- Currency: {meta.get('currency', 'N/A')}
- Document Type: {self.document_data.get('document_type', 'N/A')}
""")

        # Raw document content (send more - Claude can handle 200K tokens!)
        # Most financial docs are 10-50K chars, well within limits
        raw_text = self.document_data.get('raw_text', '')[:50000]  # Increased from 4000
        context_parts.append(f"""
**Financial Document Content:**
{raw_text}
""")

        # Analysis results if available
        if self.analysis_results:
            # Add executive summary
            if self.analysis_results.get('executive_summary', {}).get('parsed_output'):
                exec_summary = self.analysis_results['executive_summary']['parsed_output'].get('executive_summary', {})
                if exec_summary.get('headline'):
                    context_parts.append(f"""
**Executive Summary:**
{exec_summary['headline']}
""")

            # Add key anomalies
            if self.analysis_results.get('anomaly_detection', {}).get('parsed_output'):
                anomalies = self.analysis_results['anomaly_detection']['parsed_output']
                if anomalies.get('critical_issues'):
                    context_parts.append(f"""
**Anomalies Detected:** {len(anomalies['critical_issues'])} issues
""")

            # Add variance summary
            if self.analysis_results.get('variance_analysis', {}).get('parsed_output'):
                variances = self.analysis_results['variance_analysis']['parsed_output']
                if variances.get('summary'):
                    context_parts.append(f"""
**Variance Summary:**
{variances['summary']}
""")

        return "\n".join(context_parts)

    def get_conversation_summary(self) -> dict:
        """Get summary of conversation so far"""
        return {
            "total_questions": len([m for m in self.conversation_history if m["role"] == "user"]),
            "conversation_history": self.conversation_history
        }


class InteractiveQASession:
    """Interactive command-line Q&A session"""

    def __init__(self, document_path: str = None, analysis_path: str = None):
        """
        Initialize interactive session

        Args:
            document_path: Path to parsed_document.json
            analysis_path: Path to analysis_results.json (optional)
        """
        self.qa_system = None

        # Load document data
        if document_path and os.path.exists(document_path):
            with open(document_path, 'r') as f:
                document_data = json.load(f)
        else:
            print("⚠️  No document data provided")
            document_data = {}

        # Load analysis results if available
        analysis_results = None
        if analysis_path and os.path.exists(analysis_path):
            with open(analysis_path, 'r') as f:
                loaded = json.load(f)
                # Handle both formats (with/without timestamp wrapper)
                analysis_results = loaded.get('results', loaded)

        self.qa_system = SAPDataQA(document_data, analysis_results)

    def run(self):
        """Run interactive Q&A session"""
        print("="*60)
        print("🤖 SAP FI/CO Interactive Q&A Session")
        print("="*60)
        print()
        print("Ask questions about your SAP financial data.")
        print("Type 'exit' or 'quit' to end the session.")
        print("Type 'reset' to clear conversation history.")
        print("Type 'summary' to see conversation summary.")
        print()

        while True:
            try:
                # Get user question
                question = input("\n💬 Your question: ").strip()

                if not question:
                    continue

                # Handle commands
                if question.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Ending Q&A session. Goodbye!")
                    break

                if question.lower() == 'reset':
                    self.qa_system.reset_conversation()
                    print("🔄 Conversation history cleared.")
                    continue

                if question.lower() == 'summary':
                    summary = self.qa_system.get_conversation_summary()
                    print(f"\n📊 Asked {summary['total_questions']} questions so far")
                    continue

                # Ask the question
                print("\n🔍 Analyzing...\n")
                result = self.qa_system.ask(question)

                if result['success']:
                    print("💡 Answer:")
                    print("-" * 60)
                    print(result['answer'])
                    print("-" * 60)
                    print(f"📊 Tokens: {result['usage']['total_tokens']:,}")
                else:
                    print(f"❌ Error: {result['error']}")

            except KeyboardInterrupt:
                print("\n\n👋 Session interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")


def demo_questions():
    """Demo showing example questions you can ask"""
    print("="*60)
    print("📋 Example Questions You Can Ask")
    print("="*60)
    print()

    examples = [
        "General Understanding:",
        "- What's the overall financial performance this quarter?",
        "- Is the company profitable?",
        "- What are the biggest issues I should be concerned about?",
        "",
        "Specific Deep Dives:",
        "- Why did material costs exceed budget?",
        "- Which operating expenses are over budget and why?",
        "- Explain the revenue variance between actual and budget",
        "- What's driving the margin compression?",
        "",
        "Actionable Insights:",
        "- What immediate actions should management take?",
        "- Which cost centers need attention?",
        "- How can we improve profitability next quarter?",
        "- What are the risks if these trends continue?",
        "",
        "Specific Calculations:",
        "- What's the gross margin percentage?",
        "- Calculate the operating margin",
        "- What's the variance on COGS as a % of revenue?",
        "- How much do we need to cut costs to hit budget?",
        "",
        "Comparative Analysis:",
        "- Which GL accounts have the largest unfavorable variances?",
        "- Is product revenue performing better than services?",
        "- What's the biggest driver of the profit miss?",
        "",
        "Follow-up Questions:",
        "- Can you elaborate on that?",
        "- What's the root cause?",
        "- Show me the numbers",
        "- What's the impact on cash flow?",
    ]

    for example in examples:
        print(example)

    print()
    print("="*60)


if __name__ == "__main__":
    import sys

    # Show examples if no arguments
    if len(sys.argv) == 1:
        demo_questions()
        print("\nUsage:")
        print("  python3 interactive_qa.py <parsed_document.json> [analysis_results.json]")
        print("\nExample:")
        print("  python3 interactive_qa.py parsed_document.json demo_analysis_results.json")
        sys.exit(0)

    # Get file paths
    doc_path = sys.argv[1] if len(sys.argv) > 1 else "parsed_document.json"
    analysis_path = sys.argv[2] if len(sys.argv) > 2 else "demo_analysis_results.json"

    # Run interactive session
    session = InteractiveQASession(doc_path, analysis_path)
    session.run()
