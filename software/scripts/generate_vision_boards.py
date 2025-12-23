#!/usr/bin/env python3
"""
LUXX BUILDZ / De Loera Development Vision Boards
20 designs for Instagram and device backgrounds
Soviet propaganda meets Narcos meets construction grit
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black, Color
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import os

# Brand Colors
RED = HexColor('#DC2626')
DARK_RED = HexColor('#991B1B')
BLACK = HexColor('#0A0A0A')
CHARCOAL = HexColor('#1C1C1C')
WHITE = white
GRAY = HexColor('#6B7280')
GOLD = HexColor('#D4AF37')
TEAL = HexColor('#0D9488')

BASE_DIR = "/Users/ericdeloera/Downloads/luxx-haus 5"
OUTPUT_DIR = f"{BASE_DIR}/Vision_Boards"

# Instagram = 1080x1080, Phone = 1170x2532 (iPhone 14 Pro), Desktop = 2560x1440
# We'll do square format for Instagram (can crop for others)

def create_vision_board(c, width, height, design_num, quote, subtext, style):
    """Create a single vision board design"""

    if style == "soviet_red":
        # Red background, bold white text, propaganda style
        c.setFillColor(RED)
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Diagonal stripes
        c.setStrokeColor(DARK_RED)
        c.setLineWidth(20)
        for i in range(-10, 20):
            c.line(i * 80, 0, i * 80 + height, height)

        # Text box
        c.setFillColor(BLACK)
        c.rect(width * 0.1, height * 0.35, width * 0.8, height * 0.3, fill=1, stroke=0)

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 48)
        c.drawCentredString(width/2, height * 0.55, quote)
        c.setFont("Helvetica", 18)
        c.drawCentredString(width/2, height * 0.42, subtext)

        # Brand
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width/2, height * 0.15, "LUXX BUILDZ")

    elif style == "dark_grit":
        # Black background, red accents
        c.setFillColor(BLACK)
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Red accent bar
        c.setFillColor(RED)
        c.rect(0, height * 0.45, width, height * 0.15, fill=1, stroke=0)

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 44)
        c.drawCentredString(width/2, height * 0.50, quote)

        c.setFillColor(GRAY)
        c.setFont("Helvetica", 16)
        c.drawCentredString(width/2, height * 0.30, subtext)

        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 20)
        c.drawCentredString(width/2, height * 0.12, "DE LOERA DEVELOPMENT")

    elif style == "split_bilingual":
        # Split screen - Spanish/English
        c.setFillColor(BLACK)
        c.rect(0, height/2, width, height/2, fill=1, stroke=0)
        c.setFillColor(RED)
        c.rect(0, 0, width, height/2, fill=1, stroke=0)

        # Spanish on top
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 42)
        words = quote.split("/")
        if len(words) >= 2:
            c.drawCentredString(width/2, height * 0.72, words[0].strip())
            c.setFillColor(BLACK)
            c.drawCentredString(width/2, height * 0.28, words[1].strip())
        else:
            c.drawCentredString(width/2, height * 0.72, quote)
            c.setFillColor(BLACK)
            c.drawCentredString(width/2, height * 0.28, subtext)

        # Divider line
        c.setStrokeColor(WHITE)
        c.setLineWidth(4)
        c.line(width * 0.2, height/2, width * 0.8, height/2)

    elif style == "gold_luxury":
        # Black with gold accents - luxury feel
        c.setFillColor(BLACK)
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Gold border
        c.setStrokeColor(GOLD)
        c.setLineWidth(8)
        c.rect(30, 30, width - 60, height - 60, fill=0, stroke=1)

        # Inner border
        c.setLineWidth(2)
        c.rect(50, 50, width - 100, height - 100, fill=0, stroke=1)

        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 40)
        c.drawCentredString(width/2, height * 0.55, quote)

        c.setFillColor(WHITE)
        c.setFont("Helvetica", 16)
        c.drawCentredString(width/2, height * 0.42, subtext)

        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(width/2, height * 0.15, "LUXX BUILDZ")

    elif style == "minimalist_white":
        # Clean white, black text, red accent
        c.setFillColor(WHITE)
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Red accent line
        c.setFillColor(RED)
        c.rect(width * 0.35, height * 0.48, width * 0.3, 6, fill=1, stroke=0)

        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 38)
        c.drawCentredString(width/2, height * 0.58, quote)

        c.setFillColor(GRAY)
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height * 0.38, subtext)

        c.setFillColor(BLACK)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width/2, height * 0.12, "DE LOERA DEVELOPMENT")

    elif style == "construction_bold":
        # Yellow/black construction zone feel
        c.setFillColor(HexColor('#FCD34D'))
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Black diagonal stripes (caution tape style)
        c.setFillColor(BLACK)
        for i in range(0, 30):
            if i % 2 == 0:
                c.saveState()
                c.translate(width/2, height/2)
                c.rotate(45)
                c.rect(-width, -height/2 + i*40, width*3, 20, fill=1, stroke=0)
                c.restoreState()

        # Text box
        c.setFillColor(BLACK)
        c.rect(width * 0.08, height * 0.38, width * 0.84, height * 0.24, fill=1, stroke=0)

        c.setFillColor(HexColor('#FCD34D'))
        c.setFont("Helvetica-Bold", 36)
        c.drawCentredString(width/2, height * 0.52, quote)
        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height * 0.42, subtext)

    elif style == "teal_ihp":
        # I.H.P. brand style
        c.setFillColor(TEAL)
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Circuit pattern suggestion
        c.setStrokeColor(Color(1, 1, 1, alpha=0.1))
        c.setLineWidth(1)
        for i in range(0, 20):
            c.line(0, i * 40, width, i * 40)
            c.line(i * 40, 0, i * 40, height)

        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 44)
        c.drawCentredString(width/2, height * 0.55, quote)

        c.setFont("Helvetica", 16)
        c.drawCentredString(width/2, height * 0.42, subtext)

        c.setFont("Helvetica-Bold", 28)
        c.drawCentredString(width/2, height * 0.15, "I.H.P.")

    elif style == "street_poster":
        # Worn poster look
        c.setFillColor(HexColor('#1a1a1a'))
        c.rect(0, 0, width, height, fill=1, stroke=0)

        # Distressed background elements
        c.setFillColor(Color(1, 1, 1, alpha=0.03))
        for i in range(50):
            import random
            random.seed(design_num * 100 + i)
            x = random.randint(0, int(width))
            y = random.randint(0, int(height))
            size = random.randint(20, 100)
            c.rect(x, y, size, size, fill=1, stroke=0)

        c.setFillColor(RED)
        c.setFont("Helvetica-Bold", 52)
        c.drawCentredString(width/2, height * 0.58, quote)

        c.setFillColor(WHITE)
        c.setFont("Helvetica", 18)
        c.drawCentredString(width/2, height * 0.40, subtext)

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width/2, height * 0.10, "LUXX BUILDZ • OKC")


def generate_all_vision_boards():
    """Generate all 20 vision boards"""

    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Define all 20 designs
    designs = [
        # LUXX BUILDZ / Construction
        (1, "VISIÓN", "Build what others only imagine", "soviet_red"),
        (2, "COJONES", "Execution takes courage", "dark_grit"),
        (3, "VISIÓN / COJONES", "", "split_bilingual"),
        (4, "RESILIENCIA", "From the ground up", "soviet_red"),
        (5, "BUILD EMPIRES", "Not excuses", "gold_luxury"),
        (6, "WORK IN SILENCE", "Let success make the noise", "minimalist_white"),
        (7, "UNDER CONSTRUCTION", "So is greatness", "construction_bold"),
        (8, "LEVEL UP", "Or get left behind", "dark_grit"),

        # Motivational / Hustle
        (9, "STAY HUNGRY", "Comfort is the enemy", "soviet_red"),
        (10, "OUTWORK THEM", "Every. Single. Day.", "dark_grit"),
        (11, "NO DAYS OFF", "The grind doesn't stop", "street_poster"),
        (12, "BUILT DIFFERENT", "Not born different", "gold_luxury"),
        (13, "PROVE THEM WRONG", "Then prove yourself right", "minimalist_white"),
        (14, "EARN IT", "Nobody gave me anything", "soviet_red"),

        # I.H.P. / Tech Vision
        (15, "PROTECT", "Every home. Every family.", "teal_ihp"),
        (16, "INNOVATE", "Or become irrelevant", "teal_ihp"),
        (17, "DATA IS POWER", "Own the intelligence", "dark_grit"),
        (18, "THE FUTURE", "Belongs to builders", "teal_ihp"),

        # Personal Brand
        (19, "DORMANT GIANT", "Waking up", "street_poster"),
        (20, "DE LOERA", "Building legacy", "gold_luxury"),
    ]

    # Instagram size (square)
    size = 1080

    for design_num, quote, subtext, style in designs:
        filename = f"{OUTPUT_DIR}/vision_{design_num:02d}_{quote.replace(' ', '_').replace('/', '_')}.pdf"
        c = canvas.Canvas(filename, pagesize=(size, size))
        create_vision_board(c, size, size, design_num, quote, subtext, style)
        c.save()
        print(f"  Created: vision_{design_num:02d} - {quote}")

    print(f"\n{'=' * 60}")
    print(f"ALL 20 VISION BOARDS CREATED")
    print(f"{'=' * 60}")
    print(f"\nLocation: {OUTPUT_DIR}")
    print("\nTo convert to PNG for Instagram/phone:")
    print("  Open each PDF in Preview → File → Export → PNG")
    print("\nOr use this command to batch convert:")
    print(f"  for f in \"{OUTPUT_DIR}\"/*.pdf; do")
    print("    sips -s format png \"$f\" --out \"${f%.pdf}.png\"")
    print("  done")


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING 20 VISION BOARDS")
    print("LUXX BUILDZ / DE LOERA DEVELOPMENT")
    print("=" * 60)
    print()
    generate_all_vision_boards()
