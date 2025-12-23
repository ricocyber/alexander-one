#!/usr/bin/env python3
"""
I.H.P. - Intelligent Home Protection
Market Research & Data Intelligence Report PDF Generator
"""

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, ListFlowable, ListItem
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
from reportlab.graphics.shapes import Drawing, Rect, String, Circle, Line
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.piecharts import Pie
from reportlab.graphics.charts.linecharts import HorizontalLineChart
import os

LOGO_PATH = "/Users/ericdeloera/Downloads/luxx-haus 5/assets/luxx_logo_light.png"
ICON_PATH = "/Users/ericdeloera/Downloads/luxx-haus 5/assets/luxx_icon.png"

# Color palette
PRIMARY_DARK = colors.HexColor('#1a1a2e')
PRIMARY_TEAL = colors.HexColor('#00b99b')
ACCENT_BLUE = colors.HexColor('#3282d2')
ACCENT_CYAN = colors.HexColor('#00d2be')
WARNING_RED = colors.HexColor('#dc3545')
SUCCESS_GREEN = colors.HexColor('#28a745')
LIGHT_GRAY = colors.HexColor('#f8f9fa')
MID_GRAY = colors.HexColor('#6c757d')

def create_header(canvas, doc):
    """Custom header with logo"""
    canvas.saveState()

    if os.path.exists(LOGO_PATH):
        canvas.drawImage(LOGO_PATH, inch, letter[1] - 0.85*inch,
                        width=2.2*inch, height=0.6*inch,
                        preserveAspectRatio=True, mask='auto')

    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawRightString(letter[0] - inch, letter[1] - 0.5*inch,
                          f"Market Research Report | {datetime.now().strftime('%B %Y')}")

    canvas.setStrokeColor(PRIMARY_TEAL)
    canvas.setLineWidth(2)
    canvas.line(inch, letter[1] - 0.95*inch, letter[0] - inch, letter[1] - 0.95*inch)
    canvas.restoreState()

def create_footer(canvas, doc):
    """Custom footer"""
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(MID_GRAY)
    canvas.drawString(inch, 0.5*inch, "CONFIDENTIAL - I.H.P. Intelligent Home Protection")
    canvas.drawRightString(letter[0] - inch, 0.5*inch, f"Page {doc.page}")
    canvas.restoreState()

def header_footer(canvas, doc):
    create_header(canvas, doc)
    create_footer(canvas, doc)

def create_bar_chart(data, labels, title, width=400, height=150):
    """Create a bar chart"""
    drawing = Drawing(width, height)

    bc = VerticalBarChart()
    bc.x = 50
    bc.y = 30
    bc.height = height - 50
    bc.width = width - 80
    bc.data = [data]
    bc.categoryAxis.categoryNames = labels
    bc.categoryAxis.labels.fontName = 'Helvetica'
    bc.categoryAxis.labels.fontSize = 8
    bc.categoryAxis.labels.angle = 45
    bc.categoryAxis.labels.boxAnchor = 'ne'
    bc.valueAxis.valueMin = 0
    bc.valueAxis.labels.fontName = 'Helvetica'
    bc.valueAxis.labels.fontSize = 8
    bc.bars[0].fillColor = PRIMARY_TEAL

    drawing.add(bc)
    return drawing

# Create PDF
output_path = "/Users/ericdeloera/Downloads/luxx-haus 5/IHP_Market_Research_Report.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=1.1*inch,
    bottomMargin=0.75*inch
)

# Styles
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='MainTitle',
    parent=styles['Heading1'],
    fontSize=32,
    textColor=PRIMARY_DARK,
    spaceAfter=10,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
))

styles.add(ParagraphStyle(
    name='Subtitle',
    parent=styles['Normal'],
    fontSize=16,
    textColor=MID_GRAY,
    spaceAfter=30,
    alignment=TA_CENTER
))

styles.add(ParagraphStyle(
    name='SectionHeader',
    parent=styles['Heading2'],
    fontSize=18,
    textColor=PRIMARY_DARK,
    spaceBefore=25,
    spaceAfter=12,
    fontName='Helvetica-Bold'
))

styles.add(ParagraphStyle(
    name='SubSection',
    parent=styles['Heading3'],
    fontSize=14,
    textColor=ACCENT_BLUE,
    spaceBefore=15,
    spaceAfter=8,
    fontName='Helvetica-Bold'
))

styles.add(ParagraphStyle(
    name='BodyTextCustom',
    parent=styles['Normal'],
    fontSize=10,
    textColor=colors.HexColor('#333333'),
    spaceAfter=8,
    alignment=TA_JUSTIFY,
    leading=14
))

styles.add(ParagraphStyle(
    name='DataPoint',
    parent=styles['Normal'],
    fontSize=11,
    textColor=PRIMARY_DARK,
    spaceAfter=6,
    fontName='Helvetica-Bold'
))

styles.add(ParagraphStyle(
    name='BigNumber',
    parent=styles['Normal'],
    fontSize=36,
    textColor=PRIMARY_TEAL,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
))

styles.add(ParagraphStyle(
    name='NumberLabel',
    parent=styles['Normal'],
    fontSize=10,
    textColor=MID_GRAY,
    alignment=TA_CENTER
))

styles.add(ParagraphStyle(
    name='Quote',
    parent=styles['Normal'],
    fontSize=12,
    textColor=PRIMARY_DARK,
    leftIndent=20,
    rightIndent=20,
    spaceAfter=15,
    fontName='Helvetica-Oblique',
    alignment=TA_CENTER
))

def create_metric_box(number, label, color=PRIMARY_TEAL):
    """Create a metric display"""
    return [
        Paragraph(number, ParagraphStyle('Num', fontSize=28, textColor=color,
                                         alignment=TA_CENTER, fontName='Helvetica-Bold')),
        Paragraph(label, ParagraphStyle('Lbl', fontSize=9, textColor=MID_GRAY,
                                        alignment=TA_CENTER))
    ]

# Build document
story = []

# ==================== TITLE PAGE ====================
story.append(Spacer(1, 1.5*inch))

if os.path.exists(LOGO_PATH):
    logo = Image(LOGO_PATH, width=5*inch, height=1.4*inch)
    logo.hAlign = 'CENTER'
    story.append(logo)

story.append(Spacer(1, 0.5*inch))
story.append(HRFlowable(width="50%", thickness=3, color=PRIMARY_TEAL, hAlign='CENTER'))
story.append(Spacer(1, 0.3*inch))

story.append(Paragraph("Market Research &<br/>Data Intelligence Report", styles['MainTitle']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Comprehensive Analysis of the Home Protection Technology Market", styles['Subtitle']))

story.append(Spacer(1, 0.8*inch))

# Key stats on cover
cover_stats = [
    ['$417B', '$150B', '96%', '$700B'],
    ['Economic Losses\n(2024)', 'Annual Insured\nLosses', 'Damage\nReduction', 'Reinsurance\nCapital Pool']
]
cover_table = Table(cover_stats, colWidths=[1.6*inch]*4)
cover_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 24),
    ('TEXTCOLOR', (0, 0), (-1, 0), PRIMARY_TEAL),
    ('FONTSIZE', (0, 1), (-1, 1), 9),
    ('TEXTCOLOR', (0, 1), (-1, 1), MID_GRAY),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
]))
story.append(cover_table)

story.append(Spacer(1, 1*inch))
story.append(Paragraph(f"Prepared: {datetime.now().strftime('%B %d, %Y')}",
                       ParagraphStyle('Date', fontSize=11, textColor=MID_GRAY, alignment=TA_CENTER)))
story.append(Paragraph("Version 1.0 | Confidential",
                       ParagraphStyle('Ver', fontSize=9, textColor=MID_GRAY, alignment=TA_CENTER)))

story.append(PageBreak())

# ==================== EXECUTIVE SUMMARY ====================
story.append(Paragraph("Executive Summary", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_DARK))
story.append(Spacer(1, 0.2*inch))

exec_text = """
I.H.P. (Intelligent Home Protection) addresses a <b>$50+ billion annual problem</b> in the US homeowners
insurance market through predictive, AI-driven home protection across multiple perils: water damage,
fire, electrical faults, structural integrity, and HVAC systems. Unlike single-peril competitors,
I.H.P. provides a unified, cross-correlated data platform that delivers unprecedented risk insights
to insurance carriers, reinsurers, and property portfolios.
"""
story.append(Paragraph(exec_text, styles['BodyTextCustom']))
story.append(Spacer(1, 0.2*inch))

# Value props
story.append(Paragraph("Proven Prevention Technology", styles['SubSection']))

prevention_data = [
    ['Technology', 'Claim Reduction', 'Source'],
    ['Smart Water Shutoff (Flo/Moen)', '96%', 'Moen Data'],
    ['Electrical Fire Prevention (Ting)', '80%', 'Whisker Labs'],
    ['Leak Detection (LeakBot/Ondo)', '70%', 'Consumer Intelligence Study'],
    ['Smart Water Sensors (General)', '39% frequency, 12% severity', 'Independent Actuarial Study'],
]
prev_table = Table(prevention_data, colWidths=[2.8*inch, 1.8*inch, 2*inch])
prev_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('TEXTCOLOR', (1, 1), (1, -1), SUCCESS_GREEN),
    ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
]))
story.append(prev_table)

story.append(PageBreak())

# ==================== THE PROBLEM ====================
story.append(Paragraph("1. The Problem: A $417 Billion Crisis", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=WARNING_RED))
story.append(Spacer(1, 0.2*inch))

problem_text = """
The property insurance industry is facing unprecedented losses. In 2024 alone, global natural disasters
resulted in <b>$417 billion in economic losses</b>, with insurers covering $137-154 billion. The US
accounted for 76% of global insured catastrophe losses. For the <b>fifth consecutive year</b>, insured
losses exceeded $100 billion, and experts project a new annual "normal" of $150 billion.
"""
story.append(Paragraph(problem_text, styles['BodyTextCustom']))
story.append(Spacer(1, 0.2*inch))

# Global losses table
story.append(Paragraph("Global Catastrophe Losses (2024)", styles['SubSection']))

cat_data = [
    ['Metric', 'Value', 'Source'],
    ['Total Economic Losses', '$417 billion', 'Gallagher Re'],
    ['Insured Losses', '$137-154 billion', 'Swiss Re / Gallagher'],
    ['US Share of Insured Losses', '76%', 'Gallagher Re'],
    ['Consecutive Years Above $100B', '5 years', 'Swiss Re'],
    ['Projected 2025 Losses', '$145 billion', 'Swiss Re'],
    ['New Annual "Normal"', '$150 billion', 'Gallagher Re'],
    ['Modeled Average Annual Loss', '$152 billion', 'Verisk'],
]
cat_table = Table(cat_data, colWidths=[2.5*inch, 2*inch, 2*inch])
cat_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), WARNING_RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
]))
story.append(cat_table)

story.append(Spacer(1, 0.3*inch))

# Homeowners specific
story.append(Paragraph("Homeowners Insurance: 7 Years of Losses", styles['SubSection']))

ho_text = """
The homeowners insurance segment has experienced <b>seven consecutive years of underwriting losses</b>.
In 2024, carriers collectively lost $2.2 billion on homeowners policies alone—an improvement from
the $15.2 billion loss in 2022, but still unprofitable. Insurance carriers are desperate for
loss prevention technology.
"""
story.append(Paragraph(ho_text, styles['BodyTextCustom']))

ho_data = [
    ['Metric', '2023', '2024', 'Change'],
    ['Combined Ratio', '101.8%', '96.6%', '-5.2 pts'],
    ['Loss Ratio', '66.5%', '61.6%', '-4.9 pts'],
    ['Net Underwriting Result', '-$22B', '+$25B', '$47B swing'],
    ['Homeowners Combined Ratio', '110.9%', '105.7%', 'Still unprofitable'],
    ['Homeowners Underwriting Loss', '-$15.2B', '-$2.2B', 'Improving'],
]
ho_table = Table(ho_data, colWidths=[2.2*inch, 1.3*inch, 1.3*inch, 1.5*inch])
ho_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('BACKGROUND', (0, 4), (-1, 5), colors.HexColor('#fff3cd')),
]))
story.append(ho_table)

story.append(PageBreak())

# ==================== WATER DAMAGE ====================
story.append(Paragraph("2. Water Damage: The $13 Billion Peril", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_BLUE))
story.append(Spacer(1, 0.2*inch))

water_text = """
Water damage is the <b>second most frequent type of insurance claim</b>, accounting for 22.6% of all
homeowner claims between 2019-2023. With 14,000 water damage incidents occurring daily and an average
claim of $15,400, this peril costs insurers approximately <b>$13 billion annually</b>.
"""
story.append(Paragraph(water_text, styles['BodyTextCustom']))

# Water stats
water_stats = [
    ['$13B', '14,000', '1 in 67', '$15,400'],
    ['Annual Claims Cost', 'Daily Incidents', 'Homes File Claims/Year', 'Average Claim']
]
water_stat_table = Table(water_stats, colWidths=[1.6*inch]*4)
water_stat_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 22),
    ('TEXTCOLOR', (0, 0), (-1, 0), ACCENT_BLUE),
    ('FONTSIZE', (0, 1), (-1, 1), 9),
    ('TEXTCOLOR', (0, 1), (-1, 1), MID_GRAY),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('BACKGROUND', (0, 0), (-1, -1), LIGHT_GRAY),
]))
story.append(water_stat_table)
story.append(Spacer(1, 0.2*inch))

# Water heater stats
story.append(Paragraph("Water Heater Failure Statistics", styles['SubSection']))

wh_text = """
Water heater failures represent a significant portion of water damage claims. According to IBHS,
<b>69% of water heater failures</b> result from slow leaks or sudden bursts. By year 9, more than
40% of water heaters have burst, and the average claim costs $4,444.
"""
story.append(Paragraph(wh_text, styles['BodyTextCustom']))

wh_data = [
    ['Metric', 'Value'],
    ['Failures from leak/burst', '69%'],
    ['Average lifespan', '8-12 years'],
    ['Burst rate by year 9', '40%+'],
    ['Failure rate by year 6', '15%'],
    ['Tank capacity (potential damage)', '20-80 gallons'],
    ['Average claim', '$4,444'],
]
wh_table = Table(wh_data, colWidths=[3.5*inch, 2.5*inch])
wh_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
]))
story.append(wh_table)

story.append(PageBreak())

# ==================== FIRE & ELECTRICAL ====================
story.append(Paragraph("3. Fire & Electrical: The $12.7 Billion Threat", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=WARNING_RED))
story.append(Spacer(1, 0.2*inch))

fire_text = """
Fire damage costs the US <b>$11.3 billion annually</b>, with an additional $1.4 billion from electrical
fires specifically. A house fire occurs every 87 seconds, and homes burn <b>8x faster today</b> than
50 years ago due to synthetic materials. The critical insight: <b>90% of house fires are preventable</b>.
"""
story.append(Paragraph(fire_text, styles['BodyTextCustom']))

# Fire stats
fire_stats = [
    ['344,600', '$77,340', '87 sec', '90%'],
    ['House Fires (2023)', 'Avg Fire Claim', 'Fire Frequency', 'Preventable']
]
fire_stat_table = Table(fire_stats, colWidths=[1.6*inch]*4)
fire_stat_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 22),
    ('TEXTCOLOR', (0, 0), (-1, 0), WARNING_RED),
    ('FONTSIZE', (0, 1), (-1, 1), 9),
    ('TEXTCOLOR', (0, 1), (-1, 1), MID_GRAY),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8d7da')),
]))
story.append(fire_stat_table)
story.append(Spacer(1, 0.2*inch))

# Electrical
story.append(Paragraph("Electrical Fire Statistics", styles['SubSection']))

elec_data = [
    ['Metric', 'Value'],
    ['Electrical fires annually', '47,700'],
    ['Annual property damage', '$1.3-1.4 billion'],
    ['Deaths per year', '418'],
    ['Injuries per year', '1,570'],
    ['Night fires (10PM-6AM)', '50%+ of house fires'],
    ['Homes without working smoke alarm (deaths)', '59%'],
]
elec_table = Table(elec_data, colWidths=[3.5*inch, 2.5*inch])
elec_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), WARNING_RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
]))
story.append(elec_table)

story.append(Spacer(1, 0.2*inch))

# Ting highlight
ting_text = """
<b>Smart Electrical Monitoring (Ting/Whisker Labs):</b> Analyzes 30 million electrical signals per second,
detecting micro-arcs and spark signatures. Proven to prevent ~80% of electrical fires. Trusted by
over 1 million homes, saving 15,000+ families from devastating fires.
"""
story.append(Paragraph(ting_text, styles['BodyTextCustom']))

story.append(PageBreak())

# ==================== STRUCTURAL & HVAC ====================
story.append(Paragraph("4. Structural & HVAC Monitoring", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_TEAL))
story.append(Spacer(1, 0.2*inch))

struct_text = """
Foundation damage and HVAC failures represent significant costs that are often NOT covered by standard
insurance policies. Foundation repairs range from <b>$2,220 to $100,000+</b>, while standard policies
exclude gradual settlement and wear-and-tear damage. This creates a massive opportunity for predictive
monitoring technology.
"""
story.append(Paragraph(struct_text, styles['BodyTextCustom']))

# Structural sensors
story.append(Paragraph("IoT Structural Monitoring Technology", styles['SubSection']))

struct_data = [
    ['Sensor Type', 'Function', 'Application'],
    ['Accelerometers', 'Vibration & movement detection', 'Structural shifts, seismic'],
    ['Strain Gauges', 'Material deformation monitoring', 'Stress levels, crack detection'],
    ['Inclinometer/Tilt', 'Foundation movement tracking', 'Settlement, collapse warning'],
    ['Piezometers', 'Fluid pressure monitoring', 'Water intrusion, soil moisture'],
    ['MEMS Sensors', 'Low-cost wireless monitoring', 'Residential-scale deployment'],
]
struct_table = Table(struct_data, colWidths=[1.8*inch, 2.2*inch, 2.2*inch])
struct_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_TEAL),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
]))
story.append(struct_table)

story.append(Spacer(1, 0.2*inch))

# HVAC
story.append(Paragraph("HVAC/Boiler Failure Data", styles['SubSection']))

hvac_text = """
HVAC failures account for significant insurance claims, with <b>44% caused by wear and tear</b>
(typically not covered). Power surges affect 10% of boiler claims. Equipment breakdown coverage
costs only $25-50/year as an add-on but provides critical protection.
"""
story.append(Paragraph(hvac_text, styles['BodyTextCustom']))

hvac_data = [
    ['Cause of Loss', 'Percentage', 'Coverage Status'],
    ['Wear and Tear', '44%', 'NOT Covered'],
    ['Power Surges', '10%', 'Usually Covered'],
    ['Theft/Vandalism', '2%', 'Covered'],
    ['Sudden Explosion/Crack', 'Varies', 'Covered'],
]
hvac_table = Table(hvac_data, colWidths=[2.5*inch, 1.5*inch, 2*inch])
hvac_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('TEXTCOLOR', (2, 1), (2, 1), WARNING_RED),
    ('FONTNAME', (2, 1), (2, 1), 'Helvetica-Bold'),
]))
story.append(hvac_table)

story.append(PageBreak())

# ==================== MARKET OPPORTUNITY ====================
story.append(Paragraph("5. The $700 Billion Market Opportunity", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=SUCCESS_GREEN))
story.append(Spacer(1, 0.2*inch))

market_text = """
The global smart home market is projected to reach <b>$300-633 billion by 2030</b>, with security
and monitoring representing the largest segment (29%+). The reinsurance capital pool exceeds
<b>$700 billion</b>, and insurers are actively seeking data-driven loss prevention solutions.
"""
story.append(Paragraph(market_text, styles['BodyTextCustom']))

# Reinsurance capital
story.append(Paragraph("Reinsurance Capital Pool", styles['SubSection']))

reins_data = [
    ['Capital Type', 'Amount'],
    ['Traditional Reinsurance Capital', '~$500 billion'],
    ['Alternative Capital (Cat Bonds)', '~$50 billion'],
    ['Global Reinsurer Capital (Aon)', '~$700 billion'],
]
reins_table = Table(reins_data, colWidths=[4*inch, 2.5*inch])
reins_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), SUCCESS_GREEN),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('FONTNAME', (1, 1), (1, -1), 'Helvetica-Bold'),
]))
story.append(reins_table)

story.append(Spacer(1, 0.2*inch))

# Smart home market
story.append(Paragraph("Smart Home Market Projections", styles['SubSection']))

sh_data = [
    ['Year', 'Market Size', 'CAGR'],
    ['2024', '$121-128 billion', '-'],
    ['2025', '$147 billion', '~23%'],
    ['2030', '$300-633 billion', '15-27%'],
    ['Matter Devices by 2030', '5.5 billion', '-'],
]
sh_table = Table(sh_data, colWidths=[2.2*inch, 2.2*inch, 2*inch])
sh_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
]))
story.append(sh_table)

story.append(PageBreak())

# ==================== WHO PAYS ====================
story.append(Paragraph("6. Enterprise Revenue Model", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_TEAL))
story.append(Spacer(1, 0.2*inch))

revenue_text = """
I.H.P.'s data platform generates revenue from multiple enterprise tiers. The primary value proposition
is <b>loss prevention data</b> that helps insurance carriers reduce claims, improve underwriting, and
increase retention. According to McKinsey, analytics can improve loss ratios by 3-5 percentage points.
"""
story.append(Paragraph(revenue_text, styles['BodyTextCustom']))

# Tier 1
story.append(Paragraph("Tier 1: Insurance Carriers", styles['SubSection']))

t1_data = [
    ['Carrier Size', 'Annual Value', 'Use Case'],
    ['Top 10 P&C Carriers', '$10-50M each', 'Portfolio-wide risk reduction'],
    ['Regional Carriers (100+)', '$1-5M each', 'Underwriting data, loss prevention'],
    ['MGAs/MGUs', '$500K-2M each', 'Risk selection, pricing'],
]
t1_table = Table(t1_data, colWidths=[2.2*inch, 1.8*inch, 2.5*inch])
t1_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_TEAL),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
]))
story.append(t1_table)

story.append(Spacer(1, 0.15*inch))

# Tier 2
story.append(Paragraph("Tier 2: Reinsurers (Data Licensing)", styles['SubSection']))

t2_data = [
    ['Company', 'Potential Value', 'Use Case'],
    ['Swiss Re', '$20-100M', 'Catastrophe modeling enhancement'],
    ['Munich Re', '$20-100M', 'Risk portfolio optimization'],
    ['Berkshire Hathaway', '$50-200M', 'Loss prediction, reserving'],
    ["Lloyd's Syndicates", '$5-20M each', 'Treaty pricing'],
]
t2_table = Table(t2_data, colWidths=[2.2*inch, 1.8*inch, 2.5*inch])
t2_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
]))
story.append(t2_table)

story.append(Spacer(1, 0.15*inch))

# Tier 3
story.append(Paragraph("Tier 3: Real Estate Portfolios", styles['SubSection']))

t3_data = [
    ['Segment', 'Properties', 'Annual Value'],
    ['Multifamily REITs', '500K+ units', '$50-100M'],
    ['Single-Family Rental', '1M+ homes', '$100-200M'],
    ['Commercial REITs', '50K+ properties', '$25-50M'],
]
t3_table = Table(t3_data, colWidths=[2.2*inch, 2*inch, 2.3*inch])
t3_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
]))
story.append(t3_table)

story.append(PageBreak())

# ==================== 10-YEAR MODEL ====================
story.append(Paragraph("7. The 10-Year Financial Model", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=SUCCESS_GREEN))
story.append(Spacer(1, 0.2*inch))

# Aggressive scenario
story.append(Paragraph("Aggressive Scenario (Major Carrier Partnerships)", styles['SubSection']))

fin_data = [
    ['Year', 'Homes Monitored', 'Data Revenue', 'Platform Fees', 'Total'],
    ['2025', '200,000', '$20M', '$50M', '$70M'],
    ['2027', '2,000,000', '$300M', '$800M', '$1.1B'],
    ['2030', '20,000,000', '$2B', '$8B', '$10B'],
    ['2035', '100,000,000', '$8B', '$40B', '$48B'],
]
fin_table = Table(fin_data, colWidths=[1*inch, 1.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
fin_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), SUCCESS_GREEN),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('FONTNAME', (-1, -1), (-1, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (-1, -1), (-1, -1), SUCCESS_GREEN),
    ('FONTSIZE', (-1, -1), (-1, -1), 12),
]))
story.append(fin_table)

story.append(Spacer(1, 0.3*inch))

# Value creation
story.append(Paragraph("Value Creation for Partners (Annual)", styles['SubSection']))

value_data = [
    ['Partner', 'Current Annual Loss', 'I.H.P. Reduction', 'Value Created'],
    ['Top 10 Insurers', '$50B claims', '20% reduction', '$10B/year'],
    ['Reinsurers', '$150B cat losses', '5% improvement', '$7.5B/year'],
    ['REITs', '$20B maintenance', '15% reduction', '$3B/year'],
    ['Homeowners', '$21B premium increase', 'Offset', '$21B value'],
]
value_table = Table(value_data, colWidths=[1.5*inch, 1.6*inch, 1.5*inch, 1.5*inch])
value_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('TEXTCOLOR', (-1, 1), (-1, -1), SUCCESS_GREEN),
    ('FONTNAME', (-1, 1), (-1, -1), 'Helvetica-Bold'),
]))
story.append(value_table)

story.append(Spacer(1, 0.3*inch))

# Big number
story.append(Paragraph("TOTAL 10-YEAR VALUE CREATION", styles['NumberLabel']))
story.append(Paragraph("$200 - $500 BILLION", styles['BigNumber']))

story.append(PageBreak())

# ==================== TESLA INTEGRATION ====================
story.append(Paragraph("8. Tesla/Energy Ecosystem Integration", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=PRIMARY_TEAL))
story.append(Spacer(1, 0.2*inch))

tesla_text = """
I.H.P. is architecturally aligned with Tesla's energy ecosystem through the <b>Matter 1.4 protocol</b>,
which added native support for water heaters, heat pumps, batteries, solar systems, and EV chargers
in November 2024. This creates natural data integration opportunities.
"""
story.append(Paragraph(tesla_text, styles['BodyTextCustom']))

story.append(Paragraph('"Data is the key to Elon\'s heart."', styles['Quote']))

# Tesla integration table
tesla_data = [
    ['Tesla Product', 'I.H.P. Data Value'],
    ['Powerwall', 'Emergency backup triggers, grid arbitrage signals'],
    ['Solar', 'Production optimization, storm preparation'],
    ['HVAC (Heat Pumps)', 'Efficiency monitoring, failure prediction'],
    ['Vehicle', 'Home/away detection, emergency notifications'],
    ['Tesla Insurance', 'Real-time home risk scoring'],
    ['Energy Grid', 'Demand response, load balancing'],
]
tesla_table = Table(tesla_data, colWidths=[2*inch, 4.5*inch])
tesla_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), PRIMARY_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, 1), (0, -1), PRIMARY_TEAL),
]))
story.append(tesla_table)

story.append(Spacer(1, 0.3*inch))

# Matter 1.4
story.append(Paragraph("Matter 1.4 Protocol Alignment (November 2024)", styles['SubSection']))

matter_text = """
The Matter 1.4 specification creates perfect ecosystem alignment between I.H.P. and Tesla Energy products:
"""
story.append(Paragraph(matter_text, styles['BodyTextCustom']))

matter_items = [
    "Water heaters (I.H.P. core monitoring)",
    "Heat pumps (I.H.P. HVAC monitoring)",
    "Batteries/solar systems (Tesla Powerwall)",
    "Electric vehicle chargers (Tesla)",
    "Home routers (connectivity infrastructure)",
]
for item in matter_items:
    story.append(Paragraph(f"• {item}", styles['BodyTextCustom']))

story.append(PageBreak())

# ==================== DATA MOAT ====================
story.append(Paragraph("9. Data Moat & Competitive Advantage", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=ACCENT_BLUE))
story.append(Spacer(1, 0.2*inch))

moat_text = """
I.H.P.'s competitive advantage lies in <b>multi-peril cross-correlation</b>—the ability to analyze
water, electrical, structural, and HVAC data together to generate insights no single-peril competitor
can match. Each additional sensor deployed improves the ML models for all users.
"""
story.append(Paragraph(moat_text, styles['BodyTextCustom']))

# Network effects
story.append(Paragraph("Network Effects", styles['SubSection']))

network_items = [
    ("<b>More homes = better ML models</b> — Each sensor improves prediction accuracy", styles['BodyTextCustom']),
    ("<b>Geographic density = regional insights</b> — Microclimate, soil, infrastructure data", styles['BodyTextCustom']),
    ("<b>Temporal depth = pattern recognition</b> — Seasonal, cyclical, degradation patterns", styles['BodyTextCustom']),
    ("<b>Cross-peril correlation</b> — Water + electrical + structural = holistic risk scoring", styles['BodyTextCustom']),
]
for text, style in network_items:
    story.append(Paragraph(f"• {text}", style))

story.append(Spacer(1, 0.2*inch))

# Competitive comparison
story.append(Paragraph("Competitive Landscape", styles['SubSection']))

comp_data = [
    ['Company', 'Focus', 'I.H.P. Advantage'],
    ['Flo by Moen', 'Water only', 'Multi-peril correlation'],
    ['Phyn', 'Water only', 'Multi-peril correlation'],
    ['LeakBot/Ondo', 'Water only', 'Multi-peril correlation'],
    ['Ting/Whisker Labs', 'Electrical only', 'Integrated water/structural'],
    ['SimpliSafe/Ring', 'Security', 'Claim prevention focus'],
    ['I.H.P.', 'MULTI-PERIL UNIFIED', 'UNIQUE CROSS-PERIL DATA'],
]
comp_table = Table(comp_data, colWidths=[2*inch, 2*inch, 2.5*inch])
comp_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), ACCENT_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, LIGHT_GRAY]),
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4edda')),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
]))
story.append(comp_table)

story.append(PageBreak())

# ==================== SOURCES ====================
story.append(Paragraph("10. Data Sources & References", styles['SectionHeader']))
story.append(HRFlowable(width="100%", thickness=2, color=MID_GRAY))
story.append(Spacer(1, 0.2*inch))

sources = [
    ("Catastrophe & Reinsurance", [
        "Swiss Re Sigma Research - Natural Catastrophes 2024/2025",
        "Gallagher Re - 2024 Natural Catastrophe Report",
        "Verisk - Average Annual Loss Modeling",
        "Artemis - Reinsurance Market Analysis",
    ]),
    ("Insurance Industry", [
        "S&P Global - 2024 US P&C Statutory Results",
        "McKinsey - Data Analytics in P&C Underwriting",
        "AM Best - Industry Performance Reports",
        "Triple-I (Insurance Information Institute) - Claims Statistics",
    ]),
    ("Water Damage", [
        "Consumer Affairs - Water Damage Claims Statistics",
        "Insurify - Water Damage Statistics",
        "IBHS - Water Heater Failure Data",
        "SmartRent, Moen, LeakBot - Prevention Technology Data",
    ]),
    ("Fire & Electrical", [
        "Vivint - 2024 House Fire Statistics",
        "NFPA - Fire Prevention Data",
        "Ting/Whisker Labs - Electrical Fire Prevention",
        "ABB - Arc Fault Detection Technology",
    ]),
    ("Smart Home & IoT", [
        "Fortune Business Insights - Smart Home Market Report",
        "Grand View Research - Smart Building Analysis",
        "ABI Research - Matter Protocol Projections",
        "CSA-IoT - Matter Specification Documentation",
    ]),
]

for category, items in sources:
    story.append(Paragraph(category, styles['SubSection']))
    for item in items:
        story.append(Paragraph(f"• {item}", ParagraphStyle('Source', fontSize=9,
                                                           textColor=MID_GRAY, leftIndent=15)))
    story.append(Spacer(1, 0.1*inch))

# ==================== FINAL PAGE ====================
story.append(PageBreak())
story.append(Spacer(1, 2*inch))

if os.path.exists(LOGO_PATH):
    final_logo = Image(LOGO_PATH, width=4*inch, height=1.1*inch)
    final_logo.hAlign = 'CENTER'
    story.append(final_logo)

story.append(Spacer(1, 0.5*inch))
story.append(HRFlowable(width="40%", thickness=3, color=PRIMARY_TEAL, hAlign='CENTER'))
story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("Intelligent Home Protection", styles['Subtitle']))
story.append(Spacer(1, 0.3*inch))

taglines = [
    "Data-Driven. Multi-Peril. Universal Platform.",
    "",
    "Protecting Homes | Preventing Claims | Creating Value",
]
for line in taglines:
    story.append(Paragraph(line, ParagraphStyle('Tag', fontSize=12, textColor=MID_GRAY,
                                                 alignment=TA_CENTER)))

story.append(Spacer(1, 1*inch))
story.append(Paragraph("partners@ihp-home.io", ParagraphStyle('Contact', fontSize=11,
                                                              textColor=PRIMARY_TEAL,
                                                              alignment=TA_CENTER)))

# Build PDF
print("Generating I.H.P. Market Research Report...")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"\nPDF generated: {output_path}")
