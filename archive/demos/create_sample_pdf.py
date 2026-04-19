"""
Create a sample SAP FI/CO PDF for testing
Uses reportlab to generate a realistic SAP variance report
"""

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False
    print("⚠️  reportlab not installed. Installing...")
    import subprocess
    subprocess.check_call(["pip", "install", "reportlab"])
    from reportlab.lib.pagesizes import A4
    from reportlab.lib import colors
    from reportlab.lib.units import mm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_CENTER, TA_RIGHT


def create_sample_sap_variance_report(output_path="samples/sap_variance_report.pdf"):
    """Create a realistic SAP FI/CO variance report"""

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=colors.HexColor('#003366'),
        spaceAfter=12,
        alignment=TA_CENTER
    )

    header_style = ParagraphStyle(
        'CustomHeader',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.grey
    )

    # Header
    story.append(Paragraph("SAP ERP - Financial Accounting", title_style))
    story.append(Paragraph("Profit & Loss Variance Report", title_style))
    story.append(Spacer(1, 10))

    # Metadata
    metadata = [
        ["Company Code:", "1000", "Period:", "03/2024"],
        ["Company Name:", "ACME Corporation Ltd.", "Currency:", "USD"],
        ["Report Date:", "2024-04-01", "User:", "SAPUSER01"]
    ]

    meta_table = Table(metadata, colWidths=[80, 150, 80, 100])
    meta_table.setStyle(TableStyle([
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.grey),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))

    # Main variance table
    story.append(Paragraph("<b>Actual vs Budget Variance Analysis - Q1 2024</b>", styles['Heading2']))
    story.append(Spacer(1, 10))

    data = [
        ["GL Account", "Account Description", "Actual", "Budget", "Variance", "Var %"],
        ["", "", "", "", "", ""],
        ["4000", "Sales Revenue - Products", "2,450,000", "2,200,000", "250,000", "11.4%"],
        ["4100", "Sales Revenue - Services", "890,000", "950,000", "-60,000", "-6.3%"],
        ["4200", "Other Operating Income", "45,000", "40,000", "5,000", "12.5%"],
        ["", "<b>Total Revenue</b>", "<b>3,385,000</b>", "<b>3,190,000</b>", "<b>195,000</b>", "<b>6.1%</b>"],
        ["", "", "", "", "", ""],
        ["5000", "Cost of Goods Sold - Materials", "980,000", "850,000", "-130,000", "-15.3%"],
        ["5100", "Cost of Goods Sold - Labor", "420,000", "400,000", "-20,000", "-5.0%"],
        ["5200", "Manufacturing Overhead", "215,000", "200,000", "-15,000", "-7.5%"],
        ["", "<b>Total COGS</b>", "<b>1,615,000</b>", "<b>1,450,000</b>", "<b>-165,000</b>", "<b>-11.4%</b>"],
        ["", "", "", "", "", ""],
        ["", "<b>Gross Profit</b>", "<b>1,770,000</b>", "<b>1,740,000</b>", "<b>30,000</b>", "<b>1.7%</b>"],
        ["", "", "", "", "", ""],
        ["6000", "Payroll Expenses", "650,000", "620,000", "-30,000", "-4.8%"],
        ["6100", "Rent & Facilities", "120,000", "120,000", "0", "0.0%"],
        ["6200", "IT & Software Licenses", "95,000", "80,000", "-15,000", "-18.8%"],
        ["6300", "Marketing & Advertising", "180,000", "150,000", "-30,000", "-20.0%"],
        ["6400", "Professional Fees", "75,000", "60,000", "-15,000", "-25.0%"],
        ["6500", "Travel & Entertainment", "42,000", "35,000", "-7,000", "-20.0%"],
        ["6600", "Utilities & Telecom", "28,000", "30,000", "2,000", "6.7%"],
        ["6700", "Office Supplies", "15,000", "15,000", "0", "0.0%"],
        ["6800", "Depreciation", "85,000", "85,000", "0", "0.0%"],
        ["", "<b>Total Operating Expenses</b>", "<b>1,290,000</b>", "<b>1,195,000</b>", "<b>-95,000</b>", "<b>-7.9%</b>"],
        ["", "", "", "", "", ""],
        ["", "<b>Operating Profit (EBIT)</b>", "<b>480,000</b>", "<b>545,000</b>", "<b>-65,000</b>", "<b>-11.9%</b>"],
        ["", "", "", "", "", ""],
        ["7000", "Interest Income", "8,000", "5,000", "3,000", "60.0%"],
        ["7100", "Interest Expense", "-25,000", "-20,000", "-5,000", "-25.0%"],
        ["7200", "Foreign Exchange Gain/Loss", "-12,000", "0", "-12,000", "n/a"],
        ["", "<b>Net Profit Before Tax</b>", "<b>451,000</b>", "<b>530,000</b>", "<b>-79,000</b>", "<b>-14.9%</b>"],
        ["", "", "", "", "", ""],
        ["8000", "Income Tax Expense", "-112,750", "-132,500", "19,750", "14.9%"],
        ["", "", "", "", "", ""],
        ["", "<b>Net Profit After Tax</b>", "<b>338,250</b>", "<b>397,500</b>", "<b>-59,250</b>", "<b>-14.9%</b>"],
    ]

    # Create table
    table = Table(data, colWidths=[60, 150, 80, 80, 80, 50])

    # Styling
    table.setStyle(TableStyle([
        # Header row
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#003366')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),

        # Data rows
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ALIGN', (2, 1), (-1, -1), 'RIGHT'),
        ('ALIGN', (0, 1), (1, -1), 'LEFT'),

        # Grid
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('LINEBELOW', (0, 0), (-1, 0), 2, colors.HexColor('#003366')),

        # Bold totals
        ('FONTNAME', (1, 5), (1, 5), 'Helvetica-Bold'),
        ('FONTNAME', (1, 10), (1, 10), 'Helvetica-Bold'),
        ('FONTNAME', (1, 12), (1, 12), 'Helvetica-Bold'),
        ('FONTNAME', (1, 21), (1, 21), 'Helvetica-Bold'),
        ('FONTNAME', (1, 23), (1, 23), 'Helvetica-Bold'),
        ('FONTNAME', (1, 27), (1, 27), 'Helvetica-Bold'),
        ('FONTNAME', (1, 29), (1, 29), 'Helvetica-Bold'),

        # Highlight unfavorable variances in red
        ('TEXTCOLOR', (4, 7), (5, 9), colors.red),  # COGS variances
        ('TEXTCOLOR', (4, 14), (5, 14), colors.red),  # Payroll
        ('TEXTCOLOR', (4, 16), (5, 16), colors.red),  # IT
        ('TEXTCOLOR', (4, 17), (5, 17), colors.red),  # Marketing
        ('TEXTCOLOR', (4, 18), (5, 18), colors.red),  # Professional fees
        ('TEXTCOLOR', (4, 19), (5, 19), colors.red),  # Travel
        ('TEXTCOLOR', (4, 26), (5, 26), colors.red),  # FX loss
        ('TEXTCOLOR', (4, 27), (5, 27), colors.red),  # Net profit variance

        # Highlight favorable variances in green
        ('TEXTCOLOR', (4, 2), (5, 2), colors.green),  # Product revenue
        ('TEXTCOLOR', (4, 24), (5, 24), colors.green),  # Interest income
    ]))

    story.append(table)
    story.append(Spacer(1, 20))

    # Footer notes
    story.append(Paragraph("<b>Key Observations:</b>", styles['Heading3']))
    notes = """
    1. <b>Revenue Performance:</b> Product sales exceeded budget by 11.4% ($250k favorable),
       however service revenue underperformed by 6.3% ($60k unfavorable).<br/><br/>

    2. <b>Cost Overruns:</b> Material costs are significantly over budget by 15.3% ($130k),
       indicating potential supply chain issues or pricing increases.<br/><br/>

    3. <b>Operating Expense Issues:</b> Marketing spend exceeded budget by 20% ($30k) and
       Professional Fees by 25% ($15k). Both require immediate review.<br/><br/>

    4. <b>Bottom Line Impact:</b> Net profit is 14.9% below budget ($59k shortfall),
       primarily driven by higher COGS and increased operating expenses.<br/><br/>

    <b>Generated by SAP FI/CO System | Confidential</b>
    """
    story.append(Paragraph(notes, styles['Normal']))

    # Build PDF
    doc.build(story)
    print(f"✅ Sample SAP variance report created: {output_path}")
    return output_path


if __name__ == "__main__":
    create_sample_sap_variance_report()
