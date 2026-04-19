#!/bin/bash

# Setup script for enhanced SAP FI/CO Agent with LlamaParse + LlamaIndex

echo "================================================================"
echo "SAP FI/CO Agent - Enhanced Setup with LlamaParse + LlamaIndex"
echo "================================================================"
echo ""

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Error: Please run this script from the 'SAP FICO Agent' directory"
    exit 1
fi

echo "📦 Step 1: Installing enhanced dependencies..."
echo "----------------------------------------"

pip install -q llama-parse llama-index llama-index-embeddings-openai

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "🔑 Step 2: Checking API keys..."
echo "----------------------------------------"

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
fi

# Check for Anthropic key
if grep -q "ANTHROPIC_API_KEY=sk-ant-" .env 2>/dev/null; then
    echo "✅ Anthropic API key found"
else
    echo "⚠️  Anthropic API key not found in .env"
    echo "   Please add: ANTHROPIC_API_KEY=sk-ant-your-key-here"
fi

# Check for LlamaIndex key
if grep -q "LLAMA_CLOUD_API_KEY=" .env 2>/dev/null; then
    if grep -q "LLAMA_CLOUD_API_KEY=llx-" .env; then
        echo "✅ LlamaIndex API key found"
    else
        echo "⚠️  LlamaIndex API key appears incomplete"
        echo "   Please update .env with: LLAMA_CLOUD_API_KEY=llx-your-key-here"
    fi
else
    echo "⚠️  LlamaIndex API key not found"
    echo "   Adding placeholder to .env..."
    echo "" >> .env
    echo "# LlamaIndex API Key (get from https://cloud.llamaindex.ai)" >> .env
    echo "LLAMA_CLOUD_API_KEY=llx-your-key-here" >> .env
    echo ""
    echo "   Please edit .env and add your actual LlamaIndex key"
    echo "   Get it from: https://cloud.llamaindex.ai"
fi

echo ""
echo "✅ Step 3: Testing enhanced parser..."
echo "----------------------------------------"

# Test if imports work
python3 -c "from document_ingestion_enhanced import EnhancedDocumentParser; print('✅ Enhanced parser imports successfully')" 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Enhanced parser is ready to use"
else
    echo "⚠️  Enhanced parser test failed"
    echo "   This might be okay - test with a real document"
fi

echo ""
echo "================================================================"
echo "Setup Complete!"
echo "================================================================"
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Update your API keys in .env:"
echo "   nano .env"
echo ""
echo "2. Test with SAP report:"
echo "   python3 analyze_annual_report.py samples/sap_variance_report.pdf"
echo ""
echo "3. Download and analyze a real annual report:"
echo "   # Get from SEC: https://www.sec.gov/edgar"
echo "   python3 analyze_annual_report.py company_10k.pdf --interactive"
echo ""
echo "4. Read the upgrade guide:"
echo "   cat UPGRADE_GUIDE.md"
echo ""
echo "================================================================"
echo ""
echo "💡 Quick Commands:"
echo ""
echo "  # Analyze SAP report (PyPDF2 - fast & free)"
echo "  python3 main.py samples/sap_variance_report.pdf"
echo ""
echo "  # Analyze annual report (LlamaParse - better quality)"
echo "  python3 analyze_annual_report.py annual_report.pdf"
echo ""
echo "  # Any document with Q&A"
echo "  python3 main_with_qa.py document.pdf --interactive"
echo ""
echo "================================================================"
