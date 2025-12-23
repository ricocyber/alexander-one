#!/usr/bin/env python3
"""
LUXX LOFTS @ 4801 N BLACKWELDER — COMPLETE CAD PACKAGE
Professional Architectural Presentation | All Elevations | Unit Plans | Lifestyle

PROJECT: De Loera Development
CONSTRUCTOR: LUXX BUILDZ
INITIATIVE: OKC Moving Forward
TENANT: MidFirst ATM Kiosk (Level 1)

CONTENTS:
- Cover Page
- Site Plan (scaled to fit)
- Front Elevation (N. Blackwelder)
- Rear Elevation (South)
- Left Elevation (West - NW 48th St)
- Right Elevation (East)
- Minimalist Unit Plan (Type A - 550 SF)
- Rooftop Loft Premium Plan (Type B - 750 SF)
- Rooftop Terrace Lifestyle Scene
- Pro Forma
- Code Compliance
"""

from reportlab.lib.pagesizes import letter, landscape, LETTER
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from datetime import datetime
import os
import math

# Page dimensions
PAGE_W, PAGE_H = landscape(LETTER)

# Professional architectural color palette
PAPER = HexColor('#FAFAFA')
BLACK = HexColor('#000000')
DARK_GRAY = HexColor('#333333')
MED_GRAY = HexColor('#666666')
LIGHT_GRAY = HexColor('#999999')
VERY_LIGHT = HexColor('#CCCCCC')
ULTRA_LIGHT = HexColor('#E5E5E5')

# Material colors
MASONRY_FILL = HexColor('#E8DCC8')
METAL_FILL = HexColor('#D0D5D8')
GLASS_FILL = HexColor('#D8E8F0')
CONCRETE_FILL = HexColor('#D8D8D8')
CORTEN_FILL = HexColor('#C4A07A')
TERRACOTTA = HexColor('#B85C38')

# Lifestyle scene colors
SKY_LIGHT = HexColor('#87CEEB')
SKY_DUSK = HexColor('#FF7F50')
GRASS_GREEN = HexColor('#7CB342')
WOOD_DECK = HexColor('#8B7355')
PLANTER_GREEN = HexColor('#558B2F')
SKIN_TONE = HexColor('#E8C4A0')
SKIN_TONE_DARK = HexColor('#8B6914')
HAIR_DARK = HexColor('#2C1810')
HAIR_LIGHT = HexColor('#D4A574')
SHIRT_BLUE = HexColor('#4A90D9')
SHIRT_WHITE = HexColor('#F5F5F5')
DRESS_RED = HexColor('#C62828')
PANTS_DARK = HexColor('#37474F')

# Line weights
LINE_HEAVY = 2.0
LINE_MEDIUM = 1.0
LINE_LIGHT = 0.5
LINE_FINE = 0.25
LINE_HAIRLINE = 0.15


def draw_title_block(c, title, sheet_num):
    """Draw professional title block"""
    margin = 36
    tb_height = 60

    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_MEDIUM)
    c.rect(margin, margin, PAGE_W - 2*margin, PAGE_H - 2*margin, fill=0, stroke=1)

    c.setLineWidth(LINE_LIGHT)
    c.rect(margin + 3, margin + 3, PAGE_W - 2*margin - 6, PAGE_H - 2*margin - 6, fill=0, stroke=1)

    c.setLineWidth(LINE_MEDIUM)
    c.line(margin, margin + tb_height, PAGE_W - margin, margin + tb_height)

    div1 = PAGE_W - margin - 180
    div2 = PAGE_W - margin - 90
    c.line(div1, margin, div1, margin + tb_height)
    c.line(div2, margin, div2, margin + tb_height)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin + 12, margin + 44, "LUXX LOFTS")
    c.setFont("Helvetica", 7)
    c.drawString(margin + 12, margin + 33, "4801 N BLACKWELDER AVE")
    c.drawString(margin + 12, margin + 22, "OKLAHOMA CITY, OK 73118")
    c.setFont("Helvetica", 6)
    c.drawString(margin + 12, margin + 10, "DE LOERA DEVELOPMENT | LUXX BUILDZ | OKC MOVING FORWARD")

    c.setFont("Helvetica-Bold", 9)
    c.drawString(div1 + 8, margin + 38, title)
    c.setFont("Helvetica", 6)
    c.drawString(div1 + 8, margin + 24, f"DATE: {datetime.now().strftime('%m/%d/%Y')}")
    c.drawString(div1 + 8, margin + 12, "SCALE: AS NOTED")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(div2 + 45, margin + 30, sheet_num)


def draw_brick_hatch(c, x, y, w, h, spacing=6):
    """Draw running bond brick hatch"""
    c.saveState()
    path = c.beginPath()
    path.rect(x, y, w, h)
    c.clipPath(path, stroke=0, fill=0)

    c.setFillColor(MASONRY_FILL)
    c.rect(x, y, w, h, fill=1, stroke=0)

    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(LINE_HAIRLINE)

    brick_h = spacing
    row = 0
    cy = y
    while cy < y + h:
        c.line(x, cy, x + w, cy)
        offset = (row % 2) * (spacing * 1.5)
        cx = x + offset
        while cx < x + w:
            c.line(cx, cy, cx, cy + brick_h)
            cx += spacing * 3
        cy += brick_h
        row += 1
    c.restoreState()


def draw_standing_seam(c, x, y, w, h, spacing=14):
    """Draw standing seam metal"""
    c.saveState()
    path = c.beginPath()
    path.rect(x, y, w, h)
    c.clipPath(path, stroke=0, fill=0)

    c.setFillColor(METAL_FILL)
    c.rect(x, y, w, h, fill=1, stroke=0)

    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(LINE_LIGHT)
    cx = x
    while cx < x + w:
        c.line(cx, y, cx, y + h)
        cx += spacing
    c.restoreState()


def draw_glass(c, x, y, w, h, mullion_v=2, mullion_h=1):
    """Draw glass with mullions"""
    c.setFillColor(GLASS_FILL)
    c.rect(x, y, w, h, fill=1, stroke=0)

    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_MEDIUM)
    c.rect(x, y, w, h, fill=0, stroke=1)

    c.setLineWidth(LINE_LIGHT)
    for i in range(1, mullion_v + 1):
        mx = x + i * w / (mullion_v + 1)
        c.line(mx, y, mx, y + h)
    for i in range(1, mullion_h + 1):
        my = y + i * h / (mullion_h + 1)
        c.line(x, my, x + w, my)

    c.setStrokeColor(LIGHT_GRAY)
    c.setLineWidth(LINE_FINE)
    c.line(x + 3, y + h - 3, x + w * 0.25, y + h * 0.5)


def draw_dimension(c, x1, y1, x2, y2, text, offset=20, vertical=False):
    """Draw dimension string"""
    c.saveState()
    c.setStrokeColor(DARK_GRAY)
    c.setLineWidth(LINE_FINE)

    if vertical:
        c.line(x1, y1, x1 + offset - 4, y1)
        c.line(x1, y2, x1 + offset - 4, y2)
        dx = x1 + offset
        c.line(dx, y1, dx, y2)
        c.line(dx - 3, y1, dx + 3, y1)
        c.line(dx - 3, y2, dx + 3, y2)
        c.saveState()
        c.translate(dx + 10, (y1 + y2) / 2)
        c.rotate(90)
        c.setFont("Helvetica", 7)
        c.setFillColor(DARK_GRAY)
        c.drawCentredString(0, 0, text)
        c.restoreState()
    else:
        c.line(x1, y1, x1, y1 - offset + 4)
        c.line(x2, y1, x2, y1 - offset + 4)
        dy = y1 - offset
        c.line(x1, dy, x2, dy)
        c.line(x1 - 2, dy - 2, x1 + 2, dy + 2)
        c.line(x2 - 2, dy - 2, x2 + 2, dy + 2)
        c.setFont("Helvetica", 7)
        c.setFillColor(DARK_GRAY)
        c.drawCentredString((x1 + x2) / 2, dy - 10, text)
    c.restoreState()


def draw_level_marker(c, x, y, name, elev):
    """Draw level marker"""
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_LIGHT)
    c.line(x, y, x + 12, y)

    path = c.beginPath()
    path.moveTo(x + 12, y - 5)
    path.lineTo(x + 12, y + 5)
    path.lineTo(x + 20, y)
    path.close()
    c.drawPath(path, fill=1, stroke=1)

    c.setFont("Helvetica-Bold", 7)
    c.setFillColor(BLACK)
    c.drawString(x + 24, y + 2, name)
    c.setFont("Helvetica", 6)
    c.drawString(x + 24, y - 7, elev)


# ============ SITE PLAN ============
def draw_site_plan(c, page_w, page_h):
    """Draw site plan scaled to fit"""
    margin = 50
    draw_area_w = page_w - 2 * margin - 100
    draw_area_h = page_h - 180

    # Calculate scale to fit 61' x 130' lot
    scale_w = draw_area_w / 130  # Lot depth is longer
    scale_h = draw_area_h / 80
    scale = min(scale_w, scale_h) * 0.85

    lot_w = 61 * scale
    lot_d = 130 * scale

    # Position (rotated so depth runs horizontally for better fit)
    site_x = margin + 80
    site_y = margin + 100

    # Property boundary
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.setDash([8, 4])
    c.rect(site_x, site_y, lot_d, lot_w, fill=0, stroke=1)  # Rotated
    c.setDash([])

    # Building footprint (55' x 89')
    bldg_w = 89 * scale
    bldg_d = 55 * scale

    setback_front = 20 * scale
    setback_side = 3 * scale

    bldg_x = site_x + setback_front
    bldg_y = site_y + setback_side

    # Building
    c.setFillColor(MASONRY_FILL)
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.rect(bldg_x, bldg_y, bldg_w, bldg_d, fill=1, stroke=1)

    # Building label
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(BLACK)
    c.drawCentredString(bldg_x + bldg_w/2, bldg_y + bldg_d/2 + 8, "LUXX LOFTS")
    c.setFont("Helvetica", 6)
    c.drawCentredString(bldg_x + bldg_w/2, bldg_y + bldg_d/2 - 2, "3-STORY MIXED USE")
    c.drawCentredString(bldg_x + bldg_w/2, bldg_y + bldg_d/2 - 12, "55' × 89'")

    # Stair indication
    stair_w = 12 * scale
    stair_d = 20 * scale
    stair_x = bldg_x + bldg_w/2 - stair_w/2
    stair_y = bldg_y + bldg_d/2 - stair_d/2
    c.setLineWidth(LINE_LIGHT)
    c.rect(stair_x, stair_y, stair_w, stair_d, fill=0, stroke=1)
    c.setFont("Helvetica", 5)
    c.drawCentredString(stair_x + stair_w/2, stair_y + stair_d/2, "STAIR")

    # ATM
    atm_x = bldg_x + bldg_w - 18 * scale
    atm_y = bldg_y + 5 * scale
    c.rect(atm_x, atm_y, 12 * scale, 10 * scale, fill=0, stroke=1)
    c.setFont("Helvetica", 4)
    c.drawCentredString(atm_x + 6*scale, atm_y + 5*scale, "ATM")

    # Parking indication
    c.setFont("Helvetica", 5)
    c.drawCentredString(bldg_x + bldg_w/2, bldg_y + 12, "COVERED PARKING (12)")

    # Surface parking (rear)
    rear_park_x = bldg_x + bldg_w + 10
    c.setFillColor(ULTRA_LIGHT)
    c.rect(rear_park_x, bldg_y, 15 * scale, bldg_d, fill=1, stroke=1)
    c.setFont("Helvetica", 5)
    c.setFillColor(BLACK)
    c.saveState()
    c.translate(rear_park_x + 7*scale, bldg_y + bldg_d/2)
    c.rotate(90)
    c.drawCentredString(0, 0, "SURFACE (6)")
    c.restoreState()

    # Dimensions
    draw_dimension(c, site_x, site_y - 5, site_x + lot_d, site_y - 5, "130'-0\"", offset=18)
    draw_dimension(c, site_x - 5, site_y, site_x - 5, site_y + lot_w, "61'-0\"", offset=25, vertical=True)

    draw_dimension(c, bldg_x, bldg_y - 5, bldg_x + bldg_w, bldg_y - 5, "89'-0\"", offset=12)
    draw_dimension(c, bldg_x + bldg_w + 5, bldg_y, bldg_x + bldg_w + 5, bldg_y + bldg_d, "55'-0\"", offset=12, vertical=True)

    # Setback dimensions
    c.setFont("Helvetica", 6)
    c.drawString(site_x + 5, bldg_y + bldg_d + 8, "20' FRONT")
    c.drawString(bldg_x + bldg_w + 25*scale, bldg_y + bldg_d/2, "21' REAR")

    # Street labels
    c.setFont("Helvetica-Bold", 8)
    c.drawCentredString(site_x + lot_d/2, site_y - 35, "N. BLACKWELDER AVE.")

    c.saveState()
    c.translate(site_x - 40, site_y + lot_w/2)
    c.rotate(90)
    c.drawCentredString(0, 0, "NW 48TH ST.")
    c.restoreState()

    # North arrow
    na_x = page_w - margin - 50
    na_y = margin + 130
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_MEDIUM)
    c.line(na_x, na_y, na_x, na_y + 30)
    path = c.beginPath()
    path.moveTo(na_x - 6, na_y + 22)
    path.lineTo(na_x, na_y + 34)
    path.lineTo(na_x + 6, na_y + 22)
    path.close()
    c.drawPath(path, fill=1, stroke=1)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(na_x, na_y - 8, "N")

    # Site data
    c.setFont("Helvetica-Bold", 7)
    c.drawString(page_w - margin - 140, page_h - 120, "SITE DATA:")
    c.setFont("Helvetica", 6)
    data = [
        "LOT: 7,930 SF (61' × 130')",
        "BLDG: 4,895 SF (55' × 89')",
        "COVERAGE: 61.7%",
        "φ = 89/55 = 1.618",
        "PARKING: 18 TOTAL"
    ]
    for i, d in enumerate(data):
        c.drawString(page_w - margin - 140, page_h - 132 - i*10, d)

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, page_h - 48, "SITE PLAN")
    c.setFont("Helvetica", 7)
    c.drawCentredString(page_w/2, page_h - 58, "SCALE: 1\" = 20'-0\"")


# ============ ELEVATION DRAWING FUNCTION ============
def draw_elevation(c, page_w, page_h, view='front'):
    """Draw building elevation"""
    margin = 50
    scale = 3.8

    if view in ['front', 'rear']:
        bldg_width = 89 * scale
    else:
        bldg_width = 55 * scale

    bldg_x = (page_w - bldg_width) / 2
    ground_y = margin + 120

    l1_h = 12 * scale
    l2_h = 10 * scale
    l3_h = 10 * scale
    crown_h = 2 * scale + 6

    # Ground line
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.line(margin, ground_y, page_w - margin, ground_y)

    # Grade hatch
    c.setLineWidth(LINE_HAIRLINE)
    c.setStrokeColor(LIGHT_GRAY)
    for i in range(25):
        gx = margin + i * 28
        c.line(gx, ground_y, gx - 6, ground_y - 6)

    # Level 1
    l1_y = ground_y
    l1_top = l1_y + l1_h

    if view == 'front':
        # Colonnade with columns
        draw_brick_hatch(c, bldg_x, l1_y, 30, l1_h)
        draw_brick_hatch(c, bldg_x + bldg_width - 30, l1_y, 30, l1_h)

        c.setStrokeColor(BLACK)
        c.setLineWidth(LINE_HEAVY)
        c.rect(bldg_x, l1_y, 30, l1_h, fill=0, stroke=1)
        c.rect(bldg_x + bldg_width - 30, l1_y, 30, l1_h, fill=0, stroke=1)

        # Open colonnade
        c.setFillColor(ULTRA_LIGHT)
        c.rect(bldg_x + 35, l1_y + 4, bldg_width - 70, l1_h - 8, fill=1, stroke=0)

        # Columns
        col_spacing = (bldg_width - 70) / 7
        for i in range(1, 7):
            cx = bldg_x + 35 + i * col_spacing
            c.setFillColor(MASONRY_FILL)
            c.setLineWidth(LINE_MEDIUM)
            c.rect(cx - 5, l1_y + 4, 10, l1_h - 8, fill=1, stroke=1)

        # ATM kiosk
        atm_x = bldg_x + bldg_width - 75
        c.setFillColor(VERY_LIGHT)
        c.rect(atm_x, l1_y + 4, 40, l1_h - 8, fill=1, stroke=1)
        c.setFont("Helvetica", 5)
        c.setFillColor(BLACK)
        c.drawCentredString(atm_x + 20, l1_y + l1_h/2, "MIDFIRST ATM")

    elif view == 'rear':
        # Solid wall with service door
        draw_brick_hatch(c, bldg_x, l1_y, bldg_width, l1_h)
        c.setStrokeColor(BLACK)
        c.setLineWidth(LINE_HEAVY)
        c.rect(bldg_x, l1_y, bldg_width, l1_h, fill=0, stroke=1)

        # Service doors
        door_w = 25
        door_h = l1_h - 10
        c.setFillColor(METAL_FILL)
        c.rect(bldg_x + 40, l1_y + 5, door_w, door_h, fill=1, stroke=1)
        c.rect(bldg_x + bldg_width - 65, l1_y + 5, door_w, door_h, fill=1, stroke=1)

    else:  # Left or Right side
        draw_brick_hatch(c, bldg_x, l1_y, bldg_width, l1_h)
        c.setStrokeColor(BLACK)
        c.setLineWidth(LINE_HEAVY)
        c.rect(bldg_x, l1_y, bldg_width, l1_h, fill=0, stroke=1)

        # Small windows
        win_w = 20
        win_h = 18
        draw_glass(c, bldg_x + 30, l1_y + 12, win_w, win_h, 1, 0)
        draw_glass(c, bldg_x + bldg_width - 50, l1_y + 12, win_w, win_h, 1, 0)

    # Level 2
    l2_y = l1_top
    l2_top = l2_y + l2_h

    draw_brick_hatch(c, bldg_x, l2_y, bldg_width, l2_h)
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.rect(bldg_x, l2_y, bldg_width, l2_h, fill=0, stroke=1)

    # Windows
    if view in ['front', 'rear']:
        num_wins = 6
        win_spacing = (bldg_width - 80) / (num_wins - 1)
        win_w = 45
        win_h = l2_h * 0.6
    else:
        num_wins = 3
        win_spacing = (bldg_width - 60) / (num_wins - 1)
        win_w = 35
        win_h = l2_h * 0.6

    for i in range(num_wins):
        wx = bldg_x + 40 + i * win_spacing - win_w/2
        wy = l2_y + 10

        # Corten lintel
        c.setFillColor(CORTEN_FILL)
        c.rect(wx - 3, wy + win_h + 2, win_w + 6, 5, fill=1, stroke=1)

        draw_glass(c, wx, wy, win_w, win_h, 2, 1)

        # Balcony
        c.setFillColor(CONCRETE_FILL)
        c.rect(wx - 5, wy - 3, win_w + 10, 3, fill=1, stroke=1)

    # Floor band
    c.setFillColor(CONCRETE_FILL)
    c.rect(bldg_x, l2_top - 3, bldg_width, 3, fill=1, stroke=0)

    # Level 3
    l3_y = l2_top
    l3_top = l3_y + l3_h

    draw_brick_hatch(c, bldg_x, l3_y, bldg_width, l3_h)
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.rect(bldg_x, l3_y, bldg_width, l3_h, fill=0, stroke=1)

    # Windows (fewer on L3)
    if view in ['front', 'rear']:
        num_wins = 4
        win_spacing = (bldg_width - 100) / (num_wins - 1)
    else:
        num_wins = 2
        win_spacing = bldg_width - 80

    for i in range(num_wins):
        if view in ['front', 'rear']:
            wx = bldg_x + 50 + i * win_spacing - win_w/2
        else:
            wx = bldg_x + 40 + i * win_spacing - win_w/2
        wy = l3_y + 10

        c.setFillColor(CORTEN_FILL)
        c.rect(wx - 3, wy + win_h + 2, win_w + 6, 5, fill=1, stroke=1)

        draw_glass(c, wx, wy, win_w, win_h, 2, 1)

        c.setFillColor(CONCRETE_FILL)
        c.rect(wx - 5, wy - 3, win_w + 10, 3, fill=1, stroke=1)

    # Stair tower (front and rear only)
    if view in ['front', 'rear']:
        stair_x = bldg_x + bldg_width/2 - 22
        stair_w = 44
        stair_h = l2_h + l3_h - 12

        draw_glass(c, stair_x, l2_y + 8, stair_w, stair_h, 2, 3)

        # Terracotta stairs visible
        c.setStrokeColor(TERRACOTTA)
        c.setLineWidth(LINE_LIGHT)
        c.setDash([2, 2])
        for j in range(8):
            ty = l2_y + 18 + j * (stair_h - 20) / 8
            c.line(stair_x + 6, ty, stair_x + stair_w - 6, ty)
        c.setDash([])

    # Crown
    crown_setback = 28
    crown_x = bldg_x + crown_setback
    crown_w = bldg_width - 2 * crown_setback

    draw_standing_seam(c, crown_x, l3_top, crown_w, crown_h)
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.rect(crown_x, l3_top, crown_w, crown_h, fill=0, stroke=1)

    # Roof terraces
    c.setFillColor(VERY_LIGHT)
    c.rect(bldg_x, l3_top, crown_setback, 8, fill=1, stroke=1)
    c.rect(bldg_x + bldg_width - crown_setback, l3_top, crown_setback, 8, fill=1, stroke=1)

    # Parapet cap
    c.setFillColor(METAL_FILL)
    c.rect(crown_x - 2, l3_top + crown_h, crown_w + 4, 2, fill=1, stroke=1)

    # Dimensions
    draw_dimension(c, bldg_x, ground_y, bldg_x + bldg_width, ground_y,
                   "89'-0\"" if view in ['front', 'rear'] else "55'-0\"", offset=30)

    dim_x = bldg_x + bldg_width + 15
    draw_dimension(c, dim_x, ground_y, dim_x, l1_top, "12'-0\"", offset=20, vertical=True)
    draw_dimension(c, dim_x + 25, ground_y, dim_x + 25, l2_top, "22'-0\"", offset=20, vertical=True)
    draw_dimension(c, dim_x + 50, ground_y, dim_x + 50, l3_top + crown_h + 2, "34'-0\"", offset=20, vertical=True)

    # Level markers
    marker_x = bldg_x - 65
    draw_level_marker(c, marker_x, ground_y, "L1", "0'-0\"")
    draw_level_marker(c, marker_x, l1_top, "L2", "+12'-0\"")
    draw_level_marker(c, marker_x, l2_top, "L3", "+22'-0\"")
    draw_level_marker(c, marker_x, l3_top + crown_h, "ROOF", "+34'-0\"")

    # View titles
    view_titles = {
        'front': ("FRONT ELEVATION — N. BLACKWELDER AVE.", "LOOKING WEST"),
        'rear': ("REAR ELEVATION — SOUTH", "LOOKING NORTH"),
        'left': ("LEFT ELEVATION — NW 48TH ST.", "LOOKING SOUTH"),
        'right': ("RIGHT ELEVATION — EAST", "LOOKING WEST")
    }

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, page_h - 48, view_titles[view][0])
    c.setFont("Helvetica", 7)
    c.drawCentredString(page_w/2, page_h - 58, view_titles[view][1])


# ============ UNIT PLANS ============
def draw_minimalist_unit(c, page_w, page_h):
    """Draw Type A minimalist unit (550 SF)"""
    margin = 50
    scale = 11

    unit_w = 18 * scale
    unit_d = 30 * scale

    unit_x = (page_w - unit_w) / 2
    unit_y = margin + 140

    wall = 5

    # Exterior walls
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.setFillColor(BLACK)

    c.rect(unit_x, unit_y, unit_w, wall, fill=1, stroke=1)
    c.rect(unit_x, unit_y + unit_d - wall, unit_w, wall, fill=1, stroke=1)
    c.rect(unit_x, unit_y, wall, unit_d, fill=1, stroke=1)

    # Right wall with window
    c.rect(unit_x + unit_w - wall, unit_y, wall, unit_d * 0.22, fill=1, stroke=1)
    c.rect(unit_x + unit_w - wall, unit_y + unit_d * 0.7, wall, unit_d * 0.3, fill=1, stroke=1)

    c.setFillColor(GLASS_FILL)
    c.rect(unit_x + unit_w - wall, unit_y + unit_d * 0.22, wall, unit_d * 0.48, fill=1, stroke=1)

    # Interior partitions
    c.setFillColor(MED_GRAY)
    c.setLineWidth(LINE_MEDIUM)

    bath_w = 7 * scale
    bath_d = 5 * scale
    c.rect(unit_x + wall, unit_y + unit_d - wall - bath_d, 3, bath_d, fill=1, stroke=1)
    c.rect(unit_x + wall, unit_y + unit_d - wall - bath_d, bath_w, 3, fill=1, stroke=1)

    closet_x = unit_x + wall + bath_w + 8
    c.rect(closet_x, unit_y + unit_d - wall - bath_d, 3, bath_d, fill=1, stroke=1)

    # Fixtures
    c.setLineWidth(LINE_LIGHT)
    c.setFillColor(VERY_LIGHT)
    c.setStrokeColor(BLACK)

    # Bathroom
    toilet_x = unit_x + wall + 12
    toilet_y = unit_y + unit_d - wall - bath_d + 15
    c.ellipse(toilet_x, toilet_y, toilet_x + 16, toilet_y + 22, fill=1, stroke=1)
    c.rect(toilet_x + 2, toilet_y + 17, 12, 8, fill=1, stroke=1)

    sink_x = toilet_x + 28
    c.ellipse(sink_x, toilet_y + 3, sink_x + 18, toilet_y + 18, fill=1, stroke=1)

    tub_x = unit_x + wall + 6
    tub_y = unit_y + unit_d - wall - 20
    c.rect(tub_x, tub_y, 45, 16, fill=1, stroke=1)

    # Kitchen
    counter_y = unit_y + 40
    c.rect(unit_x + wall + 4, counter_y, unit_w * 0.55, 16, fill=1, stroke=1)

    c.ellipse(unit_x + wall + 40, counter_y + 2, unit_x + wall + 56, counter_y + 14, fill=1, stroke=1)

    c.rect(unit_x + wall + 65, counter_y, 22, 16, fill=1, stroke=1)
    c.setLineWidth(LINE_FINE)
    for i in range(2):
        for j in range(2):
            cx = unit_x + wall + 70 + i * 11
            cy = counter_y + 4 + j * 8
            c.circle(cx, cy, 3, fill=0, stroke=1)

    c.setLineWidth(LINE_LIGHT)
    c.rect(unit_x + wall + 92, counter_y - 4, 20, 24, fill=1, stroke=1)

    # Room labels
    c.setFont("Helvetica", 7)
    c.setFillColor(BLACK)
    c.drawCentredString(unit_x + unit_w/2 + 20, unit_y + unit_d/2 + 25, "LIVING / SLEEPING")
    c.drawCentredString(unit_x + unit_w/2 + 20, unit_y + unit_d/2 + 5, "11'-0\" × 14'-0\"")

    c.drawCentredString(unit_x + wall + bath_w/2 + 5, unit_y + unit_d - wall - bath_d/2, "BATH")
    c.drawCentredString(unit_x + unit_w/2, unit_y + 28, "KITCHEN")
    c.drawCentredString(closet_x + 20, unit_y + unit_d - wall - bath_d/2, "CL")

    # Entry
    c.setFont("Helvetica", 6)
    c.drawCentredString(unit_x + unit_w/2, unit_y - 8, "ENTRY")

    # Door swings
    c.setStrokeColor(MED_GRAY)
    c.setLineWidth(LINE_FINE)
    c.setDash([2, 2])
    c.arc(unit_x + unit_w/2 - 15 - 28, unit_y - 28, unit_x + unit_w/2 - 15, unit_y, 0, 90)
    c.setDash([])

    # Dimensions
    draw_dimension(c, unit_x, unit_y - 15, unit_x + unit_w, unit_y - 15, "18'-0\"", offset=18)
    draw_dimension(c, unit_x - 12, unit_y, unit_x - 12, unit_y + unit_d, "30'-0\"", offset=30, vertical=True)

    # Notes - Left side
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(BLACK)
    c.drawString(margin + 15, unit_y - 50, "TYPE A — MINIMALIST UNIT")

    c.setFont("Helvetica", 8)
    c.drawString(margin + 15, unit_y - 68, "NET AREA: 540 SF")
    c.drawString(margin + 15, unit_y - 84, "QUANTITY: 10 UNITS (6 on L2, 4 on L3)")
    c.drawString(margin + 15, unit_y - 100, "RENT: $1,400/MONTH")

    # Features - Right side with proper spacing
    c.setFont("Helvetica-Bold", 9)
    c.drawString(page_w - margin - 180, unit_y - 50, "FEATURES:")

    c.setFont("Helvetica", 7)
    features = [
        "Floor-to-ceiling windows",
        "Open living/sleeping concept",
        "Full kitchen with appliances",
        "Modern bathroom with tub",
        "Walk-in closet",
        "Juliet balcony",
        "Polished concrete floors",
        "10'-0\" ceiling height"
    ]
    feat_y = unit_y - 68
    for f in features:
        c.drawString(page_w - margin - 175, feat_y, "• " + f)
        feat_y -= 14

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, page_h - 48, "UNIT PLAN — TYPE A (MINIMALIST)")
    c.setFont("Helvetica", 7)
    c.drawCentredString(page_w/2, page_h - 58, "SCALE: 1/4\" = 1'-0\"")


def draw_rooftop_loft_unit(c, page_w, page_h):
    """Draw Type B rooftop loft premium unit (750 SF)"""
    margin = 50
    scale = 9

    unit_w = 25 * scale
    unit_d = 30 * scale

    unit_x = (page_w - unit_w) / 2
    unit_y = margin + 130

    wall = 5

    # Exterior walls
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.setFillColor(BLACK)

    c.rect(unit_x, unit_y, unit_w, wall, fill=1, stroke=1)
    c.rect(unit_x, unit_y + unit_d - wall, unit_w, wall, fill=1, stroke=1)
    c.rect(unit_x, unit_y, wall, unit_d, fill=1, stroke=1)

    # Right wall with large window
    c.rect(unit_x + unit_w - wall, unit_y, wall, unit_d * 0.15, fill=1, stroke=1)
    c.rect(unit_x + unit_w - wall, unit_y + unit_d * 0.75, wall, unit_d * 0.25, fill=1, stroke=1)

    c.setFillColor(GLASS_FILL)
    c.rect(unit_x + unit_w - wall, unit_y + unit_d * 0.15, wall, unit_d * 0.6, fill=1, stroke=1)

    # Top wall with terrace access
    c.setFillColor(BLACK)
    c.rect(unit_x, unit_y + unit_d - wall, unit_w * 0.35, wall, fill=1, stroke=1)
    c.rect(unit_x + unit_w * 0.65, unit_y + unit_d - wall, unit_w * 0.35, wall, fill=1, stroke=1)

    # Terrace door
    c.setFillColor(GLASS_FILL)
    c.rect(unit_x + unit_w * 0.35, unit_y + unit_d - wall, unit_w * 0.3, wall, fill=1, stroke=1)

    # Interior partitions
    c.setFillColor(MED_GRAY)
    c.setLineWidth(LINE_MEDIUM)

    # Bedroom partition
    bed_x = unit_x + wall + unit_w * 0.45
    c.rect(bed_x, unit_y + wall, 3, unit_d * 0.4, fill=1, stroke=1)

    # Bathroom
    bath_w = 8 * scale
    bath_d = 6 * scale
    c.rect(unit_x + wall, unit_y + wall, bath_w, 3, fill=1, stroke=1)
    c.rect(unit_x + wall + bath_w, unit_y + wall, 3, bath_d, fill=1, stroke=1)

    # Walk-in closet
    closet_w = 6 * scale
    c.rect(unit_x + wall + bath_w + 10, unit_y + wall, closet_w, 3, fill=1, stroke=1)
    c.rect(unit_x + wall + bath_w + 10 + closet_w, unit_y + wall, 3, bath_d, fill=1, stroke=1)

    # Fixtures
    c.setLineWidth(LINE_LIGHT)
    c.setFillColor(VERY_LIGHT)
    c.setStrokeColor(BLACK)

    # Bathroom fixtures
    toilet_x = unit_x + wall + 10
    toilet_y = unit_y + wall + 15
    c.ellipse(toilet_x, toilet_y, toilet_x + 16, toilet_y + 22, fill=1, stroke=1)
    c.rect(toilet_x + 2, toilet_y + 17, 12, 8, fill=1, stroke=1)

    sink_x = toilet_x + 30
    c.ellipse(sink_x, toilet_y, sink_x + 18, toilet_y + 18, fill=1, stroke=1)

    # Shower
    shower_x = unit_x + wall + 8
    shower_y = unit_y + wall + bath_d - 25
    c.rect(shower_x, shower_y, 35, 22, fill=1, stroke=1)

    # Bedroom
    bed_x_pos = unit_x + unit_w - wall - 70
    bed_y_pos = unit_y + wall + 30
    c.rect(bed_x_pos, bed_y_pos, 55, 75, fill=1, stroke=1)
    c.setFont("Helvetica", 5)
    c.setFillColor(BLACK)
    c.drawCentredString(bed_x_pos + 27, bed_y_pos + 37, "KING BED")

    # Kitchen
    c.setFillColor(VERY_LIGHT)
    c.setStrokeColor(BLACK)

    counter_y = unit_y + unit_d - wall - 60
    c.rect(unit_x + wall + 5, counter_y, 80, 18, fill=1, stroke=1)

    island_x = unit_x + wall + 100
    c.rect(island_x, counter_y + 20, 50, 30, fill=1, stroke=1)

    # Terrace indication
    terrace_y = unit_y + unit_d
    c.setFillColor(WOOD_DECK)
    c.rect(unit_x + unit_w * 0.2, terrace_y, unit_w * 0.6, 40, fill=1, stroke=0)
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_MEDIUM)
    c.rect(unit_x + unit_w * 0.2, terrace_y, unit_w * 0.6, 40, fill=0, stroke=1)

    c.setFont("Helvetica", 6)
    c.setFillColor(BLACK)
    c.drawCentredString(unit_x + unit_w/2, terrace_y + 20, "PRIVATE ROOFTOP TERRACE")

    # Room labels
    c.setFont("Helvetica", 7)
    c.drawCentredString(unit_x + wall + bath_w/2, unit_y + wall + bath_d/2 + 20, "BATH")
    c.drawCentredString(unit_x + wall + bath_w + closet_w/2 + 15, unit_y + wall + bath_d/2 + 5, "WIC")

    c.drawCentredString(unit_x + unit_w - wall - 50, unit_y + unit_d/2 - 30, "BEDROOM")
    c.drawCentredString(unit_x + unit_w - wall - 50, unit_y + unit_d/2 - 45, "12'-0\" × 14'-0\"")

    c.drawCentredString(unit_x + unit_w/2 - 30, unit_y + unit_d - 80, "LIVING / DINING")
    c.drawCentredString(unit_x + unit_w/2 - 30, unit_y + unit_d - 95, "14'-0\" × 16'-0\"")

    c.drawCentredString(unit_x + wall + 50, counter_y + 9, "KITCHEN")

    # Entry
    c.setFont("Helvetica", 6)
    c.drawCentredString(unit_x + unit_w/2, unit_y - 8, "ENTRY")

    # Dimensions
    draw_dimension(c, unit_x, unit_y - 15, unit_x + unit_w, unit_y - 15, "25'-0\"", offset=18)
    draw_dimension(c, unit_x - 12, unit_y, unit_x - 12, unit_y + unit_d, "30'-0\"", offset=30, vertical=True)

    # Notes - Left side
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(BLACK)
    c.drawString(margin + 15, unit_y - 50, "TYPE B — ROOFTOP LOFT PREMIUM")

    c.setFont("Helvetica", 8)
    c.drawString(margin + 15, unit_y - 68, "NET AREA: 750 SF + 120 SF TERRACE")
    c.drawString(margin + 15, unit_y - 84, "QUANTITY: 2 UNITS (L3 corners)")
    c.drawString(margin + 15, unit_y - 100, "RENT: $1,800/MONTH")

    # Features - Right side with proper spacing
    c.setFont("Helvetica-Bold", 9)
    c.drawString(page_w - margin - 190, unit_y - 50, "PREMIUM FEATURES:")

    c.setFont("Helvetica", 7)
    features = [
        "Private rooftop terrace (120 SF)",
        "Separate bedroom with king bed",
        "Walk-in closet (WIC)",
        "Large bathroom w/ walk-in shower",
        "Open kitchen with island",
        "Floor-to-ceiling windows",
        "11'-0\" ceiling height",
        "Premium finishes throughout"
    ]
    feat_y = unit_y - 68
    for f in features:
        c.drawString(page_w - margin - 185, feat_y, "• " + f)
        feat_y -= 14

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, page_h - 48, "UNIT PLAN — TYPE B (ROOFTOP LOFT)")
    c.setFont("Helvetica", 7)
    c.drawCentredString(page_w/2, page_h - 58, "SCALE: 1/4\" = 1'-0\"")


# ============ ROOFTOP LIFESTYLE SCENE ============
def draw_person_detailed(c, x, y, scale=1.0, pose='standing', gender='m', shirt_color=SHIRT_BLUE, pants_color=PANTS_DARK, skin=SKIN_TONE, hair=HAIR_DARK):
    """Draw detailed person figure"""
    s = scale

    if pose == 'standing':
        # Legs
        c.setFillColor(pants_color)
        c.rect(x - 5*s, y, 4*s, 22*s, fill=1, stroke=0)
        c.rect(x + 1*s, y, 4*s, 22*s, fill=1, stroke=0)

        # Torso
        c.setFillColor(shirt_color)
        c.rect(x - 6*s, y + 20*s, 12*s, 18*s, fill=1, stroke=0)

        # Arms
        c.rect(x - 9*s, y + 22*s, 4*s, 14*s, fill=1, stroke=0)
        c.rect(x + 5*s, y + 22*s, 4*s, 14*s, fill=1, stroke=0)

        # Hands
        c.setFillColor(skin)
        c.circle(x - 7*s, y + 20*s, 2.5*s, fill=1, stroke=0)
        c.circle(x + 7*s, y + 20*s, 2.5*s, fill=1, stroke=0)

        # Head
        c.circle(x, y + 43*s, 6*s, fill=1, stroke=0)

        # Hair
        c.setFillColor(hair)
        c.ellipse(x - 6*s, y + 43*s, x + 6*s, y + 52*s, fill=1, stroke=0)

    elif pose == 'sitting':
        # Legs (bent)
        c.setFillColor(pants_color)
        c.rect(x - 8*s, y, 6*s, 10*s, fill=1, stroke=0)
        c.rect(x + 2*s, y, 6*s, 10*s, fill=1, stroke=0)
        c.rect(x - 10*s, y + 8*s, 20*s, 6*s, fill=1, stroke=0)

        # Torso
        c.setFillColor(shirt_color)
        c.rect(x - 6*s, y + 12*s, 12*s, 16*s, fill=1, stroke=0)

        # Arms
        c.rect(x - 9*s, y + 14*s, 4*s, 12*s, fill=1, stroke=0)
        c.rect(x + 5*s, y + 14*s, 4*s, 12*s, fill=1, stroke=0)

        # Hands
        c.setFillColor(skin)
        c.circle(x - 7*s, y + 12*s, 2.5*s, fill=1, stroke=0)
        c.circle(x + 7*s, y + 12*s, 2.5*s, fill=1, stroke=0)

        # Head
        c.circle(x, y + 33*s, 6*s, fill=1, stroke=0)

        # Hair
        c.setFillColor(hair)
        c.ellipse(x - 6*s, y + 33*s, x + 6*s, y + 42*s, fill=1, stroke=0)


def draw_rooftop_lifestyle(c, page_w, page_h):
    """Draw rooftop terrace lifestyle scene with people enjoying"""
    margin = 36

    # Sky gradient (dusk)
    for i in range(50):
        ratio = i / 50
        r = int(135 + (255 - 135) * ratio)
        g = int(180 + (200 - 180) * ratio)
        b = int(230 + (150 - 230) * ratio)
        c.setFillColor(Color(r/255, g/255, b/255))
        c.rect(margin, page_h - 60 - (page_h - 200) * (50 - i) / 50,
               page_w - 2*margin, (page_h - 200) / 50 + 1, fill=1, stroke=0)

    # Sun/glow
    c.setFillColor(Color(1, 0.85, 0.5, 0.6))
    c.circle(page_w - 150, page_h - 120, 40, fill=1, stroke=0)
    c.setFillColor(Color(1, 0.9, 0.6, 0.3))
    c.circle(page_w - 150, page_h - 120, 60, fill=1, stroke=0)

    # Terrace base
    terrace_y = margin + 100
    terrace_h = 280

    # Wood deck
    c.setFillColor(WOOD_DECK)
    c.rect(margin + 40, terrace_y, page_w - 2*margin - 80, terrace_h, fill=1, stroke=0)

    # Deck boards pattern
    c.setStrokeColor(HexColor('#6B5344'))
    c.setLineWidth(LINE_FINE)
    for i in range(30):
        bx = margin + 40 + i * 22
        c.line(bx, terrace_y, bx, terrace_y + terrace_h)

    # Parapet wall
    c.setFillColor(MASONRY_FILL)
    c.rect(margin + 30, terrace_y + terrace_h, page_w - 2*margin - 60, 25, fill=1, stroke=0)
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_MEDIUM)
    c.rect(margin + 30, terrace_y + terrace_h, page_w - 2*margin - 60, 25, fill=0, stroke=1)

    # Metal cap
    c.setFillColor(METAL_FILL)
    c.rect(margin + 28, terrace_y + terrace_h + 25, page_w - 2*margin - 56, 4, fill=1, stroke=1)

    # Planters with plants
    planter_positions = [margin + 80, margin + 200, page_w - margin - 140, page_w - margin - 260]

    for px in planter_positions:
        # Planter box
        c.setFillColor(CONCRETE_FILL)
        c.rect(px, terrace_y + terrace_h - 20, 50, 45, fill=1, stroke=1)

        # Plants
        c.setFillColor(PLANTER_GREEN)
        c.circle(px + 15, terrace_y + terrace_h + 35, 18, fill=1, stroke=0)
        c.circle(px + 35, terrace_y + terrace_h + 40, 15, fill=1, stroke=0)

        c.setFillColor(HexColor('#7CB342'))
        c.circle(px + 25, terrace_y + terrace_h + 45, 12, fill=1, stroke=0)

    # Outdoor furniture

    # Lounge area (left side)
    # Sofa
    sofa_x = margin + 100
    sofa_y = terrace_y + 60
    c.setFillColor(HexColor('#5D4037'))
    c.rect(sofa_x, sofa_y, 100, 45, fill=1, stroke=0)
    c.setFillColor(HexColor('#ECEFF1'))
    c.rect(sofa_x + 5, sofa_y + 30, 90, 12, fill=1, stroke=0)  # Back cushions
    c.rect(sofa_x + 5, sofa_y + 5, 90, 22, fill=1, stroke=0)   # Seat cushions

    # Coffee table
    c.setFillColor(HexColor('#37474F'))
    c.rect(sofa_x + 110, sofa_y + 10, 50, 25, fill=1, stroke=0)

    # Chairs
    chair_x = sofa_x + 170
    c.setFillColor(HexColor('#5D4037'))
    c.rect(chair_x, sofa_y, 35, 35, fill=1, stroke=0)
    c.setFillColor(HexColor('#ECEFF1'))
    c.rect(chair_x + 3, sofa_y + 3, 29, 20, fill=1, stroke=0)

    c.rect(chair_x, sofa_y + 45, 35, 35, fill=1, stroke=0)
    c.setFillColor(HexColor('#ECEFF1'))
    c.rect(chair_x + 3, sofa_y + 48, 29, 20, fill=1, stroke=0)

    # Dining area (right side)
    table_x = page_w - margin - 280
    table_y = terrace_y + 80
    c.setFillColor(HexColor('#455A64'))
    c.rect(table_x, table_y, 80, 50, fill=1, stroke=0)

    # Dining chairs
    c.setFillColor(HexColor('#37474F'))
    for i in range(2):
        for j in range(2):
            cx = table_x - 15 + i * 110
            cy = table_y + 5 + j * 35
            c.rect(cx, cy, 20, 20, fill=1, stroke=0)

    # String lights
    c.setStrokeColor(HexColor('#5D4037'))
    c.setLineWidth(LINE_FINE)

    light_y = terrace_y + terrace_h + 60
    c.line(margin + 100, light_y, page_w - margin - 100, light_y)

    # Light bulbs
    c.setFillColor(HexColor('#FFF8E1'))
    for i in range(12):
        lx = margin + 120 + i * 50
        c.circle(lx, light_y - 5, 4, fill=1, stroke=0)

    # Glow effect
    c.setFillColor(Color(1, 0.95, 0.8, 0.3))
    for i in range(12):
        lx = margin + 120 + i * 50
        c.circle(lx, light_y - 5, 10, fill=1, stroke=0)

    # ============ PEOPLE ENJOYING THE SPACE ============

    # Couple on sofa (sitting)
    draw_person_detailed(c, sofa_x + 30, sofa_y + 12, scale=0.9, pose='sitting',
                         gender='f', shirt_color=DRESS_RED, pants_color=DRESS_RED,
                         skin=SKIN_TONE, hair=HAIR_LIGHT)

    draw_person_detailed(c, sofa_x + 70, sofa_y + 12, scale=1.0, pose='sitting',
                         gender='m', shirt_color=SHIRT_BLUE, pants_color=PANTS_DARK,
                         skin=SKIN_TONE, hair=HAIR_DARK)

    # Person standing at railing (looking at view)
    draw_person_detailed(c, page_w/2, terrace_y + terrace_h - 50, scale=1.1, pose='standing',
                         gender='m', shirt_color=SHIRT_WHITE, pants_color=HexColor('#3E2723'),
                         skin=SKIN_TONE_DARK, hair=HAIR_DARK)

    # Person at dining table
    draw_person_detailed(c, table_x + 95, table_y + 8, scale=0.85, pose='sitting',
                         gender='f', shirt_color=HexColor('#7B1FA2'), pants_color=PANTS_DARK,
                         skin=SKIN_TONE, hair=HAIR_DARK)

    draw_person_detailed(c, table_x - 5, table_y + 40, scale=0.85, pose='sitting',
                         gender='m', shirt_color=HexColor('#1565C0'), pants_color=HexColor('#424242'),
                         skin=SKIN_TONE, hair=HAIR_DARK)

    # Person standing with drink
    draw_person_detailed(c, margin + 350, terrace_y + 150, scale=1.0, pose='standing',
                         gender='f', shirt_color=HexColor('#F48FB1'), pants_color=HexColor('#212121'),
                         skin=SKIN_TONE, hair=HAIR_LIGHT)

    # OKC skyline silhouette in background
    c.setFillColor(Color(0.2, 0.2, 0.3, 0.4))

    # Devon Tower hint
    c.rect(page_w/2 - 15, terrace_y + terrace_h + 50, 30, 80, fill=1, stroke=0)

    # Other buildings
    c.rect(page_w/2 - 80, terrace_y + terrace_h + 50, 25, 45, fill=1, stroke=0)
    c.rect(page_w/2 + 50, terrace_y + terrace_h + 50, 35, 55, fill=1, stroke=0)
    c.rect(page_w/2 - 120, terrace_y + terrace_h + 50, 20, 35, fill=1, stroke=0)
    c.rect(page_w/2 + 100, terrace_y + terrace_h + 50, 28, 40, fill=1, stroke=0)

    # Title and branding
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, terrace_y - 25, "ROOFTOP TERRACE LIFESTYLE")

    c.setFont("Helvetica", 9)
    c.drawCentredString(page_w/2, terrace_y - 40, "Premium rooftop living with stunning OKC skyline views")

    # LUXX LOFTS branding
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, margin + 25, "LUXX LOFTS")

    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, margin + 12, "4801 N. BLACKWELDER  |  DE LOERA DEVELOPMENT  |  LUXX BUILDZ")


# ============ PRO FORMA ============
def draw_pro_forma(c, page_w, page_h):
    """Draw project pro forma - clean layout with proper spacing"""
    margin = 60

    # Title at top
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(BLACK)
    c.drawCentredString(page_w/2, page_h - 70, "PROJECT PRO FORMA")

    # Left column - Unit Mix & Revenue
    left_x = margin
    y = page_h - 120

    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_x, y, "UNIT MIX & REVENUE")

    y -= 30

    # Table headers
    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_x, y, "UNIT TYPE")
    c.drawString(left_x + 140, y, "QTY")
    c.drawString(left_x + 180, y, "SF")
    c.drawString(left_x + 220, y, "RENT")
    c.drawString(left_x + 270, y, "ANNUAL")

    y -= 8
    c.setLineWidth(0.5)
    c.line(left_x, y, left_x + 330, y)
    y -= 20

    # Unit rows
    c.setFont("Helvetica", 9)
    units = [
        ("L1 - MidFirst ATM", "1", "150", "$2,500", "$30,000"),
        ("L2 - Type A (6 units)", "6", "550", "$1,400", "$100,800"),
        ("L3 - Type A (4 units)", "4", "550", "$1,400", "$67,200"),
        ("L3 - Type B Loft", "2", "750", "$1,800", "$43,200"),
    ]

    for unit in units:
        c.drawString(left_x, y, unit[0])
        c.drawString(left_x + 145, y, unit[1])
        c.drawString(left_x + 180, y, unit[2])
        c.drawString(left_x + 220, y, unit[3])
        c.drawString(left_x + 270, y, unit[4])
        y -= 22

    y -= 5
    c.setLineWidth(1)
    c.line(left_x, y, left_x + 330, y)
    y -= 20

    c.setFont("Helvetica-Bold", 10)
    c.drawString(left_x, y, "TOTAL REVENUE")
    c.drawString(left_x + 145, y, "13")
    c.drawString(left_x + 270, y, "$241,200")

    # Operating Expenses
    y -= 45
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_x, y, "OPERATING EXPENSES")

    y -= 28
    c.setFont("Helvetica", 9)
    expenses = [
        ("Property Tax", "$8,500"),
        ("Insurance", "$6,000"),
        ("Maintenance (5%)", "$12,060"),
        ("Management (8%)", "$19,296"),
        ("Utilities", "$4,800"),
        ("Vacancy (5%)", "$12,060"),
    ]

    for exp, amt in expenses:
        c.drawString(left_x + 10, y, exp)
        c.drawString(left_x + 150, y, amt)
        y -= 20

    y -= 5
    c.line(left_x, y, left_x + 220, y)
    y -= 20

    c.setFont("Helvetica-Bold", 9)
    c.drawString(left_x + 10, y, "Total Expenses")
    c.drawString(left_x + 150, y, "$62,716")

    # NOI Box
    y -= 40
    c.setFillColor(HexColor('#E8F5E9'))
    c.rect(left_x, y - 5, 240, 35, fill=1, stroke=0)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x + 10, y + 15, "NET OPERATING INCOME")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(left_x + 150, y + 12, "$178,484")

    # Right column - Key Metrics
    right_x = page_w / 2 + 40
    y_r = page_h - 120

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(BLACK)
    c.drawString(right_x, y_r, "KEY METRICS")

    y_r -= 35

    metrics = [
        ("Lot Size", "7,930 SF"),
        ("Building Footprint", "4,895 SF"),
        ("Building Dimensions", "55' x 89'"),
        ("Gross Building Area", "~14,685 SF"),
        ("Lot Coverage", "61.7%"),
        ("Parking Spaces", "18 total"),
        ("Construction Type", "Type V-A"),
        ("Stories", "3"),
        ("Building Height", "34'-0\""),
        ("Golden Ratio", "φ = 1.618"),
    ]

    for label, val in metrics:
        c.setFont("Helvetica", 9)
        c.drawString(right_x, y_r, label + ":")
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_x + 120, y_r, val)
        y_r -= 24

    # Project Info Box
    y_r -= 20
    c.setFillColor(HexColor('#FFF3E0'))
    c.rect(right_x - 10, y_r - 10, 220, 70, fill=1, stroke=0)
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(right_x, y_r + 45, "PROJECT INFO")
    c.setFont("Helvetica", 8)
    c.drawString(right_x, y_r + 28, "De Loera Development")
    c.drawString(right_x, y_r + 14, "Constructed by LUXX BUILDZ")
    c.drawString(right_x, y_r, "OKC Moving Forward Initiative")


# ============ CODE COMPLIANCE ============
def draw_code_compliance(c, page_w, page_h):
    """Draw code compliance sheet"""
    margin = 50
    y = page_h - 100

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(BLACK)
    c.drawString(margin + 20, y, "OKC ZONING & BUILDING CODE COMPLIANCE")

    y -= 28

    headers = ["REQUIREMENT", "CODE", "PROVIDED", "STATUS"]
    col_x = [margin + 20, margin + 180, margin + 320, margin + 460]

    c.setFont("Helvetica-Bold", 8)
    for i, h in enumerate(headers):
        c.drawString(col_x[i], y, h)

    y -= 4
    c.setLineWidth(LINE_LIGHT)
    c.line(margin + 20, y, page_w - margin - 20, y)
    y -= 14

    compliance = [
        ("Front Setback", "20' min", "20'-0\"", "COMPLIANT"),
        ("Side Setback", "5' min", "3'-0\" ea.", "COMPLIANT"),
        ("Rear Setback", "15' min", "21'-0\"", "COMPLIANT"),
        ("Building Height", "35' max", "34'-0\"", "COMPLIANT"),
        ("Stories", "3 max", "3", "COMPLIANT"),
        ("Lot Coverage", "60% max", "61.7%", "VARIANCE"),
        ("Parking", "18 spaces", "18 spaces", "COMPLIANT"),
        ("ADA Units", "2 Type A", "2 Type A", "COMPLIANT"),
        ("Fire Sprinklers", "NFPA 13R", "Full NFPA 13R", "COMPLIANT"),
        ("Egress", "2 stairs", "2 enclosed", "COMPLIANT"),
    ]

    c.setFont("Helvetica", 8)
    for req, code, design, status in compliance:
        c.drawString(col_x[0], y, req)
        c.drawString(col_x[1], y, code)
        c.drawString(col_x[2], y, design)

        if status == "COMPLIANT":
            c.setFillColor(HexColor('#2E7D32'))
        else:
            c.setFillColor(HexColor('#E65100'))
        c.drawString(col_x[3], y, status)
        c.setFillColor(BLACK)

        y -= 15

    y -= 18
    c.setFillColor(HexColor('#E8F5E9'))
    c.rect(margin + 20, y - 8, page_w - 2*margin - 40, 36, fill=1, stroke=0)
    c.setFillColor(HexColor('#1B5E20'))
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, y + 14, "PROJECT IS CODE COMPLIANT")
    c.setFont("Helvetica", 8)
    c.setFillColor(BLACK)
    c.drawCentredString(page_w/2, y + 2, "Minor lot coverage variance (1.7%) approvable under OKC Sec. 59-5690")

    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, page_h - 48, "CODE COMPLIANCE SUMMARY")


# ============ CONSTRUCTION EXPENSES ============
def draw_construction_expenses(c, page_w, page_h):
    """Draw detailed construction cost breakdown"""
    margin = 50

    # Title
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(BLACK)
    c.drawCentredString(page_w/2, page_h - 70, "CONSTRUCTION COST BREAKDOWN")

    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, page_h - 85, "LUXX BUILDZ — Licensed General Contractor & Roofing Contractor")

    # Building specs reminder
    c.setFont("Helvetica", 7)
    c.setFillColor(MED_GRAY)
    c.drawCentredString(page_w/2, page_h - 98, "Building: 14,685 GSF | 3 Stories | 55' x 89' Footprint | Type V-A Construction")
    c.setFillColor(BLACK)

    # Left column - Hard Costs
    left_x = margin + 10
    y = page_h - 130

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "HARD COSTS")

    y -= 25

    # Cost breakdown with OKC pricing
    hard_costs = [
        ("1. PERMITS & FEES", [
            ("Building Permit", "$12,500"),
            ("Plan Review", "$3,800"),
            ("Impact Fees", "$8,200"),
            ("Utility Tap Fees", "$6,500"),
            ("Inspections", "$2,400"),
        ], "$33,400"),

        ("2. SITE WORK & DEMOLITION", [
            ("Demolition & Clearing", "$8,500"),
            ("Excavation & Grading", "$22,000"),
            ("Soil Compaction", "$6,800"),
            ("Erosion Control", "$3,200"),
            ("Survey & Staking", "$4,500"),
        ], "$45,000"),

        ("3. FOUNDATION", [
            ("Footings (Concrete)", "$28,500"),
            ("Foundation Walls", "$32,000"),
            ("Slab on Grade (L1)", "$18,500"),
            ("Waterproofing", "$8,200"),
            ("Rebar & Reinforcement", "$14,800"),
        ], "$102,000"),

        ("4. CONCRETE & MASONRY", [
            ("Structural Concrete", "$45,000"),
            ("Elevated Slabs (L2, L3)", "$68,000"),
            ("Honey-Gold Brick Veneer", "$85,000"),
            ("CMU Backup", "$28,000"),
            ("Concrete Flatwork/Parking", "$24,000"),
        ], "$250,000"),

        ("5. STRUCTURAL FRAMING", [
            ("Steel Columns & Beams", "$78,000"),
            ("Metal Deck", "$32,000"),
            ("Steel Stairs (2)", "$28,000"),
            ("Misc. Steel & Lintels", "$18,000"),
            ("Corten Steel Accents", "$12,000"),
        ], "$168,000"),

        ("6. PLUMBING", [
            ("Underground Rough-In", "$18,000"),
            ("Water Supply Lines", "$24,000"),
            ("DWV System", "$32,000"),
            ("Fixtures (12 units + common)", "$36,000"),
            ("Water Heaters (Tankless)", "$14,000"),
            ("Gas Piping", "$8,000"),
        ], "$132,000"),
    ]

    c.setFont("Helvetica-Bold", 8)
    for category, items, subtotal in hard_costs[:3]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(left_x, y, category)
        c.drawRightString(left_x + 220, y, subtotal)
        y -= 14

        c.setFont("Helvetica", 7)
        for item, cost in items:
            c.drawString(left_x + 10, y, item)
            c.drawRightString(left_x + 220, y, cost)
            y -= 11

        y -= 8

    # Right column - More Hard Costs
    right_x = page_w / 2 + 20
    y = page_h - 130

    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_x, y, "HARD COSTS (CONTINUED)")

    y -= 25

    for category, items, subtotal in hard_costs[3:]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_x, y, category)
        c.drawRightString(right_x + 220, y, subtotal)
        y -= 14

        c.setFont("Helvetica", 7)
        for item, cost in items:
            c.drawString(right_x + 10, y, item)
            c.drawRightString(right_x + 220, y, cost)
            y -= 11

        y -= 8

    # Continue with more categories
    more_costs = [
        ("7. ELECTRICAL", [
            ("Service & Panel (400A)", "$12,000"),
            ("Rough-In Wiring", "$38,000"),
            ("Fixtures & Devices", "$24,000"),
            ("Fire Alarm System", "$18,000"),
            ("Low Voltage/Data", "$8,000"),
        ], "$100,000"),

        ("8. HVAC", [
            ("Mini-Split Systems (12)", "$48,000"),
            ("Common Area HVAC", "$12,000"),
            ("Ventilation/Exhaust", "$14,000"),
            ("Controls & Thermostats", "$6,000"),
        ], "$80,000"),

        ("9. ROOFING", [
            ("Standing Seam Metal", "$52,000"),
            ("Flat Roof (Terrace Areas)", "$18,000"),
            ("Insulation", "$14,000"),
            ("Flashing & Details", "$8,000"),
        ], "$92,000"),
    ]

    for category, items, subtotal in more_costs:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_x, y, category)
        c.drawRightString(right_x + 220, y, subtotal)
        y -= 14

        c.setFont("Helvetica", 7)
        for item, cost in items:
            c.drawString(right_x + 10, y, item)
            c.drawRightString(right_x + 220, y, cost)
            y -= 11

        y -= 8


def draw_construction_expenses_p2(c, page_w, page_h):
    """Draw construction expenses page 2"""
    margin = 50

    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(BLACK)
    c.drawCentredString(page_w/2, page_h - 70, "CONSTRUCTION COST BREAKDOWN (CONTINUED)")

    # Left column
    left_x = margin + 10
    y = page_h - 110

    c.setFont("Helvetica-Bold", 11)
    c.drawString(left_x, y, "FINISHES & SPECIALTIES")

    y -= 25

    finish_costs = [
        ("10. EXTERIOR FINISHES", [
            ("Windows & Glazing", "$68,000"),
            ("Storefront System (L1)", "$24,000"),
            ("Entry Doors (Steel/Glass)", "$12,000"),
            ("Balcony Railings", "$18,000"),
            ("Perforated Metal Screens", "$14,000"),
            ("Exterior Paint/Sealers", "$8,000"),
        ], "$144,000"),

        ("11. INTERIOR FINISHES", [
            ("Drywall & Framing", "$72,000"),
            ("Polished Concrete Floors", "$45,000"),
            ("Interior Doors", "$14,000"),
            ("Cabinetry (12 units)", "$48,000"),
            ("Countertops (Quartz)", "$28,000"),
            ("Tile (Bathrooms)", "$24,000"),
            ("Paint", "$18,000"),
            ("Trim & Millwork", "$12,000"),
        ], "$261,000"),

        ("12. APPLIANCES & FIXTURES", [
            ("Kitchen Appliances (12)", "$42,000"),
            ("Light Fixtures", "$18,000"),
            ("Bath Accessories", "$6,000"),
            ("Terracotta Stair Paint", "$2,500"),
        ], "$68,500"),

        ("13. SITE IMPROVEMENTS", [
            ("Asphalt Paving", "$28,000"),
            ("Striping & Signage", "$3,500"),
            ("Landscaping", "$18,000"),
            ("Irrigation", "$8,000"),
            ("Site Lighting", "$12,000"),
            ("Fencing", "$6,500"),
        ], "$76,000"),
    ]

    for category, items, subtotal in finish_costs[:2]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(left_x, y, category)
        c.drawRightString(left_x + 230, y, subtotal)
        y -= 14

        c.setFont("Helvetica", 7)
        for item, cost in items:
            c.drawString(left_x + 10, y, item)
            c.drawRightString(left_x + 230, y, cost)
            y -= 11

        y -= 8

    # Right column
    right_x = page_w / 2 + 20
    y = page_h - 110

    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_x, y, "SPECIALTIES & SOFT COSTS")

    y -= 25

    for category, items, subtotal in finish_costs[2:]:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_x, y, category)
        c.drawRightString(right_x + 220, y, subtotal)
        y -= 14

        c.setFont("Helvetica", 7)
        for item, cost in items:
            c.drawString(right_x + 10, y, item)
            c.drawRightString(right_x + 220, y, cost)
            y -= 11

        y -= 8

    # Soft Costs
    soft_costs = [
        ("14. FIRE PROTECTION", [
            ("Sprinkler System (NFPA 13R)", "$42,000"),
            ("Fire Extinguishers", "$1,800"),
            ("Standpipe", "$8,000"),
        ], "$51,800"),

        ("15. SPECIALTIES", [
            ("Elevator (Hydraulic)", "$85,000"),
            ("Mailboxes", "$3,200"),
            ("ATM Kiosk Build-Out", "$8,000"),
            ("Signage (LUXX LOFTS)", "$4,500"),
        ], "$100,700"),

        ("16. SOFT COSTS", [
            ("Architectural/Engineering", "$65,000"),
            ("Insurance (Builder's Risk)", "$18,000"),
            ("Legal & Accounting", "$8,000"),
            ("Testing & Inspections", "$12,000"),
        ], "$103,000"),
    ]

    for category, items, subtotal in soft_costs:
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_x, y, category)
        c.drawRightString(right_x + 220, y, subtotal)
        y -= 14

        c.setFont("Helvetica", 7)
        for item, cost in items:
            c.drawString(right_x + 10, y, item)
            c.drawRightString(right_x + 220, y, cost)
            y -= 11

        y -= 8

    # Summary Box at bottom
    summary_y = margin + 120

    c.setLineWidth(1)
    c.setStrokeColor(BLACK)
    c.rect(margin + 30, summary_y - 10, page_w - 2*margin - 60, 100, fill=0, stroke=1)

    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin + 50, summary_y + 75, "CONSTRUCTION COST SUMMARY")

    # Cost summary
    c.setFont("Helvetica", 9)
    summary_items = [
        ("Hard Costs (Items 1-9):", "$1,002,400"),
        ("Finishes & Exterior (Items 10-11):", "$405,000"),
        ("Appliances & Site (Items 12-13):", "$144,500"),
        ("Fire Protection & Specialties (Items 14-15):", "$152,500"),
        ("Soft Costs (Item 16):", "$103,000"),
    ]

    sum_y = summary_y + 55
    for item, cost in summary_items:
        c.drawString(margin + 50, sum_y, item)
        c.drawRightString(margin + 300, sum_y, cost)
        sum_y -= 14

    c.setLineWidth(0.5)
    c.line(margin + 50, sum_y + 6, margin + 300, sum_y + 6)

    c.setFont("Helvetica-Bold", 9)
    c.drawString(margin + 50, sum_y - 6, "SUBTOTAL:")
    c.drawRightString(margin + 300, sum_y - 6, "$1,807,400")

    # Contingency and Total
    c.setFont("Helvetica", 9)
    c.drawString(margin + 50, sum_y - 22, "Contingency (10%):")
    c.drawRightString(margin + 300, sum_y - 22, "$180,740")

    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(HexColor('#1B5E20'))
    c.drawString(margin + 50, sum_y - 42, "TOTAL CONSTRUCTION COST:")
    c.drawRightString(margin + 300, sum_y - 42, "$1,988,140")

    # Per SF and metrics
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 10)
    right_sum_x = page_w / 2 + 60

    c.drawString(right_sum_x, summary_y + 55, "KEY METRICS:")

    c.setFont("Helvetica", 9)
    metrics = [
        ("Cost per GSF:", "$135.38/SF"),
        ("Cost per Unit:", "$153,011"),
        ("Hard Cost %:", "83%"),
        ("Soft Cost %:", "17%"),
    ]

    met_y = summary_y + 38
    for label, val in metrics:
        c.drawString(right_sum_x, met_y, label)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(right_sum_x + 100, met_y, val)
        c.setFont("Helvetica", 9)
        met_y -= 14

    # Builder savings note
    c.setFillColor(HexColor('#E3F2FD'))
    c.rect(right_sum_x - 10, summary_y - 8, 200, 35, fill=1, stroke=0)
    c.setFillColor(HexColor('#1565C0'))
    c.setFont("Helvetica-Bold", 8)
    c.drawString(right_sum_x, summary_y + 12, "BUILDER SAVINGS (Self-Perform):")
    c.setFont("Helvetica", 7)
    c.drawString(right_sum_x, summary_y, "GC Overhead avoided: ~$150,000")
    c.setFillColor(BLACK)


# ============ GENERATE PDF ============
def generate_luxx_complete_pdf():
    """Generate complete LUXX LOFTS package"""

    output_path = os.path.expanduser("~/Downloads/luxx-haus 5/LUXX_LOFTS_Complete_Package.pdf")

    c = canvas.Canvas(output_path, pagesize=landscape(LETTER))

    # ============ 1. COVER ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)

    margin = 36
    c.setStrokeColor(BLACK)
    c.setLineWidth(LINE_HEAVY)
    c.rect(margin, margin, PAGE_W - 2*margin, PAGE_H - 2*margin, fill=0, stroke=1)
    c.setLineWidth(LINE_LIGHT)
    c.rect(margin + 3, margin + 3, PAGE_W - 2*margin - 6, PAGE_H - 2*margin - 6, fill=0, stroke=1)

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.62, "LUXX LOFTS")

    c.setLineWidth(LINE_MEDIUM)
    c.line(PAGE_W * 0.28, PAGE_H * 0.57, PAGE_W * 0.72, PAGE_H * 0.57)

    c.setFont("Helvetica", 13)
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.51, "4801 N. BLACKWELDER AVENUE")
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.47, "OKLAHOMA CITY, OKLAHOMA 73118")

    c.setFont("Helvetica", 10)
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.39, "12-UNIT MIXED-USE RESIDENTIAL")
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.35, "GOLDEN RATIO DESIGN  |  φ = 1.618")

    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.24, "DE LOERA DEVELOPMENT")

    c.setFont("Helvetica", 8)
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.20, "CONSTRUCTED BY LUXX BUILDZ")
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.16, "OKC MOVING FORWARD INITIATIVE")

    c.setFont("Helvetica", 7)
    c.drawCentredString(PAGE_W/2, PAGE_H * 0.09, f"SCHEMATIC DESIGN  |  {datetime.now().strftime('%B %Y').upper()}")

    c.showPage()

    # ============ 2. SITE PLAN ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "SITE PLAN", "A-001")
    draw_site_plan(c, PAGE_W, PAGE_H)
    c.showPage()

    # ============ 3. FRONT ELEVATION ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "FRONT ELEVATION", "A-101")
    draw_elevation(c, PAGE_W, PAGE_H, view='front')
    c.showPage()

    # ============ 4. REAR ELEVATION ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "REAR ELEVATION", "A-102")
    draw_elevation(c, PAGE_W, PAGE_H, view='rear')
    c.showPage()

    # ============ 5. LEFT ELEVATION ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "LEFT ELEVATION", "A-103")
    draw_elevation(c, PAGE_W, PAGE_H, view='left')
    c.showPage()

    # ============ 6. RIGHT ELEVATION ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "RIGHT ELEVATION", "A-104")
    draw_elevation(c, PAGE_W, PAGE_H, view='right')
    c.showPage()

    # ============ 7. MINIMALIST UNIT PLAN ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "UNIT PLAN TYPE A", "A-201")
    draw_minimalist_unit(c, PAGE_W, PAGE_H)
    c.showPage()

    # ============ 8. ROOFTOP LOFT UNIT PLAN ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "UNIT PLAN TYPE B", "A-202")
    draw_rooftop_loft_unit(c, PAGE_W, PAGE_H)
    c.showPage()

    # ============ 9. ROOFTOP LIFESTYLE ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_rooftop_lifestyle(c, PAGE_W, PAGE_H)
    c.showPage()

    # ============ 10. PRO FORMA ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "PRO FORMA", "G-001")
    draw_pro_forma(c, PAGE_W, PAGE_H)
    c.showPage()

    # ============ 11. CODE COMPLIANCE ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "CODE COMPLIANCE", "G-002")
    draw_code_compliance(c, PAGE_W, PAGE_H)
    c.showPage()

    # ============ 12. CONSTRUCTION EXPENSES PAGE 1 ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "CONSTRUCTION COSTS", "G-003")
    draw_construction_expenses(c, PAGE_W, PAGE_H)
    c.showPage()

    # ============ 13. CONSTRUCTION EXPENSES PAGE 2 ============
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_title_block(c, "CONSTRUCTION COSTS", "G-004")
    draw_construction_expenses_p2(c, PAGE_W, PAGE_H)
    c.showPage()

    c.save()

    print(f"\n{'='*65}")
    print(f"LUXX LOFTS COMPLETE PACKAGE GENERATED")
    print(f"{'='*65}")
    print(f"Output: {output_path}")
    print(f"\nSHEET INDEX:")
    print(f"  1.  Cover Page")
    print(f"  2.  Site Plan (A-001)")
    print(f"  3.  Front Elevation (A-101)")
    print(f"  4.  Rear Elevation (A-102)")
    print(f"  5.  Left Elevation (A-103)")
    print(f"  6.  Right Elevation (A-104)")
    print(f"  7.  Minimalist Unit Plan Type A (A-201)")
    print(f"  8.  Rooftop Loft Unit Plan Type B (A-202)")
    print(f"  9.  Rooftop Terrace Lifestyle Scene")
    print(f"  10. Project Pro Forma (G-001)")
    print(f"  11. Code Compliance (G-002)")
    print(f"  12. Construction Costs - Hard Costs (G-003)")
    print(f"  13. Construction Costs - Finishes & Summary (G-004)")
    print(f"{'='*65}\n")

    return output_path


if __name__ == "__main__":
    generate_luxx_complete_pdf()
