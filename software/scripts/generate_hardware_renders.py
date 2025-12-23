#!/usr/bin/env python3
"""
I.H.P. - Hardware Rendering Document
Visual representations of sensor modules
"""

from datetime import datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    Image, PageBreak, HRFlowable
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line, Polygon, Ellipse
from reportlab.graphics import renderPDF
from reportlab.lib.colors import HexColor
import os

LOGO_PATH = "/Users/ericdeloera/Downloads/luxx-haus 5/assets/luxx_logo_light.png"

# Colors
TECH_DARK = HexColor('#1a1a2e')
TECH_TEAL = HexColor('#00b99b')
TECH_BLUE = HexColor('#3282d2')
TECH_ORANGE = HexColor('#ff6b35')
TECH_PURPLE = HexColor('#6f42c1')
TECH_GREEN = HexColor('#20c997')
TECH_RED = HexColor('#dc3545')
LIGHT_GRAY = HexColor('#e9ecef')
MID_GRAY = HexColor('#6c757d')
DARK_GRAY = HexColor('#343a40')
PCB_GREEN = HexColor('#2d5016')
PCB_GOLD = HexColor('#d4a84b')
METAL_SILVER = HexColor('#a8a8a8')
METAL_DARK = HexColor('#555555')

def draw_water_sensor(width=400, height=300):
    """Draw Water Pressure & Flow Sensor"""
    d = Drawing(width, height)

    # Background
    d.add(Rect(0, 0, width, height, fillColor=HexColor('#f8f9fa'), strokeColor=None))

    # Title
    d.add(String(width/2, height-25, "WTR-X1 Water Sensor", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=TECH_DARK, textAnchor='middle'))

    # Main body - cylindrical brass fitting
    cx, cy = width/2, height/2 - 20

    # Brass pipe fittings (left and right)
    d.add(Rect(cx-120, cy-15, 40, 30, fillColor=PCB_GOLD, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(Rect(cx+80, cy-15, 40, 30, fillColor=PCB_GOLD, strokeColor=METAL_DARK, strokeWidth=1))

    # Pipe threads
    for i in range(4):
        d.add(Line(cx-118, cy-12+i*8, cx-82, cy-12+i*8, strokeColor=METAL_DARK, strokeWidth=0.5))
        d.add(Line(cx+82, cy-12+i*8, cx+118, cy-12+i*8, strokeColor=METAL_DARK, strokeWidth=0.5))

    # Main sensor housing
    d.add(Rect(cx-80, cy-40, 160, 80, fillColor=TECH_DARK, strokeColor=TECH_TEAL, strokeWidth=2, rx=8))

    # Top module (electronics housing)
    d.add(Rect(cx-50, cy+40, 100, 50, fillColor=TECH_DARK, strokeColor=TECH_TEAL, strokeWidth=2, rx=5))

    # LED indicators
    d.add(Circle(cx-30, cy+60, 5, fillColor=TECH_TEAL, strokeColor=None))
    d.add(Circle(cx, cy+60, 5, fillColor=TECH_BLUE, strokeColor=None))
    d.add(Circle(cx+30, cy+60, 5, fillColor=TECH_GREEN, strokeColor=None))

    # Display window
    d.add(Rect(cx-35, cy+70, 70, 15, fillColor=HexColor('#001a00'), strokeColor=TECH_TEAL, strokeWidth=1))
    d.add(String(cx, cy+80, "58.2 PSI", fontSize=8, fontName='Courier-Bold',
                 fillColor=TECH_TEAL, textAnchor='middle'))

    # Sensor label
    d.add(String(cx, cy, "I.H.P.", fontSize=14, fontName='Helvetica-Bold',
                 fillColor=TECH_TEAL, textAnchor='middle'))
    d.add(String(cx, cy-15, "WTR-X1", fontSize=10, fontName='Helvetica',
                 fillColor=MID_GRAY, textAnchor='middle'))

    # Flow direction arrows
    d.add(Polygon([cx-100, cy-5, cx-90, cy, cx-100, cy+5], fillColor=TECH_BLUE, strokeColor=None))
    d.add(Polygon([cx+100, cy-5, cx+90, cy, cx+100, cy+5], fillColor=TECH_BLUE, strokeColor=None))

    # Moisture probe (bottom)
    d.add(Line(cx, cy-40, cx, cy-70, strokeColor=TECH_TEAL, strokeWidth=2))
    d.add(Circle(cx, cy-75, 8, fillColor=TECH_TEAL, strokeColor=TECH_DARK, strokeWidth=1))

    # Specs
    specs = [
        "• Pressure: 0-150 PSI (±0.5%)",
        "• Flow: 0.1-50 L/min ultrasonic",
        "• Moisture: Capacitive probe",
        "• Protocol: Matter 1.4 / Thread",
        "• Battery: 10+ year Li-SOCL2",
    ]
    for i, spec in enumerate(specs):
        d.add(String(20, 80-i*14, spec, fontSize=9, fontName='Helvetica', fillColor=DARK_GRAY))

    return d

def draw_electrical_sensor(width=400, height=300):
    """Draw Electrical Monitoring Sensor"""
    d = Drawing(width, height)

    d.add(Rect(0, 0, width, height, fillColor=HexColor('#f8f9fa'), strokeColor=None))

    d.add(String(width/2, height-25, "ELC-X1 Electrical Monitor", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=TECH_DARK, textAnchor='middle'))

    cx, cy = width/2, height/2 - 10

    # Main enclosure (panel mount style)
    d.add(Rect(cx-90, cy-60, 180, 120, fillColor=TECH_DARK, strokeColor=TECH_ORANGE, strokeWidth=2, rx=5))

    # Inner panel
    d.add(Rect(cx-80, cy-50, 160, 100, fillColor=HexColor('#252540'), strokeColor=None, rx=3))

    # Display screen
    d.add(Rect(cx-60, cy, 120, 40, fillColor=HexColor('#001a00'), strokeColor=TECH_ORANGE, strokeWidth=1))
    d.add(String(cx, cy+30, "ARC: 0.02", fontSize=10, fontName='Courier-Bold',
                 fillColor=TECH_ORANGE, textAnchor='middle'))
    d.add(String(cx, cy+15, "PWR: 2.4kW", fontSize=8, fontName='Courier',
                 fillColor=TECH_GREEN, textAnchor='middle'))

    # Status LEDs
    d.add(Circle(cx-50, cy-30, 6, fillColor=TECH_GREEN, strokeColor=None))
    d.add(Circle(cx-30, cy-30, 6, fillColor=TECH_ORANGE, strokeColor=None))
    d.add(Circle(cx-10, cy-30, 6, fillColor=MID_GRAY, strokeColor=None))

    # Labels
    d.add(String(cx-50, cy-42, "OK", fontSize=6, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))
    d.add(String(cx-30, cy-42, "ARC", fontSize=6, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))
    d.add(String(cx-10, cy-42, "FAULT", fontSize=6, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # I.H.P. branding
    d.add(String(cx+40, cy-30, "I.H.P.", fontSize=12, fontName='Helvetica-Bold',
                 fillColor=TECH_ORANGE, textAnchor='middle'))

    # CT clamps (current transformers)
    for i, offset in enumerate([-50, 0, 50]):
        # CT ring
        d.add(Ellipse(cx+offset, cy-90, 20, 12, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))
        d.add(Ellipse(cx+offset, cy-90, 12, 7, fillColor=DARK_GRAY, strokeColor=None))
        # Wire coming through
        d.add(Line(cx+offset, cy-100, cx+offset, cy-80, strokeColor=['black', 'red', 'blue'][i], strokeWidth=3))
        # Cable to main unit
        d.add(Line(cx+offset, cy-78, cx+offset, cy-60, strokeColor=DARK_GRAY, strokeWidth=1))

    # CT label
    d.add(String(cx, cy-110, "Split-Core CTs (L1, L2, N)", fontSize=8, fontName='Helvetica',
                 fillColor=MID_GRAY, textAnchor='middle'))

    # Mounting tabs
    d.add(Circle(cx-80, cy-50, 5, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(Circle(cx+80, cy-50, 5, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(Circle(cx-80, cy+50, 5, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(Circle(cx+80, cy+50, 5, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))

    # Specs
    specs = [
        "• Arc Fault: 1-100 MHz detection",
        "• Sampling: 1 MSPS for signatures",
        "• Current: 0-200A per phase",
        "• Isolation: 4kV reinforced",
        "• Install: Panel mount, no rewiring",
    ]
    for i, spec in enumerate(specs):
        d.add(String(20, 80-i*14, spec, fontSize=9, fontName='Helvetica', fillColor=DARK_GRAY))

    return d

def draw_structural_sensor(width=400, height=300):
    """Draw Structural Monitoring Sensor"""
    d = Drawing(width, height)

    d.add(Rect(0, 0, width, height, fillColor=HexColor('#f8f9fa'), strokeColor=None))

    d.add(String(width/2, height-25, "STR-X1 Structural Sensor", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=TECH_DARK, textAnchor='middle'))

    cx, cy = width/2, height/2

    # Compact weatherproof housing
    d.add(Rect(cx-60, cy-40, 120, 80, fillColor=TECH_DARK, strokeColor=TECH_PURPLE, strokeWidth=2, rx=10))

    # Top cap (weatherproof seal)
    d.add(Rect(cx-55, cy+35, 110, 10, fillColor=HexColor('#333355'), strokeColor=None, rx=3))

    # Solar panel on top
    d.add(Rect(cx-45, cy+45, 90, 25, fillColor=HexColor('#1a1a3a'), strokeColor=TECH_PURPLE, strokeWidth=1))
    # Solar cells
    for i in range(6):
        d.add(Rect(cx-42+i*15, cy+48, 12, 19, fillColor=HexColor('#2a2a5a'), strokeColor=HexColor('#3a3a6a'), strokeWidth=0.5))

    # LED window
    d.add(Rect(cx-40, cy+10, 80, 20, fillColor=HexColor('#001a00'), strokeColor=TECH_PURPLE, strokeWidth=1))
    d.add(String(cx, cy+22, "TILT: 0.00°", fontSize=9, fontName='Courier-Bold',
                 fillColor=TECH_PURPLE, textAnchor='middle'))

    # Accelerometer icon
    d.add(Rect(cx-25, cy-25, 50, 30, fillColor=HexColor('#252540'), strokeColor=None, rx=3))
    # XYZ axes
    d.add(Line(cx, cy-20, cx+15, cy-20, strokeColor=TECH_RED, strokeWidth=2))
    d.add(Line(cx, cy-20, cx, cy-5, strokeColor=TECH_GREEN, strokeWidth=2))
    d.add(Line(cx, cy-20, cx-10, cy-12, strokeColor=TECH_BLUE, strokeWidth=2))
    d.add(String(cx+18, cy-22, "X", fontSize=7, fontName='Helvetica-Bold', fillColor=TECH_RED))
    d.add(String(cx+3, cy-3, "Y", fontSize=7, fontName='Helvetica-Bold', fillColor=TECH_GREEN))
    d.add(String(cx-18, cy-10, "Z", fontSize=7, fontName='Helvetica-Bold', fillColor=TECH_BLUE))

    # I.H.P. branding
    d.add(String(cx, cy-35, "I.H.P.", fontSize=10, fontName='Helvetica-Bold',
                 fillColor=TECH_PURPLE, textAnchor='middle'))

    # Mounting base
    d.add(Rect(cx-70, cy-50, 140, 12, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))
    # Mounting holes
    d.add(Circle(cx-55, cy-44, 4, fillColor=DARK_GRAY, strokeColor=None))
    d.add(Circle(cx+55, cy-44, 4, fillColor=DARK_GRAY, strokeColor=None))

    # External strain gauge connector
    d.add(Rect(cx+50, cy-10, 15, 25, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(String(cx+80, cy+2, "STRAIN", fontSize=6, fontName='Helvetica', fillColor=MID_GRAY))

    # Specs
    specs = [
        "• Accelerometer: ±16g, 3-axis",
        "• Tilt: ±60°, 0.01° resolution",
        "• Strain: 4x quarter-bridge inputs",
        "• Power: Li-SOCL2 + solar backup",
        "• Rating: -40°C to 85°C outdoor",
    ]
    for i, spec in enumerate(specs):
        d.add(String(20, 80-i*14, spec, fontSize=9, fontName='Helvetica', fillColor=DARK_GRAY))

    return d

def draw_hvac_sensor(width=400, height=300):
    """Draw HVAC Monitoring Sensor"""
    d = Drawing(width, height)

    d.add(Rect(0, 0, width, height, fillColor=HexColor('#f8f9fa'), strokeColor=None))

    d.add(String(width/2, height-25, "HVC-X1 HVAC Monitor", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=TECH_DARK, textAnchor='middle'))

    cx, cy = width/2, height/2

    # Main enclosure
    d.add(Rect(cx-70, cy-45, 140, 90, fillColor=TECH_DARK, strokeColor=TECH_GREEN, strokeWidth=2, rx=8))

    # Display
    d.add(Rect(cx-55, cy-5, 110, 35, fillColor=HexColor('#001a00'), strokeColor=TECH_GREEN, strokeWidth=1))
    d.add(String(cx, cy+22, "SUPPLY: 72°F", fontSize=9, fontName='Courier-Bold',
                 fillColor=TECH_GREEN, textAnchor='middle'))
    d.add(String(cx, cy+8, "RETURN: 58°F", fontSize=8, fontName='Courier',
                 fillColor=TECH_TEAL, textAnchor='middle'))

    # Status indicators
    d.add(Circle(cx-40, cy-30, 5, fillColor=TECH_GREEN, strokeColor=None))
    d.add(Circle(cx-20, cy-30, 5, fillColor=TECH_GREEN, strokeColor=None))
    d.add(Circle(cx, cy-30, 5, fillColor=MID_GRAY, strokeColor=None))
    d.add(String(cx-40, cy-40, "RUN", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))
    d.add(String(cx-20, cy-40, "EFF", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))
    d.add(String(cx, cy-40, "ALERT", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # I.H.P. branding
    d.add(String(cx+35, cy-30, "I.H.P.", fontSize=10, fontName='Helvetica-Bold',
                 fillColor=TECH_GREEN, textAnchor='middle'))

    # Temperature probes (cables coming out)
    d.add(Line(cx-70, cy+20, cx-100, cy+20, strokeColor=TECH_RED, strokeWidth=2))
    d.add(Line(cx-70, cy, cx-100, cy, strokeColor=TECH_BLUE, strokeWidth=2))
    d.add(Circle(cx-105, cy+20, 6, fillColor=TECH_RED, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(Circle(cx-105, cy, 6, fillColor=TECH_BLUE, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(String(cx-120, cy+22, "SUPPLY", fontSize=6, fontName='Helvetica', fillColor=TECH_RED))
    d.add(String(cx-120, cy+2, "RETURN", fontSize=6, fontName='Helvetica', fillColor=TECH_BLUE))

    # CT clamp for compressor current
    d.add(Ellipse(cx+100, cy, 15, 10, fillColor=METAL_SILVER, strokeColor=METAL_DARK, strokeWidth=1))
    d.add(Line(cx+70, cy, cx+85, cy, strokeColor=DARK_GRAY, strokeWidth=1))
    d.add(String(cx+100, cy-18, "COMP CT", fontSize=6, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Vibration sensor icon
    d.add(Rect(cx+20, cy-30, 30, 15, fillColor=HexColor('#252540'), strokeColor=None, rx=2))
    # Vibration wave
    d.add(String(cx+35, cy-20, "〰", fontSize=10, fontName='Helvetica', fillColor=TECH_GREEN, textAnchor='middle'))

    # Specs
    specs = [
        "• Temperature: -40°C to 150°C",
        "• Current: 0-50A compressor CT",
        "• Vibration: ±8g compressor health",
        "• Runtime: Cycle logging",
        "• Power: 24VAC tap or battery",
    ]
    for i, spec in enumerate(specs):
        d.add(String(20, 80-i*14, spec, fontSize=9, fontName='Helvetica', fillColor=DARK_GRAY))

    return d

def draw_environmental_sensor(width=400, height=300):
    """Draw Environmental Sensor (Smoke/CO)"""
    d = Drawing(width, height)

    d.add(Rect(0, 0, width, height, fillColor=HexColor('#f8f9fa'), strokeColor=None))

    d.add(String(width/2, height-25, "ENV-X1 Environmental Sensor", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=TECH_DARK, textAnchor='middle'))

    cx, cy = width/2, height/2

    # Circular smoke detector style housing
    d.add(Circle(cx, cy, 70, fillColor=TECH_DARK, strokeColor=TECH_RED, strokeWidth=2))
    d.add(Circle(cx, cy, 60, fillColor=HexColor('#252540'), strokeColor=None))

    # Vents/grilles (circular pattern)
    for angle in range(0, 360, 30):
        import math
        x1 = cx + 45 * math.cos(math.radians(angle))
        y1 = cy + 45 * math.sin(math.radians(angle))
        x2 = cx + 55 * math.cos(math.radians(angle))
        y2 = cy + 55 * math.sin(math.radians(angle))
        d.add(Line(x1, y1, x2, y2, strokeColor=MID_GRAY, strokeWidth=2))

    # Center display/indicator
    d.add(Circle(cx, cy, 25, fillColor=HexColor('#1a1a2e'), strokeColor=TECH_RED, strokeWidth=1))

    # Status LED ring
    d.add(Circle(cx, cy+8, 8, fillColor=TECH_GREEN, strokeColor=None))

    # I.H.P. text
    d.add(String(cx, cy-8, "I.H.P.", fontSize=10, fontName='Helvetica-Bold',
                 fillColor=TECH_RED, textAnchor='middle'))

    # Sensor labels around the unit
    d.add(String(cx, cy+90, "SMOKE + CO + TEMP + HUMIDITY", fontSize=8,
                 fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Test button
    d.add(Circle(cx+50, cy-50, 8, fillColor=MID_GRAY, strokeColor=DARK_GRAY, strokeWidth=1))
    d.add(String(cx+50, cy-65, "TEST", fontSize=6, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Mounting plate indication
    d.add(Circle(cx, cy, 75, fillColor=None, strokeColor=LIGHT_GRAY, strokeWidth=1, strokeDashArray=[3,3]))

    # Specs
    specs = [
        "• Smoke: Photoelectric + ionization",
        "• CO: 0-1000 ppm electrochemical",
        "• Temp: ±0.3°C accuracy",
        "• Humidity: 0-100% RH",
        "• Siren: 85 dB integrated",
    ]
    for i, spec in enumerate(specs):
        d.add(String(20, 80-i*14, spec, fontSize=9, fontName='Helvetica', fillColor=DARK_GRAY))

    return d

def draw_hub(width=400, height=300):
    """Draw Hub/Border Router"""
    d = Drawing(width, height)

    d.add(Rect(0, 0, width, height, fillColor=HexColor('#f8f9fa'), strokeColor=None))

    d.add(String(width/2, height-25, "HUB-X1 Border Router", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=TECH_DARK, textAnchor='middle'))

    cx, cy = width/2, height/2

    # Main housing (sleek rectangle)
    d.add(Rect(cx-80, cy-35, 160, 70, fillColor=TECH_DARK, strokeColor=TECH_TEAL, strokeWidth=2, rx=10))

    # Top light bar
    d.add(Rect(cx-60, cy+25, 120, 5, fillColor=TECH_TEAL, strokeColor=None, rx=2))

    # Front panel
    d.add(Rect(cx-70, cy-25, 140, 45, fillColor=HexColor('#252540'), strokeColor=None, rx=5))

    # I.H.P. logo
    d.add(String(cx, cy+5, "I.H.P.", fontSize=18, fontName='Helvetica-Bold',
                 fillColor=TECH_TEAL, textAnchor='middle'))
    d.add(String(cx, cy-12, "INTELLIGENT HOME PROTECTION", fontSize=6,
                 fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Status LEDs
    d.add(Circle(cx-50, cy-20, 4, fillColor=TECH_GREEN, strokeColor=None))
    d.add(Circle(cx-35, cy-20, 4, fillColor=TECH_BLUE, strokeColor=None))
    d.add(Circle(cx-20, cy-20, 4, fillColor=TECH_TEAL, strokeColor=None))

    # LED labels
    d.add(String(cx-50, cy-28, "NET", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))
    d.add(String(cx-35, cy-28, "MESH", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))
    d.add(String(cx-20, cy-28, "CLOUD", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Back ports
    d.add(Rect(cx-70, cy-45, 140, 12, fillColor=METAL_DARK, strokeColor=None))
    # Ethernet port
    d.add(Rect(cx-55, cy-43, 15, 8, fillColor=DARK_GRAY, strokeColor=None))
    # USB port
    d.add(Rect(cx-30, cy-43, 10, 8, fillColor=DARK_GRAY, strokeColor=None))
    # Power port
    d.add(Circle(cx+50, cy-39, 4, fillColor=DARK_GRAY, strokeColor=None))

    # Antenna (if external)
    d.add(Rect(cx+65, cy-35, 8, 60, fillColor=TECH_DARK, strokeColor=TECH_TEAL, strokeWidth=1, rx=3))
    d.add(Circle(cx+69, cy+30, 6, fillColor=TECH_TEAL, strokeColor=None))

    # Wireless signals
    for i in range(3):
        r = 90 + i*15
        d.add(Circle(cx, cy, r, fillColor=None, strokeColor=TECH_TEAL, strokeWidth=0.5,
                     strokeDashArray=[2,4]))

    # Specs
    specs = [
        "• Thread 1.3 Border Router",
        "• WiFi 6 + LTE-M backup",
        "• Matter 1.4 controller",
        "• 256-bit AES encryption",
        "• Supports 100+ sensors",
    ]
    for i, spec in enumerate(specs):
        d.add(String(20, 80-i*14, spec, fontSize=9, fontName='Helvetica', fillColor=DARK_GRAY))

    return d

def draw_pcb_layout(width=400, height=300):
    """Draw PCB Layout (Common Core)"""
    d = Drawing(width, height)

    d.add(Rect(0, 0, width, height, fillColor=HexColor('#f8f9fa'), strokeColor=None))

    d.add(String(width/2, height-25, "Common Core PCB Layout", fontSize=16,
                 fontName='Helvetica-Bold', fillColor=TECH_DARK, textAnchor='middle'))

    cx, cy = width/2, height/2

    # PCB board
    d.add(Rect(cx-120, cy-70, 240, 140, fillColor=PCB_GREEN, strokeColor=HexColor('#1a3a0a'), strokeWidth=2))

    # Mounting holes
    for x, y in [(cx-105, cy-55), (cx+105, cy-55), (cx-105, cy+55), (cx+105, cy+55)]:
        d.add(Circle(x, y, 5, fillColor=METAL_SILVER, strokeColor=PCB_GOLD, strokeWidth=1))

    # nRF5340 MCU (main chip)
    d.add(Rect(cx-30, cy-20, 60, 40, fillColor=DARK_GRAY, strokeColor=None))
    d.add(String(cx, cy+5, "nRF5340", fontSize=7, fontName='Helvetica-Bold', fillColor=colors.white, textAnchor='middle'))
    d.add(String(cx, cy-8, "ARM M33", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Chip pins (simplified)
    for i in range(8):
        d.add(Rect(cx-32-3, cy-18+i*7, 5, 4, fillColor=PCB_GOLD, strokeColor=None))
        d.add(Rect(cx+30, cy-18+i*7, 5, 4, fillColor=PCB_GOLD, strokeColor=None))

    # FEM (nRF21540)
    d.add(Rect(cx+50, cy-10, 30, 20, fillColor=DARK_GRAY, strokeColor=None))
    d.add(String(cx+65, cy+2, "FEM", fontSize=6, fontName='Helvetica-Bold', fillColor=colors.white, textAnchor='middle'))

    # Power management
    d.add(Rect(cx-90, cy-10, 25, 20, fillColor=DARK_GRAY, strokeColor=None))
    d.add(String(cx-77, cy+2, "PMIC", fontSize=5, fontName='Helvetica-Bold', fillColor=colors.white, textAnchor='middle'))

    # Crystals
    d.add(Rect(cx-50, cy+30, 15, 8, fillColor=METAL_SILVER, strokeColor=None))
    d.add(String(cx-42, cy+36, "32M", fontSize=5, fontName='Helvetica', fillColor=PCB_GREEN, textAnchor='middle'))
    d.add(Rect(cx-30, cy+30, 12, 6, fillColor=METAL_SILVER, strokeColor=None))
    d.add(String(cx-24, cy+36, "32K", fontSize=4, fontName='Helvetica', fillColor=PCB_GREEN, textAnchor='middle'))

    # Antenna (chip or trace)
    d.add(Rect(cx+85, cy-5, 20, 10, fillColor=PCB_GOLD, strokeColor=None))
    d.add(String(cx+95, cy+10, "ANT", fontSize=5, fontName='Helvetica', fillColor=PCB_GREEN, textAnchor='middle'))

    # Sensor expansion header
    d.add(Rect(cx-10, cy-60, 70, 12, fillColor=DARK_GRAY, strokeColor=None))
    for i in range(10):
        d.add(Rect(cx-7+i*7, cy-58, 4, 8, fillColor=PCB_GOLD, strokeColor=None))
    d.add(String(cx+25, cy-50, "SENSOR HDR", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Debug header
    d.add(Rect(cx-90, cy+35, 30, 8, fillColor=DARK_GRAY, strokeColor=None))
    d.add(String(cx-75, cy+48, "SWD", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # USB-C
    d.add(Rect(cx+70, cy+35, 18, 8, fillColor=METAL_SILVER, strokeColor=None))
    d.add(String(cx+79, cy+48, "USB-C", fontSize=5, fontName='Helvetica', fillColor=MID_GRAY, textAnchor='middle'))

    # Traces (simplified)
    d.add(Line(cx+30, cy, cx+50, cy, strokeColor=PCB_GOLD, strokeWidth=1))
    d.add(Line(cx-30, cy, cx-65, cy, strokeColor=PCB_GOLD, strokeWidth=1))
    d.add(Line(cx, cy+20, cx, cy+30, strokeColor=PCB_GOLD, strokeWidth=1))

    # Board label
    d.add(String(cx-95, cy+55, "I.H.P. CORE v1.0", fontSize=6, fontName='Helvetica', fillColor=PCB_GOLD))

    # Specs
    specs = [
        "• 4-layer PCB (sig/GND/pwr/sig)",
        "• Nordic nRF5340 + nRF21540 FEM",
        "• TI BQ25125 power management",
        "• Modular sensor daughterboards",
        "• Matter/Thread certified stack",
    ]
    for i, spec in enumerate(specs):
        d.add(String(20, 80-i*14, spec, fontSize=9, fontName='Helvetica', fillColor=DARK_GRAY))

    return d

# Create PDF
output_path = "/Users/ericdeloera/Downloads/luxx-haus 5/IHP_Hardware_Renders.pdf"
doc = SimpleDocTemplate(
    output_path,
    pagesize=letter,
    rightMargin=0.5*inch,
    leftMargin=0.5*inch,
    topMargin=0.75*inch,
    bottomMargin=0.5*inch
)

styles = getSampleStyleSheet()

styles.add(ParagraphStyle(
    name='MainTitle',
    fontSize=28,
    textColor=TECH_DARK,
    alignment=TA_CENTER,
    fontName='Helvetica-Bold',
    spaceAfter=10
))

styles.add(ParagraphStyle(
    name='Subtitle',
    fontSize=12,
    textColor=MID_GRAY,
    alignment=TA_CENTER,
    spaceAfter=30
))

# Build document
story = []

# Cover
story.append(Spacer(1, 0.5*inch))
if os.path.exists(LOGO_PATH):
    logo = Image(LOGO_PATH, width=4*inch, height=1.1*inch)
    logo.hAlign = 'CENTER'
    story.append(logo)
story.append(Spacer(1, 0.3*inch))
story.append(HRFlowable(width="40%", thickness=3, color=TECH_TEAL, hAlign='CENTER'))
story.append(Spacer(1, 0.3*inch))
story.append(Paragraph("Hardware Design Renders", styles['MainTitle']))
story.append(Paragraph("Sensor Module Visual Specifications", styles['Subtitle']))
story.append(Spacer(1, 1*inch))
story.append(Paragraph(f"Version 1.0 | {datetime.now().strftime('%B %Y')}",
                       ParagraphStyle('Date', fontSize=10, textColor=MID_GRAY, alignment=TA_CENTER)))
story.append(PageBreak())

# Sensor pages
sensors = [
    ("Water Sensor - WTR-X1", draw_water_sensor, "Primary water damage prevention. Monitors pressure, flow, and moisture at water entry points."),
    ("Electrical Monitor - ELC-X1", draw_electrical_sensor, "Arc fault and power quality monitoring. Detects electrical fire signatures before ignition."),
    ("Structural Sensor - STR-X1", draw_structural_sensor, "Foundation and structural health monitoring. Tracks settlement, vibration, and strain."),
    ("HVAC Monitor - HVC-X1", draw_hvac_sensor, "Heating and cooling system efficiency and health. Predicts failures before they occur."),
    ("Environmental Sensor - ENV-X1", draw_environmental_sensor, "Smoke, CO, temperature, and humidity monitoring. First line of defense for fire and air quality."),
    ("Hub / Border Router - HUB-X1", draw_hub, "Central intelligence hub. Bridges Thread mesh to cloud via WiFi or LTE."),
    ("Common Core PCB", draw_pcb_layout, "Shared platform architecture. All sensors use this core with modular sensor daughterboards."),
]

for title, draw_func, description in sensors:
    story.append(Paragraph(title, ParagraphStyle('SensorTitle', fontSize=20, textColor=TECH_DARK,
                                                  fontName='Helvetica-Bold', alignment=TA_CENTER)))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(description, ParagraphStyle('Desc', fontSize=10, textColor=MID_GRAY,
                                                        alignment=TA_CENTER)))
    story.append(Spacer(1, 0.2*inch))

    drawing = draw_func(500, 350)
    drawing.hAlign = 'CENTER'
    story.append(drawing)

    story.append(PageBreak())

# Build
print("Generating Hardware Renders PDF...")
doc.build(story)
print(f"\nPDF generated: {output_path}")
