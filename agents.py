"""
SAP FI/CO Analysis Agents
Three specialized agents running in parallel:
1. Anomaly Detector
2. Variance Analyst
3. Executive Summariser
"""

import anthropic
from typing import Dict, List
import json
import os
from dotenv import load_dotenv
from config import CLAUDE_MODEL, SAP_FI_CONTEXT

load_dotenv()


class SAPAnalysisAgent:
    """Base class for SAP FI/CO analysis agents"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model = CLAUDE_MODEL

    def analyze(self, document_data: Dict, agent_prompt: str) -> Dict:
        """Run analysis using Claude"""
        system_prompt = f"{SAP_FI_CONTEXT}\n\n{agent_prompt}"

        # Prepare the document content for analysis
        user_message = self._prepare_user_message(document_data)

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                system=system_prompt,
                messages=[
                    {"role": "user", "content": user_message}
                ]
            )

            return {
                "success": True,
                "content": response.content[0].text,
                "usage": {
                    "input_tokens": response.usage.input_tokens,
                    "output_tokens": response.usage.output_tokens
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def _prepare_user_message(self, document_data: Dict) -> str:
        """Prepare user message from document data"""
        msg = f"""Please analyze the following SAP FI/CO document:

**Document Type:** {document_data.get('document_type', 'Unknown')}

**Metadata:**
{json.dumps(document_data.get('metadata', {}), indent=2)}

**Document Content:**
{document_data.get('raw_text', '')[:8000]}

"""
        if document_data.get('tables'):
            msg += f"\n**Table Data Sections:** {len(document_data['tables'])} tables found\n"

        return msg


class AnomalyDetector(SAPAnalysisAgent):
    """Agent 1: Detect anomalies in SAP FI/CO data"""

    AGENT_PROMPT = """
## Your Role: Anomaly Detection Specialist

Analyze the SAP FI/CO document for unusual patterns and potential issues:

1. **Duplicate Postings**: Look for repeated GL entries with same amount/description
2. **Outlier Amounts**: Identify unusually large or small transactions
3. **Unusual Patterns**:
   - Round numbers that seem suspicious (e.g., exactly $100,000)
   - Posting patterns at month-end that seem rushed
   - Unbalanced entries or missing offsetting accounts
4. **Control Violations**:
   - Missing cost center assignments on expense accounts
   - Postings to wrong account categories
   - Unusual inter-company transactions

Return your findings in this JSON structure:
```json
{
  "anomalies_found": true/false,
  "critical_issues": [
    {
      "type": "duplicate_posting|outlier|control_violation|pattern",
      "severity": "high|medium|low",
      "description": "Clear description of the issue",
      "account": "GL account number if applicable",
      "amount": "Amount if applicable",
      "recommendation": "What to do about it"
    }
  ],
  "summary": "Brief summary of anomaly detection findings"
}
```

If no significant anomalies are found, return an empty critical_issues array.
"""

    def detect_anomalies(self, document_data: Dict) -> Dict:
        """Run anomaly detection"""
        print("🔍 Running anomaly detection...")
        result = self.analyze(document_data, self.AGENT_PROMPT)

        if result["success"]:
            # Try to parse JSON from response
            try:
                # Extract JSON from markdown code blocks if present
                content = result["content"]
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
                print(f"✓ Anomaly detection complete - Found {len(parsed.get('critical_issues', []))} issues")
            except json.JSONDecodeError:
                result["parsed_output"] = {"raw_response": content}
                print("⚠ Could not parse JSON response")

        return result


class VarianceAnalyst(SAPAnalysisAgent):
    """Agent 2: Analyze variances between actual vs plan/budget"""

    AGENT_PROMPT = """
## Your Role: Variance Analysis Specialist

Analyze the SAP FI/CO document for variances between Actual vs Plan/Budget:

1. **Revenue Variances**:
   - Are sales meeting targets?
   - Which product lines or regions are over/under performing?
2. **Cost Variances**:
   - Which cost centers are over budget?
   - Are there cost overruns in specific categories (payroll, materials, overhead)?
3. **Root Cause Analysis**:
   - For material variances (>20% or >$10,000), provide likely explanations
   - Consider volume, price, mix, and timing differences
4. **Trend Analysis**:
   - Is this variance improving or worsening vs prior periods?

Return your findings in this JSON structure:
```json
{
  "variances": [
    {
      "account_category": "Revenue|COGS|Operating Expense|Other",
      "account_name": "Account name",
      "actual": 0.00,
      "plan": 0.00,
      "variance_amount": 0.00,
      "variance_percent": 0.00,
      "favorable": true/false,
      "materiality": "high|medium|low",
      "explanation": "Natural language explanation of why this variance occurred",
      "action_required": "What management should do"
    }
  ],
  "summary": "Overall variance commentary - are we on track financially?"
}
```

Focus on variances that matter - ignore immaterial differences.
"""

    def analyze_variance(self, document_data: Dict) -> Dict:
        """Run variance analysis"""
        print("📊 Running variance analysis...")
        result = self.analyze(document_data, self.AGENT_PROMPT)

        if result["success"]:
            try:
                content = result["content"]
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
                print(f"✓ Variance analysis complete - Found {len(parsed.get('variances', []))} variances")
            except json.JSONDecodeError:
                result["parsed_output"] = {"raw_response": content}
                print("⚠ Could not parse JSON response")

        return result


class ExecutiveSummariser(SAPAnalysisAgent):
    """Agent 3: Create executive summary for CFO/leadership"""

    AGENT_PROMPT = """
## Your Role: Executive Summary Specialist

Create a concise, CFO-ready executive summary of the SAP FI/CO document.

Your audience is busy executives who need:
- The bottom line upfront
- Key numbers and trends
- Critical issues requiring attention
- Clear, jargon-free language

Return your findings in this JSON structure:
```json
{
  "executive_summary": {
    "headline": "One sentence bottom line (e.g., 'Q1 revenue exceeded plan by 12%, driven by strong APAC sales')",
    "key_metrics": [
      {
        "metric": "Metric name",
        "value": "Value with currency/units",
        "trend": "up|down|flat",
        "commentary": "Brief context"
      }
    ],
    "critical_issues": [
      "Issue 1: Brief description",
      "Issue 2: Brief description"
    ],
    "key_achievements": [
      "Achievement 1: Brief description",
      "Achievement 2: Brief description"
    ],
    "recommendations": [
      "Recommendation 1",
      "Recommendation 2"
    ],
    "overall_assessment": "2-3 sentence overall financial health assessment"
  }
}
```

Keep it concise - 5 bullets maximum in each section. Use specific numbers.
"""

    def create_summary(self, document_data: Dict) -> Dict:
        """Create executive summary"""
        print("📋 Creating executive summary...")
        result = self.analyze(document_data, self.AGENT_PROMPT)

        if result["success"]:
            try:
                content = result["content"]
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
                print("✓ Executive summary complete")
            except json.JSONDecodeError:
                result["parsed_output"] = {"raw_response": content}
                print("⚠ Could not parse JSON response")

        return result


class ParallelAgentOrchestrator:
    """Orchestrate the three agents to run in parallel"""

    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.variance_analyst = VarianceAnalyst()
        self.executive_summariser = ExecutiveSummariser()

    def run_all_agents(self, document_data: Dict) -> Dict:
        """Run all three agents and combine results"""
        print("\n" + "="*60)
        print("🚀 Running SAP FI/CO Analysis - 3 Agents in Parallel")
        print("="*60 + "\n")

        # Note: In production, use asyncio or threading for true parallelism
        # For POC simplicity, running sequentially
        results = {
            "anomaly_detection": self.anomaly_detector.detect_anomalies(document_data),
            "variance_analysis": self.variance_analyst.analyze_variance(document_data),
            "executive_summary": self.executive_summariser.create_summary(document_data),
            "metadata": {
                "document_type": document_data.get("document_type"),
                "company_code": document_data.get("metadata", {}).get("company_code"),
                "period": document_data.get("metadata", {}).get("period"),
                "fiscal_year": document_data.get("metadata", {}).get("fiscal_year")
            }
        }

        # Calculate total tokens used
        total_input_tokens = sum(
            r.get("usage", {}).get("input_tokens", 0)
            for r in results.values() if isinstance(r, dict) and "usage" in r
        )
        total_output_tokens = sum(
            r.get("usage", {}).get("output_tokens", 0)
            for r in results.values() if isinstance(r, dict) and "usage" in r
        )

        results["total_usage"] = {
            "input_tokens": total_input_tokens,
            "output_tokens": total_output_tokens,
            "total_tokens": total_input_tokens + total_output_tokens
        }

        print("\n" + "="*60)
        print(f"✓ All agents complete - Total tokens: {results['total_usage']['total_tokens']:,}")
        print("="*60 + "\n")

        return results


if __name__ == "__main__":
    # Test the agents
    print("SAP FI/CO Analysis Agents - Test Mode")
    print("Use main.py to run the full pipeline")
