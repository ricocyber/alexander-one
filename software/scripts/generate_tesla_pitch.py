#!/usr/bin/env python3
"""
I.H.P. - Tesla Executive Pitch Document
One-pager + detailed deck designed to catch Tesla's attention
"""

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT, TA_JUSTIFY
import os

LOGO_PATH = "/Users/ericdeloera/Downloads/luxx-haus 5/assets/luxx_logo_light.png"

# Tesla-inspired color palette
TESLA_RED = colors.HexColor('#e82127')
TESLA_BLACK = colors.HexColor('#171a20')
TESLA_DARK = colors.HexColor('#222222')
TESLA_GRAY = colors.HexColor('#393c41')
TESLA_LIGHT = colors.HexColor('#f4f4f4')
ELECTRIC_BLUE = colors.HexColor('#3e6ae1')
ENERGY_GREEN = colors.HexColor('#12bb00')
WHITE = colors.white

def create_header(canvas, doc):
    canvas.saveState()
    # Minimal header - Tesla style
    canvas.setStrokeColor(TESLA_RED)
    canvas.setLineWidth(3)
    canvas.line(0.5*inch, letter[1] - 0.5*inch, letter[0] - 0.5*inch, letter[1] - 0.5*inch)
    canvas.restoreState()

def create_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(TESLA_GRAY)
    canvas.drawString(inch, 0.4*inch, "CONFIDENTIAL - For Tesla Eyes Only")
    canvas.drawRightString(letter[0] - inch, 0.4*inch, f"{doc.page}")
    canvas.restoreState()

def header_footer(canvas, doc):
    create_header(canvas, doc)
    create_footer(canvas, doc)

# Create PDF
output_path = "/Users/ericdeloera/Downloads/luxx-haus 5/IHP_Tesla_Pitch.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    rightMargin=0.6*inch,
    leftMargin=0.6*inch,
    topMargin=0.7*inch,
    bottomMargin=0.6*inch
)

# Styles
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='TeslaHero',
    fontSize=48,
    textColor=TESLA_BLACK,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold',
    leading=52
))

styles.add(ParagraphStyle(
    name='TeslaSubHero',
    fontSize=24,
    textColor=TESLA_GRAY,
    alignment=TA_CENTER,
    fontName='Helvetica',
    spaceAfter=20
))

styles.add(ParagraphStyle(
    name='TeslaSection',
    fontSize=28,
    textColor=TESLA_BLACK,
    fontName='Helvetica-Bold',
    spaceBefore=20,
    spaceAfter=15
))

styles.add(ParagraphStyle(
    name='TeslaSub',
    fontSize=16,
    textColor=TESLA_RED,
    fontName='Helvetica-Bold',
    spaceBefore=15,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name='TeslaBody',
    fontSize=12,
    textColor=TESLA_DARK,
    alignment=TA_LEFT,
    leading=18,
    spaceAfter=10
))

styles.add(ParagraphStyle(
    name='TeslaBold',
    fontSize=12,
    textColor=TESLA_BLACK,
    fontName='Helvetica-Bold',
    leading=18,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name='BigStat',
    fontSize=72,
    textColor=TESLA_RED,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold'
))

styles.add(ParagraphStyle(
    name='StatLabel',
    fontSize=14,
    textColor=TESLA_GRAY,
    alignment=TA_CENTER,
    fontName='Helvetica'
))

styles.add(ParagraphStyle(
    name='Quote',
    fontSize=18,
    textColor=TESLA_BLACK,
    alignment=TA_CENTER,
    fontName='Helvetica-Oblique',
    leading=24,
    leftIndent=30,
    rightIndent=30
))

styles.add(ParagraphStyle(
    name='CallToAction',
    fontSize=20,
    textColor=WHITE,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold',
    backColor=TESLA_RED,
    borderPadding=15
))

# Build document
story = []

# ==================== PAGE 1: THE HOOK ====================
story.append(Spacer(1, 1.5*inch))

# The killer stat
story.append(Paragraph("$150 BILLION", styles['BigStat']))
story.append(Paragraph("Lost. Every. Year.", styles['TeslaSubHero']))

story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("Home insurance catastrophe losses are the new normal.<br/>Tesla Energy can own the solution.", styles['TeslaBody']))

story.append(Spacer(1, 0.5*inch))

# Logo
if os.path.exists(LOGO_PATH):
    logo = Image(LOGO_PATH, width=3.5*inch, height=1*inch)
    logo.hAlign = 'CENTER'
    story.append(logo)

story.append(Spacer(1, 0.3*inch))
story.append(HRFlowable(width="30%", thickness=3, color=TESLA_RED, hAlign='CENTER'))
story.append(Spacer(1, 0.3*inch))

story.append(Paragraph("Intelligent Home Protection", styles['TeslaSubHero']))

story.append(Spacer(1, 0.8*inch))

# The proposition
prop_text = """
<b>We built the operating system for home risk prevention.</b><br/><br/>
Water. Fire. Electrical. Structural. HVAC.<br/>
One platform. Real-time data. Matter 1.4 native.<br/><br/>
<b>Tesla Insurance needs this data. Tesla Energy can deliver it.</b>
"""
story.append(Paragraph(prop_text, ParagraphStyle('Prop', fontSize=14, textColor=TESLA_DARK,
                                                  alignment=TA_CENTER, leading=22)))

story.append(PageBreak())

# ==================== PAGE 2: THE PROBLEM TESLA UNDERSTANDS ====================
story.append(Paragraph("THE PROBLEM", styles['TeslaSection']))
story.append(HRFlowable(width="100%", thickness=2, color=TESLA_RED))
story.append(Spacer(1, 0.2*inch))

problem_text = """
Insurance is broken. Carriers lost money on homeowners policies for <b>7 consecutive years</b>.
They're raising premiums—<b>$21 billion more</b> extracted from homeowners since 2021.
The industry is reactive, not predictive. They pay claims instead of preventing them.
"""
story.append(Paragraph(problem_text, styles['TeslaBody']))

story.append(Spacer(1, 0.2*inch))

# Problem stats - Tesla style grid
problem_stats = [
    ['$417B', '$150B', '76%', '14,000'],
    ['Economic losses\n(2024)', 'Annual insured\nlosses', 'From US\nalone', 'Water incidents\nPER DAY']
]
prob_table = Table(problem_stats, colWidths=[1.7*inch]*4)
prob_table.setStyle(TableStyle([
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 32),
    ('TEXTCOLOR', (0, 0), (-1, 0), TESLA_RED),
    ('FONTSIZE', (0, 1), (-1, 1), 10),
    ('TEXTCOLOR', (0, 1), (-1, 1), TESLA_GRAY),
    ('TOPPADDING', (0, 0), (-1, -1), 15),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
    ('BACKGROUND', (0, 0), (-1, -1), TESLA_LIGHT),
]))
story.append(prob_table)

story.append(Spacer(1, 0.4*inch))

story.append(Paragraph("WHY TESLA?", styles['TeslaSection']))
story.append(HRFlowable(width="100%", thickness=2, color=TESLA_RED))
story.append(Spacer(1, 0.2*inch))

why_text = """
Tesla already disrupted auto insurance with real-time driving data.<br/><br/>
<b>Home insurance is next.</b><br/><br/>
You have the energy infrastructure. The Powerwall. The solar. The app. The
customer relationship. You're already in millions of homes.<br/><br/>
You just need the <b>data layer</b> for home risk.
"""
story.append(Paragraph(why_text, styles['TeslaBody']))

story.append(PageBreak())

# ==================== PAGE 3: THE SOLUTION ====================
story.append(Paragraph("THE SOLUTION", styles['TeslaSection']))
story.append(HRFlowable(width="100%", thickness=2, color=ENERGY_GREEN))
story.append(Spacer(1, 0.2*inch))

solution_text = """
I.H.P. is the <b>unified data platform</b> for home protection—built on Matter 1.4,
the same protocol Tesla Energy products use. Native integration. No middleware.
"""
story.append(Paragraph(solution_text, styles['TeslaBody']))

story.append(Spacer(1, 0.2*inch))

# What we monitor
story.append(Paragraph("Multi-Peril Monitoring", styles['TeslaSub']))

monitor_data = [
    ['PERIL', 'ANNUAL COST', 'I.H.P. DETECTION', 'PROVEN REDUCTION'],
    ['Water Damage', '$13 billion', 'Pressure, flow, moisture', '96%'],
    ['Fire/Smoke', '$11.3 billion', 'Heat, smoke, spread', '90% preventable'],
    ['Electrical', '$1.4 billion', 'Arc fault, power quality', '80%'],
    ['Structural', '$5+ billion', 'Vibration, tilt, strain', 'First-to-market'],
    ['HVAC', '$2+ billion', 'Efficiency, failure prediction', 'Predictive'],
]
monitor_table = Table(monitor_data, colWidths=[1.3*inch, 1.3*inch, 2*inch, 1.6*inch])
monitor_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TESLA_BLACK),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, TESLA_LIGHT),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, TESLA_LIGHT]),
    ('TEXTCOLOR', (-1, 1), (-1, -1), ENERGY_GREEN),
    ('FONTNAME', (-1, 1), (-1, -1), 'Helvetica-Bold'),
]))
story.append(monitor_table)

story.append(Spacer(1, 0.3*inch))

# Matter 1.4 alignment
story.append(Paragraph("Matter 1.4 = Perfect Ecosystem Fit", styles['TeslaSub']))

matter_text = """
Matter 1.4 (November 2024) added native support for exactly what we both need:
"""
story.append(Paragraph(matter_text, styles['TeslaBody']))

matter_grid = [
    ['I.H.P. MONITORS', 'TESLA ENERGY'],
    ['Water Heaters', 'Powerwall / Batteries'],
    ['Heat Pumps', 'Solar Systems'],
    ['HVAC Systems', 'EV Chargers'],
    ['Home Sensors', 'Energy Management'],
]
matter_table = Table(matter_grid, colWidths=[3.2*inch, 3.2*inch])
matter_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (0, 0), ELECTRIC_BLUE),
    ('BACKGROUND', (1, 0), (1, 0), TESLA_RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 11),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('GRID', (0, 0), (-1, -1), 1, TESLA_LIGHT),
]))
story.append(matter_table)

story.append(PageBreak())

# ==================== PAGE 4: THE TESLA INTEGRATION ====================
story.append(Paragraph("TESLA INTEGRATION", styles['TeslaSection']))
story.append(HRFlowable(width="100%", thickness=2, color=TESLA_RED))
story.append(Spacer(1, 0.2*inch))

integration_text = """
I.H.P. data makes every Tesla Energy product smarter and more valuable.
"""
story.append(Paragraph(integration_text, styles['TeslaBody']))

story.append(Spacer(1, 0.15*inch))

# Integration table
int_data = [
    ['TESLA PRODUCT', 'I.H.P. DATA ENABLES'],
    ['Powerwall', 'Emergency backup triggers before damage occurs\nGrid arbitrage based on home risk state\nAuto-shutoff coordination during water events'],
    ['Solar', 'Storm preparation and production optimization\nInsurance-grade weather response\nEnergy reserve for emergency systems'],
    ['Tesla App', 'Unified home health dashboard\nReal-time alerts across all perils\nPredictive maintenance notifications'],
    ['Tesla Insurance', 'Real-time home risk scoring\nDynamic premium adjustment\nClaim prevention = profit'],
    ['Virtual Power Plant', 'Risk-aware load balancing\nEmergency demand response\nGrid stability during events'],
]
int_table = Table(int_data, colWidths=[1.8*inch, 4.8*inch])
int_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TESLA_BLACK),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, 1), (0, -1), TESLA_RED),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 12),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
    ('LEFTPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, TESLA_LIGHT),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, TESLA_LIGHT]),
]))
story.append(int_table)

story.append(Spacer(1, 0.3*inch))

# The quote
story.append(Paragraph('"Tesla Insurance disrupted auto with driving data.<br/>Home insurance is disrupted with home data."', styles['Quote']))

story.append(PageBreak())

# ==================== PAGE 5: THE NUMBERS ====================
story.append(Paragraph("THE NUMBERS", styles['TeslaSection']))
story.append(HRFlowable(width="100%", thickness=2, color=ENERGY_GREEN))
story.append(Spacer(1, 0.2*inch))

numbers_text = """
The math is simple: <b>data that prevents claims is worth billions</b>.
"""
story.append(Paragraph(numbers_text, styles['TeslaBody']))

story.append(Spacer(1, 0.15*inch))

# Value creation
story.append(Paragraph("Value Creation (Annual)", styles['TeslaSub']))

value_data = [
    ['STAKEHOLDER', 'CURRENT LOSS', 'I.H.P. IMPACT', 'VALUE CREATED'],
    ['Insurance Carriers', '$50B in claims', '20% reduction', '$10B / year'],
    ['Reinsurers', '$150B cat losses', '5% improvement', '$7.5B / year'],
    ['Homeowners', '$21B premium hike', 'Offset increases', '$21B value'],
    ['Tesla Insurance', 'New market entry', 'Data advantage', 'Market leader'],
]
value_table = Table(value_data, colWidths=[1.6*inch, 1.5*inch, 1.5*inch, 1.5*inch])
value_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TESLA_BLACK),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, TESLA_LIGHT),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, TESLA_LIGHT]),
    ('TEXTCOLOR', (-1, 1), (-1, -2), ENERGY_GREEN),
    ('FONTNAME', (-1, 1), (-1, -1), 'Helvetica-Bold'),
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#fff3cd')),
]))
story.append(value_table)

story.append(Spacer(1, 0.3*inch))

# 10 year projection
story.append(Paragraph("10-Year Tesla Home Insurance Projection", styles['TeslaSub']))

projection_data = [
    ['YEAR', 'HOMES', 'DATA VALUE', 'INSURANCE PREMIUM', 'TOTAL'],
    ['2026', '500K', '$50M', '$500M', '$550M'],
    ['2028', '5M', '$400M', '$5B', '$5.4B'],
    ['2030', '25M', '$2B', '$25B', '$27B'],
    ['2035', '100M', '$8B', '$100B', '$108B'],
]
proj_table = Table(projection_data, colWidths=[1*inch, 1.2*inch, 1.3*inch, 1.7*inch, 1.3*inch])
proj_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TESLA_RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 10),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 1, TESLA_LIGHT),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, TESLA_LIGHT]),
    ('FONTNAME', (-1, 1), (-1, -1), 'Helvetica-Bold'),
    ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d4edda')),
    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
]))
story.append(proj_table)

story.append(Spacer(1, 0.3*inch))

# Big number
story.append(Paragraph("$100B+", ParagraphStyle('Huge', fontSize=60, textColor=ENERGY_GREEN,
                                                 alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Paragraph("Annual Home Insurance Market Opportunity", styles['StatLabel']))

story.append(PageBreak())

# ==================== PAGE 6: THE ASK ====================
story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("THE DEAL", styles['TeslaSection']))
story.append(HRFlowable(width="100%", thickness=3, color=TESLA_RED))
story.append(Spacer(1, 0.3*inch))

deal_text = """
We're not looking for a partnership.<br/><br/>
<b>We're looking for an exit.</b>
"""
story.append(Paragraph(deal_text, ParagraphStyle('Deal', fontSize=18, textColor=TESLA_BLACK,
                                                  alignment=TA_CENTER, leading=26)))

story.append(Spacer(1, 0.4*inch))

# What Tesla gets
story.append(Paragraph("TESLA ACQUIRES:", styles['TeslaSub']))

gets_items = [
    "Complete multi-peril home monitoring platform",
    "Matter 1.4 native architecture (plug into Tesla Energy)",
    "AI/ML anomaly detection models (water, fire, electrical, structural)",
    "Patent-pending cross-peril correlation algorithms",
    "Insurance carrier relationships and pilot data",
    "Team with deep insurance + IoT expertise",
]
for item in gets_items:
    story.append(Paragraph(f"<b>+</b>  {item}", ParagraphStyle('Item', fontSize=12,
                                                               textColor=TESLA_DARK, leftIndent=20, spaceAfter=8)))

story.append(Spacer(1, 0.3*inch))

# Strategic value
story.append(Paragraph("STRATEGIC VALUE:", styles['TeslaSub']))

strategic_items = [
    ("Tesla Insurance", "Real-time home risk scoring = lower loss ratios = profitable expansion"),
    ("Powerwall", "Emergency intelligence = higher value proposition = premium pricing"),
    ("Tesla App", "Home health dashboard = stickier customers = lifetime value"),
    ("Data Moat", "First-mover in multi-peril home data = insurmountable lead"),
]
for title, desc in strategic_items:
    story.append(Paragraph(f"<b>{title}:</b> {desc}", ParagraphStyle('Strat', fontSize=11,
                                                                      textColor=TESLA_DARK, spaceAfter=8)))

story.append(PageBreak())

# ==================== PAGE 7: FINAL ====================
story.append(Spacer(1, 1*inch))

# Logo
if os.path.exists(LOGO_PATH):
    final_logo = Image(LOGO_PATH, width=4.5*inch, height=1.25*inch)
    final_logo.hAlign = 'CENTER'
    story.append(final_logo)

story.append(Spacer(1, 0.3*inch))

story.append(Paragraph("×", ParagraphStyle('X', fontSize=36, textColor=TESLA_RED,
                                            alignment=TA_CENTER, fontName='Helvetica-Bold')))

story.append(Spacer(1, 0.1*inch))

# Tesla wordmark style
story.append(Paragraph("TESLA", ParagraphStyle('Tesla', fontSize=42, textColor=TESLA_BLACK,
                                                alignment=TA_CENTER, fontName='Helvetica-Bold',
                                                leading=46)))
story.append(Paragraph("ENERGY", ParagraphStyle('Energy', fontSize=24, textColor=TESLA_GRAY,
                                                 alignment=TA_CENTER, fontName='Helvetica')))

story.append(Spacer(1, 0.5*inch))
story.append(HRFlowable(width="40%", thickness=3, color=TESLA_RED, hAlign='CENTER'))
story.append(Spacer(1, 0.5*inch))

# The close
story.append(Paragraph("The future of home insurance is predictive.", styles['Quote']))
story.append(Spacer(1, 0.2*inch))
story.append(Paragraph("Tesla already proved it with cars.", ParagraphStyle('Close', fontSize=14,
                                                                             textColor=TESLA_GRAY,
                                                                             alignment=TA_CENTER)))
story.append(Paragraph("<b>Let's do it with homes.</b>", ParagraphStyle('Close2', fontSize=16,
                                                                         textColor=TESLA_BLACK,
                                                                         alignment=TA_CENTER,
                                                                         fontName='Helvetica-Bold')))

story.append(Spacer(1, 0.8*inch))

# Contact box
contact_data = [
    ['READY TO TALK?'],
    ['partners@ihp-home.io'],
]
contact_table = Table(contact_data, colWidths=[4*inch])
contact_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TESLA_RED),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 14),
    ('FONTSIZE', (0, 1), (-1, 1), 16),
    ('TEXTCOLOR', (0, 1), (-1, 1), TESLA_BLACK),
    ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 15),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
]))
contact_table.hAlign = 'CENTER'
story.append(contact_table)

story.append(Spacer(1, 0.5*inch))

story.append(Paragraph(f"Prepared {datetime.now().strftime('%B %Y')} | Confidential",
                       ParagraphStyle('Footer', fontSize=9, textColor=TESLA_GRAY,
                                      alignment=TA_CENTER)))

# Build PDF
print("Generating Tesla Pitch Document...")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"\nPDF generated: {output_path}")
