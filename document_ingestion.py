"""
Document Ingestion Layer
Parses SAP FI/CO PDF reports using PyPDF2
"""

import PyPDF2
import re
from typing import Dict, List
import json


class SAPDocumentParser:
    """Parse SAP FI/CO PDF documents and extract structured data"""

    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.raw_text = ""
        self.structured_data = {}

    def parse(self) -> Dict:
        """Main parsing method"""
        print(f"📄 Parsing document: {self.pdf_path}")

        # Extract text from PDF
        self.raw_text = self._extract_text()

        # Extract structured information
        self.structured_data = {
            "raw_text": self.raw_text,
            "document_type": self._identify_document_type(),
            "tables": self._extract_tables(),
            "metadata": self._extract_metadata()
        }

        print(f"✓ Extracted {len(self.raw_text)} characters")
        print(f"✓ Document type: {self.structured_data['document_type']}")
        print(f"✓ Found {len(self.structured_data['tables'])} table sections")

        return self.structured_data

    def _extract_text(self) -> str:
        """Extract raw text from PDF"""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"❌ Error reading PDF: {e}")
            return ""

    def _identify_document_type(self) -> str:
        """Identify the type of SAP FI/CO document"""
        text_lower = self.raw_text.lower()

        if "trial balance" in text_lower or "t/b" in text_lower:
            return "Trial Balance"
        elif "profit and loss" in text_lower or "p&l" in text_lower or "income statement" in text_lower:
            return "Profit & Loss"
        elif "balance sheet" in text_lower or "b/s" in text_lower:
            return "Balance Sheet"
        elif "cost center" in text_lower:
            return "Cost Center Report"
        elif "variance" in text_lower:
            return "Variance Report"
        elif "gl account" in text_lower or "general ledger" in text_lower:
            return "GL Account Report"
        else:
            return "Unknown SAP FI Report"

    def _extract_tables(self) -> List[str]:
        """Extract table sections from the document"""
        # Simple table extraction - splits on double newlines
        # In production, use more sophisticated table detection
        tables = []
        sections = self.raw_text.split('\n\n')

        for section in sections:
            # Look for sections that appear to be tables (multiple columns of data)
            lines = section.strip().split('\n')
            if len(lines) >= 3:  # At least header + 2 rows
                # Check if lines have consistent structure (numbers, multiple columns)
                if any(re.search(r'\d+[,\.]?\d*', line) for line in lines):
                    tables.append(section)

        return tables

    def _extract_metadata(self) -> Dict:
        """Extract metadata like company code, period, etc."""
        metadata = {}

        # Extract company code
        company_match = re.search(r'company\s+code[:\s]+(\d+)', self.raw_text, re.IGNORECASE)
        if company_match:
            metadata['company_code'] = company_match.group(1)

        # Extract fiscal year/period
        period_match = re.search(r'period[:\s]+(\d+)[/\-](\d{4})', self.raw_text, re.IGNORECASE)
        if period_match:
            metadata['period'] = period_match.group(1)
            metadata['fiscal_year'] = period_match.group(2)

        # Extract currency
        currency_match = re.search(r'currency[:\s]+([A-Z]{3})', self.raw_text, re.IGNORECASE)
        if currency_match:
            metadata['currency'] = currency_match.group(1)

        return metadata

    def to_json(self, output_path: str = None) -> str:
        """Export structured data to JSON"""
        json_data = json.dumps(self.structured_data, indent=2)

        if output_path:
            with open(output_path, 'w') as f:
                f.write(json_data)
            print(f"✓ Saved JSON to: {output_path}")

        return json_data


if __name__ == "__main__":
    # Test with a sample PDF
    import sys

    if len(sys.argv) > 1:
        parser = SAPDocumentParser(sys.argv[1])
        data = parser.parse()
        parser.to_json("output.json")
    else:
        print("Usage: python document_ingestion.py <pdf_path>")
