#!/usr/bin/env python3
"""
I.H.P. SBIR Phase I Application - PDF Generator
Cielo Azul LLC
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# Brand Colors
TEAL = HexColor('#0D9488')
DARK_TEAL = HexColor('#0F766E')
BLACK = HexColor('#0A0A0A')
WHITE = white
GRAY = HexColor('#6B7280')
LIGHT_GRAY = HexColor('#F3F4F6')

BASE_DIR = "/Users/ericdeloera/Downloads/luxx-haus 5"
OUTPUT_DIR = f"{BASE_DIR}/docs"

def create_sbir_application():
    """Generate SBIR Phase I Application PDF"""

    filename = f"{OUTPUT_DIR}/IHP_SBIR_Phase_I_Application.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=TEAL,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )

    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=TEAL,
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )

    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=DARK_TEAL,
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )

    h3_style = ParagraphStyle(
        'H3',
        parent=styles['Heading3'],
        fontSize=11,
        textColor=BLACK,
        spaceBefore=10,
        spaceAfter=5,
        fontName='Helvetica-Bold'
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        textColor=BLACK,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )

    bullet_style = ParagraphStyle(
        'Bullet',
        parent=styles['Normal'],
        fontSize=10,
        textColor=BLACK,
        leftIndent=20,
        spaceAfter=4,
        leading=13
    )

    # Build document
    story = []

    # === COVER PAGE ===
    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("SBIR PHASE I APPLICATION", title_style))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Intelligent Home Protection (I.H.P.)",
                          ParagraphStyle('Subtitle', parent=styles['Heading2'],
                                        fontSize=18, alignment=TA_CENTER, textColor=BLACK)))
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Multi-Peril Correlation Platform for Residential Loss Prevention",
                          ParagraphStyle('Subtitle2', parent=styles['Normal'],
                                        fontSize=12, alignment=TA_CENTER, textColor=GRAY)))

    story.append(Spacer(1, 1*inch))

    # Cover info table
    cover_data = [
        ['Applicant:', 'Cielo Azul LLC'],
        ['Principal Investigator:', 'Eric De Loera'],
        ['Address:', '4801 N Blackwelder Ave, Oklahoma City, OK 73118'],
        ['Requested Amount:', '$274,363'],
        ['Project Duration:', '6 Months'],
        ['Target Agencies:', 'DOE / NSF / DHS'],
    ]

    cover_table = Table(cover_data, colWidths=[2*inch, 4*inch])
    cover_table.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('TEXTCOLOR', (0, 0), (0, -1), TEAL),
        ('ALIGN', (0, 0), (0, -1), 'RIGHT'),
        ('ALIGN', (1, 0), (1, -1), 'LEFT'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(cover_table)

    story.append(Spacer(1, 1.5*inch))
    story.append(Paragraph("CONFIDENTIAL",
                          ParagraphStyle('Conf', parent=styles['Normal'],
                                        fontSize=10, alignment=TA_CENTER, textColor=GRAY)))
    story.append(Paragraph("Prepared by De Loera Development | December 2024",
                          ParagraphStyle('Date', parent=styles['Normal'],
                                        fontSize=10, alignment=TA_CENTER, textColor=GRAY)))

    story.append(PageBreak())

    # === SECTION 1: TECHNICAL ABSTRACT ===
    story.append(Paragraph("SECTION 1: TECHNICAL ABSTRACT", h1_style))

    abstract = """The Intelligent Home Protection (I.H.P.) platform addresses the $150 billion annual property insurance loss crisis through an innovative multi-peril correlation monitoring system. Unlike existing single-peril solutions (water-only, fire-only), I.H.P. integrates five sensor modules—water, electrical, structural, HVAC, and environmental—into a unified Matter 1.4-compliant platform that detects cross-peril failure cascades before catastrophic loss occurs.

Current competitors achieve 70-99% claim reduction for individual perils but miss correlated failures (e.g., electrical faults causing water pump failures, HVAC strain indicating electrical degradation). I.H.P.'s proprietary correlation engine analyzes multi-sensor data streams to predict compound failures, reducing false positives while increasing actionable prevention alerts.

Phase I will develop and validate the correlation algorithm using simulated multi-peril scenarios, design the sensor module architecture using Nordic nRF5340 MCUs with Thread mesh networking, and establish baseline detection accuracy metrics. Successful completion positions I.H.P. for Phase II hardware prototyping and pilot deployment with insurance carrier partners.

The platform's Tesla Powerwall integration capability and Matter 1.4 compliance enable seamless adoption within the 5,000+ device smart home ecosystem, addressing a market projected to reach $13.47 billion by 2033."""

    story.append(Paragraph(abstract, body_style))

    story.append(Spacer(1, 0.3*inch))

    # === SECTION 2: PROBLEM STATEMENT ===
    story.append(Paragraph("SECTION 2: IDENTIFICATION AND SIGNIFICANCE OF PROBLEM", h1_style))

    story.append(Paragraph("2.1 The Problem: Annual Property Losses", h2_style))

    problem_data = [
        ['Metric', 'Annual Value'],
        ['Total Property Insurance Claims', '$150 billion'],
        ['Water Damage Claims', '$15 billion'],
        ['Fire Damage Claims', '$13 billion'],
        ['Water Damage Incidents', '14,000 per day'],
        ['House Fires', '344,600 annually'],
        ['Average Water Damage Claim', '$14,000 - $15,400'],
    ]

    problem_table = Table(problem_data, colWidths=[3.5*inch, 2.5*inch])
    problem_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(problem_table)

    story.append(Paragraph("2.2 Current Solution Limitations", h2_style))

    story.append(Paragraph("Existing smart home protection solutions address only single perils:", body_style))

    comp_data = [
        ['Competitor', 'Peril Coverage', 'Limitation'],
        ['Flo by Moen', 'Water only', 'Misses electrical-water correlations'],
        ['Ting / Whisker Labs', 'Electrical only', 'No water or structural monitoring'],
        ['LeakBot', 'Water only', 'No predictive capabilities'],
        ['Phyn', 'Water only', 'No multi-peril correlation'],
        ['Nest Protect', 'Smoke/CO only', 'Reactive, not preventive'],
    ]

    comp_table = Table(comp_data, colWidths=[1.8*inch, 1.5*inch, 2.7*inch])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(comp_table)

    story.append(Paragraph("2.3 The Gap", h2_style))

    gap_text = """<b>No existing platform correlates multiple perils to detect compound failure cascades.</b>

Example: An HVAC compressor drawing excess current (electrical anomaly) may indicate bearing failure, which can cause refrigerant leak (environmental), which can lead to water condensation backup (water damage), which can cause foundation moisture (structural).

I.H.P. is the first platform designed to detect these cross-peril correlations before catastrophic loss occurs."""
    story.append(Paragraph(gap_text, body_style))

    story.append(Paragraph("2.4 Market Validation", h2_style))

    story.append(Paragraph("Competitor results prove market demand:", body_style))

    bullets = [
        "• Flo by Moen: 96% reduction in water claims (LexisNexis study)",
        "• Ting: 80% of electrical fires predicted and prevented",
        "• LeakBot: 70% reduction in water damage claim costs",
        "• Phyn: 99% less likely to experience water leak claim",
    ]
    for b in bullets:
        story.append(Paragraph(b, bullet_style))

    story.append(Paragraph("Insurance carriers actively investing in smart home loss prevention:", body_style))

    bullets2 = [
        "• Nationwide: Ting, LeakBot, Phyn partnerships",
        "• State Farm: ADT, Ting partnerships",
        "• Liberty Mutual: Flo by Moen partnership",
        "• USAA, Chubb, Allstate: Multiple smart home programs",
    ]
    for b in bullets2:
        story.append(Paragraph(b, bullet_style))

    story.append(PageBreak())

    # === SECTION 3: TECHNICAL OBJECTIVES ===
    story.append(Paragraph("SECTION 3: TECHNICAL OBJECTIVES", h1_style))

    story.append(Paragraph("3.1 Phase I Objectives", h2_style))

    obj_data = [
        ['Obj', 'Description', 'Success Metric'],
        ['O1', 'Develop multi-peril correlation algorithm', '85%+ accuracy on 3+ compound scenarios'],
        ['O2', 'Design sensor module architecture', 'Complete schematics for 5 modules'],
        ['O3', 'Validate Matter 1.4 protocol integration', 'Communication with 2+ Matter controllers'],
        ['O4', 'Establish detection baseline', '<5% false positive, <30s latency'],
        ['O5', 'Complete insurance data integration spec', 'API specification document'],
    ]

    obj_table = Table(obj_data, colWidths=[0.5*inch, 2.8*inch, 2.7*inch])
    obj_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(obj_table)

    story.append(Paragraph("3.2 Sensor Module Architecture", h2_style))

    sensor_data = [
        ['Module', 'Sensors', 'Key Measurements'],
        ['WTR-X1 (Water)', 'Pressure, flow, moisture', 'PSI, GPM, humidity %'],
        ['ELC-X1 (Electrical)', 'Arc fault, power quality', 'Voltage, current, harmonics'],
        ['STR-X1 (Structural)', 'Accelerometer, tilt', 'Vibration, settlement'],
        ['HVC-X1 (HVAC)', 'Current, temperature', 'Compressor health, efficiency'],
        ['ENV-X1 (Environmental)', 'Smoke, CO, temp, humidity', 'PPM, °F, RH%'],
    ]

    sensor_table = Table(sensor_data, colWidths=[1.8*inch, 2*inch, 2.2*inch])
    sensor_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(sensor_table)

    story.append(Paragraph("3.3 Technical Approach", h2_style))

    approach = """<b>Hardware Platform:</b> Nordic nRF5340 dual-core MCU with dedicated application and network processors. Thread mesh networking provides resilience and self-healing connectivity. Matter 1.4 native compliance ensures interoperability with Apple HomeKit, Google Home, Amazon Alexa, and Samsung SmartThings.

<b>Correlation Algorithm:</b> Multi-sensor data fusion using time-series analysis with machine learning models for anomaly correlation. Rule-based logic handles known failure cascades while ML detects novel patterns. Confidence scoring prioritizes actionable alerts.

<b>Power Design:</b> Ultra-low-power operation targeting 3+ year battery life for wireless sensors. Solar charging option for outdoor modules."""
    story.append(Paragraph(approach, body_style))

    # === SECTION 4: WORK PLAN ===
    story.append(Paragraph("SECTION 4: WORK PLAN AND SCHEDULE", h1_style))

    story.append(Paragraph("4.1 Phase I Timeline (6 Months)", h2_style))

    timeline_data = [
        ['Month', 'Tasks', 'Deliverables'],
        ['1-2', 'Algorithm design, literature review, failure mode analysis', 'Technical specification document'],
        ['3-4', 'Algorithm development, simulation environment setup', 'Working correlation engine (software)'],
        ['5', 'Hardware architecture design, component selection', 'Sensor module schematics'],
        ['6', 'Integration testing, Matter 1.4 validation, reporting', 'Final report, Phase II proposal'],
    ]

    timeline_table = Table(timeline_data, colWidths=[0.8*inch, 2.7*inch, 2.5*inch])
    timeline_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(timeline_table)

    story.append(Paragraph("4.2 Milestones", h2_style))

    mile_data = [
        ['Milestone', 'Month', 'Success Criteria'],
        ['M1: Algorithm Spec Complete', '2', 'Documented correlation logic for 10+ failure scenarios'],
        ['M2: Simulation Environment', '3', 'Functional test bed for multi-sensor data'],
        ['M3: Correlation Engine v1.0', '4', '85%+ detection accuracy on test data'],
        ['M4: Hardware Design Complete', '5', 'PCB schematics for all 5 modules'],
        ['M5: Matter Validation', '6', 'Successful interop with Apple/Google/Amazon'],
    ]

    mile_table = Table(mile_data, colWidths=[2.2*inch, 0.8*inch, 3*inch])
    mile_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(mile_table)

    story.append(PageBreak())

    # === SECTION 5: COMMERCIALIZATION ===
    story.append(Paragraph("SECTION 5: COMMERCIALIZATION PLAN", h1_style))

    story.append(Paragraph("5.1 Market Opportunity", h2_style))

    market_data = [
        ['Segment', '2024 Value', '2033 Value', 'CAGR'],
        ['Smart Home Insurance', '$3.67B', '$13.47B', '18.25%'],
        ['Smart Home Security', '$35.02B', '$145.54B', '15.31%'],
        ['Total Home Insurance', '$234.6B', '$576B', '7.6%'],
    ]

    market_table = Table(market_data, colWidths=[2*inch, 1.3*inch, 1.3*inch, 1*inch])
    market_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(market_table)

    story.append(Paragraph("5.2 Target Customers", h2_style))

    story.append(Paragraph("<b>Primary: Insurance Carriers</b>", body_style))
    story.append(Paragraph("Tier 1 (Already Investing): Nationwide, State Farm, Liberty Mutual, USAA, Chubb", bullet_style))
    story.append(Paragraph("Tier 2 (Open to Partnerships): Allstate, American Family, Farmers, Amica", bullet_style))
    story.append(Paragraph("Tier 3 (Specialty): PURE, VYRD, Hippo, SageSure", bullet_style))

    story.append(Paragraph("<b>Secondary: Homeowners (Direct-to-Consumer)</b>", body_style))
    story.append(Paragraph("94 million US households with security systems. 50%+ homes with security cameras.", bullet_style))

    story.append(Paragraph("<b>Tertiary: Contractors (LUXX BUILDZ Tech Platform)</b>", body_style))
    story.append(Paragraph("Multi-job site monitoring, labor/material tracking, Procore/Buildertrend integration.", bullet_style))

    story.append(Paragraph("5.3 Business Model", h2_style))

    biz_data = [
        ['Revenue Stream', 'Model', 'Target Price'],
        ['Hardware Sales', 'One-time purchase', '$500-800 per home'],
        ['Monitoring Subscription', 'Monthly recurring', '$15-25/month'],
        ['Insurance Data Licensing', 'Per-home fee from carriers', '$3-5/month per home'],
        ['Contractor Platform', 'SaaS subscription', '$99-299/month'],
    ]

    biz_table = Table(biz_data, colWidths=[2*inch, 2*inch, 2*inch])
    biz_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(biz_table)

    story.append(Paragraph("5.4 Competitive Advantages", h2_style))

    adv_data = [
        ['Feature', 'Competitors', 'I.H.P.'],
        ['Multi-peril correlation', '✗', '✓'],
        ['Insurance-grade data', '✗', '✓'],
        ['Matter 1.4 native', 'Partial', '✓'],
        ['Tesla integration ready', '✗', '✓'],
        ['Contractor platform', '✗', '✓'],
    ]

    adv_table = Table(adv_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
    adv_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(adv_table)

    story.append(PageBreak())

    # === SECTION 6: BUDGET ===
    story.append(Paragraph("SECTION 6: BUDGET SUMMARY", h1_style))

    story.append(Paragraph("Phase I Budget (6 Months) - Total: $274,363", h2_style))

    budget_data = [
        ['Category', 'Amount', '% of Total'],
        ['PERSONNEL', '$150,000', '55%'],
        ['   Principal Investigator', '$60,000', ''],
        ['   Hardware Engineer (contract)', '$50,000', ''],
        ['   Software Engineer (contract)', '$40,000', ''],
        ['EQUIPMENT', '$30,000', '11%'],
        ['   Dev kits, components', '$15,000', ''],
        ['   Test equipment', '$10,000', ''],
        ['   Prototyping materials', '$5,000', ''],
        ['SUPPLIES', '$10,000', '4%'],
        ['CONSULTANTS', '$25,000', '9%'],
        ['   Matter/Thread expert', '$15,000', ''],
        ['   Insurance industry advisor', '$10,000', ''],
        ['OTHER DIRECT COSTS', '$20,000', '7%'],
        ['   Cloud computing', '$8,000', ''],
        ['   Software licenses', '$7,000', ''],
        ['   Travel (conferences)', '$5,000', ''],
        ['INDIRECT COSTS', '$39,363', '14%'],
        ['TOTAL', '$274,363', '100%'],
    ]

    budget_table = Table(budget_data, colWidths=[3.5*inch, 1.5*inch, 1*inch])
    budget_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('BACKGROUND', (0, -1), (-1, -1), TEAL),
        ('TEXTCOLOR', (0, -1), (-1, -1), WHITE),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'RIGHT'),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -2), WHITE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(budget_table)

    # === SECTION 7: AGENCY TARGETING ===
    story.append(Paragraph("SECTION 7: AGENCY-SPECIFIC TARGETING", h1_style))

    story.append(Paragraph("7.1 DOE (Department of Energy) - PRIMARY TARGET", h2_style))
    story.append(Paragraph("<b>Topic Area:</b> Buildings / Smart Grid / Energy Efficiency", body_style))
    story.append(Paragraph("<b>Pitch Angle:</b> I.H.P. HVAC monitoring reduces energy waste by detecting inefficient operation. Tesla Powerwall integration enables grid-responsive home energy management. HVAC accounts for 50%+ of home energy use; early detection = 10-30% energy savings.", body_style))

    story.append(Paragraph("7.2 NSF (National Science Foundation)", h2_style))
    story.append(Paragraph("<b>Topic Area:</b> IoT / Cyber-Physical Systems / Machine Learning", body_style))
    story.append(Paragraph("<b>Pitch Angle:</b> Novel multi-sensor correlation algorithm using ML for predictive failure detection. First platform to correlate 5 perils in residential setting. Broader impacts: home safety, insurance affordability.", body_style))

    story.append(Paragraph("7.3 DHS (Department of Homeland Security)", h2_style))
    story.append(Paragraph("<b>Topic Area:</b> Critical Infrastructure / Resilience", body_style))
    story.append(Paragraph("<b>Pitch Angle:</b> Residential resilience against fire, water, electrical hazards. Mass casualty prevention through early fire/CO detection. I.H.P. provides 10-15 minute early warning vs. smoke detectors.", body_style))

    story.append(PageBreak())

    # === SECTION 8: NEXT STEPS ===
    story.append(Paragraph("SECTION 8: SUBMISSION CHECKLIST", h1_style))

    story.append(Paragraph("Required Registrations", h2_style))

    reg_bullets = [
        "☐ SBIR.gov account",
        "☐ Grants.gov account",
        "☐ SAM.gov registration (REQUIRED)",
        "☐ D-U-N-S number verified ✓",
    ]
    for b in reg_bullets:
        story.append(Paragraph(b, bullet_style))

    story.append(Paragraph("Required Documents", h2_style))

    doc_bullets = [
        "☐ Cielo Azul LLC Articles of Organization",
        "☐ EIN Letter",
        "☐ Principal Investigator Resume/CV",
        "☐ Key Personnel Resumes",
        "☐ Facilities Description",
        "☐ Letters of Support (insurance carriers)",
        "☐ Commercialization Letters of Intent",
        "☐ Subcontractor Quotes (if applicable)",
    ]
    for b in doc_bullets:
        story.append(Paragraph(b, bullet_style))

    story.append(Paragraph("Submission Timeline", h2_style))

    story.append(Paragraph("<b>DOE SBIR Solicitations:</b> May-August and September-January", body_style))
    story.append(Paragraph("<b>NSF SBIR Solicitations:</b> January-April and June-August", body_style))
    story.append(Paragraph("<b>Check weekly:</b> sbir.gov for open opportunities", body_style))

    story.append(Spacer(1, 0.5*inch))

    # Footer
    story.append(Paragraph("─" * 60, body_style))
    story.append(Paragraph("CONFIDENTIAL - Cielo Azul LLC",
                          ParagraphStyle('Footer', parent=styles['Normal'],
                                        fontSize=9, alignment=TA_CENTER, textColor=GRAY)))
    story.append(Paragraph("Prepared by De Loera Development | December 2024",
                          ParagraphStyle('Footer2', parent=styles['Normal'],
                                        fontSize=9, alignment=TA_CENTER, textColor=GRAY)))

    # Build PDF
    doc.build(story)
    print(f"  Created: {filename}")
    return filename


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING I.H.P. SBIR PHASE I APPLICATION")
    print("Cielo Azul LLC")
    print("=" * 60)
    print()

    filename = create_sbir_application()

    print()
    print("=" * 60)
    print("SBIR APPLICATION PDF CREATED")
    print("=" * 60)
    print(f"\nLocation: {filename}")
    print("\nOpening PDF...")
    os.system(f'open "{filename}"')
