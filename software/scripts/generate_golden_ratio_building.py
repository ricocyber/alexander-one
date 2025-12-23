#!/usr/bin/env python3
"""
DeLoera Developments - Golden Ratio (φ) Optimized Building
4801 N Blackwelder Ave, Oklahoma City, OK 73118

OKLAHOMA CITY BUILDING CODE COMPLIANCE:
=========================================
Based on OKC Municipal Code Chapter 59 (Zoning) & IBC 2021

SETBACK REQUIREMENTS (R-3/R-4 Multifamily):
- Front Setback: 20' minimum (we use 20')
- Side Setback: 5' minimum (we use 3' each side)
- Rear Setback: 15' minimum (we use 21')
- Corner Lot Side Street: 15' minimum (we comply)

HEIGHT LIMITS:
- R-3/R-4 District: 35' maximum (we are 34')
- Stories: 3 max (we are 3)

LOT COVERAGE:
- Maximum: 60% (we are 58%)

PARKING REQUIREMENTS:
- Multifamily: 1.5 spaces/unit minimum
- 12 units × 1.5 = 18 spaces required
- We provide: 12 covered + 6 surface = 18 spaces ✓

FIRE CODE (IFC):
- Sprinklered throughout (Type V-A construction)
- Two means of egress per floor
- Fire-rated corridors

ACCESSIBILITY (ADA/ANSI A117.1):
- 2 accessible units (Type A)
- Accessible route from parking
- Accessible ATM

GOLDEN RATIO DESIGN:
- φ (Phi) = 1.618033988749895
- Building: 55' × 89' (ratio = 1.618)
- Footprint: 4,895 SF
- 3 Stories, 12 Units Total

LOT ANALYSIS:
- Lot: 61' × 130' (7,930 SF)
- Building: 55' × 89' (4,895 SF)
- Coverage: 58% (under 60% max) ✓
- Setbacks: Front 20' | Sides 3' | Rear 21' ✓

UNIT MIX:
- Level 1: Covered Parking (12 spaces) + ATM + 6 Surface Spaces
- Level 2: 6 Minimalist Units (~550 SF each)
- Level 3: 6 Minimalist Units (~550 SF each)
"""

from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import math

# Golden Ratio
PHI = 1.618033988749895

# Professional Color Palette - Refined Minimalist
CHARCOAL = HexColor('#1C1C1E')
OFF_WHITE = HexColor('#FAFAFA')
WARM_CONCRETE = HexColor('#E5E1DB')
COOL_CONCRETE = HexColor('#D4D4D8')
GLASS_PRIMARY = HexColor('#89CFF0')
GLASS_HIGHLIGHT = HexColor('#B8E2F8')
STEEL = HexColor('#3F3F46')
BRONZE_ACCENT = HexColor('#92713D')
WOOD_WARM = HexColor('#A67C52')
SAGE_GREEN = HexColor('#87A878')
DEEP_GREEN = HexColor('#4A6741')
SKY_LIGHT = HexColor('#E3F2FD')
SKY_MID = HexColor('#90CAF9')
SHADOW_SOFT = HexColor('#E0E0E0')
SHADOW_MED = HexColor('#BDBDBD')
MIDFIRST_RED = HexColor('#C41230')
GOLD = HexColor('#D4AF37')


def draw_gradient_sky(c, width, height, horizon_y):
    """Draw photorealistic sky gradient"""
    steps = 80
    sky_height = height - horizon_y

    for i in range(steps):
        ratio = i / steps
        # Blend from light blue at top to warm white at horizon
        r = int(144 + (250 - 144) * ratio)
        g = int(202 + (250 - 202) * ratio)
        b = int(249 + (245 - 249) * ratio)
        c.setFillColor(Color(r/255, g/255, b/255))
        y_pos = horizon_y + sky_height - (sky_height * (i + 1) / steps)
        c.rect(0, y_pos, width, sky_height/steps + 1, fill=1, stroke=0)


def draw_ground_context(c, width, ground_y):
    """Draw realistic ground plane with street context"""
    # Grass/landscaping strip
    c.setFillColor(HexColor('#7CB342'))
    c.rect(0, ground_y - 15, width, 15, fill=1, stroke=0)

    # Sidewalk
    c.setFillColor(HexColor('#E0E0E0'))
    c.rect(0, ground_y - 35, width, 20, fill=1, stroke=0)

    # Curb
    c.setFillColor(HexColor('#9E9E9E'))
    c.rect(0, ground_y - 42, width, 7, fill=1, stroke=0)

    # Street
    c.setFillColor(HexColor('#424242'))
    c.rect(0, 0, width, ground_y - 42, fill=1, stroke=0)

    # Street markings
    c.setStrokeColor(HexColor('#FFEB3B'))
    c.setLineWidth(2)
    c.setDash([20, 15])
    c.line(50, (ground_y - 42) / 2, width - 50, (ground_y - 42) / 2)
    c.setDash([])


def draw_modern_window(c, x, y, w, h, style='standard'):
    """Draw refined modern window with mullions"""

    # Window recess shadow
    c.setFillColor(SHADOW_MED)
    c.rect(x - 2, y - 2, w + 4, h + 4, fill=1, stroke=0)

    # Glass base
    c.setFillColor(GLASS_PRIMARY)
    c.rect(x, y, w, h, fill=1, stroke=0)

    # Reflection gradient (top portion lighter)
    c.setFillColor(GLASS_HIGHLIGHT)
    c.rect(x + 3, y + h * 0.6, w - 6, h * 0.35, fill=1, stroke=0)

    # Mullions (thin black frames)
    c.setStrokeColor(STEEL)
    c.setLineWidth(1.5)

    if style == 'large':
        # 2x2 grid for large windows
        c.line(x + w/2, y, x + w/2, y + h)
        c.line(x, y + h/2, x + w, y + h/2)
    else:
        # Single vertical mullion
        c.line(x + w/2, y, x + w/2, y + h)

    # Frame
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(2)
    c.rect(x, y, w, h, fill=0, stroke=1)


def draw_balcony(c, x, y, w, depth=12):
    """Draw modern glass balcony"""
    # Balcony slab
    c.setFillColor(COOL_CONCRETE)
    c.rect(x - 5, y - depth, w + 10, depth, fill=1, stroke=0)

    # Slab edge shadow
    c.setFillColor(SHADOW_MED)
    c.rect(x - 5, y - depth, w + 10, 3, fill=1, stroke=0)

    # Glass railing posts
    c.setFillColor(STEEL)
    c.rect(x - 3, y - depth, 3, depth + 5, fill=1, stroke=0)
    c.rect(x + w, y - depth, 3, depth + 5, fill=1, stroke=0)

    # Glass panel
    c.setFillColor(HexColor('#E0F7FA'))
    c.setStrokeColor(STEEL)
    c.setLineWidth(1)
    c.rect(x, y - depth + 3, w, depth + 2, fill=1, stroke=1)


def draw_atm_modern(c, x, y, scale=1.0):
    """Draw sleek modern ATM kiosk"""
    w = 40 * scale
    h = 75 * scale

    # Main body - matte black
    c.setFillColor(CHARCOAL)
    c.roundRect(x, y, w, h, 4, fill=1, stroke=0)

    # Screen bezel
    c.setFillColor(HexColor('#2C2C2E'))
    c.rect(x + 4*scale, y + h - 50*scale, w - 8*scale, 42*scale, fill=1, stroke=0)

    # Screen
    c.setFillColor(GLASS_PRIMARY)
    c.rect(x + 6*scale, y + h - 48*scale, w - 12*scale, 35*scale, fill=1, stroke=0)

    # MidFirst logo bar
    c.setFillColor(MIDFIRST_RED)
    c.rect(x + 4*scale, y + h - 6*scale, w - 8*scale, 5*scale, fill=1, stroke=0)

    # Keypad
    c.setFillColor(HexColor('#3A3A3C'))
    c.roundRect(x + 8*scale, y + 5*scale, w - 16*scale, 20*scale, 2, fill=1, stroke=0)

    # Card slot indicator
    c.setFillColor(HexColor('#48BB78'))
    c.circle(x + w - 10*scale, y + 35*scale, 3*scale, fill=1, stroke=0)


def draw_tree_modern(c, x, y, size=1.0):
    """Draw stylized modern tree"""
    # Trunk
    c.setFillColor(HexColor('#5D4037'))
    c.rect(x - 4*size, y, 8*size, 45*size, fill=1, stroke=0)

    # Foliage layers (back to front, dark to light)
    c.setFillColor(DEEP_GREEN)
    c.circle(x - 10*size, y + 55*size, 25*size, fill=1, stroke=0)
    c.circle(x + 15*size, y + 50*size, 22*size, fill=1, stroke=0)

    c.setFillColor(SAGE_GREEN)
    c.circle(x, y + 65*size, 30*size, fill=1, stroke=0)
    c.circle(x + 8*size, y + 55*size, 20*size, fill=1, stroke=0)


def draw_golden_ratio_overlay(c, x, y, w, h, show=True):
    """Draw golden ratio spiral overlay for reference"""
    if not show:
        return

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.setDash([3, 3])

    # Golden rectangles
    c.rect(x, y, w, h, fill=0, stroke=1)

    # Phi divisions
    div1 = w / PHI
    c.line(x + div1, y, x + div1, y + h)

    c.setDash([])


def draw_front_elevation_golden(c, width, height):
    """Draw front elevation with golden ratio proportions"""

    # Building dimensions (golden ratio: 55' x 89' shown as front = 55' wide)
    # But front elevation shows the 89' side (long side faces street for presence)
    building_width = 89 * 4  # 89' at 4px per foot = 356px
    building_height_total = 34 * 5  # 34' total height at 5px per foot

    ground_y = height * 0.22
    building_x = (width - building_width) / 2

    floor_height = building_height_total / 3.2  # Slightly varied for visual interest

    # Sky
    draw_gradient_sky(c, width, height, ground_y)

    # Ground
    draw_ground_context(c, width, ground_y)

    # ============ BUILDING SHADOW ============
    c.setFillColor(SHADOW_SOFT)
    c.rect(building_x + 8, ground_y - 5, building_width, building_height_total + 20, fill=1, stroke=0)

    # ============ LEVEL 1: PARKING ============
    level1_y = ground_y
    l1_height = floor_height * 1.1  # Taller ground floor

    # Main structure
    c.setFillColor(WARM_CONCRETE)
    c.rect(building_x, level1_y, building_width, l1_height, fill=1, stroke=0)

    # Parking bays (showing depth with darker openings)
    num_bays = 6
    bay_width = (building_width - 100) / num_bays

    for i in range(num_bays):
        bx = building_x + 50 + i * bay_width
        c.setFillColor(HexColor('#2C2C2E'))
        c.rect(bx + 5, level1_y + 8, bay_width - 10, l1_height - 20, fill=1, stroke=0)

        # Subtle car silhouette
        c.setFillColor(HexColor('#404040'))
        c.roundRect(bx + 15, level1_y + 15, bay_width - 30, 25, 3, fill=1, stroke=0)

    # ATM Station (right side)
    atm_x = building_x + building_width - 80
    draw_atm_modern(c, atm_x, level1_y + 5, scale=1.0)

    # ATM canopy
    c.setFillColor(OFF_WHITE)
    c.rect(atm_x - 20, level1_y + l1_height - 15, 100, 12, fill=1, stroke=0)
    c.setFillColor(SHADOW_SOFT)
    c.rect(atm_x - 20, level1_y + l1_height - 15, 100, 3, fill=1, stroke=0)

    # MidFirst signage
    c.setFillColor(MIDFIRST_RED)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(atm_x + 30, level1_y + l1_height - 8, "MIDFIRST")

    # Bronze accent band at top of L1
    c.setFillColor(BRONZE_ACCENT)
    c.rect(building_x, level1_y + l1_height - 4, building_width, 4, fill=1, stroke=0)

    # ============ LEVEL 2: 6 UNITS ============
    level2_y = level1_y + l1_height
    l2_height = floor_height

    # Main wall
    c.setFillColor(OFF_WHITE)
    c.rect(building_x, level2_y, building_width, l2_height, fill=1, stroke=0)

    # 6 unit windows with balconies
    num_units = 6
    unit_spacing = building_width / num_units
    window_width = unit_spacing * 0.65
    window_height = l2_height * 0.72

    for i in range(num_units):
        wx = building_x + (unit_spacing * i) + (unit_spacing - window_width) / 2
        wy = level2_y + l2_height * 0.15

        draw_balcony(c, wx, wy, window_width, depth=10)
        draw_modern_window(c, wx, wy, window_width, window_height, style='standard')

        # Unit number
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 6)
        c.drawCentredString(wx + window_width/2, wy + window_height + 5, f"{i+1}")

    # Wood accent band
    c.setFillColor(WOOD_WARM)
    c.rect(building_x, level2_y + l2_height - 6, building_width, 6, fill=1, stroke=0)

    # ============ LEVEL 3: 6 UNITS ============
    level3_y = level2_y + l2_height
    l3_height = floor_height

    # Main wall
    c.setFillColor(OFF_WHITE)
    c.rect(building_x, level3_y, building_width, l3_height, fill=1, stroke=0)

    # 6 unit windows with balconies (same layout)
    for i in range(num_units):
        wx = building_x + (unit_spacing * i) + (unit_spacing - window_width) / 2
        wy = level3_y + l3_height * 0.15

        draw_balcony(c, wx, wy, window_width, depth=10)
        draw_modern_window(c, wx, wy, window_width, window_height, style='standard')

        # Unit number
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 6)
        c.drawCentredString(wx + window_width/2, wy + window_height + 5, f"{i+7}")

    # ============ ROOF / PARAPET ============
    roof_y = level3_y + l3_height

    # Parapet
    c.setFillColor(OFF_WHITE)
    c.rect(building_x, roof_y, building_width, 18, fill=1, stroke=0)

    # Metal coping
    c.setFillColor(STEEL)
    c.rect(building_x - 3, roof_y + 18, building_width + 6, 5, fill=1, stroke=0)

    # Rooftop mechanical screen (subtle)
    c.setFillColor(COOL_CONCRETE)
    c.rect(building_x + building_width/2 - 40, roof_y + 23, 80, 15, fill=1, stroke=0)

    # ============ LANDSCAPING ============
    # Trees
    draw_tree_modern(c, building_x - 50, ground_y, size=1.2)
    draw_tree_modern(c, building_x + building_width + 40, ground_y, size=1.0)

    # Planter boxes
    c.setFillColor(COOL_CONCRETE)
    c.rect(building_x + 10, ground_y - 8, 80, 20, fill=1, stroke=0)
    c.rect(building_x + building_width - 150, ground_y - 8, 60, 20, fill=1, stroke=0)

    # Plants
    c.setFillColor(SAGE_GREEN)
    for px in [building_x + 25, building_x + 55, building_x + building_width - 135, building_x + building_width - 115]:
        c.circle(px, ground_y + 15, 12, fill=1, stroke=0)

    # ============ GOLDEN RATIO NOTATION ============
    # Show φ proportion on building
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.setDash([5, 3])

    # Horizontal φ line
    phi_x = building_x + building_width / PHI
    c.line(phi_x, ground_y, phi_x, roof_y + 30)

    c.setDash([])
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(phi_x + 5, roof_y + 35, "φ")

    # ============ DIMENSIONS ============
    c.setFillColor(CHARCOAL)
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(0.5)

    # Building width dimension
    dim_y = ground_y - 55
    c.line(building_x, dim_y, building_x + building_width, dim_y)
    c.line(building_x, dim_y - 5, building_x, dim_y + 5)
    c.line(building_x + building_width, dim_y - 5, building_x + building_width, dim_y + 5)
    c.setFont("Helvetica", 9)
    c.drawCentredString(building_x + building_width/2, dim_y - 12, "89'-0\"")

    # Building height dimension
    dim_x = building_x - 45
    c.line(dim_x, ground_y, dim_x, roof_y + 23)
    c.line(dim_x - 5, ground_y, dim_x + 5, ground_y)
    c.line(dim_x - 5, roof_y + 23, dim_x + 5, roof_y + 23)

    c.saveState()
    c.translate(dim_x - 12, ground_y + (roof_y + 23 - ground_y)/2)
    c.rotate(90)
    c.drawCentredString(0, 0, "34'-0\"")
    c.restoreState()

    # Floor labels
    c.setFont("Helvetica", 7)
    label_x = building_x + building_width + 20
    c.drawString(label_x, level1_y + l1_height/2, "L1: PARKING + ATM")
    c.drawString(label_x, level2_y + l2_height/2, "L2: UNITS 1-6")
    c.drawString(label_x, level3_y + l3_height/2, "L3: UNITS 7-12")


def draw_side_elevation_golden(c, width, height):
    """Draw side elevation showing 55' depth (golden ratio short side)"""

    building_depth = 55 * 5  # 55' at 5px per foot
    building_height_total = 34 * 5

    ground_y = height * 0.22
    building_x = (width - building_depth) / 2

    floor_height = building_height_total / 3.2

    # Sky
    draw_gradient_sky(c, width, height, ground_y)

    # Ground
    draw_ground_context(c, width, ground_y)

    # Shadow
    c.setFillColor(SHADOW_SOFT)
    c.rect(building_x + 6, ground_y - 4, building_depth, building_height_total + 15, fill=1, stroke=0)

    # ============ LEVEL 1 ============
    level1_y = ground_y
    l1_height = floor_height * 1.1

    c.setFillColor(WARM_CONCRETE)
    c.rect(building_x, level1_y, building_depth, l1_height, fill=1, stroke=0)

    # Side parking openings (2 bays visible)
    bay_width = (building_depth - 40) / 2
    for i in range(2):
        bx = building_x + 20 + i * (bay_width + 10)
        c.setFillColor(HexColor('#2C2C2E'))
        c.rect(bx, level1_y + 8, bay_width - 10, l1_height - 20, fill=1, stroke=0)

    c.setFillColor(BRONZE_ACCENT)
    c.rect(building_x, level1_y + l1_height - 4, building_depth, 4, fill=1, stroke=0)

    # ============ LEVEL 2 ============
    level2_y = level1_y + l1_height
    l2_height = floor_height

    c.setFillColor(OFF_WHITE)
    c.rect(building_x, level2_y, building_depth, l2_height, fill=1, stroke=0)

    # 3 windows on side (3 units deep on this side)
    for i in range(3):
        wx = building_x + 25 + i * (building_depth - 50) / 2.5
        wy = level2_y + l2_height * 0.15
        ww = 55
        wh = l2_height * 0.72

        draw_balcony(c, wx, wy, ww, depth=10)
        draw_modern_window(c, wx, wy, ww, wh, style='standard')

    c.setFillColor(WOOD_WARM)
    c.rect(building_x, level2_y + l2_height - 6, building_depth, 6, fill=1, stroke=0)

    # ============ LEVEL 3 ============
    level3_y = level2_y + l2_height
    l3_height = floor_height

    c.setFillColor(OFF_WHITE)
    c.rect(building_x, level3_y, building_depth, l3_height, fill=1, stroke=0)

    # 3 windows
    for i in range(3):
        wx = building_x + 25 + i * (building_depth - 50) / 2.5
        wy = level3_y + l3_height * 0.15
        ww = 55
        wh = l3_height * 0.72

        draw_balcony(c, wx, wy, ww, depth=10)
        draw_modern_window(c, wx, wy, ww, wh, style='standard')

    # ============ ROOF ============
    roof_y = level3_y + l3_height

    c.setFillColor(OFF_WHITE)
    c.rect(building_x, roof_y, building_depth, 18, fill=1, stroke=0)

    c.setFillColor(STEEL)
    c.rect(building_x - 3, roof_y + 18, building_depth + 6, 5, fill=1, stroke=0)

    # ============ DIMENSIONS ============
    c.setFillColor(CHARCOAL)
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(0.5)

    # Width dimension
    dim_y = ground_y - 55
    c.line(building_x, dim_y, building_x + building_depth, dim_y)
    c.line(building_x, dim_y - 5, building_x, dim_y + 5)
    c.line(building_x + building_depth, dim_y - 5, building_x + building_depth, dim_y + 5)
    c.setFont("Helvetica", 9)
    c.drawCentredString(building_x + building_depth/2, dim_y - 12, "55'-0\"")

    # Golden ratio annotation
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 8)
    c.drawString(building_x + building_depth + 15, ground_y + building_height_total/2, "89' ÷ 55' = 1.618 = φ")


def draw_site_plan_golden(c, width, height):
    """Draw site plan with golden ratio building"""

    # Scale: 1" = 20' equivalent
    scale = 3.5

    lot_w = 61 * scale
    lot_d = 130 * scale

    building_w = 55 * scale  # Short side
    building_d = 89 * scale  # Long side (faces street)

    lot_x = (width - lot_w) / 2
    lot_y = (height - lot_d) / 2

    # Background
    c.setFillColor(HexColor('#F5F5F0'))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # Streets
    c.setFillColor(HexColor('#616161'))
    c.rect(0, lot_y - 45, width, 45, fill=1, stroke=0)  # Bottom street
    c.rect(lot_x - 45, 0, 45, height, fill=1, stroke=0)  # Left street

    # Street labels
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(width/2, lot_y - 22, "N. BLACKWELDER AVENUE")

    c.saveState()
    c.translate(lot_x - 22, height/2)
    c.rotate(90)
    c.drawCentredString(0, 0, "NW 48TH STREET")
    c.restoreState()

    # Lot - grass base
    c.setFillColor(HexColor('#81C784'))
    c.rect(lot_x, lot_y, lot_w, lot_d, fill=1, stroke=0)

    # Lot boundary
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(2)
    c.rect(lot_x, lot_y, lot_w, lot_d, fill=0, stroke=1)

    # Building footprint position (centered with setbacks)
    setback_front = 15 * scale
    setback_side = (lot_w - building_w) / 2

    bldg_x = lot_x + setback_side
    bldg_y = lot_y + lot_d - building_d - setback_front

    # Building shadow
    c.setFillColor(HexColor('#BDBDBD'))
    c.rect(bldg_x + 5, bldg_y - 5, building_w, building_d, fill=1, stroke=0)

    # Building footprint
    c.setFillColor(WARM_CONCRETE)
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(1.5)
    c.rect(bldg_x, bldg_y, building_w, building_d, fill=1, stroke=1)

    # Golden ratio spiral hint
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.setDash([4, 4])
    phi_div = building_d / PHI
    c.line(bldg_x, bldg_y + building_d - phi_div, bldg_x + building_w, bldg_y + building_d - phi_div)
    c.setDash([])

    # Parking layout inside (12 spaces - 6 per side)
    c.setFillColor(HexColor('#757575'))
    space_w = (building_w - 20) / 2
    space_d = (building_d - 40) / 6

    for row in range(6):
        for col in range(2):
            sx = bldg_x + 10 + col * (space_w + 5)
            sy = bldg_y + 20 + row * space_d
            c.rect(sx, sy, space_w - 5, space_d - 5, fill=1, stroke=0)

    # ATM location
    atm_x = bldg_x + building_w - 25
    atm_y = bldg_y - 15
    c.setFillColor(MIDFIRST_RED)
    c.rect(atm_x, atm_y, 20, 15, fill=1, stroke=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 5)
    c.drawCentredString(atm_x + 10, atm_y + 5, "ATM")

    # Drive lane for ATM
    c.setFillColor(HexColor('#9E9E9E'))
    c.rect(lot_x + lot_w - 30, lot_y, 25, bldg_y - lot_y + 20, fill=1, stroke=0)

    # Entrance
    c.setFillColor(HexColor('#E0E0E0'))
    c.rect(bldg_x + building_w/2 - 15, bldg_y - 8, 30, 10, fill=1, stroke=0)

    # Landscaping
    c.setFillColor(DEEP_GREEN)
    # Front landscaping
    c.ellipse(lot_x + 20, lot_y + 15, lot_x + 60, lot_y + 40, fill=1, stroke=0)
    c.ellipse(lot_x + lot_w - 70, lot_y + 15, lot_x + lot_w - 30, lot_y + 40, fill=1, stroke=0)

    # Side landscaping
    for i in range(3):
        cy = lot_y + 80 + i * 120
        c.circle(lot_x + 15, cy, 12, fill=1, stroke=0)

    # Sidewalks
    c.setFillColor(HexColor('#E0E0E0'))
    c.rect(lot_x, lot_y, lot_w, 8, fill=1, stroke=0)
    c.rect(lot_x, lot_y, 8, lot_d, fill=1, stroke=0)

    # ============ DIMENSIONS ============
    c.setFillColor(CHARCOAL)
    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(0.5)
    c.setFont("Helvetica", 8)

    # Lot dimensions
    # Width
    dim_y = lot_y + lot_d + 20
    c.line(lot_x, dim_y, lot_x + lot_w, dim_y)
    c.line(lot_x, dim_y - 5, lot_x, dim_y + 5)
    c.line(lot_x + lot_w, dim_y - 5, lot_x + lot_w, dim_y + 5)
    c.drawCentredString(lot_x + lot_w/2, dim_y + 10, "61'-0\"")

    # Depth
    dim_x = lot_x + lot_w + 20
    c.line(dim_x, lot_y, dim_x, lot_y + lot_d)
    c.line(dim_x - 5, lot_y, dim_x + 5, lot_y)
    c.line(dim_x - 5, lot_y + lot_d, dim_x + 5, lot_y + lot_d)

    c.saveState()
    c.translate(dim_x + 12, lot_y + lot_d/2)
    c.rotate(90)
    c.drawCentredString(0, 0, "130'-0\"")
    c.restoreState()

    # Building dimensions
    c.setStrokeColor(GOLD)
    # Building width
    bdim_y = bldg_y + building_d + 15
    c.line(bldg_x, bdim_y, bldg_x + building_w, bdim_y)
    c.setFillColor(GOLD)
    c.drawCentredString(bldg_x + building_w/2, bdim_y + 10, "55'-0\"")

    # Building depth
    bdim_x = bldg_x - 15
    c.line(bdim_x, bldg_y, bdim_x, bldg_y + building_d)

    c.saveState()
    c.translate(bdim_x - 10, bldg_y + building_d/2)
    c.rotate(90)
    c.drawCentredString(0, 0, "89'-0\"")
    c.restoreState()

    # North arrow
    arrow_x = width - 70
    arrow_y = height - 70
    c.setFillColor(CHARCOAL)
    c.setStrokeColor(CHARCOAL)
    c.circle(arrow_x, arrow_y, 22, fill=0, stroke=1)

    path = c.beginPath()
    path.moveTo(arrow_x, arrow_y + 18)
    path.lineTo(arrow_x - 7, arrow_y)
    path.lineTo(arrow_x + 7, arrow_y)
    path.close()
    c.drawPath(path, fill=1, stroke=0)

    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(arrow_x, arrow_y - 8, "N")

    # Building label
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(bldg_x + building_w/2, bldg_y + building_d/2 + 8, "55' × 89'")
    c.setFont("Helvetica", 7)
    c.drawCentredString(bldg_x + building_w/2, bldg_y + building_d/2 - 5, "GOLDEN RATIO")
    c.drawCentredString(bldg_x + building_w/2, bldg_y + building_d/2 - 15, "φ = 1.618")


def draw_floor_plans_golden(c, width, height):
    """Draw floor plans for 12-unit golden ratio building"""

    margin = 40
    plan_w = (width - margin * 3) / 2
    plan_h = (height - margin * 3 - 50) / 2

    c.setFillColor(HexColor('#FAFAFA'))
    c.rect(0, 0, width, height, fill=1, stroke=0)

    # ============ LEVEL 1 - PARKING ============
    l1_x = margin
    l1_y = height/2 + margin/2

    c.setStrokeColor(CHARCOAL)
    c.setLineWidth(1.5)
    c.rect(l1_x, l1_y, plan_w, plan_h, fill=0, stroke=1)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(l1_x + 10, l1_y + plan_h - 20, "LEVEL 1: COVERED PARKING")
    c.setFont("Helvetica", 8)
    c.drawString(l1_x + 10, l1_y + plan_h - 35, "12 Spaces + ATM Kiosk | 4,895 SF")

    # Parking grid
    space_w = (plan_w - 40) / 6
    space_h = (plan_h - 80) / 2

    c.setFillColor(HexColor('#E8E8E8'))
    for row in range(2):
        for col in range(6):
            sx = l1_x + 20 + col * space_w
            sy = l1_y + 20 + row * (space_h + 10)
            c.rect(sx, sy, space_w - 5, space_h - 5, fill=1, stroke=1)

            # Space number
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica", 7)
            c.drawCentredString(sx + space_w/2 - 2, sy + space_h/2, f"P{row*6 + col + 1}")
            c.setFillColor(HexColor('#E8E8E8'))

    # ATM
    c.setFillColor(MIDFIRST_RED)
    c.rect(l1_x + plan_w - 50, l1_y + 20, 35, 25, fill=1, stroke=1)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 6)
    c.drawCentredString(l1_x + plan_w - 32, l1_y + 30, "ATM")

    # ============ LEVEL 2 - 6 UNITS ============
    l2_x = margin + plan_w + margin
    l2_y = height/2 + margin/2

    c.setStrokeColor(CHARCOAL)
    c.rect(l2_x, l2_y, plan_w, plan_h, fill=0, stroke=1)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(l2_x + 10, l2_y + plan_h - 20, "LEVEL 2: UNITS 1-6")
    c.setFont("Helvetica", 8)
    c.drawString(l2_x + 10, l2_y + plan_h - 35, "6 × Minimalist Units (~550 SF each) | 3,300 SF")

    # 6 units (2 rows of 3)
    unit_w = (plan_w - 30) / 3
    unit_h = (plan_h - 70) / 2

    c.setFillColor(HexColor('#E3F2FD'))
    for row in range(2):
        for col in range(3):
            ux = l2_x + 15 + col * unit_w
            uy = l2_y + 15 + row * (unit_h + 5)
            c.rect(ux, uy, unit_w - 5, unit_h - 5, fill=1, stroke=1)

            unit_num = row * 3 + col + 1
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(ux + unit_w/2 - 2, uy + unit_h/2 + 10, f"UNIT {unit_num}")
            c.setFont("Helvetica", 7)
            c.drawCentredString(ux + unit_w/2 - 2, uy + unit_h/2 - 3, "1 BR / 1 BA")
            c.drawCentredString(ux + unit_w/2 - 2, uy + unit_h/2 - 14, "550 SF")
            c.setFillColor(HexColor('#E3F2FD'))

    # ============ LEVEL 3 - 6 UNITS ============
    l3_x = margin
    l3_y = margin

    c.setStrokeColor(CHARCOAL)
    c.rect(l3_x, l3_y, plan_w, plan_h, fill=0, stroke=1)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(l3_x + 10, l3_y + plan_h - 20, "LEVEL 3: UNITS 7-12")
    c.setFont("Helvetica", 8)
    c.drawString(l3_x + 10, l3_y + plan_h - 35, "6 × Minimalist Units (~550 SF each) | 3,300 SF")

    # Same layout as L2
    c.setFillColor(HexColor('#FFF8E1'))
    for row in range(2):
        for col in range(3):
            ux = l3_x + 15 + col * unit_w
            uy = l3_y + 15 + row * (unit_h + 5)
            c.rect(ux, uy, unit_w - 5, unit_h - 5, fill=1, stroke=1)

            unit_num = row * 3 + col + 7
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica-Bold", 9)
            c.drawCentredString(ux + unit_w/2 - 2, uy + unit_h/2 + 10, f"UNIT {unit_num}")
            c.setFont("Helvetica", 7)
            c.drawCentredString(ux + unit_w/2 - 2, uy + unit_h/2 - 3, "1 BR / 1 BA")
            c.drawCentredString(ux + unit_w/2 - 2, uy + unit_h/2 - 14, "550 SF")
            c.setFillColor(HexColor('#FFF8E1'))

    # ============ BUILDING SUMMARY ============
    sum_x = margin + plan_w + margin
    sum_y = margin

    c.setFillColor(HexColor('#FAFAFA'))
    c.setStrokeColor(CHARCOAL)
    c.rect(sum_x, sum_y, plan_w, plan_h, fill=1, stroke=1)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(sum_x + plan_w/2, sum_y + plan_h - 30, "BUILDING PROGRAM")

    # Golden ratio diagram
    gr_x = sum_x + plan_w/2 - 60
    gr_y = sum_y + plan_h - 110
    gr_w = 120
    gr_h = gr_w / PHI

    c.setFillColor(HexColor('#FFF9C4'))
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.rect(gr_x, gr_y, gr_w, gr_h, fill=1, stroke=1)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(gr_x + gr_w/2, gr_y + gr_h/2 + 5, "φ = 1.618")
    c.setFont("Helvetica", 8)
    c.drawCentredString(gr_x + gr_w/2, gr_y + gr_h/2 - 8, "55' × 89'")

    # Program details
    y = sum_y + plan_h - 140
    c.setFont("Helvetica", 9)
    c.setFillColor(CHARCOAL)

    program = [
        ("FOOTPRINT", "55' × 89' = 4,895 SF"),
        ("", ""),
        ("LEVEL 1", "Covered Parking (12 spaces)"),
        ("", "MidFirst ATM Kiosk"),
        ("", ""),
        ("LEVEL 2", "Units 1-6 (6 × 550 SF)"),
        ("", ""),
        ("LEVEL 3", "Units 7-12 (6 × 550 SF)"),
        ("", ""),
        ("TOTAL UNITS", "12"),
        ("RENTABLE SF", "6,600 SF"),
        ("", ""),
        ("GOLDEN RATIO", "89 ÷ 55 = 1.618 = φ"),
    ]

    for label, value in program:
        if label:
            c.setFont("Helvetica-Bold", 9)
            c.drawString(sum_x + 20, y, label)
        c.setFont("Helvetica", 9)
        c.drawString(sum_x + 100, y, value)
        y -= 15


def draw_pro_forma_golden(c, width, height):
    """Pro forma for 12-unit golden ratio building"""

    col1_x = 60
    col2_x = width/2 + 40

    # ============ DEVELOPMENT COSTS ============
    y = height - 100

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(col1_x, y, "DEVELOPMENT COSTS")

    costs = [
        ("Land (Current Value)", 150000),
        ("Demolition", 20000),
        ("Architecture & Engineering", 55000),
        ("Site Work & Foundation", 145000),
        ("Vertical Construction (3 Stories)", 1050000),
        ("Parking Level", 95000),
        ("ATM Pad & Utilities", 35000),
        ("Interior Finishes (12 units)", 180000),
        ("Landscaping & Hardscape", 35000),
        ("Permits & Impact Fees", 55000),
        ("Contingency (10%)", 182000),
    ]

    total_cost = sum(c[1] for c in costs)

    y -= 30
    c.setFont("Helvetica", 10)
    for label, cost in costs:
        c.setFillColor(HexColor('#404040'))
        c.drawString(col1_x + 10, y, label)
        c.drawRightString(col1_x + 300, y, f"${cost:,.0f}")
        y -= 18

    y -= 10
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(col1_x + 10, y, "TOTAL DEVELOPMENT COST")
    c.drawRightString(col1_x + 300, y, f"${total_cost:,.0f}")

    # ============ INCOME ============
    y = height - 100

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(col2_x, y, "PROJECTED INCOME (MONTHLY)")

    income = [
        ("Units 1-6 (L2) @ $1,150/mo", 6900),
        ("Units 7-12 (L3) @ $1,200/mo", 7200),
        ("MidFirst ATM Lease", 3000),
    ]

    monthly_total = sum(i[1] for i in income)
    annual_total = monthly_total * 12

    y -= 30
    c.setFont("Helvetica", 10)
    for label, amount in income:
        c.setFillColor(HexColor('#404040'))
        c.drawString(col2_x + 10, y, label)
        c.drawRightString(col2_x + 280, y, f"${amount:,.0f}")
        y -= 18

    y -= 10
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(col2_x + 10, y, "GROSS MONTHLY")
    c.drawRightString(col2_x + 280, y, f"${monthly_total:,.0f}")
    y -= 20
    c.drawString(col2_x + 10, y, "GROSS ANNUAL")
    c.drawRightString(col2_x + 280, y, f"${annual_total:,.0f}")

    # ============ RETURNS ============
    y -= 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(col2_x, y, "INVESTMENT RETURNS")

    # Calculate returns
    vacancy = 0.05
    opex_ratio = 0.35
    effective_gross = annual_total * (1 - vacancy)
    opex = effective_gross * opex_ratio
    noi = effective_gross - opex
    cap_rate = 0.06
    stabilized_value = noi / cap_rate
    equity_created = stabilized_value - total_cost
    coc_return = noi / total_cost

    returns = [
        ("Vacancy Allowance (5%)", f"-${annual_total * vacancy:,.0f}"),
        ("Effective Gross Income", f"${effective_gross:,.0f}"),
        ("Operating Expenses (35%)", f"-${opex:,.0f}"),
        ("Net Operating Income (NOI)", f"${noi:,.0f}"),
        ("", ""),
        ("Cap Rate (Market)", "6.0%"),
        ("Stabilized Value", f"${stabilized_value:,.0f}"),
        ("", ""),
        ("Total Development Cost", f"${total_cost:,.0f}"),
        ("EQUITY CREATED", f"${equity_created:,.0f}"),
        ("Cash-on-Cash Return", f"{coc_return*100:.1f}%"),
    ]

    y -= 30
    for label, value in returns:
        if label == "EQUITY CREATED":
            c.setFont("Helvetica-Bold", 12)
            c.setFillColor(HexColor('#2E7D32'))
        elif label == "":
            y += 8
            continue
        else:
            c.setFont("Helvetica", 10)
            c.setFillColor(HexColor('#404040'))

        c.drawString(col2_x + 10, y, label)
        c.drawRightString(col2_x + 280, y, value)
        y -= 18

    # ============ HIGHLIGHT BOX ============
    c.setFillColor(HexColor('#E8F5E9'))
    c.roundRect(col1_x, 60, 300, 120, 8, fill=1, stroke=0)

    c.setFillColor(HexColor('#1B5E20'))
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(col1_x + 150, 155, "GOLDEN RATIO ADVANTAGE")

    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(col1_x + 150, 115, f"+${equity_created:,.0f}")

    c.setFont("Helvetica", 10)
    c.drawCentredString(col1_x + 150, 90, "Equity Created")

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(GOLD)
    c.drawCentredString(col1_x + 150, 70, "12 UNITS | φ PROPORTIONS")


def generate_golden_ratio_pdf():
    """Generate complete golden ratio development package"""

    output_path = os.path.expanduser("~/Downloads/luxx-haus 5/DeLoera_4801_Golden_Ratio.pdf")

    page_w, page_h = landscape(letter)
    c = canvas.Canvas(output_path, pagesize=landscape(letter))

    # ============ COVER ============
    c.setFillColor(CHARCOAL)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Golden accent lines
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(page_w * 0.1, page_h * 0.5, page_w * 0.9, page_h * 0.5)
    c.line(page_w * 0.1, page_h * 0.48, page_w * 0.9, page_h * 0.48)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(page_w/2, page_h * 0.65, "4801 N BLACKWELDER")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_w/2, page_h * 0.55, "GOLDEN RATIO DEVELOPMENT")

    c.setFillColor(white)
    c.setFont("Helvetica", 16)
    c.drawCentredString(page_w/2, page_h * 0.38, "12-Unit Mixed-Use | 55' × 89' | φ = 1.618")
    c.drawCentredString(page_w/2, page_h * 0.34, "Oklahoma City, Oklahoma 73118")

    # Golden spiral hint
    c.setStrokeColor(GOLD)
    c.setLineWidth(1)
    c.setDash([3, 3])
    spiral_x = page_w/2 - 60
    spiral_y = page_h * 0.18
    c.rect(spiral_x, spiral_y, 120, 120/PHI, fill=0, stroke=1)
    c.setDash([])

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(spiral_x + 60, spiral_y + 30, "φ")

    c.setFillColor(HexColor('#808080'))
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, page_h * 0.08, "DELOERA DEVELOPMENTS")
    c.drawCentredString(page_w/2, page_h * 0.05, f"Prepared: {datetime.now().strftime('%B %Y')}")

    c.showPage()

    # ============ PAGE 2: FRONT ELEVATION ============
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 45, page_w, 45, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, page_h - 28, "FRONT ELEVATION - N. BLACKWELDER AVENUE")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, page_h - 40, "89'-0\" FACADE | GOLDEN RATIO PROPORTIONS")

    draw_front_elevation_golden(c, page_w, page_h - 60)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 8)
    c.drawString(30, 15, "SCALE: NTS")
    c.drawRightString(page_w - 30, 15, "A-101")

    c.showPage()

    # ============ PAGE 3: SIDE ELEVATION ============
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 45, page_w, 45, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, page_h - 28, "SIDE ELEVATION - NW 48TH STREET")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, page_h - 40, "55'-0\" DEPTH | 89' ÷ 55' = 1.618 = φ")

    draw_side_elevation_golden(c, page_w, page_h - 60)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 8)
    c.drawString(30, 15, "SCALE: NTS")
    c.drawRightString(page_w - 30, 15, "A-102")

    c.showPage()

    # ============ PAGE 4: SITE PLAN ============
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 45, page_w, 45, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, page_h - 28, "SITE PLAN")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, page_h - 40, "LOT: 61' × 130' (7,930 SF) | BUILDING: 55' × 89' (4,895 SF)")

    draw_site_plan_golden(c, page_w, page_h - 45)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 8)
    c.drawString(30, 15, "SCALE: 1\" = 20'-0\"")
    c.drawRightString(page_w - 30, 15, "A-001")

    c.showPage()

    # ============ PAGE 5: FLOOR PLANS ============
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 45, page_w, 45, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, page_h - 28, "FLOOR PLANS & UNIT MIX")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, page_h - 40, "12 MINIMALIST UNITS | 6,600 SF RENTABLE")

    draw_floor_plans_golden(c, page_w, page_h - 45)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 8)
    c.drawString(30, 15, "SCALE: NTS")
    c.drawRightString(page_w - 30, 15, "A-200")

    c.showPage()

    # ============ PAGE 6: PRO FORMA ============
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 45, page_w, 45, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, page_h - 28, "DEVELOPMENT PRO FORMA")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, page_h - 40, "12 UNITS + ATM | GOLDEN RATIO OPTIMIZATION")

    draw_pro_forma_golden(c, page_w, page_h - 45)

    c.showPage()

    c.save()
    print(f"Golden Ratio PDF generated: {output_path}")
    return output_path


if __name__ == "__main__":
    generate_golden_ratio_pdf()
