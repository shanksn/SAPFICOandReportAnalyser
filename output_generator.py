"""
Structured Output Generator
Creates JSON and HTML dashboard from agent results
"""

import json
from datetime import datetime
from jinja2 import Template
from typing import Dict


class OutputGenerator:
    """Generate structured outputs from agent results"""

    def __init__(self, results: Dict):
        self.results = results
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def save_json(self, output_path: str = "analysis_results.json"):
        """Save results as JSON"""
        output_data = {
            "timestamp": self.timestamp,
            "results": self.results
        }

        with open(output_path, 'w') as f:
            json.dump(output_data, f, indent=2)

        print(f"✓ JSON results saved to: {output_path}")
        return output_path

    def generate_html_dashboard(self, output_path: str = "dashboard.html"):
        """Generate HTML dashboard"""
        template = self._get_html_template()

        # Prepare data for template
        metadata = self.results.get("metadata", {})
        exec_summary = self.results.get("executive_summary", {}).get("parsed_output", {}).get("executive_summary", {})
        anomalies = self.results.get("anomaly_detection", {}).get("parsed_output", {})
        variances = self.results.get("variance_analysis", {}).get("parsed_output", {})
        usage = self.results.get("total_usage", {})

        html_content = template.render(
            timestamp=self.timestamp,
            metadata=metadata,
            exec_summary=exec_summary,
            anomalies=anomalies,
            variances=variances,
            usage=usage
        )

        with open(output_path, 'w') as f:
            f.write(html_content)

        print(f"✓ HTML dashboard saved to: {output_path}")
        return output_path

    def _get_html_template(self) -> Template:
        """HTML template for dashboard"""
        template_str = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAP FI/CO Analysis Dashboard</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f5f7fa;
            color: #2c3e50;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 10px;
            margin-bottom: 30px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 {
            font-size: 32px;
            margin-bottom: 10px;
        }
        .metadata {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
            margin-top: 15px;
            opacity: 0.95;
        }
        .metadata-item {
            background: rgba(255,255,255,0.2);
            padding: 8px 15px;
            border-radius: 5px;
            font-size: 14px;
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-bottom: 20px;
        }
        .card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
        .card h2 {
            font-size: 20px;
            margin-bottom: 20px;
            color: #667eea;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .card.full-width {
            grid-column: 1 / -1;
        }
        .metric {
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #ecf0f1;
        }
        .metric:last-child {
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }
        .metric-header {
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 5px;
        }
        .metric-value {
            font-size: 14px;
            color: #7f8c8d;
            line-height: 1.5;
        }
        .issue {
            background: #fff5f5;
            border-left: 4px solid #e74c3c;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 5px;
        }
        .issue.medium {
            background: #fffbf0;
            border-left-color: #f39c12;
        }
        .issue.low {
            background: #f0f9ff;
            border-left-color: #3498db;
        }
        .issue-type {
            font-weight: 600;
            text-transform: uppercase;
            font-size: 12px;
            color: #e74c3c;
            margin-bottom: 5px;
        }
        .issue.medium .issue-type {
            color: #f39c12;
        }
        .issue.low .issue-type {
            color: #3498db;
        }
        .variance {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 12px;
            background: #f8f9fa;
            border-radius: 5px;
            margin-bottom: 10px;
        }
        .variance.favorable {
            background: #d4edda;
            border-left: 3px solid #28a745;
        }
        .variance.unfavorable {
            background: #f8d7da;
            border-left: 3px solid #dc3545;
        }
        .variance-info {
            flex: 1;
        }
        .variance-name {
            font-weight: 600;
            margin-bottom: 3px;
        }
        .variance-explanation {
            font-size: 13px;
            color: #6c757d;
        }
        .variance-amount {
            font-weight: 700;
            font-size: 18px;
            text-align: right;
            min-width: 120px;
        }
        .no-data {
            text-align: center;
            padding: 30px;
            color: #95a5a6;
            font-style: italic;
        }
        .achievement {
            background: #d4edda;
            border-left: 4px solid #28a745;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        .recommendation {
            background: #d1ecf1;
            border-left: 4px solid #17a2b8;
            padding: 12px 15px;
            margin-bottom: 10px;
            border-radius: 5px;
            font-size: 14px;
        }
        .headline {
            font-size: 18px;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 20px;
            padding: 15px;
            background: #e8f4f8;
            border-radius: 5px;
        }
        .footer {
            text-align: center;
            margin-top: 30px;
            padding: 20px;
            color: #95a5a6;
            font-size: 13px;
        }
        .badge {
            display: inline-block;
            padding: 4px 8px;
            border-radius: 3px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
        }
        .badge-high {
            background: #fee;
            color: #c33;
        }
        .badge-medium {
            background: #ffeeba;
            color: #856404;
        }
        .badge-low {
            background: #d1ecf1;
            color: #0c5460;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 SAP FI/CO Analysis Dashboard</h1>
            <div class="metadata">
                <div class="metadata-item">🕐 Generated: {{ timestamp }}</div>
                {% if metadata.document_type %}
                <div class="metadata-item">📄 {{ metadata.document_type }}</div>
                {% endif %}
                {% if metadata.company_code %}
                <div class="metadata-item">🏢 Company: {{ metadata.company_code }}</div>
                {% endif %}
                {% if metadata.period and metadata.fiscal_year %}
                <div class="metadata-item">📅 Period: {{ metadata.period }}/{{ metadata.fiscal_year }}</div>
                {% endif %}
                {% if usage.total_tokens %}
                <div class="metadata-item">🤖 AI Tokens: {{ "{:,}".format(usage.total_tokens) }}</div>
                {% endif %}
            </div>
        </header>

        <!-- Executive Summary -->
        <div class="card full-width">
            <h2>📋 Executive Summary</h2>
            {% if exec_summary.headline %}
                <div class="headline">{{ exec_summary.headline }}</div>

                {% if exec_summary.key_metrics %}
                <h3 style="margin: 20px 0 10px 0; font-size: 16px;">Key Metrics</h3>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin-bottom: 20px;">
                    {% for metric in exec_summary.key_metrics %}
                    <div class="metric">
                        <div class="metric-header">{{ metric.metric }}</div>
                        <div class="metric-value">
                            <strong>{{ metric.value }}</strong>
                            {% if metric.trend == 'up' %}📈{% elif metric.trend == 'down' %}📉{% else %}➡️{% endif %}
                            <br>{{ metric.commentary }}
                        </div>
                    </div>
                    {% endfor %}
                </div>
                {% endif %}

                {% if exec_summary.key_achievements %}
                <h3 style="margin: 20px 0 10px 0; font-size: 16px;">✓ Key Achievements</h3>
                {% for achievement in exec_summary.key_achievements %}
                <div class="achievement">{{ achievement }}</div>
                {% endfor %}
                {% endif %}

                {% if exec_summary.critical_issues %}
                <h3 style="margin: 20px 0 10px 0; font-size: 16px;">⚠️ Critical Issues</h3>
                {% for issue in exec_summary.critical_issues %}
                <div class="issue">{{ issue }}</div>
                {% endfor %}
                {% endif %}

                {% if exec_summary.recommendations %}
                <h3 style="margin: 20px 0 10px 0; font-size: 16px;">💡 Recommendations</h3>
                {% for rec in exec_summary.recommendations %}
                <div class="recommendation">{{ rec }}</div>
                {% endfor %}
                {% endif %}

                {% if exec_summary.overall_assessment %}
                <h3 style="margin: 20px 0 10px 0; font-size: 16px;">Overall Assessment</h3>
                <p style="line-height: 1.6; color: #555;">{{ exec_summary.overall_assessment }}</p>
                {% endif %}
            {% else %}
                <div class="no-data">Executive summary not available</div>
            {% endif %}
        </div>

        <div class="dashboard-grid">
            <!-- Anomaly Detection -->
            <div class="card">
                <h2>🔍 Anomaly Detection</h2>
                {% if anomalies.critical_issues %}
                    {% for issue in anomalies.critical_issues %}
                    <div class="issue {{ issue.severity }}">
                        <div class="issue-type">
                            <span class="badge badge-{{ issue.severity }}">{{ issue.severity }}</span>
                            {{ issue.type.replace('_', ' ') }}
                        </div>
                        <div style="margin: 8px 0; font-weight: 500;">{{ issue.description }}</div>
                        {% if issue.account %}
                        <div style="font-size: 13px; color: #666;">Account: {{ issue.account }}</div>
                        {% endif %}
                        {% if issue.amount %}
                        <div style="font-size: 13px; color: #666;">Amount: {{ issue.amount }}</div>
                        {% endif %}
                        {% if issue.recommendation %}
                        <div style="margin-top: 8px; font-size: 13px; font-style: italic; color: #555;">
                            → {{ issue.recommendation }}
                        </div>
                        {% endif %}
                    </div>
                    {% endfor %}
                    {% if anomalies.summary %}
                    <div style="margin-top: 15px; padding: 12px; background: #f8f9fa; border-radius: 5px; font-size: 14px;">
                        <strong>Summary:</strong> {{ anomalies.summary }}
                    </div>
                    {% endif %}
                {% else %}
                    <div class="no-data">✓ No significant anomalies detected</div>
                {% endif %}
            </div>

            <!-- Variance Analysis -->
            <div class="card">
                <h2>📊 Variance Analysis</h2>
                {% if variances.variances %}
                    {% for v in variances.variances %}
                    <div class="variance {% if v.favorable %}favorable{% else %}unfavorable{% endif %}">
                        <div class="variance-info">
                            <div class="variance-name">{{ v.account_name }}</div>
                            <div class="variance-explanation">{{ v.explanation }}</div>
                            {% if v.action_required %}
                            <div style="margin-top: 5px; font-size: 12px; font-weight: 600; color: #333;">
                                Action: {{ v.action_required }}
                            </div>
                            {% endif %}
                        </div>
                        <div class="variance-amount">
                            {{ v.variance_percent|round(1) }}%
                            <div style="font-size: 13px; font-weight: normal; color: #666;">
                                ${{ "{:,.0f}".format(v.variance_amount) }}
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                    {% if variances.summary %}
                    <div style="margin-top: 15px; padding: 12px; background: #f8f9fa; border-radius: 5px; font-size: 14px;">
                        <strong>Summary:</strong> {{ variances.summary }}
                    </div>
                    {% endif %}
                {% else %}
                    <div class="no-data">No variance data available</div>
                {% endif %}
            </div>
        </div>

        <div class="footer">
            Powered by Claude ({{ usage.output_tokens|default(0)|int }} output tokens) |
            SAP FI/CO Analysis Agent |
            Generated {{ timestamp }}
        </div>
    </div>
</body>
</html>
        """
        return Template(template_str)


if __name__ == "__main__":
    print("Output Generator - Use main.py to run the full pipeline")
