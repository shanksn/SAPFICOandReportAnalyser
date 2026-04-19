"""
Create demo analysis output to show what the pipeline produces
(Simulates what Claude would return when API credits are available)
"""

import json
from output_generator import OutputGenerator

# Simulated agent responses (what Claude would return)
demo_results = {
    "anomaly_detection": {
        "success": True,
        "content": """```json
{
  "anomalies_found": true,
  "critical_issues": [
    {
      "type": "outlier",
      "severity": "high",
      "description": "Material costs (GL 5000) are 15.3% over budget ($130k variance) - highest cost overrun",
      "account": "5000 - Cost of Goods Sold - Materials",
      "amount": "$980,000 (Budget: $850,000)",
      "recommendation": "Investigate supplier pricing changes and material waste. Review procurement contracts for potential cost savings."
    },
    {
      "type": "pattern",
      "severity": "high",
      "description": "Professional Fees (GL 6400) exceeded budget by 25% - unusual spike in consulting spend",
      "account": "6400 - Professional Fees",
      "amount": "$75,000 (Budget: $60,000)",
      "recommendation": "Review all professional service contracts. Ensure proper approval process for external consultants."
    },
    {
      "type": "pattern",
      "severity": "medium",
      "description": "Marketing spend (GL 6300) 20% over budget - may indicate unplanned campaigns or inefficient spend",
      "account": "6300 - Marketing & Advertising",
      "amount": "$180,000 (Budget: $150,000)",
      "recommendation": "Analyze marketing ROI by campaign. Consider pausing low-performing initiatives."
    },
    {
      "type": "control_violation",
      "severity": "medium",
      "description": "Foreign Exchange Loss (GL 7200) of $12k with no budget allocation - indicates unhedged FX exposure",
      "account": "7200 - Foreign Exchange Gain/Loss",
      "amount": "-$12,000 (Budget: $0)",
      "recommendation": "Implement FX hedging strategy for foreign currency transactions. Review treasury policies."
    }
  ],
  "summary": "Detected 4 material anomalies requiring management attention. Primary concerns are COGS overruns (materials up 15.3%) and unbudgeted professional fees/marketing spend. FX controls need strengthening."
}
```""",
        "usage": {"input_tokens": 3200, "output_tokens": 450},
        "parsed_output": {
            "anomalies_found": True,
            "critical_issues": [
                {
                    "type": "outlier",
                    "severity": "high",
                    "description": "Material costs (GL 5000) are 15.3% over budget ($130k variance) - highest cost overrun",
                    "account": "5000 - Cost of Goods Sold - Materials",
                    "amount": "$980,000 (Budget: $850,000)",
                    "recommendation": "Investigate supplier pricing changes and material waste. Review procurement contracts for potential cost savings."
                },
                {
                    "type": "pattern",
                    "severity": "high",
                    "description": "Professional Fees (GL 6400) exceeded budget by 25% - unusual spike in consulting spend",
                    "account": "6400 - Professional Fees",
                    "amount": "$75,000 (Budget: $60,000)",
                    "recommendation": "Review all professional service contracts. Ensure proper approval process for external consultants."
                },
                {
                    "type": "pattern",
                    "severity": "medium",
                    "description": "Marketing spend (GL 6300) 20% over budget - may indicate unplanned campaigns or inefficient spend",
                    "account": "6300 - Marketing & Advertising",
                    "amount": "$180,000 (Budget: $150,000)",
                    "recommendation": "Analyze marketing ROI by campaign. Consider pausing low-performing initiatives."
                },
                {
                    "type": "control_violation",
                    "severity": "medium",
                    "description": "Foreign Exchange Loss (GL 7200) of $12k with no budget allocation - indicates unhedged FX exposure",
                    "account": "7200 - Foreign Exchange Gain/Loss",
                    "amount": "-$12,000 (Budget: $0)",
                    "recommendation": "Implement FX hedging strategy for foreign currency transactions. Review treasury policies."
                }
            ],
            "summary": "Detected 4 material anomalies requiring management attention. Primary concerns are COGS overruns (materials up 15.3%) and unbudgeted professional fees/marketing spend. FX controls need strengthening."
        }
    },
    "variance_analysis": {
        "success": True,
        "content": """```json
{
  "variances": [
    {
      "account_category": "Revenue",
      "account_name": "Sales Revenue - Products",
      "actual": 2450000,
      "plan": 2200000,
      "variance_amount": 250000,
      "variance_percent": 11.4,
      "favorable": true,
      "materiality": "high",
      "explanation": "Product sales beat expectations by 11.4%, likely driven by strong Q1 demand and successful product launches in January-February timeframe",
      "action_required": "Maintain momentum - ensure inventory levels can support continued demand"
    },
    {
      "account_category": "Revenue",
      "account_name": "Sales Revenue - Services",
      "actual": 890000,
      "plan": 950000,
      "variance_amount": -60000,
      "variance_percent": -6.3,
      "favorable": false,
      "materiality": "medium",
      "explanation": "Service revenue fell short by 6.3% ($60k). Possible causes: delayed project starts, customer churn, or sales pipeline gaps",
      "action_required": "Review service backlog and renewal rates. Accelerate sales pipeline conversion"
    },
    {
      "account_category": "COGS",
      "account_name": "Cost of Goods Sold - Materials",
      "actual": 980000,
      "plan": 850000,
      "variance_amount": -130000,
      "variance_percent": -15.3,
      "favorable": false,
      "materiality": "high",
      "explanation": "Materials cost 15.3% over budget - most significant variance. Driven by combination of higher unit prices (supplier increases) and potentially higher material waste/scrap rates",
      "action_required": "URGENT: Negotiate with suppliers for better pricing. Conduct material waste analysis"
    },
    {
      "account_category": "Operating Expense",
      "account_name": "IT & Software Licenses",
      "actual": 95000,
      "plan": 80000,
      "variance_amount": -15000,
      "variance_percent": -18.8,
      "favorable": false,
      "materiality": "medium",
      "explanation": "IT costs 18.8% over budget, likely due to new software subscriptions or license true-ups not captured in original budget",
      "action_required": "Review all SaaS subscriptions. Optimize license counts and eliminate unused tools"
    },
    {
      "account_category": "Operating Expense",
      "account_name": "Marketing & Advertising",
      "actual": 180000,
      "plan": 150000,
      "variance_amount": -30000,
      "variance_percent": -20.0,
      "favorable": false,
      "materiality": "medium",
      "explanation": "Marketing overspent by 20%, possibly supporting product launch campaigns or responding to competitive pressure",
      "action_required": "Measure campaign ROI. Cut low-performing channels and reallocate budget"
    },
    {
      "account_category": "Operating Expense",
      "account_name": "Professional Fees",
      "actual": 75000,
      "plan": 60000,
      "variance_amount": -15000,
      "variance_percent": -25.0,
      "favorable": false,
      "materiality": "medium",
      "explanation": "Professional fees 25% over budget - likely unplanned legal/consulting work. May relate to M&A, litigation, or compliance projects",
      "action_required": "Review SOWs for all professional service providers. Approve large engagements in advance"
    }
  ],
  "summary": "Overall variance story: Strong product revenue (+11.4%) offset by service shortfall (-6.3%), resulting in 6.1% revenue beat. However, COGS significantly exceeded plan (-11.4%), primarily due to material cost inflation. OpEx also ran over budget (-7.9%), driven by marketing, IT, and professional fees. Net result: Operating profit missed budget by 11.9% despite revenue growth - a margin compression story requiring immediate cost control action."
}
```""",
        "usage": {"input_tokens": 3200, "output_tokens": 850},
        "parsed_output": {
            "variances": [
                {
                    "account_category": "Revenue",
                    "account_name": "Sales Revenue - Products",
                    "actual": 2450000,
                    "plan": 2200000,
                    "variance_amount": 250000,
                    "variance_percent": 11.4,
                    "favorable": True,
                    "materiality": "high",
                    "explanation": "Product sales beat expectations by 11.4%, likely driven by strong Q1 demand and successful product launches in January-February timeframe",
                    "action_required": "Maintain momentum - ensure inventory levels can support continued demand"
                },
                {
                    "account_category": "Revenue",
                    "account_name": "Sales Revenue - Services",
                    "actual": 890000,
                    "plan": 950000,
                    "variance_amount": -60000,
                    "variance_percent": -6.3,
                    "favorable": False,
                    "materiality": "medium",
                    "explanation": "Service revenue fell short by 6.3% ($60k). Possible causes: delayed project starts, customer churn, or sales pipeline gaps",
                    "action_required": "Review service backlog and renewal rates. Accelerate sales pipeline conversion"
                },
                {
                    "account_category": "COGS",
                    "account_name": "Cost of Goods Sold - Materials",
                    "actual": 980000,
                    "plan": 850000,
                    "variance_amount": -130000,
                    "variance_percent": -15.3,
                    "favorable": False,
                    "materiality": "high",
                    "explanation": "Materials cost 15.3% over budget - most significant variance. Driven by combination of higher unit prices (supplier increases) and potentially higher material waste/scrap rates",
                    "action_required": "URGENT: Negotiate with suppliers for better pricing. Conduct material waste analysis"
                },
                {
                    "account_category": "Operating Expense",
                    "account_name": "IT & Software Licenses",
                    "actual": 95000,
                    "plan": 80000,
                    "variance_amount": -15000,
                    "variance_percent": -18.8,
                    "favorable": False,
                    "materiality": "medium",
                    "explanation": "IT costs 18.8% over budget, likely due to new software subscriptions or license true-ups not captured in original budget",
                    "action_required": "Review all SaaS subscriptions. Optimize license counts and eliminate unused tools"
                },
                {
                    "account_category": "Operating Expense",
                    "account_name": "Marketing & Advertising",
                    "actual": 180000,
                    "plan": 150000,
                    "variance_amount": -30000,
                    "variance_percent": -20.0,
                    "favorable": False,
                    "materiality": "medium",
                    "explanation": "Marketing overspent by 20%, possibly supporting product launch campaigns or responding to competitive pressure",
                    "action_required": "Measure campaign ROI. Cut low-performing channels and reallocate budget"
                },
                {
                    "account_category": "Operating Expense",
                    "account_name": "Professional Fees",
                    "actual": 75000,
                    "plan": 60000,
                    "variance_amount": -15000,
                    "variance_percent": -25.0,
                    "favorable": False,
                    "materiality": "medium",
                    "explanation": "Professional fees 25% over budget - likely unplanned legal/consulting work. May relate to M&A, litigation, or compliance projects",
                    "action_required": "Review SOWs for all professional service providers. Approve large engagements in advance"
                }
            ],
            "summary": "Overall variance story: Strong product revenue (+11.4%) offset by service shortfall (-6.3%), resulting in 6.1% revenue beat. However, COGS significantly exceeded plan (-11.4%), primarily due to material cost inflation. OpEx also ran over budget (-7.9%), driven by marketing, IT, and professional fees. Net result: Operating profit missed budget by 11.9% despite revenue growth - a margin compression story requiring immediate cost control action."
        }
    },
    "executive_summary": {
        "success": True,
        "content": """```json
{
  "executive_summary": {
    "headline": "Q1 2024: Revenue beat by 6.1% offset by 11.4% COGS overrun and 7.9% OpEx overspend, resulting in 11.9% operating profit miss",
    "key_metrics": [
      {
        "metric": "Total Revenue",
        "value": "$3.39M (vs $3.19M budget)",
        "trend": "up",
        "commentary": "+6.1% driven by strong product sales (+11.4%), partially offset by service shortfall (-6.3%)"
      },
      {
        "metric": "Gross Margin",
        "value": "52.3% (vs 54.5% budget)",
        "trend": "down",
        "commentary": "Margin compression of 220bps due to material cost inflation (COGS +11.4%)"
      },
      {
        "metric": "Operating Profit",
        "value": "$480k (vs $545k budget)",
        "trend": "down",
        "commentary": "Missed budget by $65k (-11.9%) despite revenue growth"
      },
      {
        "metric": "Net Profit",
        "value": "$338k (vs $398k budget)",
        "trend": "down",
        "commentary": "14.9% below plan, with net margin at 10.0% (vs 12.5% budget)"
      }
    ],
    "critical_issues": [
      "Material costs $130k over budget (+15.3%) - urgent supplier negotiation and waste reduction required",
      "Professional fees spiked 25% over budget ($15k) - consulting spend needs tighter controls",
      "Marketing overspent by 20% ($30k) - ROI analysis needed to optimize spend",
      "Foreign exchange loss of $12k unhedged - treasury needs FX risk management strategy"
    ],
    "key_achievements": [
      "Product revenue exceeded target by $250k (+11.4%) - strong market demand",
      "Gross profit delivered $30k above budget despite COGS pressure",
      "Operating expenses on payroll, rent, and depreciation held to budget - good cost discipline"
    ],
    "recommendations": [
      "Immediate action: Launch material cost reduction initiative (target: 5-7% savings through supplier negotiations and waste reduction)",
      "Implement pre-approval process for all professional service engagements >$10k",
      "Conduct marketing spend effectiveness review - cut bottom 20% of campaigns by ROI",
      "Address service revenue gap - accelerate pipeline conversion and review pricing strategy",
      "Establish FX hedging policy for transactions >$50k"
    ],
    "overall_assessment": "Mixed quarter: Revenue growth is positive but insufficient to offset cost pressures. The business is experiencing margin compression from material inflation and OpEx creep. Immediate cost control actions required in procurement, professional services, and marketing to restore profitability to plan levels. Service revenue weakness also needs urgent attention to prevent trend continuation into Q2."
  }
}
```""",
        "usage": {"input_tokens": 3200, "output_tokens": 750},
        "parsed_output": {
            "executive_summary": {
                "headline": "Q1 2024: Revenue beat by 6.1% offset by 11.4% COGS overrun and 7.9% OpEx overspend, resulting in 11.9% operating profit miss",
                "key_metrics": [
                    {
                        "metric": "Total Revenue",
                        "value": "$3.39M (vs $3.19M budget)",
                        "trend": "up",
                        "commentary": "+6.1% driven by strong product sales (+11.4%), partially offset by service shortfall (-6.3%)"
                    },
                    {
                        "metric": "Gross Margin",
                        "value": "52.3% (vs 54.5% budget)",
                        "trend": "down",
                        "commentary": "Margin compression of 220bps due to material cost inflation (COGS +11.4%)"
                    },
                    {
                        "metric": "Operating Profit",
                        "value": "$480k (vs $545k budget)",
                        "trend": "down",
                        "commentary": "Missed budget by $65k (-11.9%) despite revenue growth"
                    },
                    {
                        "metric": "Net Profit",
                        "value": "$338k (vs $398k budget)",
                        "trend": "down",
                        "commentary": "14.9% below plan, with net margin at 10.0% (vs 12.5% budget)"
                    }
                ],
                "critical_issues": [
                    "Material costs $130k over budget (+15.3%) - urgent supplier negotiation and waste reduction required",
                    "Professional fees spiked 25% over budget ($15k) - consulting spend needs tighter controls",
                    "Marketing overspent by 20% ($30k) - ROI analysis needed to optimize spend",
                    "Foreign exchange loss of $12k unhedged - treasury needs FX risk management strategy"
                ],
                "key_achievements": [
                    "Product revenue exceeded target by $250k (+11.4%) - strong market demand",
                    "Gross profit delivered $30k above budget despite COGS pressure",
                    "Operating expenses on payroll, rent, and depreciation held to budget - good cost discipline"
                ],
                "recommendations": [
                    "Immediate action: Launch material cost reduction initiative (target: 5-7% savings through supplier negotiations and waste reduction)",
                    "Implement pre-approval process for all professional service engagements >$10k",
                    "Conduct marketing spend effectiveness review - cut bottom 20% of campaigns by ROI",
                    "Address service revenue gap - accelerate pipeline conversion and review pricing strategy",
                    "Establish FX hedging policy for transactions >$50k"
                ],
                "overall_assessment": "Mixed quarter: Revenue growth is positive but insufficient to offset cost pressures. The business is experiencing margin compression from material inflation and OpEx creep. Immediate cost control actions required in procurement, professional services, and marketing to restore profitability to plan levels. Service revenue weakness also needs urgent attention to prevent trend continuation into Q2."
            }
        }
    },
    "metadata": {
        "document_type": "Variance Report",
        "company_code": "1000",
        "period": "03",
        "fiscal_year": "2024"
    },
    "total_usage": {
        "input_tokens": 9600,
        "output_tokens": 2050,
        "total_tokens": 11650
    }
}

# Generate the dashboard
generator = OutputGenerator(demo_results)
generator.save_json("demo_analysis_results.json")
generator.generate_html_dashboard("demo_dashboard.html")

print("\n" + "="*60)
print("✅ Demo outputs created successfully!")
print("="*60)
print("\n📊 Files created:")
print("  - demo_analysis_results.json (JSON output)")
print("  - demo_dashboard.html (Interactive dashboard)")
print("\n💡 Open demo_dashboard.html in your browser to see what")
print("   the full pipeline produces with Claude API access")
print("="*60)
