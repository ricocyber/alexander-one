#!/usr/bin/env python3
"""
I.H.P. - Intelligent Home Protection

THE CPU HOUSE - Universal Intelligence Platform

The house IS a microprocessor.
The pins represent universal connectivity:
- Matter Protocol (universal IoT)
- Apple HomeKit
- Google Home
- Amazon Alexa
- Tesla Energy
- Open API (any system)

This is not a closed ecosystem.
This is the UNIVERSAL BRAIN for any smart home.
"""

from PIL import Image, ImageDraw, ImageFont
import os
import math

def create_ihp_logo(width=1000, height=280, dark_mode=True):
    """The CPU House - Universal Intelligence Platform"""

    img = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Premium tech palette
    chip_teal = (0, 185, 155, 255)       # Primary silicon teal
    circuit_blue = (50, 130, 210, 255)   # Circuit traces
    data_cyan = (0, 210, 190, 255)       # Active data
    pin_gold = (210, 175, 80, 255)       # Connection pins
    core_white = (255, 255, 255, 255)
    text_dark = (25, 40, 50, 255)

    cx = 120
    cy = 140

    # === THE CPU CHIP HOUSE ===
    chip_w = 90
    chip_h = 100

    chip_left = cx - chip_w / 2
    chip_right = cx + chip_w / 2
    chip_top = cy - chip_h / 2 + 15
    chip_bottom = cy + chip_h / 2 + 15

    # Main chip body - rounded corners effect
    corner = 8
    # Draw chip body
    draw.rectangle([chip_left + corner, chip_top, chip_right - corner, chip_bottom],
                   fill=None, outline=chip_teal, width=2)
    draw.rectangle([chip_left, chip_top + corner, chip_right, chip_bottom - corner],
                   fill=None, outline=chip_teal, width=2)
    # Corner arcs
    draw.arc([chip_left, chip_top, chip_left + corner*2, chip_top + corner*2],
             90, 180, fill=chip_teal, width=2)
    draw.arc([chip_right - corner*2, chip_top, chip_right, chip_top + corner*2],
             0, 90, fill=chip_teal, width=2)
    draw.arc([chip_left, chip_bottom - corner*2, chip_left + corner*2, chip_bottom],
             180, 270, fill=chip_teal, width=2)
    draw.arc([chip_right - corner*2, chip_bottom - corner*2, chip_right, chip_bottom],
             270, 360, fill=chip_teal, width=2)

    # Inner die area
    die_margin = 12
    draw.rectangle([chip_left + die_margin, chip_top + die_margin,
                   chip_right - die_margin, chip_bottom - die_margin],
                   outline=circuit_blue, width=1)

    # === ROOF INTEGRATED INTO CHIP ===
    roof_peak = chip_top - 25
    roof_left = chip_left - 8
    roof_right = chip_right + 8

    draw.line([(roof_left, chip_top), (cx, roof_peak)], fill=chip_teal, width=2)
    draw.line([(cx, roof_peak), (roof_right, chip_top)], fill=chip_teal, width=2)

    # === CONNECTION PINS - Universal I/O ===
    pin_length = 12
    pin_spacing = 14
    pin_width = 3

    # Left side pins (4 pins)
    for i in range(4):
        py = chip_top + 25 + i * pin_spacing
        # Pin
        draw.rectangle([chip_left - pin_length, py - pin_width/2,
                       chip_left, py + pin_width/2], fill=pin_gold)
        # Connection dot
        draw.ellipse([chip_left - pin_length - 4, py - 4,
                     chip_left - pin_length + 4, py + 4], fill=chip_teal)

    # Right side pins (4 pins)
    for i in range(4):
        py = chip_top + 25 + i * pin_spacing
        draw.rectangle([chip_right, py - pin_width/2,
                       chip_right + pin_length, py + pin_width/2], fill=pin_gold)
        draw.ellipse([chip_right + pin_length - 4, py - 4,
                     chip_right + pin_length + 4, py + 4], fill=chip_teal)

    # Bottom pins (3 pins)
    for i in range(3):
        px = chip_left + 22 + i * 23
        draw.rectangle([px - pin_width/2, chip_bottom,
                       px + pin_width/2, chip_bottom + pin_length], fill=pin_gold)
        draw.ellipse([px - 4, chip_bottom + pin_length - 4,
                     px + 4, chip_bottom + pin_length + 4], fill=chip_teal)

    # === CORE PROCESSOR - The brain ===
    core_cx = cx
    core_cy = cy + 25
    core_r = 18

    # Outer ring
    draw.ellipse([core_cx - core_r, core_cy - core_r,
                 core_cx + core_r, core_cy + core_r],
                 outline=data_cyan, width=2)

    # Inner core
    draw.ellipse([core_cx - core_r + 6, core_cy - core_r + 6,
                 core_cx + core_r - 6, core_cy + core_r - 6],
                 fill=chip_teal)

    # Core highlight
    draw.ellipse([core_cx - 5, core_cy - 5, core_cx + 5, core_cy + 5],
                 fill=data_cyan)

    # === CIRCUIT TRACES ===
    # Traces from core to pins
    trace_color = (*circuit_blue[:3], 150)

    # To left pins
    draw.line([(core_cx - core_r, core_cy), (chip_left + die_margin, core_cy)],
              fill=trace_color, width=1)
    draw.line([(chip_left + die_margin, core_cy), (chip_left + die_margin, chip_top + 35)],
              fill=trace_color, width=1)

    # To right pins
    draw.line([(core_cx + core_r, core_cy), (chip_right - die_margin, core_cy)],
              fill=trace_color, width=1)
    draw.line([(chip_right - die_margin, core_cy), (chip_right - die_margin, chip_top + 35)],
              fill=trace_color, width=1)

    # To bottom
    draw.line([(core_cx, core_cy + core_r), (core_cx, chip_bottom - die_margin)],
              fill=trace_color, width=1)

    # === DATA NODES - Grid inside chip ===
    node_rows = 2
    node_cols = 3
    node_start_x = chip_left + 25
    node_start_y = chip_top + 28
    node_spacing_x = 20
    node_spacing_y = 18

    for row in range(node_rows):
        for col in range(node_cols):
            nx = node_start_x + col * node_spacing_x
            ny = node_start_y + row * node_spacing_y
            # Skip if too close to core
            if abs(nx - core_cx) < 25 and abs(ny - core_cy) < 25:
                continue
            draw.ellipse([nx - 3, ny - 3, nx + 3, ny + 3], fill=data_cyan)

    # === CLOUD BRAIN - Platform agnostic AI ===
    cloud_cx = cx
    cloud_cy = roof_peak - 35

    # Simple clean cloud
    cloud_r = 18
    draw.ellipse([cloud_cx - cloud_r - 15, cloud_cy - 8, cloud_cx - cloud_r + 10, cloud_cy + 15],
                 outline=circuit_blue, width=2)
    draw.ellipse([cloud_cx - 10, cloud_cy - 15, cloud_cx + 10, cloud_cy + 8],
                 outline=circuit_blue, width=2)
    draw.ellipse([cloud_cx + cloud_r - 10, cloud_cy - 8, cloud_cx + cloud_r + 15, cloud_cy + 15],
                 outline=circuit_blue, width=2)

    # Cloud core
    draw.ellipse([cloud_cx - 5, cloud_cy - 5, cloud_cx + 5, cloud_cy + 5], fill=circuit_blue)

    # === DATA UPLINK ===
    for i in range(4):
        t = i / 3
        y = roof_peak - 8 - t * 22
        size = 2 + t * 1.5
        alpha = int(150 + t * 105)
        draw.ellipse([cx - size, y - size, cx + size, y + size],
                    fill=(*data_cyan[:3], alpha))

    # === I.H.P. TEXT ===
    text_x = 235
    text_y = 55

    try:
        font_paths = [
            "/System/Library/Fonts/Helvetica.ttc",
            "/System/Library/Fonts/SFNSDisplay.ttf",
        ]
        font_main = None
        for fp in font_paths:
            if os.path.exists(fp):
                font_main = ImageFont.truetype(fp, 75)
                font_tag = ImageFont.truetype(fp, 15)
                font_small = ImageFont.truetype(fp, 11)
                break
        if not font_main:
            raise Exception()
    except:
        font_main = ImageFont.load_default()
        font_tag = font_main
        font_small = font_main

    draw.text((text_x, text_y), "I.H.P.", font=font_main, fill=text_dark)
    bbox = draw.textbbox((text_x, text_y), "I.H.P.", font=font_main)

    # Tagline
    tag_y = bbox[3] + 8
    draw.text((text_x + 5, tag_y), "INTELLIGENT HOME PROTECTION", font=font_tag, fill=chip_teal)

    # === UNIVERSAL PLATFORM INDICATOR ===
    platform_y = tag_y + 28

    # Gradient bar
    bar_start = text_x
    bar_end = bbox[2] + 20
    bar_y = platform_y

    for x in range(int(bar_start), int(bar_end)):
        t = (x - bar_start) / (bar_end - bar_start)
        r = int(chip_teal[0] + (circuit_blue[0] - chip_teal[0]) * t)
        g = int(chip_teal[1] + (circuit_blue[1] - chip_teal[1]) * t)
        b = int(chip_teal[2] + (circuit_blue[2] - chip_teal[2]) * t)
        draw.line([(x, bar_y), (x, bar_y + 2)], fill=(r, g, b, 255))

    # Platform nodes
    platforms = 5  # Matter, HomeKit, Google, Alexa, Tesla/Open
    for i in range(platforms):
        px = bar_start + (bar_end - bar_start) * i / (platforms - 1)
        draw.ellipse([px - 5, bar_y - 4, px + 5, bar_y + 6], fill=chip_teal if i % 2 == 0 else circuit_blue)
        draw.ellipse([px - 2, bar_y - 1, px + 2, bar_y + 3], fill=core_white)

    # "UNIVERSAL PLATFORM" text
    draw.text((text_x + 5, bar_y + 12), "UNIVERSAL SMART HOME PLATFORM", font=font_small, fill=(*chip_teal[:3], 180))

    # === SIGNAL/CONNECTIVITY ===
    sig_x = width - 80
    sig_y = 140

    for i in range(3):
        r = 12 + i * 11
        alpha = 200 - i * 55
        draw.arc([sig_x - r, sig_y - r, sig_x + r, sig_y + r],
                 215, 325, fill=(*chip_teal[:3], alpha), width=2)

    draw.ellipse([sig_x - 4, sig_y - 4, sig_x + 4, sig_y + 4], fill=chip_teal)

    return img


def create_icon(size=200):
    """CPU House icon"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    chip_teal = (0, 185, 155, 255)
    circuit_blue = (50, 130, 210, 255)
    data_cyan = (0, 210, 190, 255)
    pin_gold = (210, 175, 80, 255)

    cx, cy = size // 2, size // 2 + 15

    # Chip body
    chip_w, chip_h = 70, 80
    chip_left = cx - chip_w / 2
    chip_right = cx + chip_w / 2
    chip_top = cy - chip_h / 2 + 10
    chip_bottom = cy + chip_h / 2 + 10

    draw.rectangle([chip_left, chip_top, chip_right, chip_bottom], outline=chip_teal, width=2)

    # Roof
    draw.line([(chip_left - 5, chip_top), (cx, chip_top - 22)], fill=chip_teal, width=2)
    draw.line([(cx, chip_top - 22), (chip_right + 5, chip_top)], fill=chip_teal, width=2)

    # Pins
    for i in range(3):
        py = chip_top + 20 + i * 18
        draw.rectangle([chip_left - 8, py - 2, chip_left, py + 2], fill=pin_gold)
        draw.rectangle([chip_right, py - 2, chip_right + 8, py + 2], fill=pin_gold)

    for i in range(2):
        px = cx - 15 + i * 30
        draw.rectangle([px - 2, chip_bottom, px + 2, chip_bottom + 8], fill=pin_gold)

    # Core
    core_y = cy + 20
    draw.ellipse([cx - 12, core_y - 12, cx + 12, core_y + 12], outline=data_cyan, width=2)
    draw.ellipse([cx - 5, core_y - 5, cx + 5, core_y + 5], fill=chip_teal)

    # Cloud
    cloud_y = chip_top - 45
    draw.ellipse([cx - 18, cloud_y - 8, cx - 2, cloud_y + 10], outline=circuit_blue, width=2)
    draw.ellipse([cx - 8, cloud_y - 12, cx + 8, cloud_y + 5], outline=circuit_blue, width=2)
    draw.ellipse([cx + 2, cloud_y - 8, cx + 18, cloud_y + 10], outline=circuit_blue, width=2)
    draw.ellipse([cx - 4, cloud_y - 4, cx + 4, cloud_y + 4], fill=circuit_blue)

    # Data uplink
    for i in range(3):
        t = i / 2
        y = chip_top - 25 - t * 15
        size = 2 + t
        draw.ellipse([cx - size, y - size, cx + size, y + size], fill=data_cyan)

    return img


if __name__ == "__main__":
    output_dir = "/Users/ericdeloera/Downloads/luxx-haus 5/assets"
    os.makedirs(output_dir, exist_ok=True)

    logo = create_ihp_logo(1000, 280)
    logo.save(f"{output_dir}/luxx_logo_dark.png", "PNG")
    logo.save(f"{output_dir}/luxx_logo_light.png", "PNG")

    icon = create_icon(200)
    icon.save(f"{output_dir}/luxx_icon.png", "PNG")

    print("✓ CPU HOUSE - Universal Intelligence Platform")
    print("  Compatible: Matter | HomeKit | Google | Alexa | Tesla | Open API")
