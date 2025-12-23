#!/usr/bin/env python3
"""
LUXX LOFTS — INVESTOR/BANK PACKAGE & TENANT MARKETING
Professional documents for financing and leasing

INVESTOR/BANK PACKAGE:
- Executive Summary
- Investment Highlights
- Financial Projections
- Construction Budget
- Risk Analysis
- Exit Strategy

TENANT MARKETING:
- Lifestyle branding
- Unit features
- Amenities
- Location highlights
- Leasing information
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

# Colors
PAPER = HexColor('#FAFAFA')
BLACK = HexColor('#000000')
DARK_GRAY = HexColor('#333333')
MED_GRAY = HexColor('#666666')
LIGHT_GRAY = HexColor('#999999')
VERY_LIGHT = HexColor('#CCCCCC')

# Brand colors - Golden Ratio Aesthetic
LUXX_GOLD = HexColor('#C9A227')       # Primary accent - warm gold
LUXX_DARK = HexColor('#1A1A1A')       # Rich black
LUXX_CREAM = HexColor('#F5F0E6')      # Warm cream background
NAVY = HexColor('#1A365D')            # Deep navy for headers
FOREST_GREEN = HexColor('#1B5E20')    # Success/positive
ACCENT_ORANGE = HexColor('#E65100')   # Warning/attention

# Golden Ratio Palette - Sophisticated minimalist
WARM_WHITE = HexColor('#FAF8F5')      # Clean background
CHARCOAL = HexColor('#2C2C2C')        # Primary text
WARM_GRAY = HexColor('#6B6560')       # Secondary text
HONEY = HexColor('#D4A574')           # Brick/warm accent
RUST = HexColor('#8B4513')            # Corten steel accent
SAGE = HexColor('#7A8B6E')            # Natural accent

# Material colors
BRICK_HONEY = HexColor('#D4A574')
CORTEN = HexColor('#8B4513')
TERRACOTTA = HexColor('#B85C38')


def draw_deloera_logo(c, x, y, scale=1.0, color_scheme="dark"):
    """
    Draw De Loera Development industrial contemporary logo

    The logo features:
    - Geometric 'D' formed by stacked horizontal bars (industrial/construction aesthetic)
    - Clean modernist typography
    - Corten steel-inspired color palette

    Args:
        c: canvas object
        x, y: center position of logo
        scale: size multiplier (1.0 = standard size)
        color_scheme: "dark" (for light backgrounds) or "light" (for dark backgrounds)
    """
    if color_scheme == "light":
        primary = white
        accent = LUXX_GOLD
        secondary = HexColor('#CCCCCC')
    else:
        primary = LUXX_DARK
        accent = HexColor('#8B4513')  # Corten steel
        secondary = HexColor('#666666')

    # Save state
    c.saveState()
    c.translate(x, y)
    c.scale(scale, scale)

    # === GEOMETRIC 'D' ICON ===
    # Industrial stacked bar design representing building/construction
    icon_x = -85
    icon_y = -12

    bar_height = 5
    bar_gap = 3

    # Draw 5 horizontal bars that form a 'D' shape
    bars = [
        (0, 28, 35),   # Top bar - full width
        (0, 20, 40),   # Second bar - extends right
        (0, 12, 42),   # Middle bar - longest
        (0, 4, 40),    # Fourth bar - extends right
        (0, -4, 35),   # Bottom bar - full width
    ]

    # Left vertical element (stem of D)
    c.setFillColor(accent)
    c.rect(icon_x, icon_y - 4, 6, 37, fill=1, stroke=0)

    # Horizontal bars
    c.setFillColor(primary)
    for bx, by, bw in bars:
        c.rect(icon_x + 8, icon_y + by, bw, bar_height, fill=1, stroke=0)

    # Right curved element (arc of D) - using rectangles for industrial look
    c.setFillColor(accent)
    c.rect(icon_x + 43, icon_y + 20, 6, 13, fill=1, stroke=0)  # Top right vertical
    c.rect(icon_x + 45, icon_y + 8, 6, 16, fill=1, stroke=0)   # Middle right
    c.rect(icon_x + 43, icon_y - 1, 6, 13, fill=1, stroke=0)   # Bottom right vertical

    # === COMPANY NAME ===
    # "DE LOERA" in bold modernist type
    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 22)
    c.drawString(-20, 8, "DE LOERA")

    # "DEVELOPMENT" in lighter weight below
    c.setFillColor(secondary if color_scheme == "dark" else HexColor('#AAAAAA'))
    c.setFont("Helvetica", 10)
    c.drawString(-20, -6, "D E V E L O P M E N T")

    # Accent line under text
    c.setStrokeColor(accent)
    c.setLineWidth(2)
    c.line(-20, -12, 95, -12)

    c.restoreState()


def draw_deloera_logo_stacked(c, x, y, scale=1.0, color_scheme="dark"):
    """
    Stacked version of logo for smaller spaces
    Icon on top, text below
    """
    if color_scheme == "light":
        primary = white
        accent = LUXX_GOLD
        secondary = HexColor('#CCCCCC')
    else:
        primary = LUXX_DARK
        accent = HexColor('#8B4513')
        secondary = HexColor('#666666')

    c.saveState()
    c.translate(x, y)
    c.scale(scale, scale)

    # === GEOMETRIC ICON (centered) ===
    # Abstract building/D shape
    icon_x = -25
    icon_y = 15

    # Three stacked blocks forming abstract building
    c.setFillColor(accent)
    c.rect(icon_x, icon_y + 25, 50, 8, fill=1, stroke=0)      # Top block
    c.setFillColor(primary)
    c.rect(icon_x + 5, icon_y + 13, 45, 8, fill=1, stroke=0)  # Middle block
    c.setFillColor(accent)
    c.rect(icon_x + 10, icon_y + 1, 40, 8, fill=1, stroke=0)  # Bottom block

    # Vertical accent bar
    c.setFillColor(primary)
    c.rect(icon_x - 5, icon_y + 1, 4, 32, fill=1, stroke=0)

    # === TEXT ===
    c.setFillColor(primary)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(0, -5, "DE LOERA")

    c.setFillColor(secondary if color_scheme == "dark" else HexColor('#AAAAAA'))
    c.setFont("Helvetica", 7)
    c.drawCentredString(0, -16, "D E V E L O P M E N T")

    c.restoreState()


def draw_five_pointed_star(c, cx, cy, outer_r, inner_r=None, fill=True):
    """Draw a five-pointed star"""
    if inner_r is None:
        inner_r = outer_r * 0.382  # Golden ratio for nice star

    p = c.beginPath()
    for i in range(10):
        angle = math.radians(90 + i * 36)  # Start from top
        r = outer_r if i % 2 == 0 else inner_r
        px = cx + r * math.cos(angle)
        py = cy + r * math.sin(angle)
        if i == 0:
            p.moveTo(px, py)
        else:
            p.lineTo(px, py)
    p.close()
    c.drawPath(p, fill=1 if fill else 0, stroke=1 if not fill else 0)


def draw_oklahoma_state_seal(c, x, y, scale=1.0):
    """
    Draw the Great Seal of Oklahoma
    - Large 5-pointed star on blue background
    - 45 smaller stars around it
    - Central scene with pioneer and Native American
    - Five tribal seals in star rays
    - "GREAT SEAL OF THE STATE OF OKLAHOMA" text
    """
    c.saveState()
    c.translate(x, y)
    c.scale(scale, scale)

    radius = 45

    # Outer gold ring
    c.setStrokeColor(HexColor('#C9A227'))
    c.setLineWidth(3)
    c.setFillColor(HexColor('#1A365D'))  # Navy blue background
    c.circle(0, 0, radius, fill=1, stroke=1)

    # Inner decorative ring
    c.setStrokeColor(HexColor('#C9A227'))
    c.setLineWidth(1)
    c.circle(0, 0, radius - 4, fill=0, stroke=1)

    # === 45 SMALL STARS around the edge ===
    c.setFillColor(HexColor('#C9A227'))
    for i in range(45):
        angle = math.radians(90 + i * 8)  # Distribute evenly
        sx = (radius - 8) * math.cos(angle)
        sy = (radius - 8) * math.sin(angle)
        draw_five_pointed_star(c, sx, sy, 2, 0.8)

    # === LARGE CENTRAL 5-POINTED STAR ===
    c.setFillColor(HexColor('#C9A227'))
    c.setStrokeColor(HexColor('#8B6914'))
    c.setLineWidth(0.5)
    draw_five_pointed_star(c, 0, 0, 28, 11)

    # === CENTER SCENE (simplified) ===
    # Blue center circle
    c.setFillColor(HexColor('#1A365D'))
    c.circle(0, 0, 10, fill=1, stroke=0)

    # Columbia figure (central - scales of justice)
    c.setFillColor(HexColor('#C9A227'))
    # Simple representation: triangle for figure
    p = c.beginPath()
    p.moveTo(0, 8)
    p.lineTo(-3, -2)
    p.lineTo(3, -2)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Scales of justice (simplified)
    c.setStrokeColor(HexColor('#C9A227'))
    c.setLineWidth(0.8)
    c.line(-6, 5, 6, 5)  # Balance bar
    c.line(0, 5, 0, 8)   # Pole

    # Pioneer (left) and Native American (right) - simplified figures
    c.setFillColor(HexColor('#C9A227'))
    # Left figure
    c.circle(-5, 0, 2, fill=1, stroke=0)
    c.rect(-6, -5, 2, 4, fill=1, stroke=0)
    # Right figure
    c.circle(5, 0, 2, fill=1, stroke=0)
    c.rect(4, -5, 2, 4, fill=1, stroke=0)

    # Handshake in center
    c.rect(-2, -3, 4, 2, fill=1, stroke=0)

    # === TEXT "GREAT SEAL OF THE STATE OF OKLAHOMA" ===
    # This would be curved text - simplified as straight for legibility
    c.setFillColor(HexColor('#C9A227'))
    c.setFont("Helvetica-Bold", 4)

    # Top arc text
    text = "GREAT SEAL OF THE STATE OF OKLAHOMA"
    for i, char in enumerate(text):
        angle = math.radians(155 - i * 8.5)
        tx = (radius - 14) * math.cos(angle)
        ty = (radius - 14) * math.sin(angle)
        c.saveState()
        c.translate(tx, ty)
        c.rotate(math.degrees(angle) - 90)
        c.drawCentredString(0, 0, char)
        c.restoreState()

    c.restoreState()


def draw_okc_city_seal(c, x, y, scale=1.0):
    """
    Draw Oklahoma City official seal (adopted Feb 23, 1965)
    Features:
    - Shield (law and protection)
    - Hatchet and stake (89'ers Land Run 1889)
    - Plow (pioneer agriculture, Creek Nation)
    - Peace pipe with eagle feathers (Native American heritage)
    - Atomic symbol (industrial/scientific future)
    - Post oak leaves (Council Grove)
    - "CITY OF OKLAHOMA CITY" text
    """
    c.saveState()
    c.translate(x, y)
    c.scale(scale, scale)

    radius = 42

    # Outer ring - navy blue
    c.setStrokeColor(HexColor('#1A365D'))
    c.setLineWidth(4)
    c.setFillColor(white)
    c.circle(0, 0, radius, fill=1, stroke=1)

    # Inner decorative ring
    c.setStrokeColor(HexColor('#1A365D'))
    c.setLineWidth(1.5)
    c.circle(0, 0, radius - 5, fill=0, stroke=1)

    # === SHIELD (center) ===
    c.setFillColor(HexColor('#1A365D'))
    c.setStrokeColor(HexColor('#8B4513'))
    c.setLineWidth(1)
    # Shield shape
    p = c.beginPath()
    p.moveTo(-15, 15)
    p.lineTo(15, 15)
    p.lineTo(15, 0)
    p.lineTo(12, -10)
    p.lineTo(0, -18)
    p.lineTo(-12, -10)
    p.lineTo(-15, 0)
    p.close()
    c.drawPath(p, fill=1, stroke=1)

    # === Elements on shield ===
    c.setFillColor(HexColor('#C9A227'))

    # Hatchet (top left of shield)
    c.setStrokeColor(HexColor('#C9A227'))
    c.setLineWidth(1.5)
    c.line(-8, 10, -8, 2)  # Handle
    # Blade
    p = c.beginPath()
    p.moveTo(-8, 10)
    p.lineTo(-12, 12)
    p.lineTo(-10, 8)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Stake (top right)
    c.line(8, 12, 8, 4)
    p = c.beginPath()
    p.moveTo(6, 4)
    p.lineTo(10, 4)
    p.lineTo(8, 0)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Plow (center)
    c.setLineWidth(1)
    p = c.beginPath()
    p.moveTo(-5, -2)
    p.lineTo(5, -2)
    p.lineTo(3, -8)
    p.lineTo(-3, -8)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # Plow blade
    c.line(0, -8, 0, -12)

    # Peace pipe (left side, outside shield)
    c.setStrokeColor(HexColor('#8B4513'))
    c.setLineWidth(1.5)
    c.line(-20, 5, -18, -5)
    # Feathers
    c.setFillColor(HexColor('#C9A227'))
    for i in range(3):
        p = c.beginPath()
        p.moveTo(-20, 5 - i*3)
        p.lineTo(-24, 3 - i*3)
        p.lineTo(-20, 2 - i*3)
        p.close()
        c.drawPath(p, fill=1, stroke=0)

    # Atomic symbol (right side - representing future)
    c.setStrokeColor(HexColor('#1A365D'))
    c.setLineWidth(0.8)
    # Electron orbits
    c.ellipse(16, -5, 26, 5, fill=0, stroke=1)
    c.saveState()
    c.translate(21, 0)
    c.rotate(60)
    c.ellipse(-5, -5, 5, 5, fill=0, stroke=1)
    c.restoreState()
    c.saveState()
    c.translate(21, 0)
    c.rotate(-60)
    c.ellipse(-5, -5, 5, 5, fill=0, stroke=1)
    c.restoreState()
    # Nucleus
    c.setFillColor(HexColor('#1A365D'))
    c.circle(21, 0, 2, fill=1, stroke=0)

    # Post oak leaves (bottom corners)
    c.setFillColor(HexColor('#2E5A1E'))
    # Left leaf
    p = c.beginPath()
    p.moveTo(-18, -15)
    p.curveTo(-22, -12, -24, -18, -20, -20)
    p.curveTo(-18, -22, -16, -18, -18, -15)
    p.close()
    c.drawPath(p, fill=1, stroke=0)
    # Right leaf
    p = c.beginPath()
    p.moveTo(18, -15)
    p.curveTo(22, -12, 24, -18, 20, -20)
    p.curveTo(18, -22, 16, -18, 18, -15)
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # === TEXT around edge ===
    c.setFillColor(HexColor('#1A365D'))
    c.setFont("Helvetica-Bold", 5)

    # "CITY OF OKLAHOMA CITY" at top
    text_top = "CITY OF OKLAHOMA CITY"
    for i, char in enumerate(text_top):
        angle = math.radians(160 - i * 7.5)
        tx = (radius - 10) * math.cos(angle)
        ty = (radius - 10) * math.sin(angle)
        c.saveState()
        c.translate(tx, ty)
        c.rotate(math.degrees(angle) - 90)
        c.drawCentredString(0, 0, char)
        c.restoreState()

    # "FOUNDED 1889" at bottom
    text_bottom = "FOUNDED 1889"
    for i, char in enumerate(text_bottom):
        angle = math.radians(-125 + i * 9)
        tx = (radius - 10) * math.cos(angle)
        ty = (radius - 10) * math.sin(angle)
        c.saveState()
        c.translate(tx, ty)
        c.rotate(math.degrees(angle) + 90)
        c.drawCentredString(0, 0, char)
        c.restoreState()

    c.restoreState()


def draw_building_rendering(c, x, y, width, height, time_of_day="dusk"):
    """
    Draw high-quality 3D perspective rendering of LUXX LOFTS
    View from Blackwelder Ave facing South

    Enhanced with:
    - Detailed brick texture with mortar lines
    - Realistic window mullions and reflections
    - Proper shadows and depth
    - Detailed balconies with perforated screens
    - Rich atmospheric effects
    - Street-level detail
    """
    c.saveState()
    c.translate(x, y)

    # Scale to fit
    scale = min(width / 420, height / 300)
    c.scale(scale, scale)

    # === RICH SKY GRADIENT (golden hour) ===
    # Multiple color bands for realistic sunset
    sky_colors = [
        (255, 200, 150),  # Warm orange at horizon
        (255, 180, 130),
        (255, 160, 120),
        (240, 150, 130),
        (200, 140, 150),
        (160, 130, 170),
        (120, 120, 180),
        (90, 100, 160),
        (70, 80, 140),
        (50, 60, 120),
    ]
    for i, (r, g, b) in enumerate(sky_colors):
        c.setFillColor(Color(r/255, g/255, b/255))
        c.rect(-30, 200 + i * 12, 460, 14, fill=1, stroke=0)

    # Subtle clouds
    c.setFillColor(Color(1, 0.95, 0.9, 0.4))
    c.ellipse(50, 280, 120, 295, fill=1, stroke=0)
    c.ellipse(200, 270, 280, 288, fill=1, stroke=0)
    c.ellipse(320, 275, 380, 290, fill=1, stroke=0)

    # === BACKGROUND BUILDINGS (cityscape) ===
    c.setFillColor(HexColor('#3A3A4A'))
    c.rect(-20, 180, 60, 40, fill=1, stroke=0)
    c.rect(360, 175, 70, 50, fill=1, stroke=0)
    c.setFillColor(HexColor('#4A4A5A'))
    c.rect(370, 165, 40, 60, fill=1, stroke=0)

    # === GROUND PLANE ===
    # Street with asphalt texture
    c.setFillColor(HexColor('#3A3A3A'))
    c.rect(-30, -30, 460, 55, fill=1, stroke=0)

    # Road markings
    c.setStrokeColor(HexColor('#FFCC00'))
    c.setLineWidth(1.5)
    c.setDash([15, 10])
    c.line(-30, 5, 430, 5)
    c.setDash([])

    # Sidewalk with texture
    c.setFillColor(HexColor('#B8B8B8'))
    c.rect(-30, 22, 460, 22, fill=1, stroke=0)
    # Sidewalk joints
    c.setStrokeColor(HexColor('#A0A0A0'))
    c.setLineWidth(0.5)
    for sx in range(-30, 430, 40):
        c.line(sx, 22, sx, 44)

    # Curb
    c.setFillColor(HexColor('#909090'))
    c.rect(-30, 20, 460, 4, fill=1, stroke=0)

    # === BUILDING DIMENSIONS ===
    bx = 55      # Building left edge
    bw = 290     # Building width (55' in golden ratio)
    bh = 195     # Building height (3 stories @ 35')
    by = 44      # Building base y
    persp = 6    # Perspective convergence

    # === LEFT SIDE WALL (showing depth) ===
    c.setFillColor(HexColor('#9A7B5A'))  # Shadowed brick
    pts_side = [
        (bx - 18, by),
        (bx, by),
        (bx + persp, by + bh),
        (bx - 12, by + bh - 8)
    ]
    p = c.beginPath()
    p.moveTo(pts_side[0][0], pts_side[0][1])
    for pt in pts_side[1:]:
        p.lineTo(pt[0], pt[1])
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # === MAIN FACADE ===
    # Base brick color
    c.setFillColor(HexColor('#D4A574'))
    pts_main = [
        (bx, by),
        (bx + bw, by),
        (bx + bw - persp, by + bh),
        (bx + persp, by + bh)
    ]
    p = c.beginPath()
    p.moveTo(pts_main[0][0], pts_main[0][1])
    for pt in pts_main[1:]:
        p.lineTo(pt[0], pt[1])
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # === DETAILED BRICK TEXTURE ===
    c.setStrokeColor(HexColor('#C49A6C'))
    c.setLineWidth(0.2)
    # Horizontal mortar lines
    for row in range(0, 195, 4):
        y_line = by + row
        x_l = bx + (persp * row / bh)
        x_r = bx + bw - (persp * row / bh)
        c.line(x_l, y_line, x_r, y_line)

    # Vertical mortar lines (staggered like real brick)
    c.setLineWidth(0.15)
    for row in range(0, 195, 8):
        y_line = by + row
        x_l = bx + (persp * row / bh)
        x_r = bx + bw - (persp * row / bh)
        offset = 12 if (row // 8) % 2 == 0 else 0
        for vx in range(int(x_l) + offset, int(x_r), 24):
            c.line(vx, y_line, vx, y_line + 4)

    # === CORTEN STEEL FLOOR BANDS ===
    floor_ys = [65, 130]  # Floor 2 and 3 levels
    for fy in floor_ys:
        x_l = bx + (persp * fy / bh)
        x_r = bx + bw - (persp * fy / bh)
        # Main band
        c.setFillColor(HexColor('#8B4513'))
        c.rect(x_l, by + fy - 3, x_r - x_l, 7, fill=1, stroke=0)
        # Rust texture highlights
        c.setFillColor(HexColor('#A05A23'))
        c.rect(x_l + 20, by + fy - 2, 40, 3, fill=1, stroke=0)
        c.rect(x_l + 100, by + fy - 1, 60, 2, fill=1, stroke=0)
        c.rect(x_l + 200, by + fy - 2, 30, 4, fill=1, stroke=0)

    # === WINDOWS WITH DETAIL ===
    win_w = 48
    win_h = 45
    win_gap = 20

    for floor in range(3):
        floor_base = by + 8 + floor * 65
        p_off = persp * (floor_base - by) / bh

        for win in range(4):
            wx = bx + 22 + win * (win_w + win_gap) + p_off * 0.5
            wy = floor_base

            # Window reveal (deep shadow)
            c.setFillColor(HexColor('#2A2A2A'))
            c.rect(wx - 3, wy - 2, win_w + 6, win_h + 4, fill=1, stroke=0)

            # Black steel frame
            c.setFillColor(HexColor('#1A1A1A'))
            c.rect(wx, wy, win_w, win_h, fill=1, stroke=0)

            # Glass panes (4 panes per window)
            glass_w = (win_w - 6) / 2
            glass_h = (win_h - 6) / 2

            for gx in range(2):
                for gy in range(2):
                    gpx = wx + 2 + gx * (glass_w + 2)
                    gpy = wy + 2 + gy * (glass_h + 2)

                    # Base glass color (reflects sky)
                    if time_of_day == "dusk":
                        c.setFillColor(HexColor('#2A4A6A'))
                    else:
                        c.setFillColor(HexColor('#5A8AAA'))
                    c.rect(gpx, gpy, glass_w, glass_h, fill=1, stroke=0)

                    # Sky reflection gradient
                    c.setFillColor(Color(1, 0.7, 0.5, 0.25))
                    c.rect(gpx, gpy + glass_h * 0.6, glass_w, glass_h * 0.4, fill=1, stroke=0)

                    # Highlight reflection
                    c.setFillColor(Color(1, 1, 1, 0.15))
                    c.rect(gpx + 1, gpy + glass_h - 5, glass_w - 2, 3, fill=1, stroke=0)

            # Interior warm glow (lights on)
            if time_of_day == "dusk":
                c.setFillColor(Color(1, 0.9, 0.6, 0.2))
                c.rect(wx + 2, wy + 2, win_w - 4, win_h - 4, fill=1, stroke=0)

    # === BALCONIES WITH PERFORATED SCREENS ===
    balc_floors = [1, 2]  # Floors 2 and 3
    for bf in balc_floors:
        balc_y = by + 8 + bf * 65
        p_off = persp * (balc_y - by) / bh

        for bi in [1, 2]:  # Middle two windows get balconies
            bx_pos = bx + 22 + bi * (win_w + win_gap) + p_off * 0.5

            # Balcony floor
            c.setFillColor(HexColor('#4A4A4A'))
            c.rect(bx_pos - 5, balc_y - 8, win_w + 10, 6, fill=1, stroke=0)

            # Perforated metal screen railing
            c.setFillColor(HexColor('#3A3A3A'))
            c.rect(bx_pos - 5, balc_y - 8, 3, 20, fill=1, stroke=0)
            c.rect(bx_pos + win_w + 2, balc_y - 8, 3, 20, fill=1, stroke=0)

            # Perforations (dots pattern)
            c.setFillColor(HexColor('#5A5A5A'))
            for px in range(int(bx_pos), int(bx_pos + win_w), 6):
                for py in range(int(balc_y - 6), int(balc_y + 8), 5):
                    c.circle(px, py, 1, fill=1, stroke=0)

    # === ROOFTOP CROWN (Standing seam metal) ===
    crown_y = by + bh
    x_l = bx + persp - 3
    x_r = bx + bw - persp + 3

    # Crown fascia
    c.setFillColor(HexColor('#3A3A3A'))
    pts_crown = [
        (x_l, crown_y),
        (x_r, crown_y),
        (x_r - 2, crown_y + 15),
        (x_l + 2, crown_y + 15)
    ]
    p = c.beginPath()
    p.moveTo(pts_crown[0][0], pts_crown[0][1])
    for pt in pts_crown[1:]:
        p.lineTo(pt[0], pt[1])
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    # Standing seam ribs
    c.setStrokeColor(HexColor('#2A2A2A'))
    c.setLineWidth(1)
    for i in range(12):
        sx = x_l + 10 + i * 23
        c.line(sx, crown_y, sx, crown_y + 15)

    # === ROOFTOP TERRACE ===
    # Deck
    c.setFillColor(HexColor('#7A6350'))
    c.rect(x_l + 30, crown_y + 15, 140, 12, fill=1, stroke=0)

    # Deck boards
    c.setStrokeColor(HexColor('#6A5340'))
    c.setLineWidth(0.5)
    for dx in range(int(x_l + 30), int(x_l + 170), 8):
        c.line(dx, crown_y + 15, dx, crown_y + 27)

    # Glass railing
    c.setStrokeColor(HexColor('#1A1A1A'))
    c.setLineWidth(1.5)
    c.line(x_l + 28, crown_y + 27, x_l + 172, crown_y + 27)
    c.setFillColor(Color(0.7, 0.85, 0.95, 0.3))
    c.rect(x_l + 28, crown_y + 15, 144, 12, fill=1, stroke=0)

    # === PEOPLE ON ROOFTOP (detailed) ===
    # Person 1 - standing
    p1x = x_l + 60
    c.setFillColor(HexColor('#E8C4A0'))  # Skin
    c.circle(p1x, crown_y + 38, 4, fill=1, stroke=0)
    c.setFillColor(HexColor('#1A365D'))  # Blue shirt
    c.rect(p1x - 4, crown_y + 27, 8, 11, fill=1, stroke=0)
    c.setFillColor(HexColor('#2C2C2C'))  # Pants
    c.rect(p1x - 3, crown_y + 27, 3, 6, fill=1, stroke=0)
    c.rect(p1x, crown_y + 27, 3, 6, fill=1, stroke=0)

    # Person 2 - sitting
    p2x = x_l + 90
    c.setFillColor(HexColor('#D4A574'))  # Skin
    c.circle(p2x, crown_y + 33, 3.5, fill=1, stroke=0)
    c.setFillColor(HexColor('#C62828'))  # Red top
    c.rect(p2x - 3.5, crown_y + 27, 7, 6, fill=1, stroke=0)

    # Person 3 - leaning on rail
    p3x = x_l + 130
    c.setFillColor(HexColor('#E8C4A0'))
    c.circle(p3x, crown_y + 35, 3.5, fill=1, stroke=0)
    c.setFillColor(HexColor('#F5F5F5'))  # White shirt
    c.rect(p3x - 3.5, crown_y + 27, 7, 8, fill=1, stroke=0)

    # === GROUND FLOOR DETAIL ===
    # Foundation/base
    c.setFillColor(HexColor('#808080'))
    c.rect(bx - 2, by - 4, bw + 4, 6, fill=1, stroke=0)

    # MidFirst ATM Kiosk
    c.setFillColor(HexColor('#E8E8E8'))
    c.rect(bx + 15, by, 70, 55, fill=1, stroke=0)
    # ATM glass
    c.setFillColor(HexColor('#4A7AB0'))
    c.rect(bx + 20, by + 10, 25, 35, fill=1, stroke=0)
    # MidFirst logo area
    c.setFillColor(HexColor('#1A365D'))
    c.rect(bx + 18, by + 48, 50, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 5)
    c.drawString(bx + 22, by + 50, "MidFirst Bank")

    # Main Entry
    c.setFillColor(HexColor('#2A2A2A'))
    c.rect(bx + 120, by, 45, 55, fill=1, stroke=0)
    # Entry glass doors
    c.setFillColor(HexColor('#3A5A7A'))
    c.rect(bx + 123, by + 3, 18, 49, fill=1, stroke=0)
    c.rect(bx + 144, by + 3, 18, 49, fill=1, stroke=0)
    # Door handles
    c.setFillColor(HexColor('#C9A227'))
    c.rect(bx + 139, by + 25, 2, 10, fill=1, stroke=0)
    c.rect(bx + 144, by + 25, 2, 10, fill=1, stroke=0)

    # Parking garage entry (right side)
    c.setFillColor(HexColor('#1A1A1A'))
    c.rect(bx + 200, by, 60, 45, fill=1, stroke=0)
    c.setFillColor(HexColor('#2A2A2A'))
    c.rect(bx + 205, by + 5, 50, 35, fill=1, stroke=0)

    # === BUILDING SIGNAGE ===
    # Illuminated LUXX LOFTS sign
    c.setFillColor(HexColor('#C9A227'))
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(bx + bw/2, by + bh - 20, "LUXX LOFTS")
    # Glow effect
    c.setFillColor(Color(0.8, 0.65, 0.15, 0.3))
    c.rect(bx + bw/2 - 55, by + bh - 28, 110, 20, fill=1, stroke=0)

    # === LANDSCAPING ===
    # Large planters
    c.setFillColor(HexColor('#4A4A4A'))
    c.rect(bx - 8, by - 8, 20, 15, fill=1, stroke=0)
    c.rect(bx + bw - 12, by - 8, 20, 15, fill=1, stroke=0)

    # Ornamental grasses
    c.setFillColor(HexColor('#4A7A3A'))
    for i in range(5):
        c.ellipse(bx - 5 + i*3, by + 5, bx + i*3, by + 18, fill=1, stroke=0)
        c.ellipse(bx + bw - 9 + i*3, by + 5, bx + bw - 6 + i*3, by + 18, fill=1, stroke=0)

    # Small tree
    c.setFillColor(HexColor('#5A3A2A'))
    c.rect(bx + bw + 25, by - 5, 4, 35, fill=1, stroke=0)
    c.setFillColor(HexColor('#2E5A1E'))
    c.circle(bx + bw + 27, by + 40, 18, fill=1, stroke=0)
    c.setFillColor(HexColor('#3A6A2A'))
    c.circle(bx + bw + 22, by + 35, 12, fill=1, stroke=0)
    c.circle(bx + bw + 32, by + 38, 10, fill=1, stroke=0)

    # === STREET FURNITURE ===
    # Modern street lamp
    c.setFillColor(HexColor('#2A2A2A'))
    c.rect(bx - 35, 22, 4, 85, fill=1, stroke=0)
    # Lamp arm
    c.rect(bx - 35, 105, 20, 3, fill=1, stroke=0)
    # Light fixture
    c.setFillColor(HexColor('#FFE082'))
    c.ellipse(bx - 20, 100, bx - 8, 110, fill=1, stroke=0)
    # Light glow
    c.setFillColor(Color(1, 0.95, 0.7, 0.25))
    c.circle(bx - 14, 105, 20, fill=1, stroke=0)

    # Parked car (more detailed)
    car_x = bx + bw + 50
    c.setFillColor(HexColor('#2A3A4A'))
    # Body
    c.roundRect(car_x, 2, 55, 20, 3, fill=1, stroke=0)
    # Cabin
    c.setFillColor(HexColor('#3A4A5A'))
    c.roundRect(car_x + 10, 18, 35, 14, 4, fill=1, stroke=0)
    # Windows
    c.setFillColor(HexColor('#5A7A9A'))
    c.rect(car_x + 13, 20, 14, 10, fill=1, stroke=0)
    c.rect(car_x + 29, 20, 14, 10, fill=1, stroke=0)
    # Wheels
    c.setFillColor(HexColor('#1A1A1A'))
    c.circle(car_x + 12, 4, 6, fill=1, stroke=0)
    c.circle(car_x + 43, 4, 6, fill=1, stroke=0)
    # Hubcaps
    c.setFillColor(HexColor('#606060'))
    c.circle(car_x + 12, 4, 3, fill=1, stroke=0)
    c.circle(car_x + 43, 4, 3, fill=1, stroke=0)

    # === GROUND SHADOWS ===
    c.setFillColor(Color(0, 0, 0, 0.15))
    # Building shadow
    pts_shadow = [
        (bx - 18, by - 5),
        (bx - 40, 22),
        (bx + 60, 22),
        (bx, by - 5)
    ]
    p = c.beginPath()
    p.moveTo(pts_shadow[0][0], pts_shadow[0][1])
    for pt in pts_shadow[1:]:
        p.lineTo(pt[0], pt[1])
    p.close()
    c.drawPath(p, fill=1, stroke=0)

    c.restoreState()


def draw_rendering_page(c, page_w, page_h):
    """Full page sophisticated rendering with large De Loera header"""
    # Light cream background
    c.setFillColor(HexColor('#F8F6F0'))
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # === LARGE DE LOERA DEVELOPMENT HEADER ===
    # Dark header bar
    c.setFillColor(LUXX_DARK)
    c.rect(0, page_h - 90, page_w, 90, fill=1, stroke=0)

    # Gold accent line
    c.setFillColor(LUXX_GOLD)
    c.rect(0, page_h - 93, page_w, 3, fill=1, stroke=0)

    # Oklahoma State Seal on left side of header
    draw_oklahoma_state_seal(c, 85, page_h - 45, scale=0.75)

    # Large company name
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 36)
    c.drawCentredString(page_w/2, page_h - 50, "DE LOERA DEVELOPMENT")

    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_w/2, page_h - 72, "ERIC DE LOERA  •  PRINCIPAL")

    # OKC City Seal on right side of header
    draw_okc_city_seal(c, page_w - 90, page_h - 45, scale=0.85)

    # === RENDERING TITLE ===
    c.setFillColor(LUXX_DARK)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_w/2, page_h - 120, "ARCHITECTURAL RENDERING")

    c.setFillColor(MED_GRAY)
    c.setFont("Helvetica", 11)
    c.drawCentredString(page_w/2, page_h - 138, "View from N. Blackwelder Avenue  •  Facing South  •  Dusk")

    # === MAIN RENDERING ===
    # Rendering frame
    render_x = 60
    render_y = 100
    render_w = page_w - 120
    render_h = page_h - 270

    # Frame border with double line
    c.setStrokeColor(LUXX_DARK)
    c.setLineWidth(3)
    c.rect(render_x - 8, render_y - 8, render_w + 16, render_h + 16, fill=0, stroke=1)
    c.setLineWidth(1)
    c.rect(render_x - 3, render_y - 3, render_w + 6, render_h + 6, fill=0, stroke=1)

    # Draw the building rendering
    draw_building_rendering(c, render_x, render_y, render_w, render_h, "dusk")

    # === FOOTER WITH STAMPS ===
    # Footer background bar
    c.setFillColor(HexColor('#F0EDE5'))
    c.rect(0, 0, page_w, 95, fill=1, stroke=0)
    c.setFillColor(LUXX_DARK)
    c.rect(0, 93, page_w, 2, fill=1, stroke=0)

    # Oklahoma State Seal (bottom left)
    draw_oklahoma_state_seal(c, 75, 50, scale=0.7)

    # Center info
    c.setFillColor(LUXX_DARK)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w/2, 68, "LUXX LOFTS")

    c.setFont("Helvetica", 11)
    c.drawCentredString(page_w/2, 52, "4801 N. BLACKWELDER AVE  •  OKLAHOMA CITY, OK 73118")

    c.setFillColor(MED_GRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(page_w/2, 36, "12 Contemporary Loft Units  •  Golden Ratio Design (φ = 1.618)  •  MidFirst ATM Anchor")

    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, 20, "LUXX BUILDZ Constructor  •  OKC Moving Forward Initiative")

    # OKC City Seal (bottom right)
    draw_okc_city_seal(c, page_w - 80, 50, scale=0.9)

    # Fine print copyright
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 5)
    c.drawCentredString(page_w/2, 5, "© 2024 Eric De Loera | De Loera Development | All Rights Reserved | Unauthorized reproduction prohibited")


def draw_investor_cover(c, page_w, page_h):
    """Investor package cover page"""
    # Dark sophisticated background
    c.setFillColor(LUXX_DARK)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # === LARGE DE LOERA DEVELOPMENT HEADER ===
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(page_w/2, page_h - 45, "DE LOERA DEVELOPMENT")

    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, page_h - 65, "ERIC DE LOERA  •  PRINCIPAL")

    # Gold accent bar
    c.setFillColor(LUXX_GOLD)
    c.rect(0, page_h * 0.48, page_w, 8, fill=1, stroke=0)

    # Title
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 52)
    c.drawCentredString(page_w/2, page_h * 0.62, "LUXX LOFTS")

    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica", 16)
    c.drawCentredString(page_w/2, page_h * 0.54, "INVESTMENT OPPORTUNITY")

    c.setFillColor(white)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, page_h * 0.42, "4801 N. BLACKWELDER AVENUE  |  OKLAHOMA CITY, OK 73118")

    # Key stats boxes
    box_y = page_h * 0.20
    box_h = 55
    box_w = 140
    boxes = [
        ("$1.99M", "Total Project Cost"),
        ("$241K", "Annual Revenue"),
        ("$178K", "Net Operating Income"),
        ("8.9%", "Cash-on-Cash Return"),
    ]

    start_x = (page_w - (4 * box_w + 3 * 20)) / 2
    for i, (value, label) in enumerate(boxes):
        bx = start_x + i * (box_w + 20)

        c.setFillColor(Color(1, 1, 1, 0.1))
        c.rect(bx, box_y, box_w, box_h, fill=1, stroke=0)

        c.setFillColor(LUXX_GOLD)
        c.setFont("Helvetica-Bold", 22)
        c.drawCentredString(bx + box_w/2, box_y + 32, value)

        c.setFillColor(white)
        c.setFont("Helvetica", 9)
        c.drawCentredString(bx + box_w/2, box_y + 12, label)

    # Footer with Eric De Loera
    c.setFillColor(MED_GRAY)
    c.setFont("Helvetica", 9)
    c.drawCentredString(page_w/2, 55, "Presented by ERIC DE LOERA")
    c.drawCentredString(page_w/2, 42, "DE LOERA DEVELOPMENT  |  LUXX BUILDZ  |  CONFIDENTIAL")
    c.drawCentredString(page_w/2, 29, f"Prepared {datetime.now().strftime('%B %Y')}")

    # Fine print copyright
    c.setFillColor(DARK_GRAY)
    c.setFont("Helvetica", 5)
    c.drawCentredString(page_w/2, 12, "© 2024 Eric De Loera | De Loera Development | All Rights Reserved | Unauthorized reproduction prohibited")


def draw_executive_summary(c, page_w, page_h):
    """Executive summary page"""
    margin = 50

    # Header
    c.setFillColor(NAVY)
    c.rect(0, page_h - 70, page_w, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, page_h - 45, "EXECUTIVE SUMMARY")

    y = page_h - 110

    # Investment Overview
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "INVESTMENT OVERVIEW")

    y -= 25
    c.setFont("Helvetica", 10)
    overview = [
        "LUXX LOFTS is a 12-unit mixed-use residential development located at a prime corner lot in",
        "Oklahoma City's rapidly growing Northwest corridor. The project features contemporary industrial",
        "design with golden ratio proportions, premium finishes, and ground-floor commercial space leased",
        "to MidFirst Bank for an ATM kiosk, providing stable anchor income."
    ]
    for line in overview:
        c.drawString(margin, y, line)
        y -= 14

    # Two column layout
    col1_x = margin
    col2_x = page_w/2 + 20
    y -= 20

    # Left column - Property Details
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col1_x, y, "PROPERTY DETAILS")

    y -= 20
    c.setFont("Helvetica", 9)
    details = [
        ("Address:", "4801 N Blackwelder Ave, OKC 73118"),
        ("Lot Size:", "7,930 SF (61' × 130')"),
        ("Building Size:", "14,685 GSF"),
        ("Stories:", "3"),
        ("Unit Count:", "12 residential + 1 commercial"),
        ("Parking:", "18 spaces (12 covered + 6 surface)"),
        ("Year Built:", "2025 (Proposed)"),
        ("Construction:", "Type V-A, Fully Sprinklered"),
        ("Zoning:", "Mixed-Use Commercial"),
    ]

    for label, val in details:
        c.setFont("Helvetica", 9)
        c.drawString(col1_x, y, label)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(col1_x + 90, y, val)
        y -= 14

    # Right column - Financial Summary
    y_right = page_h - 200
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col2_x, y_right, "FINANCIAL SUMMARY")

    y_right -= 20
    financials = [
        ("Total Development Cost:", "$1,988,140"),
        ("Annual Gross Revenue:", "$241,200"),
        ("Operating Expenses:", "$62,716"),
        ("Net Operating Income:", "$178,484"),
        ("Cap Rate:", "8.97%"),
        ("Cash-on-Cash (Year 1):", "8.9%"),
        ("Debt Service Coverage:", "1.45x"),
        ("Break-Even Occupancy:", "72%"),
        ("Stabilized Value (7% Cap):", "$2,549,771"),
    ]

    for label, val in financials:
        c.setFont("Helvetica", 9)
        c.drawString(col2_x, y_right, label)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(col2_x + 140, y_right, val)
        y_right -= 14

    # Investment Highlights Box
    y = min(y, y_right) - 30

    c.setFillColor(HexColor('#E8F5E9'))
    c.rect(margin, y - 80, page_w - 2*margin, 85, fill=1, stroke=0)

    c.setFillColor(FOREST_GREEN)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin + 15, y - 5, "INVESTMENT HIGHLIGHTS")

    c.setFillColor(BLACK)
    c.setFont("Helvetica", 9)
    highlights = [
        "✓  Prime corner location near NW Expressway & Classen Blvd retail corridor",
        "✓  New shopping center under construction directly across the street",
        "✓  MidFirst Bank ATM provides stable anchor tenant income ($30,000/year)",
        "✓  Golden Ratio design (φ = 1.618) maximizes space efficiency and aesthetic appeal",
        "✓  Builder/Developer self-performing saves ~$150,000 in GC overhead",
    ]

    hy = y - 22
    for h in highlights:
        c.drawString(margin + 15, hy, h)
        hy -= 14


def draw_financial_projections(c, page_w, page_h):
    """5-year financial projections"""
    margin = 50

    # Header
    c.setFillColor(NAVY)
    c.rect(0, page_h - 70, page_w, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, page_h - 45, "FINANCIAL PROJECTIONS")

    y = page_h - 110

    # Revenue Table
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "5-YEAR PRO FORMA (3% Annual Rent Growth)")

    y -= 25

    # Table headers
    headers = ["", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    col_widths = [180, 85, 85, 85, 85, 85]
    col_x = [margin]
    for w in col_widths[:-1]:
        col_x.append(col_x[-1] + w)

    c.setFillColor(NAVY)
    c.rect(margin, y - 5, sum(col_widths), 20, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    for i, h in enumerate(headers):
        c.drawString(col_x[i] + 5, y, h)

    y -= 25
    c.setFillColor(BLACK)

    # Financial rows
    rows = [
        ("Gross Rental Income", "$241,200", "$248,436", "$255,889", "$263,566", "$271,473"),
        ("Less: Vacancy (5%)", "($12,060)", "($12,422)", "($12,794)", "($13,178)", "($13,574)"),
        ("Effective Gross Income", "$229,140", "$236,014", "$243,095", "$250,388", "$257,899"),
        ("", "", "", "", "", ""),
        ("Operating Expenses:", "", "", "", "", ""),
        ("  Property Tax", "$8,500", "$8,755", "$9,018", "$9,288", "$9,567"),
        ("  Insurance", "$6,000", "$6,180", "$6,365", "$6,556", "$6,753"),
        ("  Maintenance", "$12,060", "$12,422", "$12,794", "$13,178", "$13,574"),
        ("  Management (8%)", "$18,331", "$18,881", "$19,448", "$20,031", "$20,632"),
        ("  Utilities", "$4,800", "$4,944", "$5,092", "$5,245", "$5,402"),
        ("Total Expenses", "$49,691", "$51,182", "$52,717", "$54,298", "$55,928"),
        ("", "", "", "", "", ""),
        ("NET OPERATING INCOME", "$179,449", "$184,832", "$190,378", "$196,090", "$201,971"),
    ]

    c.setFont("Helvetica", 9)
    for row in rows:
        if row[0] == "NET OPERATING INCOME":
            c.setFillColor(HexColor('#E8F5E9'))
            c.rect(margin, y - 4, sum(col_widths), 16, fill=1, stroke=0)
            c.setFillColor(FOREST_GREEN)
            c.setFont("Helvetica-Bold", 9)
        elif row[0] == "":
            y -= 8
            continue
        elif ":" in row[0]:
            c.setFont("Helvetica-Bold", 9)
            c.setFillColor(BLACK)
        else:
            c.setFont("Helvetica", 9)
            c.setFillColor(BLACK)

        for i, val in enumerate(row):
            c.drawString(col_x[i] + 5, y, val)
        y -= 15

    # Returns Analysis
    y -= 25
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "RETURNS ANALYSIS")

    y -= 20

    # Assuming 75% LTV financing
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "Financing Assumptions:")
    c.setFont("Helvetica", 9)
    c.drawString(margin + 140, y, "75% LTV  |  7.5% Interest  |  25-Year Amortization  |  Loan Amount: $1,491,105")

    y -= 25

    returns_headers = ["", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5"]
    c.setFillColor(NAVY)
    c.rect(margin, y - 5, sum(col_widths), 20, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    for i, h in enumerate(returns_headers):
        c.drawString(col_x[i] + 5, y, h)

    y -= 25
    c.setFillColor(BLACK)

    returns_rows = [
        ("NOI", "$179,449", "$184,832", "$190,378", "$196,090", "$201,971"),
        ("Debt Service", "($131,124)", "($131,124)", "($131,124)", "($131,124)", "($131,124)"),
        ("Cash Flow Before Tax", "$48,325", "$53,708", "$59,254", "$64,966", "$70,847"),
        ("Cash-on-Cash Return", "9.7%", "10.8%", "11.9%", "13.1%", "14.3%"),
    ]

    for row in returns_rows:
        if "Return" in row[0]:
            c.setFillColor(HexColor('#FFF3E0'))
            c.rect(margin, y - 4, sum(col_widths), 16, fill=1, stroke=0)
            c.setFillColor(ACCENT_ORANGE)
            c.setFont("Helvetica-Bold", 9)
        else:
            c.setFont("Helvetica", 9)
            c.setFillColor(BLACK)

        for i, val in enumerate(row):
            c.drawString(col_x[i] + 5, y, val)
        y -= 15


def draw_construction_budget(c, page_w, page_h):
    """Construction budget summary for investors"""
    margin = 50

    # Header
    c.setFillColor(NAVY)
    c.rect(0, page_h - 70, page_w, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, page_h - 45, "CONSTRUCTION BUDGET")

    y = page_h - 110

    # Two column layout
    col1_x = margin
    col2_x = page_w/2 + 30

    # Left column - Budget breakdown
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col1_x, y, "DEVELOPMENT BUDGET")

    y -= 22

    budget_items = [
        ("HARD COSTS", "", True),
        ("Site Work & Demolition", "$45,000"),
        ("Foundation", "$102,000"),
        ("Concrete & Masonry", "$250,000"),
        ("Structural Framing", "$168,000"),
        ("Plumbing", "$132,000"),
        ("Electrical", "$100,000"),
        ("HVAC", "$80,000"),
        ("Roofing", "$92,000"),
        ("Exterior Finishes", "$144,000"),
        ("Interior Finishes", "$261,000"),
        ("Appliances & Fixtures", "$68,500"),
        ("Fire Protection", "$51,800"),
        ("Elevator", "$85,000"),
        ("Site Improvements", "$76,000"),
        ("Subtotal Hard Costs", "$1,655,300", True),
        ("", ""),
        ("SOFT COSTS", "", True),
        ("Permits & Fees", "$33,400"),
        ("Architectural/Engineering", "$65,000"),
        ("Insurance", "$18,000"),
        ("Legal & Accounting", "$8,000"),
        ("Testing & Inspections", "$12,000"),
        ("Subtotal Soft Costs", "$136,400", True),
        ("", ""),
        ("Contingency (10%)", "$180,740"),
        ("", ""),
        ("TOTAL PROJECT COST", "$1,988,140", True),
    ]

    for item in budget_items:
        if len(item) == 2:
            label, val = item
            is_bold = False
        else:
            label, val, is_bold = item

        if label == "":
            y -= 8
            continue

        if is_bold:
            c.setFont("Helvetica-Bold", 9)
            if "TOTAL" in label:
                c.setFillColor(HexColor('#E8F5E9'))
                c.rect(col1_x - 5, y - 4, 250, 16, fill=1, stroke=0)
                c.setFillColor(FOREST_GREEN)
        else:
            c.setFont("Helvetica", 9)
            c.setFillColor(BLACK)

        c.drawString(col1_x, y, label)
        if val:
            c.drawRightString(col1_x + 240, y, val)
        y -= 14

    # Right column - Sources & Uses
    y_right = page_h - 110

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(col2_x, y_right, "SOURCES & USES")

    y_right -= 22

    c.setFont("Helvetica-Bold", 10)
    c.drawString(col2_x, y_right, "SOURCES OF FUNDS")
    y_right -= 18

    sources = [
        ("Construction Loan (75% LTV)", "$1,491,105"),
        ("Developer Equity", "$497,035"),
        ("Total Sources", "$1,988,140"),
    ]

    for label, val in sources:
        if "Total" in label:
            c.setFont("Helvetica-Bold", 9)
        else:
            c.setFont("Helvetica", 9)
        c.drawString(col2_x, y_right, label)
        c.drawRightString(col2_x + 200, y_right, val)
        y_right -= 14

    y_right -= 15
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col2_x, y_right, "USES OF FUNDS")
    y_right -= 18

    uses = [
        ("Land Acquisition", "$140,000"),
        ("Hard Costs", "$1,655,300"),
        ("Soft Costs", "$136,400"),
        ("Contingency", "$180,740"),
        ("Financing Costs", "$45,000"),
        ("Operating Reserve", "$30,700"),
        ("Total Uses", "$1,988,140"),
    ]

    for label, val in uses:
        if "Total" in label:
            c.setFont("Helvetica-Bold", 9)
        else:
            c.setFont("Helvetica", 9)
        c.drawString(col2_x, y_right, label)
        c.drawRightString(col2_x + 200, y_right, val)
        y_right -= 14

    # Builder advantage box
    y_right -= 25
    c.setFillColor(HexColor('#E3F2FD'))
    c.rect(col2_x - 10, y_right - 60, 230, 75, fill=1, stroke=0)

    c.setFillColor(HexColor('#1565C0'))
    c.setFont("Helvetica-Bold", 10)
    c.drawString(col2_x, y_right, "BUILDER ADVANTAGE")

    c.setFont("Helvetica", 8)
    c.setFillColor(BLACK)
    advantage = [
        "Developer holds General Contractor",
        "and Roofing licenses, enabling:",
        "",
        "• Self-performance of key trades",
        "• ~$150,000 GC overhead savings",
        "• Direct quality control",
        "• Accelerated schedule",
    ]

    y_right -= 14
    for line in advantage:
        c.drawString(col2_x, y_right, line)
        y_right -= 13


def draw_risk_analysis(c, page_w, page_h):
    """Risk analysis and mitigation"""
    margin = 50

    # Header
    c.setFillColor(NAVY)
    c.rect(0, page_h - 70, page_w, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, page_h - 45, "RISK ANALYSIS & MITIGATION")

    y = page_h - 110

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "RISK FACTORS & MITIGATION STRATEGIES")

    y -= 25

    risks = [
        ("Construction Risk", "MEDIUM",
         "Cost overruns, delays, material shortages",
         ["10% contingency built into budget",
          "Developer is licensed GC with proven track record",
          "Fixed-price subcontracts for major trades",
          "Material costs locked at contract signing"]),

        ("Market/Leasing Risk", "LOW-MEDIUM",
         "Vacancy, rental rate pressure",
         ["OKC multifamily vacancy at historic low (4.2%)",
          "Location near major retail development",
          "Unit sizes optimized for highest-demand segment",
          "Pre-leasing to begin 90 days before completion"]),

        ("Interest Rate Risk", "MEDIUM",
         "Rising rates affect refinancing",
         ["Conservative 7.5% rate assumption",
          "Strong DSCR (1.45x) provides cushion",
          "Option to lock permanent financing early",
          "Project cash flows at higher rate scenarios"]),

        ("Regulatory Risk", "LOW",
         "Zoning, permitting delays",
         ["Site is properly zoned for mixed-use",
          "All required variances are minor (1.7% coverage)",
          "Pre-application meetings completed with OKC",
          "Experienced permit expediter engaged"]),
    ]

    for risk_name, level, description, mitigations in risks:
        # Risk header
        c.setFont("Helvetica-Bold", 10)
        c.setFillColor(BLACK)
        c.drawString(margin, y, risk_name)

        # Risk level badge
        if level == "LOW":
            badge_color = FOREST_GREEN
        elif level == "LOW-MEDIUM":
            badge_color = HexColor('#FF9800')
        else:
            badge_color = ACCENT_ORANGE

        c.setFillColor(badge_color)
        c.rect(margin + 150, y - 2, 60, 14, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(margin + 180, y + 1, level)

        y -= 16
        c.setFillColor(MED_GRAY)
        c.setFont("Helvetica-Oblique", 9)
        c.drawString(margin + 10, y, description)

        y -= 14
        c.setFillColor(BLACK)
        c.setFont("Helvetica", 9)
        for mit in mitigations:
            c.drawString(margin + 20, y, "• " + mit)
            y -= 14

        y -= 15

    # Sensitivity Analysis
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "SENSITIVITY ANALYSIS")

    y -= 20

    c.setFillColor(NAVY)
    c.rect(margin, y - 5, 450, 20, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    headers = ["Scenario", "Occupancy", "NOI", "DSCR", "Cash-on-Cash"]
    hx = [margin + 10, margin + 120, margin + 200, margin + 290, margin + 370]
    for i, h in enumerate(headers):
        c.drawString(hx[i], y, h)

    y -= 22
    c.setFillColor(BLACK)

    scenarios = [
        ("Base Case", "95%", "$178,484", "1.45x", "9.7%"),
        ("Conservative", "90%", "$166,200", "1.35x", "7.1%"),
        ("Downside", "85%", "$153,900", "1.25x", "4.6%"),
        ("Break-Even", "72%", "$131,124", "1.00x", "0.0%"),
    ]

    for scenario in scenarios:
        c.setFont("Helvetica", 9)
        for i, val in enumerate(scenario):
            c.drawString(hx[i], y, val)
        y -= 14


def draw_exit_strategy(c, page_w, page_h):
    """Exit strategy page"""
    margin = 50

    # Header
    c.setFillColor(NAVY)
    c.rect(0, page_h - 70, page_w, 70, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(margin, page_h - 45, "EXIT STRATEGY & RETURNS")

    y = page_h - 110

    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "EXIT OPTIONS")

    y -= 25

    exits = [
        ("HOLD & CASH FLOW",
         "Maintain ownership and collect rental income. Strong cash-on-cash returns (9.7%+ Year 1) "
         "provide attractive ongoing income with 3% annual rent growth. Ideal for long-term wealth building."),

        ("REFINANCE (Year 3-5)",
         "Refinance at stabilized value to return equity while maintaining ownership. At Year 5 NOI of "
         "$202K and 7% cap rate, property value reaches $2.88M. 75% LTV refinance returns ~$650K to investors."),

        ("SALE (Year 5-7)",
         "Sell to institutional buyer or 1031 exchange investor. OKC multifamily cap rates currently "
         "6.5-7.5%. Conservative 7% exit cap on Year 5 NOI yields $2.88M sale price, 45% total return."),
    ]

    for title, desc in exits:
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin, y, title)
        y -= 14

        c.setFont("Helvetica", 9)
        # Word wrap description
        words = desc.split()
        line = ""
        for word in words:
            test_line = line + word + " "
            if len(test_line) > 95:
                c.drawString(margin + 15, y, line)
                y -= 12
                line = word + " "
            else:
                line = test_line
        c.drawString(margin + 15, y, line)
        y -= 25

    # Value Projection
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "PROJECTED VALUE & RETURNS")

    y -= 25

    c.setFillColor(NAVY)
    c.rect(margin, y - 5, 500, 20, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 9)
    val_headers = ["", "Year 1", "Year 3", "Year 5", "Year 7"]
    vx = [margin + 10, margin + 140, margin + 230, margin + 320, margin + 410]
    for i, h in enumerate(val_headers):
        c.drawString(vx[i], y, h)

    y -= 22
    c.setFillColor(BLACK)

    projections = [
        ("NOI", "$179,449", "$190,378", "$201,971", "$214,261"),
        ("Value (7% Cap)", "$2,563,557", "$2,719,686", "$2,885,300", "$3,060,871"),
        ("Equity (75% LTV)", "$640,889", "$679,921", "$721,325", "$765,218"),
        ("Total Return", "29%", "61%", "98%", "141%"),
        ("IRR", "29%", "22%", "19%", "17%"),
    ]

    for row in projections:
        if "Return" in row[0] or "IRR" in row[0]:
            c.setFillColor(HexColor('#E8F5E9'))
            c.rect(margin, y - 4, 500, 16, fill=1, stroke=0)
            c.setFillColor(FOREST_GREEN)
            c.setFont("Helvetica-Bold", 9)
        else:
            c.setFillColor(BLACK)
            c.setFont("Helvetica", 9)

        for i, val in enumerate(row):
            c.drawString(vx[i], y, val)
        y -= 16

    # Call to Action
    y -= 30
    c.setFillColor(LUXX_GOLD)
    c.rect(margin, y - 50, page_w - 2*margin, 60, fill=1, stroke=0)

    c.setFillColor(LUXX_DARK)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, y - 8, "INVESTMENT OPPORTUNITY")
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, y - 28, "Minimum Investment: $50,000  |  Target Close: Q1 2025")
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(page_w/2, y - 43, "Contact: De Loera Development  |  luxx.okc@gmail.com")


# ============ TENANT MARKETING DOCUMENT ============

def draw_tenant_cover(c, page_w, page_h):
    """Tenant marketing cover"""
    # Warm gradient background
    for i in range(50):
        ratio = i / 50
        r = int(245 - (245 - 26) * ratio * 0.3)
        g = int(240 - (240 - 26) * ratio * 0.3)
        b = int(230 - (230 - 26) * ratio * 0.3)
        c.setFillColor(Color(r/255, g/255, b/255))
        c.rect(0, page_h * (50 - i) / 50, page_w, page_h / 50 + 1, fill=1, stroke=0)

    # Dark bottom section
    c.setFillColor(LUXX_DARK)
    c.rect(0, 0, page_w, page_h * 0.35, fill=1, stroke=0)

    # Gold accent line
    c.setFillColor(LUXX_GOLD)
    c.rect(0, page_h * 0.35, page_w, 6, fill=1, stroke=0)

    # Logo at top
    draw_deloera_logo(c, page_w/2, page_h - 50, scale=0.7, color_scheme="dark")

    # Title
    c.setFillColor(LUXX_DARK)
    c.setFont("Helvetica-Bold", 56)
    c.drawCentredString(page_w/2, page_h * 0.55, "LUXX LOFTS")

    c.setFillColor(BRICK_HONEY)
    c.setFont("Helvetica", 18)
    c.drawCentredString(page_w/2, page_h * 0.47, "CONTEMPORARY URBAN LIVING")

    # Tagline
    c.setFillColor(white)
    c.setFont("Helvetica-Oblique", 14)
    c.drawCentredString(page_w/2, page_h * 0.22, "\"Where industrial heritage meets modern sophistication\"")

    # Location
    c.setFont("Helvetica", 11)
    c.drawCentredString(page_w/2, page_h * 0.14, "4801 N. BLACKWELDER  |  OKLAHOMA CITY")

    # Coming Soon
    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w/2, page_h * 0.06, "NOW PRE-LEASING  |  MOVE-IN READY 2025")

    # Fine print copyright
    c.setFillColor(MED_GRAY)
    c.setFont("Helvetica", 5)
    c.drawCentredString(page_w/2, 10, "© 2024 Eric De Loera | De Loera Development | All Rights Reserved | Unauthorized reproduction prohibited")


def draw_lifestyle_page(c, page_w, page_h):
    """Lifestyle and design page"""
    margin = 50

    # Header
    c.setFillColor(LUXX_DARK)
    c.rect(0, page_h - 80, page_w, 80, fill=1, stroke=0)
    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_w/2, page_h - 50, "THE LUXX LIFESTYLE")

    y = page_h - 120

    # Design Philosophy
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "DESIGN PHILOSOPHY")

    y -= 20
    c.setFont("Helvetica", 10)
    philosophy = [
        "LUXX LOFTS draws inspiration from Oklahoma's industrial brick heritage and the bold geometric",
        "confidence of Mexico City's Condesa district. The result is a building that feels both rooted in",
        "place and refreshingly contemporary—warm honey-gold masonry, weathered steel accents, and",
        "floor-to-ceiling windows that flood each unit with natural light."
    ]
    for line in philosophy:
        c.drawString(margin, y, line)
        y -= 14

    y -= 20

    # Features in columns
    col1_x = margin
    col2_x = page_w/2 + 20

    # Left column
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(BRICK_HONEY)
    c.drawString(col1_x, y, "ARCHITECTURAL DETAILS")

    y -= 18
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 9)
    arch_features = [
        "• Honey-gold Norman brick facade",
        "• Corten steel lintels & accents",
        "• Standing-seam metal crown",
        "• Black powder-coated steel frames",
        "• Terracotta red staircase (visible at dusk)",
        "• Perforated metal balcony screens",
        "• Deep window reveals for drama",
        "• Golden Ratio proportions (φ = 1.618)",
    ]
    for f in arch_features:
        c.drawString(col1_x, y, f)
        y -= 13

    y -= 15
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(BRICK_HONEY)
    c.drawString(col1_x, y, "INTERIOR FINISHES")

    y -= 18
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 9)
    interior = [
        "• Polished concrete floors",
        "• 10'-11' ceiling heights",
        "• Floor-to-ceiling windows",
        "• Quartz countertops",
        "• Stainless steel appliances",
        "• Custom cabinetry",
        "• Frameless glass showers",
        "• USB outlets throughout",
    ]
    for f in interior:
        c.drawString(col1_x, y, f)
        y -= 13

    # Right column
    y_right = page_h - 175

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(BRICK_HONEY)
    c.drawString(col2_x, y_right, "BUILDING AMENITIES")

    y_right -= 18
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 9)
    amenities = [
        "• Covered parking (1 space/unit)",
        "• Rooftop terraces with city views",
        "• Secure building entry",
        "• Package lockers",
        "• Bike storage",
        "• On-site MidFirst ATM",
        "• Pet-friendly policy",
        "• High-speed internet ready",
    ]
    for f in amenities:
        c.drawString(col2_x, y_right, f)
        y_right -= 13

    y_right -= 15
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(BRICK_HONEY)
    c.drawString(col2_x, y_right, "NEIGHBORHOOD")

    y_right -= 18
    c.setFillColor(BLACK)
    c.setFont("Helvetica", 9)
    neighborhood = [
        "• Steps from NW Expressway retail",
        "• New shopping center across street",
        "• 10 min to Classen Curve",
        "• 15 min to Downtown OKC",
        "• Near Mercy Hospital",
        "• Lake Hefner 5 minutes away",
        "• Excellent school district",
        "• Low crime neighborhood",
    ]
    for f in neighborhood:
        c.drawString(col2_x, y_right, f)
        y_right -= 13


def draw_unit_options(c, page_w, page_h):
    """Unit types and pricing - Minimalist Golden Ratio Design"""
    margin = 45

    # Clean warm background
    c.setFillColor(WARM_WHITE)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    # Elegant header with gold accent
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 70, page_w, 70, fill=1, stroke=0)
    c.setFillColor(LUXX_GOLD)
    c.rect(0, page_h - 73, page_w, 3, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, page_h - 30, "LUXX LOFTS")

    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 26)
    c.drawCentredString(page_w/2, page_h - 45, "MINIMALIST URBAN LIVING")

    c.setFillColor(white)
    c.setFont("Helvetica", 10)
    c.drawRightString(page_w - margin, page_h - 30, "OKC's Best Value")

    # === VALUE PROPOSITION BANNER ===
    y = page_h - 95

    c.setFillColor(LUXX_GOLD)
    c.rect(margin, y - 35, page_w - 2*margin, 40, fill=1, stroke=0)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, y - 12, "CENTRALIZED  •  MINIMALIST  •  AFFORDABLE")

    c.setFont("Helvetica", 9)
    c.drawCentredString(page_w/2, y - 28, "Premium downtown-adjacent living at 30% below comparable OKC lofts")

    # === COST COMPARISON ===
    y -= 60

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "WHY LUXX LOFTS IS OKC'S BEST VALUE")

    y -= 20

    # Comparison table
    c.setFillColor(CHARCOAL)
    c.rect(margin, y - 55, page_w - 2*margin, 60, fill=1, stroke=0)

    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 9)
    headers = ["LOCATION", "AVG. RENT", "AVG. SIZE", "$/SF", "COMMUTE TO DT"]
    hx = [margin + 20, margin + 150, margin + 260, margin + 350, margin + 430]
    for i, h in enumerate(headers):
        c.drawString(hx[i], y - 8, h)

    # Gold line separator
    c.setStrokeColor(LUXX_GOLD)
    c.setLineWidth(1)
    c.line(margin + 10, y - 15, page_w - margin - 10, y - 15)

    c.setFillColor(white)
    c.setFont("Helvetica", 9)

    comparisons = [
        ("Deep Deuce/Bricktown", "$1,850", "650 SF", "$2.85", "5 min"),
        ("Midtown/Classen Curve", "$1,750", "600 SF", "$2.92", "8 min"),
        ("Automobile Alley", "$1,650", "580 SF", "$2.84", "10 min"),
    ]

    cy = y - 28
    for loc, rent, size, psf, commute in comparisons:
        c.drawString(hx[0], cy, loc)
        c.drawString(hx[1], cy, rent)
        c.drawString(hx[2], cy, size)
        c.drawString(hx[3], cy, psf)
        c.drawString(hx[4], cy, commute)
        cy -= 14

    # LUXX LOFTS row - highlighted
    c.setFillColor(LUXX_GOLD)
    c.rect(margin + 5, y - 55, page_w - 2*margin - 10, 16, fill=1, stroke=0)
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 9)
    c.drawString(hx[0], y - 50, "LUXX LOFTS")
    c.drawString(hx[1], y - 50, "$1,400")
    c.drawString(hx[2], y - 50, "540 SF")
    c.drawString(hx[3], y - 50, "$2.59")
    c.drawString(hx[4], y - 50, "12 min")

    # === UNIT TYPES ===
    y -= 85

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "FLOOR PLANS")

    y -= 15

    # Golden ratio for box widths (φ = 1.618)
    total_w = page_w - 2*margin - 20
    box_a_w = total_w * 0.618  # Larger box for main unit
    box_b_w = total_w * 0.382  # Smaller box for premium

    # === TYPE A - MINIMALIST LOFT (Main focus) ===
    c.setFillColor(LUXX_CREAM)
    c.rect(margin, y - 130, box_a_w, 135, fill=1, stroke=0)

    # Gold accent bar on left
    c.setFillColor(LUXX_GOLD)
    c.rect(margin, y - 130, 5, 135, fill=1, stroke=0)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(margin + 20, y - 15, "THE MINIMALIST")

    c.setFillColor(WARM_GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(margin + 20, y - 30, "TYPE A  •  540 SF  •  10 UNITS")

    # Price - big and bold
    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 32)
    c.drawString(margin + 20, y - 65, "$1,400")
    c.setFillColor(WARM_GRAY)
    c.setFont("Helvetica", 11)
    c.drawString(margin + 120, y - 60, "/month")

    # Per SF
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin + 20, y - 85, "$2.59/SF")
    c.setFillColor(FOREST_GREEN)
    c.drawString(margin + 80, y - 85, "BEST VALUE")

    # Features in two columns
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 8)
    features_a_left = [
        "Open concept living",
        "10' ceilings",
        "Floor-to-ceiling windows",
    ]
    features_a_right = [
        "Full kitchen + appliances",
        "Walk-in closet",
        "Juliet balcony",
    ]

    fy = y - 102
    for f in features_a_left:
        c.drawString(margin + 20, fy, "• " + f)
        fy -= 11

    fy = y - 102
    for f in features_a_right:
        c.drawString(margin + 150, fy, "• " + f)
        fy -= 11

    # === TYPE B - ROOFTOP PREMIUM ===
    box_b_x = margin + box_a_w + 20
    c.setFillColor(CHARCOAL)
    c.rect(box_b_x, y - 130, box_b_w, 135, fill=1, stroke=0)

    # Gold accent bar
    c.setFillColor(LUXX_GOLD)
    c.rect(box_b_x, y - 130, 5, 135, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(box_b_x + 15, y - 15, "THE PENTHOUSE")

    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(box_b_x + 15, y - 28, "TYPE B  •  750 SF + TERRACE")

    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(box_b_x + 15, y - 55, "$1,800")
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 10)
    c.drawString(box_b_x + 95, y - 52, "/mo")

    c.setFillColor(white)
    c.setFont("Helvetica", 8)
    features_b = [
        "Private rooftop terrace",
        "Separate bedroom",
        "11' ceilings",
        "2 UNITS ONLY",
    ]

    fy = y - 75
    for f in features_b:
        c.drawString(box_b_x + 15, fy, "• " + f)
        fy -= 12

    # === WHAT'S INCLUDED ===
    y -= 155

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "INCLUDED IN EVERY UNIT")

    y -= 18

    included = [
        ("Water & Trash", "Included"),
        ("Covered Parking", "1 Space"),
        ("High-Speed Fiber", "Ready"),
        ("Package Lockers", "24/7"),
        ("Rooftop Access", "Yes"),
    ]

    c.setFont("Helvetica", 9)
    ix = margin
    for item, val in included:
        c.setFillColor(LUXX_GOLD)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(ix, y, "✓")
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(ix + 12, y, item)
        c.setFillColor(WARM_GRAY)
        c.setFont("Helvetica", 8)
        c.drawString(ix + 12, y - 11, val)
        ix += 130

    # === CTA ===
    y -= 45

    c.setFillColor(LUXX_GOLD)
    c.rect(margin, y - 40, page_w - 2*margin, 45, fill=1, stroke=0)

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, y - 12, "SCHEDULE YOUR TOUR  •  NO APPLICATION FEE")

    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, y - 28, "luxx.okc@gmail.com  •  Move-in specials available  •  Flexible lease terms")

    # Copyright
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 5)
    c.drawCentredString(page_w/2, 8, "© 2024 Eric De Loera | De Loera Development | All Rights Reserved")


def draw_location_page(c, page_w, page_h):
    """Location and contact page"""
    margin = 50

    # Header
    c.setFillColor(LUXX_DARK)
    c.rect(0, page_h - 80, page_w, 80, fill=1, stroke=0)
    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 28)
    c.drawCentredString(page_w/2, page_h - 50, "LOCATION & CONTACT")

    y = page_h - 120

    # Location description
    c.setFillColor(BLACK)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "PRIME NORTHWEST OKC LOCATION")

    y -= 20
    c.setFont("Helvetica", 10)
    location_desc = [
        "LUXX LOFTS sits at the corner of N. Blackwelder Ave and NW 48th Street, just moments from",
        "the NW Expressway retail corridor. A new shopping center is under construction directly across",
        "the street, bringing additional retail, dining, and convenience to your doorstep."
    ]
    for line in location_desc:
        c.drawString(margin, y, line)
        y -= 14

    y -= 20

    # Distances
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "DISTANCES FROM LUXX LOFTS")

    y -= 20

    distances = [
        ("NW Expressway Shopping", "2 min"),
        ("Classen Curve District", "8 min"),
        ("Downtown OKC", "12 min"),
        ("Bricktown", "15 min"),
        ("Lake Hefner", "5 min"),
        ("Will Rogers World Airport", "20 min"),
        ("Mercy Hospital", "5 min"),
        ("OU Health Sciences Center", "12 min"),
    ]

    col1_x = margin
    col2_x = page_w/2

    c.setFont("Helvetica", 10)
    for i, (place, time) in enumerate(distances):
        if i < 4:
            c.drawString(col1_x, y - i*16, place)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(col1_x + 180, y - i*16, time)
            c.setFont("Helvetica", 10)
        else:
            c.drawString(col2_x, y - (i-4)*16, place)
            c.setFont("Helvetica-Bold", 10)
            c.drawString(col2_x + 180, y - (i-4)*16, time)
            c.setFont("Helvetica", 10)

    y -= 80

    # Contact Box
    c.setFillColor(HexColor('#F5F0E6'))
    c.rect(margin, y - 100, page_w - 2*margin, 110, fill=1, stroke=0)

    c.setFillColor(LUXX_DARK)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w/2, y - 15, "CONTACT US")

    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, y - 38, "4801 N. Blackwelder Ave, Oklahoma City, OK 73118")

    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(BRICK_HONEY)
    c.drawCentredString(page_w/2, y - 58, "luxx.okc@gmail.com")

    c.setFillColor(LUXX_DARK)
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, y - 78, "Leasing Office Hours: Mon-Fri 9am-6pm | Sat 10am-4pm")

    # Footer
    c.setFillColor(LUXX_DARK)
    c.rect(0, 0, page_w, 60, fill=1, stroke=0)
    c.setFillColor(LUXX_GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(page_w/2, 42, "LUXX LOFTS")
    c.setFillColor(white)
    c.setFont("Helvetica", 9)
    c.drawCentredString(page_w/2, 28, "Eric De Loera  |  De Loera Development")
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, 16, "Constructed by LUXX BUILDZ")

    # Fine print copyright
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 4)
    c.drawCentredString(page_w/2, 5, "© 2024 Eric De Loera | De Loera Development | All Rights Reserved | Unauthorized reproduction prohibited")


# ============ GENERATE PDFs ============

def generate_investor_package():
    """Generate investor/bank package"""
    output_path = os.path.expanduser("~/Downloads/luxx-haus 5/LUXX_LOFTS_Investor_Package.pdf")

    c = canvas.Canvas(output_path, pagesize=landscape(LETTER))

    # 1. Cover
    draw_investor_cover(c, PAGE_W, PAGE_H)
    c.showPage()

    # 2. Architectural Rendering
    draw_rendering_page(c, PAGE_W, PAGE_H)
    c.showPage()

    # 3. Executive Summary
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_executive_summary(c, PAGE_W, PAGE_H)
    c.showPage()

    # 4. Financial Projections
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_financial_projections(c, PAGE_W, PAGE_H)
    c.showPage()

    # 5. Construction Budget
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_construction_budget(c, PAGE_W, PAGE_H)
    c.showPage()

    # 6. Risk Analysis
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_risk_analysis(c, PAGE_W, PAGE_H)
    c.showPage()

    # 7. Exit Strategy
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_exit_strategy(c, PAGE_W, PAGE_H)
    c.showPage()

    c.save()

    print(f"\n{'='*60}")
    print(f"INVESTOR PACKAGE GENERATED")
    print(f"{'='*60}")
    print(f"Output: {output_path}")
    print(f"\nPages:")
    print(f"  1. Cover Page")
    print(f"  2. Architectural Rendering (Blackwelder View)")
    print(f"  3. Executive Summary")
    print(f"  4. Financial Projections (5-Year)")
    print(f"  5. Construction Budget")
    print(f"  6. Risk Analysis")
    print(f"  7. Exit Strategy & Returns")
    print(f"{'='*60}\n")

    return output_path


def generate_tenant_brochure():
    """Generate tenant marketing brochure"""
    output_path = os.path.expanduser("~/Downloads/luxx-haus 5/LUXX_LOFTS_Tenant_Brochure.pdf")

    c = canvas.Canvas(output_path, pagesize=landscape(LETTER))

    # 1. Cover
    draw_tenant_cover(c, PAGE_W, PAGE_H)
    c.showPage()

    # 2. Architectural Rendering
    draw_rendering_page(c, PAGE_W, PAGE_H)
    c.showPage()

    # 3. Lifestyle
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_lifestyle_page(c, PAGE_W, PAGE_H)
    c.showPage()

    # 4. Unit Options
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_unit_options(c, PAGE_W, PAGE_H)
    c.showPage()

    # 5. Location
    c.setFillColor(PAPER)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    draw_location_page(c, PAGE_W, PAGE_H)
    c.showPage()

    c.save()

    print(f"\n{'='*60}")
    print(f"TENANT BROCHURE GENERATED")
    print(f"{'='*60}")
    print(f"Output: {output_path}")
    print(f"\nPages:")
    print(f"  1. Cover Page")
    print(f"  2. Architectural Rendering (Blackwelder View)")
    print(f"  3. The LUXX Lifestyle")
    print(f"  4. Floor Plans & Pricing")
    print(f"  5. Location & Contact")
    print(f"{'='*60}\n")

    return output_path


if __name__ == "__main__":
    generate_investor_package()
    generate_tenant_brochure()
