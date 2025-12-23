#!/usr/bin/env python3
"""
I.H.P. - Hardware Technical Specification Document
For Joe Hobart - Electrical Engineer
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
import os

LOGO_PATH = "/Users/ericdeloera/Downloads/luxx-haus 5/assets/luxx_logo_light.png"

# Technical color palette
TECH_DARK = colors.HexColor('#1a1a2e')
TECH_BLUE = colors.HexColor('#0066cc')
TECH_TEAL = colors.HexColor('#00b99b')
TECH_ORANGE = colors.HexColor('#ff6b35')
TECH_GRAY = colors.HexColor('#6c757d')
LIGHT_BG = colors.HexColor('#f8f9fa')
WHITE = colors.white

def create_header(canvas, doc):
    canvas.saveState()
    if os.path.exists(LOGO_PATH):
        canvas.drawImage(LOGO_PATH, inch, letter[1] - 0.8*inch,
                        width=1.8*inch, height=0.5*inch,
                        preserveAspectRatio=True, mask='auto')
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(TECH_GRAY)
    canvas.drawRightString(letter[0] - inch, letter[1] - 0.5*inch,
                          "Hardware Technical Specification v1.0")
    canvas.setStrokeColor(TECH_TEAL)
    canvas.setLineWidth(2)
    canvas.line(inch, letter[1] - 0.9*inch, letter[0] - inch, letter[1] - 0.9*inch)
    canvas.restoreState()

def create_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(TECH_GRAY)
    canvas.drawString(inch, 0.4*inch, "CONFIDENTIAL - I.H.P. Technical Documentation")
    canvas.drawRightString(letter[0] - inch, 0.4*inch, f"Page {doc.page}")
    canvas.restoreState()

def header_footer(canvas, doc):
    create_header(canvas, doc)
    create_footer(canvas, doc)

# Create PDF
output_path = "/Users/ericdeloera/Downloads/luxx-haus 5/IHP_Hardware_Technical_Spec.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    rightMargin=0.75*inch,
    leftMargin=0.75*inch,
    topMargin=1*inch,
    bottomMargin=0.7*inch
)

# Styles
styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='DocTitle',
    fontSize=28,
    textColor=TECH_DARK,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold',
    spaceAfter=10
))

styles.add(ParagraphStyle(
    name='DocSubtitle',
    fontSize=14,
    textColor=TECH_GRAY,
    alignment=TA_CENTER,
    spaceAfter=20
))

styles.add(ParagraphStyle(
    name='SectionHead',
    fontSize=16,
    textColor=TECH_DARK,
    fontName='Helvetica-Bold',
    spaceBefore=20,
    spaceAfter=10
))

styles.add(ParagraphStyle(
    name='SubHead',
    fontSize=12,
    textColor=TECH_BLUE,
    fontName='Helvetica-Bold',
    spaceBefore=12,
    spaceAfter=6
))

styles.add(ParagraphStyle(
    name='TechBody',
    fontSize=10,
    textColor=colors.HexColor('#333333'),
    alignment=TA_JUSTIFY,
    leading=14,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name='CodeStyle',
    fontSize=9,
    textColor=TECH_DARK,
    fontName='Courier',
    backColor=LIGHT_BG,
    leftIndent=10,
    spaceAfter=8
))

styles.add(ParagraphStyle(
    name='Callout',
    fontSize=11,
    textColor=WHITE,
    fontName='Helvetica-Bold',
    backColor=TECH_TEAL,
    alignment=TA_CENTER,
    borderPadding=12
))

styles.add(ParagraphStyle(
    name='PersonalNote',
    fontSize=11,
    textColor=TECH_DARK,
    fontName='Helvetica-Oblique',
    leftIndent=20,
    rightIndent=20,
    spaceBefore=10,
    spaceAfter=10,
    leading=16
))

# Build document
story = []

# ==================== COVER PAGE ====================
story.append(Spacer(1, 0.5*inch))

if os.path.exists(LOGO_PATH):
    logo = Image(LOGO_PATH, width=4*inch, height=1.1*inch)
    logo.hAlign = 'CENTER'
    story.append(logo)

story.append(Spacer(1, 0.3*inch))
story.append(HRFlowable(width="40%", thickness=3, color=TECH_TEAL, hAlign='CENTER'))
story.append(Spacer(1, 0.3*inch))

story.append(Paragraph("Hardware Technical Specification", styles['DocTitle']))
story.append(Paragraph("Multi-Peril Home Protection Sensor Platform", styles['DocSubtitle']))

story.append(Spacer(1, 0.5*inch))

# For Joe
story.append(Paragraph("PREPARED FOR", ParagraphStyle('For', fontSize=10, textColor=TECH_GRAY,
                                                       alignment=TA_CENTER)))
story.append(Spacer(1, 0.1*inch))
story.append(Paragraph("Joe Hobart", ParagraphStyle('Name', fontSize=20, textColor=TECH_DARK,
                                                     alignment=TA_CENTER, fontName='Helvetica-Bold')))
story.append(Paragraph("Electrical Engineer | Kicker Audio", ParagraphStyle('Title', fontSize=12,
                                                                             textColor=TECH_GRAY,
                                                                             alignment=TA_CENTER)))
story.append(Paragraph("Stillwater, Oklahoma", ParagraphStyle('Loc', fontSize=10,
                                                               textColor=TECH_GRAY,
                                                               alignment=TA_CENTER)))
story.append(Paragraph("jh@higbl.com", ParagraphStyle('Email', fontSize=10,
                                                               textColor=TECH_BLUE,
                                                               alignment=TA_CENTER)))

story.append(Spacer(1, 0.6*inch))

# Personal note
note_text = """
Joe—

I'm building something that could change how homes are protected. The platform is ready.
The software is built. The market data is compelling ($150B annual opportunity).

What I need is someone who knows hardware. Someone who can take sensor specifications
and turn them into production-ready PCBs. Someone with credibility in electrical engineering.

That's you.

This document outlines the technical requirements. I want you to tear it apart, improve it,
and help me build it. Let's talk.
"""
story.append(Paragraph(note_text, styles['PersonalNote']))

story.append(Spacer(1, 0.5*inch))
story.append(Paragraph(f"{datetime.now().strftime('%B %d, %Y')}", ParagraphStyle('Date', fontSize=10,
                                                                                   textColor=TECH_GRAY,
                                                                                   alignment=TA_CENTER)))

story.append(PageBreak())

# ==================== EXECUTIVE OVERVIEW ====================
story.append(Paragraph("1. Executive Overview", styles['SectionHead']))
story.append(HRFlowable(width="100%", thickness=1, color=TECH_DARK))
story.append(Spacer(1, 0.15*inch))

overview_text = """
I.H.P. (Intelligent Home Protection) is a <b>multi-peril home monitoring platform</b> that combines
water, fire, electrical, structural, and HVAC sensors into a unified data system. Unlike single-purpose
devices (Flo for water, Ting for electrical), I.H.P. correlates data across all perils to provide
predictive risk intelligence.
"""
story.append(Paragraph(overview_text, styles['TechBody']))

story.append(Paragraph("The Opportunity", styles['SubHead']))

opp_text = """
Insurance carriers lose <b>$150 billion annually</b> on property claims. They're desperate for
loss prevention technology. Current solutions address single perils—we address all of them
with cross-correlation that no competitor can match.
"""
story.append(Paragraph(opp_text, styles['TechBody']))

# Quick stats
stats_data = [
    ['Market Size', 'Prevention Rate', 'Avg Claim', 'Target'],
    ['$150B/year losses', '96% (water proven)', '$15,400', '100M homes'],
]
stats_table = Table(stats_data, colWidths=[1.6*inch]*4)
stats_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('TEXTCOLOR', (0, 1), (-1, 1), TECH_TEAL),
]))
story.append(stats_table)

story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("Platform Architecture", styles['SubHead']))

arch_text = """
The system consists of three layers:
"""
story.append(Paragraph(arch_text, styles['TechBody']))

arch_items = [
    "<b>Hardware Layer:</b> Multi-sensor nodes deployed at critical points (water entry, electrical panel, foundation, HVAC)",
    "<b>Communication Layer:</b> Matter 1.4 over Thread mesh network, with WiFi/cellular fallback",
    "<b>Intelligence Layer:</b> Cloud-based ML pipeline (Isolation Forest + LSTM) for anomaly detection and prediction",
]
for item in arch_items:
    story.append(Paragraph(f"• {item}", styles['TechBody']))

story.append(PageBreak())

# ==================== SENSOR SPECIFICATIONS ====================
story.append(Paragraph("2. Sensor Module Specifications", styles['SectionHead']))
story.append(HRFlowable(width="100%", thickness=1, color=TECH_DARK))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("We need five sensor module types. Each is a standalone PCB with common communication architecture.", styles['TechBody']))

# ===== WATER SENSOR =====
story.append(Paragraph("2.1 Water Pressure & Flow Sensor (WTR-X1)", styles['SubHead']))

water_specs = [
    ['Parameter', 'Specification', 'Notes'],
    ['Pressure Range', '0-150 PSI', '±0.5% accuracy, 0.1 PSI resolution'],
    ['Pressure Sensor', 'Piezoresistive MEMS', 'Honeywell HSC series or equiv'],
    ['Flow Detection', '0.1-50 L/min', 'Ultrasonic time-of-flight preferred'],
    ['Flow Sensor', 'Transit-time ultrasonic', 'No moving parts, clamp-on capable'],
    ['Moisture Detection', 'Capacitive', '<1 sec response, external probe'],
    ['Temperature', '-10°C to 85°C', '±0.5°C accuracy'],
    ['Sample Rate', '1 Hz continuous', 'Configurable 0.1-10 Hz'],
    ['MCU', 'Nordic nRF5340', 'Dual-core ARM Cortex-M33'],
    ['Radio', 'Thread 1.3 / BLE 5.3', 'Matter 1.4 certified stack'],
    ['Power', '3.6V Li-SOCL2 or 5V USB', '10+ year battery life target'],
    ['Enclosure', 'IP67', 'Brass fittings, NSF-61 compliant'],
]
water_table = Table(water_specs, colWidths=[1.5*inch, 1.8*inch, 3*inch])
water_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_BLUE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
]))
story.append(water_table)

story.append(Spacer(1, 0.15*inch))

# ===== ELECTRICAL SENSOR =====
story.append(Paragraph("2.2 Electrical Monitoring Sensor (ELC-X1)", styles['SubHead']))

elec_specs = [
    ['Parameter', 'Specification', 'Notes'],
    ['Voltage Monitoring', '120/240V AC', 'RMS, THD, sag/swell detection'],
    ['Current Sensing', '0-200A', 'Split-core CT, non-invasive'],
    ['Arc Fault Detection', '1-100 MHz bandwidth', 'Series/parallel arc signatures'],
    ['Sampling Rate', '1 MSPS', 'For arc signature analysis'],
    ['DSP', 'Dedicated FFT processor', 'Real-time spectral analysis'],
    ['Power Quality', 'IEEE 1159 compliant', 'Harmonics, PF, frequency'],
    ['MCU', 'STM32H7 + nRF5340', 'H7 for DSP, nRF for comms'],
    ['Isolation', '4kV reinforced', 'UL/IEC 62368-1'],
    ['Installation', 'Panel mount', 'Split-core CTs, no rewiring'],
    ['Certifications', 'UL 916, FCC Part 15', 'Required for US market'],
]
elec_table = Table(elec_specs, colWidths=[1.5*inch, 1.8*inch, 3*inch])
elec_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_ORANGE),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
]))
story.append(elec_table)

story.append(PageBreak())

# ===== STRUCTURAL SENSOR =====
story.append(Paragraph("2.3 Structural Monitoring Sensor (STR-X1)", styles['SubHead']))

struct_specs = [
    ['Parameter', 'Specification', 'Notes'],
    ['Accelerometer', '±16g, 3-axis', 'MEMS, vibration & seismic'],
    ['Tilt/Inclinometer', '±60°, 0.01° resolution', 'Foundation settlement'],
    ['Strain Gauge Input', '4x quarter-bridge', 'External foil gauges'],
    ['Crack Detection', 'LVDT or laser', 'Sub-mm displacement'],
    ['Sample Rate', '100 Hz (accel)', '1 Hz (tilt/strain)'],
    ['MCU', 'Nordic nRF5340', 'Low power, mesh capable'],
    ['Power', 'Li-SOCL2 + solar', '10+ year target'],
    ['Mounting', 'Epoxy/mechanical', 'Foundation, joists, walls'],
    ['Environmental', '-40°C to 85°C', 'Outdoor/crawlspace rated'],
]
struct_table = Table(struct_specs, colWidths=[1.5*inch, 1.8*inch, 3*inch])
struct_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6f42c1')),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
]))
story.append(struct_table)

story.append(Spacer(1, 0.15*inch))

# ===== HVAC SENSOR =====
story.append(Paragraph("2.4 HVAC Monitoring Sensor (HVC-X1)", styles['SubHead']))

hvac_specs = [
    ['Parameter', 'Specification', 'Notes'],
    ['Temperature', '-40°C to 150°C', 'Multiple zones (supply/return/ambient)'],
    ['Pressure (refrigerant)', '0-500 PSI', 'High/low side monitoring'],
    ['Vibration', '±8g, 3-axis', 'Compressor health'],
    ['Current (compressor)', '0-50A', 'CT-based, efficiency calc'],
    ['Runtime Logging', 'On/off cycles', 'Predictive maintenance'],
    ['MCU', 'Nordic nRF5340', 'Standard platform'],
    ['Power', '24VAC tap or battery', 'HVAC system power preferred'],
    ['Installation', 'Near air handler', 'Non-invasive'],
]
hvac_table = Table(hvac_specs, colWidths=[1.5*inch, 1.8*inch, 3*inch])
hvac_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#20c997')),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
]))
story.append(hvac_table)

story.append(Spacer(1, 0.15*inch))

# ===== ENVIRONMENTAL SENSOR =====
story.append(Paragraph("2.5 Environmental Sensor (ENV-X1)", styles['SubHead']))

env_specs = [
    ['Parameter', 'Specification', 'Notes'],
    ['Smoke Detection', 'Photoelectric + ionization', 'Dual-sensor, UL 217'],
    ['CO Detection', '0-1000 ppm', 'Electrochemical, UL 2034'],
    ['Temperature', '-10°C to 60°C', '±0.3°C accuracy'],
    ['Humidity', '0-100% RH', '±2% accuracy'],
    ['Air Quality', 'VOC, PM2.5', 'Optional AQI module'],
    ['MCU', 'Nordic nRF5340', 'Standard platform'],
    ['Power', '3x AA or hardwired', '5+ year battery'],
    ['Audio', '85 dB siren', 'Local alarm'],
]
env_table = Table(env_specs, colWidths=[1.5*inch, 1.8*inch, 3*inch])
env_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#dc3545')),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 8),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 6),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
]))
story.append(env_table)

story.append(PageBreak())

# ==================== COMMUNICATION ARCHITECTURE ====================
story.append(Paragraph("3. Communication Architecture", styles['SectionHead']))
story.append(HRFlowable(width="100%", thickness=1, color=TECH_DARK))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("3.1 Matter 1.4 / Thread Protocol Stack", styles['SubHead']))

matter_text = """
All sensors implement the <b>Matter 1.4 specification</b> (released November 2024) over Thread mesh networking.
This provides native compatibility with Apple HomeKit, Google Home, Amazon Alexa, and Samsung SmartThings—
plus direct integration with Tesla Energy products (Powerwall, Solar, EV chargers all support Matter).
"""
story.append(Paragraph(matter_text, styles['TechBody']))

matter_specs = [
    ['Layer', 'Protocol', 'Implementation'],
    ['Application', 'Matter 1.4', 'Device types: sensors, actuators'],
    ['Session/Transport', 'Matter CASE/PASE', 'Encrypted, authenticated'],
    ['Network', 'IPv6', '6LoWPAN compression'],
    ['MAC/PHY', 'Thread 1.3', '802.15.4, 2.4 GHz'],
    ['Radio', 'nRF5340 + nRF21540', 'FEM for extended range'],
]
matter_table = Table(matter_specs, colWidths=[1.5*inch, 1.8*inch, 3*inch])
matter_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
]))
story.append(matter_table)

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("3.2 Hub / Border Router", styles['SubHead']))

hub_text = """
A central hub acts as the Thread border router, bridging the mesh network to the cloud. Options:
"""
story.append(Paragraph(hub_text, styles['TechBody']))

hub_items = [
    "<b>Option A:</b> Dedicated I.H.P. hub (nRF5340 + WiFi/LTE, preferred for reliability)",
    "<b>Option B:</b> Leverage existing Matter hubs (Apple TV, Google Nest, Echo) via standard commissioning",
    "<b>Option C:</b> Tesla Powerwall as hub (future—requires Tesla partnership)",
]
for item in hub_items:
    story.append(Paragraph(f"• {item}", styles['TechBody']))

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("3.3 Data Flow", styles['SubHead']))

flow_text = """
Sensor → Thread Mesh → Border Router → TLS 1.3 → Cloud (AWS IoT Core) → ML Pipeline → API
"""
story.append(Paragraph(flow_text, styles['CodeStyle']))

data_text = """
All sensor data is encrypted end-to-end. Local processing handles time-critical decisions (water shutoff),
while cloud ML provides long-term pattern analysis and cross-peril correlation.
"""
story.append(Paragraph(data_text, styles['TechBody']))

story.append(PageBreak())

# ==================== PCB DESIGN CONSIDERATIONS ====================
story.append(Paragraph("4. PCB Design Considerations", styles['SectionHead']))
story.append(HRFlowable(width="100%", thickness=1, color=TECH_DARK))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("4.1 Common Platform Architecture", styles['SubHead']))

pcb_text = """
To minimize NRE and accelerate development, all sensor modules share a <b>common core PCB</b>:
"""
story.append(Paragraph(pcb_text, styles['TechBody']))

core_specs = [
    ['Component', 'Part', 'Rationale'],
    ['MCU', 'Nordic nRF5340', 'Dual-core (app + network), Thread certified'],
    ['FEM', 'nRF21540', '+20 dBm TX, improves mesh reliability'],
    ['Power Management', 'TI BQ25125 + TPS62840', 'Battery charging + ultra-low Iq'],
    ['Crystal', '32 MHz + 32.768 kHz', 'Required for Thread timing'],
    ['Antenna', 'PCB trace or chip', 'Johanson or Fractus chip antenna'],
    ['Debug', 'SWD + RTT', 'Segger J-Link compatible'],
    ['Connector', 'Sensor expansion header', 'Modular sensor daughterboards'],
]
core_table = Table(core_specs, colWidths=[1.5*inch, 1.8*inch, 3*inch])
core_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_TEAL),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
]))
story.append(core_table)

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("4.2 Design for Manufacturing (DFM)", styles['SubHead']))

dfm_items = [
    "4-layer PCB minimum (signal, GND, power, signal)",
    "0402 passives minimum (0603 preferred for hand rework)",
    "QFN packages with exposed pad for thermal/RF performance",
    "Panelization for pick-and-place efficiency",
    "Test points for ICT/functional test",
    "Conformal coating for moisture resistance (water sensors)",
]
for item in dfm_items:
    story.append(Paragraph(f"• {item}", styles['TechBody']))

story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("4.3 Certifications Required", styles['SubHead']))

cert_data = [
    ['Certification', 'Scope', 'Timeline'],
    ['FCC Part 15', 'RF emissions (required)', '4-6 weeks'],
    ['IC (Canada)', 'RF emissions', '4-6 weeks'],
    ['CE (EU)', 'RF + safety', '6-8 weeks'],
    ['UL/ETL', 'Safety (electrical sensor)', '8-12 weeks'],
    ['Matter Certification', 'Interoperability', '4-8 weeks'],
    ['Thread Certification', 'Protocol compliance', '2-4 weeks'],
]
cert_table = Table(cert_data, colWidths=[1.8*inch, 2.5*inch, 1.5*inch])
cert_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
    ('ALIGN', (2, 0), (2, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
]))
story.append(cert_table)

story.append(PageBreak())

# ==================== BOM & COST TARGETS ====================
story.append(Paragraph("5. BOM & Cost Targets", styles['SectionHead']))
story.append(HRFlowable(width="100%", thickness=1, color=TECH_DARK))
story.append(Spacer(1, 0.15*inch))

story.append(Paragraph("Target BOM cost at 10K unit volume:", styles['TechBody']))

bom_data = [
    ['Module', 'Target BOM', 'Target MSRP', 'Key Cost Drivers'],
    ['WTR-X1 (Water)', '$35-45', '$149', 'Pressure sensor, flow sensor'],
    ['ELC-X1 (Electrical)', '$50-65', '$199', 'High-speed ADC, isolation'],
    ['STR-X1 (Structural)', '$30-40', '$129', 'Accelerometer, tilt sensor'],
    ['HVC-X1 (HVAC)', '$35-45', '$149', 'Multi-temp, current sense'],
    ['ENV-X1 (Environmental)', '$25-35', '$99', 'Smoke/CO sensors'],
    ['Hub (Border Router)', '$40-55', '$179', 'WiFi/LTE module'],
]
bom_table = Table(bom_data, colWidths=[1.6*inch, 1.1*inch, 1.1*inch, 2.5*inch])
bom_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_TEAL),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (1, 0), (2, -1), 'CENTER'),
    ('TOPPADDING', (0, 0), (-1, -1), 8),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
]))
story.append(bom_table)

story.append(Spacer(1, 0.2*inch))

story.append(Paragraph("Typical Home Bundle", styles['SubHead']))

bundle_text = """
<b>Starter Kit:</b> 1x Water + 1x Electrical + 1x Environmental + Hub = <b>$499 MSRP</b><br/>
<b>Full Home:</b> 3x Water + 1x Electrical + 2x Structural + 1x HVAC + 2x Environmental + Hub = <b>$1,199 MSRP</b>
"""
story.append(Paragraph(bundle_text, styles['TechBody']))

story.append(PageBreak())

# ==================== DEVELOPMENT ROADMAP ====================
story.append(Paragraph("6. Development Roadmap", styles['SectionHead']))
story.append(HRFlowable(width="100%", thickness=1, color=TECH_DARK))
story.append(Spacer(1, 0.15*inch))

roadmap_data = [
    ['Phase', 'Deliverable', 'Duration'],
    ['Phase 1', 'Core platform PCB (nRF5340 base)\nWater sensor prototype\nThread/Matter stack integration', '8-10 weeks'],
    ['Phase 2', 'Electrical sensor prototype\nArc fault detection validation\nFCC pre-scan', '6-8 weeks'],
    ['Phase 3', 'Structural + HVAC + Environmental protos\nFull system integration\nField testing (10 homes)', '8-10 weeks'],
    ['Phase 4', 'DFM optimization\nCertification (FCC, Matter, UL)\nPilot production (500 units)', '10-12 weeks'],
    ['Phase 5', 'Mass production ramp\nCarrier partnerships\nScale to 10K+ units', 'Ongoing'],
]
roadmap_table = Table(roadmap_data, colWidths=[1.2*inch, 3.5*inch, 1.3*inch])
roadmap_table.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), TECH_DARK),
    ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
    ('TEXTCOLOR', (0, 1), (0, -1), TECH_BLUE),
    ('FONTSIZE', (0, 0), (-1, -1), 9),
    ('ALIGN', (2, 0), (2, -1), 'CENTER'),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('TOPPADDING', (0, 0), (-1, -1), 10),
    ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
    ('ROWBACKGROUNDS', (0, 1), (-1, -1), [WHITE, LIGHT_BG]),
]))
story.append(roadmap_table)

story.append(PageBreak())

# ==================== THE ASK ====================
story.append(Spacer(1, 0.5*inch))

story.append(Paragraph("7. The Ask", styles['SectionHead']))
story.append(HRFlowable(width="100%", thickness=2, color=TECH_TEAL))
story.append(Spacer(1, 0.2*inch))

ask_text = """
Joe, I need a co-founder who can own hardware.
"""
story.append(Paragraph(ask_text, ParagraphStyle('Ask', fontSize=16, textColor=TECH_DARK,
                                                 fontName='Helvetica-Bold', alignment=TA_CENTER)))

story.append(Spacer(1, 0.3*inch))

what_text = """
<b>What I've built:</b><br/>
• Complete backend platform (Go, QuestDB, Redis, Docker)<br/>
• ML anomaly detection pipeline<br/>
• API with authentication, rate limiting, CORS security<br/>
• Market research showing $150B opportunity<br/>
• Tesla pitch deck ready to send<br/><br/>

<b>What I need from you:</b><br/>
• PCB design and prototyping<br/>
• Sensor selection and validation<br/>
• Firmware development (Zephyr RTOS, Matter stack)<br/>
• Certification navigation (FCC, UL, Matter)<br/>
• Manufacturing relationships<br/><br/>

<b>What you get:</b><br/>
• Co-founder equity (negotiable)<br/>
• Technical leadership of hardware division<br/>
• Chance to build something that actually matters<br/>
• Oklahoma-based, your backyard
"""
story.append(Paragraph(what_text, styles['TechBody']))

story.append(Spacer(1, 0.4*inch))

# Call to action
story.append(Paragraph("Let's grab coffee and talk.", styles['Callout']))

story.append(Spacer(1, 0.5*inch))

# Contact
contact_text = """
<b>Eric De Loera</b><br/>
partners@ihp-home.io<br/><br/>
<i>"The platform is ready. The market is massive. We just need the hardware."</i>
"""
story.append(Paragraph(contact_text, ParagraphStyle('Contact', fontSize=11, textColor=TECH_DARK,
                                                     alignment=TA_CENTER, leading=16)))

# Build PDF
print("Generating Hardware Technical Specification...")
doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
print(f"\nPDF generated: {output_path}")
