#!/usr/bin/env python3
"""
I.H.P. Home Testing Kit - Eric De Loera Residence
Complete installation and testing plan
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, Color
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Colors
TEAL = HexColor('#0D9488')
CHARCOAL = HexColor('#1F2937')
LIGHT_GRAY = HexColor('#F3F4F6')
ORANGE = HexColor('#F59E0B')
GREEN = HexColor('#10B981')
RED = HexColor('#EF4444')
BLUE = HexColor('#2563EB')

BASE_DIR = "/Users/ericdeloera/Downloads/luxx-haus 5"

def draw_header(c, page_w, page_h, title):
    """Draw page header"""
    c.setFillColor(TEAL)
    c.rect(0, page_h - 60, page_w, 60, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(page_w/2, page_h - 40, title)

def draw_footer(c, page_w, page_num):
    """Draw page footer"""
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 8)
    c.drawString(40, 25, "I.H.P. HOME TESTING KIT | CONFIDENTIAL")
    c.drawRightString(page_w - 40, 25, f"Page {page_num}")
    c.drawCentredString(page_w/2, 25, "De Loera Development")

def generate_testing_kit_pdf():
    page_w, page_h = letter
    c = canvas.Canvas(f"{BASE_DIR}/IHP_Home_Testing_Kit.pdf", pagesize=letter)
    margin = 40
    page_num = 1

    # ========== COVER PAGE ==========
    c.setFillColor(TEAL)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Title
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(page_w/2, page_h - 180, "I.H.P.")
    c.setFont("Helvetica", 28)
    c.drawCentredString(page_w/2, page_h - 220, "Home Testing Kit")

    # Subtitle
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_w/2, page_h - 280, "PROTOTYPE INSTALLATION GUIDE")

    # Property info box
    c.setFillColor(Color(1, 1, 1, alpha=0.15))
    c.roundRect(margin + 40, page_h - 420, page_w - 2*margin - 80, 100, 10, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, page_h - 345, "TEST SITE")
    c.setFont("Helvetica", 16)
    c.drawCentredString(page_w/2, page_h - 370, "Eric De Loera Residence")
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, page_h - 390, "Oklahoma City, Oklahoma")
    c.drawCentredString(page_w/2, page_h - 408, "Test Site #001")

    # Classification
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w/2, page_h - 480, "CONFIDENTIAL - PROTOTYPE TESTING")

    # Bottom
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, 100, "De Loera Development")
    c.setFont("Helvetica", 11)
    c.drawCentredString(page_w/2, 80, "December 2024")

    c.showPage()
    page_num += 1

    # ========== PAGE 2: TESTING KIT CONTENTS ==========
    draw_header(c, page_w, page_h, "TESTING KIT CONTENTS")

    y = page_h - 100

    # Kit overview
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "What's In The Kit:")
    y -= 30

    kit_items = [
        ("1x", "I.H.P. Hub (Border Router)", "nRF5340 + WiFi/LTE", "$179"),
        ("2x", "WTR-X1 Water Sensors", "Pressure + Flow + Moisture", "$298"),
        ("1x", "ELC-X1 Electrical Monitor", "Arc Fault + Power Quality", "$199"),
        ("1x", "STR-X1 Structural Sensor", "Vibration + Tilt + Strain", "$129"),
        ("1x", "HVC-X1 HVAC Monitor", "Temp + Pressure + Vibration", "$149"),
        ("2x", "ENV-X1 Environmental", "Smoke + CO + Temp + Humidity", "$198"),
    ]

    c.setFillColor(LIGHT_GRAY)
    c.roundRect(margin, y - 180, page_w - 2*margin, 190, 8, fill=1, stroke=0)

    y -= 15
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(TEAL)
    c.drawString(margin + 15, y, "QTY")
    c.drawString(margin + 55, y, "DEVICE")
    c.drawString(margin + 240, y, "CAPABILITIES")
    c.drawString(page_w - margin - 60, y, "VALUE")
    y -= 5

    c.setStrokeColor(TEAL)
    c.setLineWidth(1)
    c.line(margin + 15, y, page_w - margin - 15, y)
    y -= 20

    c.setFont("Helvetica", 10)
    for qty, device, capabilities, price in kit_items:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin + 15, y, qty)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin + 55, y, device)
        c.setFont("Helvetica", 9)
        c.drawString(margin + 240, y, capabilities)
        c.setFillColor(GREEN)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(page_w - margin - 55, y, price)
        y -= 22

    # Total
    y -= 10
    c.setStrokeColor(TEAL)
    c.line(margin + 15, y + 5, page_w - margin - 15, y + 5)
    y -= 15
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin + 55, y, "TOTAL KIT VALUE (MSRP)")
    c.setFillColor(TEAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(page_w - margin - 70, y, "$1,152")

    # Additional items
    y -= 50
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Additional Items Included:")
    y -= 25

    additional = [
        "USB-C cables and power adapters for each device",
        "Mounting hardware (brackets, screws, adhesive pads)",
        "Split-core current transformers (CTs) for electrical panel",
        "Moisture probe extensions for water sensors",
        "Installation tools (screwdriver set, wire strippers)",
        "Quick start guide and installation manual",
        "Testing log sheets for data collection",
        "I.H.P. mobile app access (beta)",
    ]

    c.setFont("Helvetica", 10)
    for item in additional:
        c.setFillColor(TEAL)
        c.drawString(margin + 10, y, "•")
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 25, y, item)
        y -= 18

    draw_footer(c, page_w, page_num)
    c.showPage()
    page_num += 1

    # ========== PAGE 3: INSTALLATION LOCATIONS ==========
    draw_header(c, page_w, page_h, "INSTALLATION LOCATIONS")

    y = page_h - 100

    locations = [
        {
            "zone": "ZONE 1: WATER ENTRY",
            "device": "WTR-X1 Water Sensor #1",
            "location": "Main water shutoff valve (garage or utility room)",
            "monitors": ["Water pressure (0-150 PSI)", "Flow rate (0.1-50 L/min)", "Moisture detection"],
            "install": "Clamp-on installation, no plumbing modification required"
        },
        {
            "zone": "ZONE 2: WATER HEATER",
            "device": "WTR-X1 Water Sensor #2",
            "location": "Near water heater supply/drain",
            "monitors": ["Temperature anomalies", "Leak detection", "Pressure fluctuations"],
            "install": "Place moisture probe on floor near water heater base"
        },
        {
            "zone": "ZONE 3: ELECTRICAL PANEL",
            "device": "ELC-X1 Electrical Monitor",
            "location": "Main electrical panel",
            "monitors": ["Arc fault signatures (1-100 MHz)", "Voltage quality", "Power consumption", "Harmonic distortion"],
            "install": "Split-core CTs around main feeds, no rewiring needed"
        },
        {
            "zone": "ZONE 4: FOUNDATION",
            "device": "STR-X1 Structural Sensor",
            "location": "Foundation wall or floor joist (basement/crawlspace)",
            "monitors": ["Vibration patterns", "Tilt/settlement", "Seismic activity"],
            "install": "Epoxy mount or mechanical bracket"
        },
        {
            "zone": "ZONE 5: HVAC SYSTEM",
            "device": "HVC-X1 HVAC Monitor",
            "location": "Near air handler/furnace unit",
            "monitors": ["Supply/return temps", "Compressor vibration", "Runtime cycles"],
            "install": "24VAC power tap from HVAC system preferred"
        },
        {
            "zone": "ZONE 6: LIVING AREA",
            "device": "ENV-X1 Environmental #1",
            "location": "Main living room or hallway",
            "monitors": ["Smoke detection", "CO levels", "Temperature", "Humidity"],
            "install": "Ceiling mount, replaces existing smoke detector"
        },
        {
            "zone": "ZONE 7: BEDROOM",
            "device": "ENV-X1 Environmental #2",
            "location": "Master bedroom hallway",
            "monitors": ["Smoke/CO monitoring", "Sleep environment tracking"],
            "install": "Ceiling mount near bedroom doors"
        },
        {
            "zone": "ZONE 8: HUB CENTRAL",
            "device": "I.H.P. Hub (Border Router)",
            "location": "Central location (living room or office)",
            "monitors": ["Thread mesh coordinator", "Cloud connectivity", "Local processing"],
            "install": "Wall mount or shelf, needs WiFi access"
        },
    ]

    for loc in locations:
        # Check if we need a new page
        if y < 150:
            draw_footer(c, page_w, page_num)
            c.showPage()
            page_num += 1
            draw_header(c, page_w, page_h, "INSTALLATION LOCATIONS (CONT.)")
            y = page_h - 100

        # Zone header
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin, y, loc["zone"])
        y -= 18

        # Device and location
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin + 10, y, f"Device: {loc['device']}")
        y -= 15
        c.setFont("Helvetica", 10)
        c.drawString(margin + 10, y, f"Location: {loc['location']}")
        y -= 15

        # Monitors
        c.setFont("Helvetica", 9)
        c.setFillColor(CHARCOAL)
        monitors_text = "Monitors: " + ", ".join(loc["monitors"])
        if len(monitors_text) > 80:
            c.drawString(margin + 10, y, monitors_text[:80])
            y -= 12
            c.drawString(margin + 10, y, monitors_text[80:])
        else:
            c.drawString(margin + 10, y, monitors_text)
        y -= 15

        # Install note
        c.setFillColor(GREEN)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin + 10, y, f"Install: {loc['install']}")
        y -= 30

    draw_footer(c, page_w, page_num)
    c.showPage()
    page_num += 1

    # ========== PAGE 4: FLOOR PLAN DIAGRAM ==========
    draw_header(c, page_w, page_h, "SENSOR PLACEMENT DIAGRAM")

    y = page_h - 90

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 11)
    c.drawCentredString(page_w/2, y, "Typical Home Layout - Adjust for Your Specific Floor Plan")
    y -= 30

    # Draw a simple house floor plan
    plan_x = margin + 30
    plan_y = y - 320
    plan_w = page_w - 2*margin - 60
    plan_h = 300

    # House outline
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(2)
    c.rect(plan_x, plan_y, plan_w, plan_h, fill=0, stroke=1)

    # Room divisions
    c.setLineWidth(1)
    # Vertical divider (left third)
    c.line(plan_x + plan_w*0.35, plan_y, plan_x + plan_w*0.35, plan_y + plan_h)
    # Horizontal divider (top section)
    c.line(plan_x + plan_w*0.35, plan_y + plan_h*0.5, plan_x + plan_w, plan_y + plan_h*0.5)
    # Another vertical (bedrooms)
    c.line(plan_x + plan_w*0.65, plan_y + plan_h*0.5, plan_x + plan_w*0.65, plan_y + plan_h)

    # Room labels
    c.setFont("Helvetica", 9)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(plan_x + plan_w*0.175, plan_y + plan_h*0.85, "GARAGE")
    c.drawCentredString(plan_x + plan_w*0.175, plan_y + plan_h*0.4, "UTILITY")
    c.drawCentredString(plan_x + plan_w*0.675, plan_y + plan_h*0.25, "LIVING ROOM")
    c.drawCentredString(plan_x + plan_w*0.5, plan_y + plan_h*0.75, "BEDROOM 1")
    c.drawCentredString(plan_x + plan_w*0.825, plan_y + plan_h*0.75, "BEDROOM 2")

    # Sensor markers with colors
    sensors = [
        (plan_x + plan_w*0.175, plan_y + plan_h*0.65, BLUE, "WTR-X1", "Water Main"),
        (plan_x + plan_w*0.175, plan_y + plan_h*0.2, BLUE, "WTR-X1", "Water Heater"),
        (plan_x + plan_w*0.28, plan_y + plan_h*0.85, ORANGE, "ELC-X1", "Panel"),
        (plan_x + plan_w*0.1, plan_y + plan_h*0.1, HexColor('#8B5CF6'), "STR-X1", "Foundation"),
        (plan_x + plan_w*0.28, plan_y + plan_h*0.2, HexColor('#EC4899'), "HVC-X1", "HVAC"),
        (plan_x + plan_w*0.675, plan_y + plan_h*0.25, RED, "ENV-X1", "Living"),
        (plan_x + plan_w*0.65, plan_y + plan_h*0.6, RED, "ENV-X1", "Hall"),
        (plan_x + plan_w*0.675, plan_y + plan_h*0.1, TEAL, "HUB", "Central"),
    ]

    for sx, sy, color, label, desc in sensors:
        # Draw sensor dot
        c.setFillColor(color)
        c.circle(sx, sy, 8, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 6)
        # Draw label below
        c.setFillColor(color)
        c.setFont("Helvetica-Bold", 7)
        c.drawCentredString(sx, sy - 15, label)

    # Legend
    y = plan_y - 30
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "LEGEND:")
    y -= 20

    legend_items = [
        (BLUE, "WTR-X1 - Water Sensor"),
        (ORANGE, "ELC-X1 - Electrical Monitor"),
        (HexColor('#8B5CF6'), "STR-X1 - Structural Sensor"),
        (HexColor('#EC4899'), "HVC-X1 - HVAC Monitor"),
        (RED, "ENV-X1 - Environmental Sensor"),
        (TEAL, "HUB - Border Router"),
    ]

    x_pos = margin
    for color, text in legend_items:
        c.setFillColor(color)
        c.circle(x_pos + 5, y + 3, 5, fill=1, stroke=0)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 8)
        c.drawString(x_pos + 15, y, text)
        x_pos += 130
        if x_pos > page_w - 150:
            x_pos = margin
            y -= 15

    draw_footer(c, page_w, page_num)
    c.showPage()
    page_num += 1

    # ========== PAGE 5: TESTING PROTOCOL ==========
    draw_header(c, page_w, page_h, "TESTING PROTOCOL")

    y = page_h - 100

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "Phase 1: Installation & Baseline (Week 1)")
    y -= 25

    phase1_tasks = [
        "Install all sensors per location guide",
        "Power on Hub and connect to WiFi",
        "Commission each sensor via I.H.P. app",
        "Verify Thread mesh network formation",
        "Confirm cloud connectivity (AWS IoT Core)",
        "Establish baseline readings for all sensors",
        "Document initial sensor values in testing log",
    ]

    c.setFont("Helvetica", 10)
    for i, task in enumerate(phase1_tasks, 1):
        c.setFillColor(TEAL)
        c.drawString(margin + 10, y, f"{i}.")
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 30, y, task)
        y -= 18

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(CHARCOAL)
    c.drawString(margin, y, "Phase 2: Controlled Testing (Week 2-3)")
    y -= 25

    phase2_tests = [
        ("Water Test", "Open faucet, flush toilet - verify flow detection"),
        ("Pressure Test", "Monitor pressure during high-usage periods"),
        ("Moisture Test", "Place wet cloth near probe - verify alert"),
        ("Electrical Test", "Turn on high-draw appliances - monitor power quality"),
        ("Arc Simulation", "Use arc fault generator if available"),
        ("Structural Test", "Walk heavily near sensor - verify vibration pickup"),
        ("HVAC Test", "Run heating/cooling cycles - monitor efficiency"),
        ("Smoke Test", "Use smoke test spray near ENV sensor"),
        ("CO Test", "Verify CO sensor responds to test button"),
    ]

    c.setFont("Helvetica", 10)
    for test, desc in phase2_tests:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin + 10, y, f"• {test}:")
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 10)
        c.drawString(margin + 120, y, desc)
        y -= 18

    y -= 20
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(CHARCOAL)
    c.drawString(margin, y, "Phase 3: Long-Term Monitoring (Week 4+)")
    y -= 25

    phase3 = [
        "Monitor all sensors for 30+ days continuous",
        "Collect data for ML anomaly detection training",
        "Document any false positives or missed events",
        "Test battery life on battery-powered sensors",
        "Verify mesh network stability over time",
        "Gather user experience feedback",
        "Prepare report for investor demonstrations",
    ]

    c.setFont("Helvetica", 10)
    for item in phase3:
        c.setFillColor(TEAL)
        c.drawString(margin + 10, y, "•")
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 25, y, item)
        y -= 18

    draw_footer(c, page_w, page_num)
    c.showPage()
    page_num += 1

    # ========== PAGE 6: DATA COLLECTION ==========
    draw_header(c, page_w, page_h, "DATA COLLECTION & METRICS")

    y = page_h - 100

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Key Metrics to Track:")
    y -= 30

    metrics = [
        ("Sensor Uptime", "Target: 99.9%", "Track any disconnections or failures"),
        ("Detection Accuracy", "Target: >95%", "True positives vs false positives"),
        ("Response Time", "Target: <2 sec", "Time from event to alert"),
        ("Battery Life", "Target: 10+ years", "Track voltage levels over time"),
        ("Mesh Reliability", "Target: <1% packet loss", "Thread network performance"),
        ("Cloud Latency", "Target: <500ms", "Sensor to cloud round-trip"),
        ("User Alerts", "Track all", "Document every alert sent to user"),
        ("False Alarms", "Target: <1/month", "Minimize nuisance alerts"),
    ]

    c.setFillColor(LIGHT_GRAY)
    c.roundRect(margin, y - 200, page_w - 2*margin, 210, 8, fill=1, stroke=0)

    y -= 15
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(TEAL)
    c.drawString(margin + 15, y, "METRIC")
    c.drawString(margin + 180, y, "TARGET")
    c.drawString(margin + 300, y, "NOTES")
    y -= 5
    c.setStrokeColor(TEAL)
    c.line(margin + 15, y, page_w - margin - 15, y)
    y -= 18

    c.setFont("Helvetica", 10)
    for metric, target, notes in metrics:
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin + 15, y, metric)
        c.setFillColor(GREEN)
        c.setFont("Helvetica", 10)
        c.drawString(margin + 180, y, target)
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 300, y, notes)
        y -= 20

    # Data export
    y -= 40
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Data Export Format:")
    y -= 25

    c.setFont("Helvetica", 10)
    export_info = [
        "All sensor data logged to cloud (AWS IoT Core)",
        "JSON format with timestamps (UTC)",
        "Exportable via API or dashboard download",
        "ML pipeline receives real-time data stream",
        "30-day rolling retention for raw data",
        "Aggregated metrics retained indefinitely",
    ]

    for item in export_info:
        c.setFillColor(TEAL)
        c.drawString(margin + 10, y, "•")
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 25, y, item)
        y -= 18

    draw_footer(c, page_w, page_num)
    c.showPage()
    page_num += 1

    # ========== PAGE 7: PARTS LIST FOR PROTOTYPE ==========
    draw_header(c, page_w, page_h, "PROTOTYPE PARTS LIST")

    y = page_h - 100

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Components to Order for Prototype Build:")
    y -= 30

    # Dev boards
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(TEAL)
    c.drawString(margin, y, "Development Boards:")
    y -= 20

    dev_boards = [
        ("Nordic nRF5340-DK", "2x", "$49 each", "Main MCU dev kit"),
        ("Nordic nRF21540-EK", "2x", "$35 each", "Front-end module"),
        ("Raspberry Pi 4 (4GB)", "1x", "$55", "Hub/Border Router prototype"),
        ("Thread Border Router", "1x", "$35", "Nordic or Silicon Labs"),
    ]

    c.setFont("Helvetica", 10)
    for part, qty, price, notes in dev_boards:
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 15, y, part)
        c.drawString(margin + 200, y, qty)
        c.setFillColor(GREEN)
        c.drawString(margin + 250, y, price)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin + 320, y, notes)
        c.setFont("Helvetica", 10)
        y -= 18

    y -= 15
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(TEAL)
    c.drawString(margin, y, "Sensors:")
    y -= 20

    sensors_list = [
        ("Honeywell HSC Pressure", "2x", "$25 each", "Water pressure"),
        ("Ultrasonic Flow Sensor", "2x", "$40 each", "Water flow"),
        ("Capacitive Moisture Probe", "4x", "$5 each", "Leak detection"),
        ("Split-Core CT (100A)", "4x", "$15 each", "Current sensing"),
        ("LIS3DH Accelerometer", "2x", "$3 each", "Vibration"),
        ("SCD40 CO2 Sensor", "2x", "$45 each", "Air quality"),
        ("BME680 Environmental", "4x", "$20 each", "Temp/Humidity/VOC"),
    ]

    c.setFont("Helvetica", 10)
    for part, qty, price, notes in sensors_list:
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 15, y, part)
        c.drawString(margin + 200, y, qty)
        c.setFillColor(GREEN)
        c.drawString(margin + 250, y, price)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin + 320, y, notes)
        c.setFont("Helvetica", 10)
        y -= 18

    y -= 15
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(TEAL)
    c.drawString(margin, y, "Suppliers:")
    y -= 20

    suppliers = [
        "Digi-Key (digikey.com) - Components",
        "Mouser (mouser.com) - Components",
        "Nordic Semiconductor (nordicsemi.com) - Dev kits",
        "Adafruit (adafruit.com) - Breakout boards",
        "SparkFun (sparkfun.com) - Prototyping",
        "Amazon - Enclosures, cables, power supplies",
    ]

    c.setFont("Helvetica", 10)
    for supplier in suppliers:
        c.setFillColor(TEAL)
        c.drawString(margin + 10, y, "•")
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 25, y, supplier)
        y -= 18

    # Estimated cost
    y -= 20
    c.setFillColor(TEAL)
    c.roundRect(margin, y - 40, page_w - 2*margin, 50, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, y - 15, "ESTIMATED PROTOTYPE COST: $800 - $1,200")
    c.setFont("Helvetica", 11)
    c.drawCentredString(page_w/2, y - 35, "Includes all dev boards, sensors, and prototyping materials")

    draw_footer(c, page_w, page_num)
    c.showPage()
    page_num += 1

    # ========== PAGE 8: NEXT STEPS ==========
    draw_header(c, page_w, page_h, "NEXT STEPS")

    y = page_h - 100

    steps = [
        {
            "num": "1",
            "title": "ORDER PROTOTYPE COMPONENTS",
            "desc": "Place orders for dev boards and sensors from Digi-Key/Mouser",
            "owner": "Eric",
        },
        {
            "num": "2",
            "title": "SETUP DEVELOPMENT ENVIRONMENT",
            "desc": "Install Nordic nRF Connect SDK, Zephyr RTOS, Matter SDK",
            "owner": "Joe (Hardware)",
        },
        {
            "num": "3",
            "title": "BUILD FIRST PROTOTYPE",
            "desc": "Assemble water sensor prototype with nRF5340-DK",
            "owner": "Joe (Hardware)",
        },
        {
            "num": "4",
            "title": "INTEGRATE WITH BACKEND",
            "desc": "Connect prototype to existing Go/QuestDB platform",
            "owner": "Eric (Software)",
        },
        {
            "num": "5",
            "title": "INSTALL AT TEST HOME",
            "desc": "Deploy prototype sensors at Eric's residence",
            "owner": "Both",
        },
        {
            "num": "6",
            "title": "COLLECT DATA & ITERATE",
            "desc": "30-day monitoring period, refine based on real-world data",
            "owner": "Both",
        },
        {
            "num": "7",
            "title": "INVESTOR DEMO",
            "desc": "Use test home data for investor presentations",
            "owner": "Eric",
        },
    ]

    for step in steps:
        c.setFillColor(TEAL)
        c.circle(margin + 15, y - 5, 15, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(margin + 15, y - 10, step["num"])

        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin + 40, y, step["title"])
        y -= 18
        c.setFont("Helvetica", 10)
        c.drawString(margin + 40, y, step["desc"])
        y -= 15
        c.setFillColor(GREEN)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin + 40, y, f"Owner: {step['owner']}")
        y -= 35

    # Contact
    y -= 20
    c.setFillColor(TEAL)
    c.roundRect(margin, y - 80, page_w - 2*margin, 90, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w/2, y - 20, "LET'S BUILD THIS")
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, y - 45, "Eric De Loera | partners@ihp-home.io")
    c.setFont("Helvetica-Oblique", 11)
    c.drawCentredString(page_w/2, y - 65, "\"The platform is ready. The market is massive. We just need the hardware.\"")

    draw_footer(c, page_w, page_num)
    c.save()

    print("=" * 60)
    print("GENERATED: IHP_Home_Testing_Kit.pdf")
    print("=" * 60)
    print(f"\nLocation: {BASE_DIR}/IHP_Home_Testing_Kit.pdf")
    print("\nContents:")
    print("  • Cover page")
    print("  • Testing kit contents ($1,152 value)")
    print("  • Installation locations (8 zones)")
    print("  • Floor plan diagram")
    print("  • Testing protocol (3 phases)")
    print("  • Data collection metrics")
    print("  • Prototype parts list ($800-1,200)")
    print("  • Next steps action plan")
    print("=" * 60)

if __name__ == "__main__":
    generate_testing_kit_pdf()
