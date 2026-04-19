"""
Enhanced Document Ingestion with LlamaParse + LlamaIndex
For complex PDFs like annual reports, multi-column layouts, scanned docs
"""

import os
from typing import Dict, List, Optional
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Try to import LlamaParse/LlamaIndex (optional dependencies)
LLAMAPARSE_AVAILABLE = False
LLAMAINDEX_AVAILABLE = False

try:
    from llama_parse import LlamaParse
    LLAMAPARSE_AVAILABLE = True
except ImportError:
    print("⚠️  LlamaParse not installed. Install: pip install llama-parse")

try:
    from llama_index.core import VectorStoreIndex, Document, Settings
    from llama_index.core.node_parser import SentenceSplitter
    from llama_index.embeddings.huggingface import HuggingFaceEmbedding
    LLAMAINDEX_AVAILABLE = True

    # Use local embedding model (free, no API key needed)
    Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
except ImportError:
    print("⚠️  LlamaIndex not installed. Install: pip install llama-index llama-index-embeddings-huggingface")

# Fallback to PyPDF2
try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


class EnhancedDocumentParser:
    """
    Enhanced document parser that can handle:
    - Complex annual reports
    - Multi-column layouts
    - Scanned PDFs (with OCR)
    - Complex tables
    - Charts/images (with vision models)
    """

    def __init__(self, pdf_path: str, use_llamaparse: bool = True):
        """
        Initialize parser

        Args:
            pdf_path: Path to PDF document
            use_llamaparse: Use LlamaParse if available, else fallback to PyPDF2
        """
        self.pdf_path = pdf_path
        self.use_llamaparse = use_llamaparse and LLAMAPARSE_AVAILABLE
        self.raw_text = ""
        self.structured_data = {}
        self.index = None  # LlamaIndex vector index

    def parse(self, return_index: bool = False) -> Dict:
        """
        Parse document with best available method

        Args:
            return_index: If True, creates LlamaIndex for semantic search

        Returns:
            Structured document data
        """
        print(f"📄 Parsing document: {self.pdf_path}")

        if self.use_llamaparse:
            print("🚀 Using LlamaParse (enhanced parsing)")
            self._parse_with_llamaparse()
        elif PYPDF2_AVAILABLE:
            print("📦 Using PyPDF2 (basic parsing)")
            self._parse_with_pypdf2()
        else:
            raise RuntimeError("No PDF parser available! Install llama-parse or pypdf2")

        # Extract structured information
        self.structured_data = {
            "raw_text": self.raw_text,
            "document_type": self._identify_document_type(),
            "metadata": self._extract_metadata(),
            "parser_used": "llamaparse" if self.use_llamaparse else "pypdf2"
        }

        # Create LlamaIndex for semantic search (optional)
        if return_index and LLAMAINDEX_AVAILABLE:
            print("🔍 Creating search index...")
            self._create_index()

        print(f"✓ Extracted {len(self.raw_text):,} characters")
        print(f"✓ Document type: {self.structured_data['document_type']}")

        return self.structured_data

    def _parse_with_llamaparse(self):
        """Parse with LlamaParse (premium parsing)"""
        try:
            # Initialize LlamaParse
            parser = LlamaParse(
                api_key=os.getenv("LLAMA_CLOUD_API_KEY"),
                result_type="markdown",  # Get markdown output for better structure
                verbose=True,
                language="en",
                premium_mode=True,  # Better for complex layouts
            )

            # Parse document
            documents = parser.load_data(self.pdf_path)

            # Combine all pages
            self.raw_text = "\n\n".join([doc.text for doc in documents])

            # Store additional metadata from LlamaParse
            if documents:
                self.structured_data["pages"] = len(documents)
                self.structured_data["llamaparse_metadata"] = documents[0].metadata

        except Exception as e:
            print(f"❌ LlamaParse failed: {e}")
            print("⚠️  Falling back to PyPDF2...")
            self._parse_with_pypdf2()

    def _parse_with_pypdf2(self):
        """Fallback to basic PyPDF2 parsing"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                self.raw_text = text
                self.structured_data["pages"] = len(pdf_reader.pages)
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            self.raw_text = ""

    def _create_index(self):
        """Create LlamaIndex vector index for semantic search"""
        if not self.raw_text:
            return

        # Split into chunks
        splitter = SentenceSplitter(chunk_size=1024, chunk_overlap=200)
        documents = [Document(text=self.raw_text)]

        # Create index
        self.index = VectorStoreIndex.from_documents(
            documents,
            transformations=[splitter]
        )

        print("✓ Search index created")

    def query(self, question: str) -> str:
        """
        Query the document using semantic search

        Args:
            question: Natural language question

        Returns:
            Answer based on document content
        """
        if not self.index:
            return "Error: Index not created. Call parse(return_index=True) first."

        query_engine = self.index.as_query_engine()
        response = query_engine.query(question)
        return str(response)

    def _identify_document_type(self) -> str:
        """Identify document type from content"""
        text_lower = self.raw_text.lower()

        # Annual Report indicators
        if any(phrase in text_lower for phrase in [
            "annual report", "10-k", "10k", "form 10-k",
            "consolidated financial statements", "management discussion",
            "dear shareholders"
        ]):
            return "Annual Report"

        # SAP indicators
        if any(phrase in text_lower for phrase in [
            "trial balance", "t/b", "profit and loss", "p&l",
            "cost center", "company code", "gl account"
        ]):
            return "SAP FI/CO Report"

        # Other financial documents
        if "balance sheet" in text_lower and "income statement" in text_lower:
            return "Financial Statements"

        if "earnings" in text_lower and ("quarter" in text_lower or "quarterly" in text_lower):
            return "Quarterly Earnings Report"

        if "investor presentation" in text_lower or "earnings call" in text_lower:
            return "Investor Presentation"

        return "Unknown Financial Document"

    def _extract_metadata(self) -> Dict:
        """Extract metadata from document"""
        metadata = {}

        text = self.raw_text.lower()

        # Company name (common patterns)
        import re

        # Fiscal year
        year_match = re.search(r'fiscal year (\d{4})', text, re.IGNORECASE)
        if not year_match:
            year_match = re.search(r'year ended.*?(\d{4})', text, re.IGNORECASE)
        if not year_match:
            year_match = re.search(r'(20\d{2})', text)

        if year_match:
            metadata['fiscal_year'] = year_match.group(1)

        # Quarter
        quarter_match = re.search(r'q([1-4])\s+(\d{4})', text, re.IGNORECASE)
        if quarter_match:
            metadata['quarter'] = f"Q{quarter_match.group(1)}"
            metadata['year'] = quarter_match.group(2)

        # Currency mentions
        currencies = ['USD', 'EUR', 'GBP', 'JPY', 'INR']
        for curr in currencies:
            if curr.lower() in text:
                metadata['currency'] = curr
                break

        # Document pages
        if 'pages' in self.structured_data:
            metadata['pages'] = self.structured_data['pages']

        return metadata

    def to_json(self, output_path: str = None) -> str:
        """Export to JSON"""
        json_data = json.dumps(self.structured_data, indent=2, default=str)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(json_data)
            print(f"✓ Saved JSON to: {output_path}")

        return json_data


class AnnualReportAnalyzer:
    """Specialized analyzer for annual reports"""

    def __init__(self, pdf_path: str):
        self.parser = EnhancedDocumentParser(pdf_path, use_llamaparse=True)
        self.data = None

    def analyze(self) -> Dict:
        """Analyze annual report"""
        print("\n" + "="*60)
        print("📊 Annual Report Analysis")
        print("="*60 + "\n")

        # Parse with indexing enabled
        self.data = self.parser.parse(return_index=True)

        # Extract key sections
        analysis = {
            "document_info": {
                "type": self.data.get("document_type"),
                "pages": self.data.get("metadata", {}).get("pages"),
                "year": self.data.get("metadata", {}).get("fiscal_year"),
            },
            "key_sections": self._extract_key_sections(),
        }

        return analysis

    def _extract_key_sections(self) -> Dict:
        """Extract key sections using semantic search"""
        if not self.parser.index:
            return {}

        sections = {}

        # Define sections to extract
        queries = {
            "financial_highlights": "What are the financial highlights and key metrics?",
            "revenue_analysis": "What were the revenue results and year-over-year changes?",
            "profitability": "What were the profit margins and profitability metrics?",
            "risks": "What are the key risk factors mentioned?",
            "outlook": "What is the business outlook and future guidance?",
        }

        for section_name, query in queries.items():
            try:
                response = self.parser.query(query)
                sections[section_name] = response
            except Exception as e:
                sections[section_name] = f"Error: {e}"

        return sections

    def ask(self, question: str) -> str:
        """Ask a question about the annual report"""
        if not self.parser.index:
            return "Error: Document not indexed. Call analyze() first."

        return self.parser.query(question)


# Example usage
if __name__ == "__main__":
    import sys

    print("Enhanced Document Parser with LlamaParse + LlamaIndex")
    print()

    if len(sys.argv) > 1:
        pdf_path = sys.argv[1]

        # Basic parsing
        parser = EnhancedDocumentParser(pdf_path)
        data = parser.parse(return_index=True)
        parser.to_json("enhanced_output.json")

        # If it's an annual report, do specialized analysis
        if "annual report" in data["document_type"].lower():
            print("\n📈 Detected annual report - running specialized analysis...\n")
            analyzer = AnnualReportAnalyzer(pdf_path)
            analysis = analyzer.analyze()

            # Example queries
            print("\n💬 Example: Ask questions about the document:")
            print("-" * 60)

            questions = [
                "What were the total revenues?",
                "What is the company's strategy?",
                "What are the biggest risks?"
            ]

            for q in questions:
                print(f"\nQ: {q}")
                answer = analyzer.ask(q)
                print(f"A: {answer[:200]}...")

    else:
        print("Usage:")
        print("  python document_ingestion_enhanced.py <path_to_pdf>")
        print()
        print("Requirements:")
        print("  pip install llama-parse llama-index pypdf2")
        print()
        print("Environment:")
        print("  LLAMA_CLOUD_API_KEY=your_key  # Get from https://cloud.llamaindex.ai")
