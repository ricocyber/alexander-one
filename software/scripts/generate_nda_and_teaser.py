#!/usr/bin/env python3
"""
Generate NDA and Teaser Deck for Joe Hobart
Protect IP before sharing technical details
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime

# Colors
CHARCOAL = HexColor('#1F2937')
TEAL = HexColor('#0D9488')
LIGHT_GRAY = HexColor('#F3F4F6')
RED = HexColor('#DC2626')

BASE_DIR = "/Users/ericdeloera/Downloads/luxx-haus 5"

def generate_nda():
    """Generate Non-Disclosure Agreement"""
    page_w, page_h = letter
    c = canvas.Canvas(f"{BASE_DIR}/IHP_NDA_Joe_Hobart.pdf", pagesize=letter)
    margin = 50

    # Header
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(page_w/2, page_h - 60, "NON-DISCLOSURE AGREEMENT")

    c.setFont("Helvetica", 11)
    c.setFillColor(CHARCOAL)
    c.drawCentredString(page_w/2, page_h - 80, "Mutual Confidentiality Agreement")

    y = page_h - 120

    # Parties
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "PARTIES:")
    y -= 20

    c.setFont("Helvetica", 10)
    parties_text = [
        f"This Non-Disclosure Agreement (\"Agreement\") is entered into as of {datetime.now().strftime('%B %d, %Y')}",
        "",
        "BETWEEN:",
        "",
        "    DISCLOSING PARTY:",
        "    De Loera Development / PergoLuxx Construction LLC",
        "    Eric De Loera, Founder",
        "    Oklahoma City, Oklahoma",
        "    (\"Company\")",
        "",
        "    RECEIVING PARTY:",
        "    Joe Hobart",
        "    jh@higbl.com",
        "    Stillwater, Oklahoma",
        "    (\"Recipient\")",
    ]

    for line in parties_text:
        c.drawString(margin, y, line)
        y -= 14

    y -= 10

    # Purpose
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "1. PURPOSE")
    y -= 18
    c.setFont("Helvetica", 10)
    purpose = [
        "Company wishes to disclose certain confidential and proprietary information relating to",
        "I.H.P. (Intelligent Home Protection), a multi-peril home monitoring platform, for the",
        "purpose of evaluating a potential business relationship, including but not limited to",
        "hardware development, co-founder partnership, or consulting engagement."
    ]
    for line in purpose:
        c.drawString(margin, y, line)
        y -= 14

    y -= 10

    # Definition
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "2. DEFINITION OF CONFIDENTIAL INFORMATION")
    y -= 18
    c.setFont("Helvetica", 10)
    definition = [
        "\"Confidential Information\" includes, but is not limited to:",
        "    • Technical specifications, hardware designs, sensor configurations",
        "    • Software architecture, source code, algorithms, and ML models",
        "    • Business plans, market research, financial projections",
        "    • Customer lists, supplier relationships, pricing strategies",
        "    • Patent applications, trade secrets, and proprietary processes",
        "    • Any information marked \"Confidential\" or reasonably understood to be confidential"
    ]
    for line in definition:
        c.drawString(margin, y, line)
        y -= 14

    y -= 10

    # Obligations
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "3. OBLIGATIONS OF RECIPIENT")
    y -= 18
    c.setFont("Helvetica", 10)
    obligations = [
        "Recipient agrees to:",
        "    a) Hold all Confidential Information in strict confidence",
        "    b) Not disclose Confidential Information to any third party without prior written consent",
        "    c) Not use Confidential Information for any purpose other than evaluating the relationship",
        "    d) Not copy, reproduce, or reverse engineer any Confidential Information",
        "    e) Return or destroy all Confidential Information upon request or termination",
        "    f) Notify Company immediately of any unauthorized disclosure or use"
    ]
    for line in obligations:
        c.drawString(margin, y, line)
        y -= 14

    y -= 10

    # Term
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "4. TERM")
    y -= 18
    c.setFont("Helvetica", 10)
    term = [
        "This Agreement shall remain in effect for a period of three (3) years from the date of",
        "execution. The obligations of confidentiality shall survive termination of this Agreement."
    ]
    for line in term:
        c.drawString(margin, y, line)
        y -= 14

    y -= 10

    # Remedies
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "5. REMEDIES")
    y -= 18
    c.setFont("Helvetica", 10)
    remedies = [
        "Recipient acknowledges that any breach of this Agreement may cause irreparable harm to",
        "Company, and that monetary damages may be inadequate. Company shall be entitled to seek",
        "injunctive relief, specific performance, and any other remedies available at law or equity."
    ]
    for line in remedies:
        c.drawString(margin, y, line)
        y -= 14

    y -= 10

    # Governing Law
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "6. GOVERNING LAW")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "This Agreement shall be governed by the laws of the State of Oklahoma.")

    # Page 2
    c.showPage()

    y = page_h - 60

    # No License
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "7. NO LICENSE OR PARTNERSHIP")
    y -= 18
    c.setFont("Helvetica", 10)
    no_license = [
        "Nothing in this Agreement grants Recipient any license, ownership, or rights to any",
        "intellectual property of Company. This Agreement does not create any partnership, joint",
        "venture, or employment relationship between the parties."
    ]
    for line in no_license:
        c.drawString(margin, y, line)
        y -= 14

    y -= 20

    # Signatures
    c.setFont("Helvetica-Bold", 11)
    c.drawString(margin, y, "8. SIGNATURES")
    y -= 30

    # Company signature
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "DISCLOSING PARTY - De Loera Development")
    y -= 40

    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Signature: _______________________________________")
    y -= 20
    c.drawString(margin, y, "Name: Eric De Loera")
    y -= 20
    c.drawString(margin, y, "Title: Founder & CEO")
    y -= 20
    c.drawString(margin, y, "Date: _______________")

    y -= 50

    # Recipient signature
    c.setFont("Helvetica-Bold", 10)
    c.drawString(margin, y, "RECEIVING PARTY")
    y -= 40

    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Signature: _______________________________________")
    y -= 20
    c.drawString(margin, y, "Name: Joe Hobart")
    y -= 20
    c.drawString(margin, y, "Email: jh@higbl.com")
    y -= 20
    c.drawString(margin, y, "Date: _______________")

    # Footer
    y -= 60
    c.setFillColor(RED)
    c.setFont("Helvetica-Bold", 9)
    c.drawCentredString(page_w/2, y, "THIS IS A LEGALLY BINDING AGREEMENT - READ CAREFULLY BEFORE SIGNING")

    c.save()
    print("Generated: IHP_NDA_Joe_Hobart.pdf")


def generate_teaser():
    """Generate Teaser Deck - No technical secrets"""
    page_w, page_h = letter
    c = canvas.Canvas(f"{BASE_DIR}/IHP_Teaser_Deck.pdf", pagesize=letter)
    margin = 40

    # ========== COVER ==========
    c.setFillColor(TEAL)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 56)
    c.drawCentredString(page_w/2, page_h - 200, "I.H.P.")

    c.setFont("Helvetica", 24)
    c.drawCentredString(page_w/2, page_h - 245, "Intelligent Home Protection")

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w/2, page_h - 320, "THE HOME DATA PLATFORM")
    c.drawCentredString(page_w/2, page_h - 345, "TESLA NEEDS")

    # Watermark
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(page_w/2, page_h - 420, "CONFIDENTIAL - Prepared Exclusively For:")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, page_h - 445, "JOE HOBART")
    c.setFont("Helvetica", 10)
    c.drawCentredString(page_w/2, page_h - 465, "jh@higbl.com")

    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, 80, "De Loera Development")
    c.drawCentredString(page_w/2, 60, datetime.now().strftime("%B %Y"))

    c.showPage()

    # ========== PAGE 2: THE PROBLEM ==========
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 60, page_w, 60, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_w/2, page_h - 42, "THE PROBLEM")

    y = page_h - 110

    # Big numbers
    stats = [
        ("$150 BILLION", "Lost annually to home insurance claims"),
        ("$13 BILLION", "Water damage alone"),
        ("$11 BILLION", "Fire damage"),
        ("344,600", "House fires per year"),
        ("14,000", "Water damage incidents PER DAY"),
    ]

    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(CHARCOAL)
    c.drawString(margin, y, "Insurance companies are BLEEDING money:")
    y -= 30

    for stat, desc in stats:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 24)
        c.drawString(margin + 20, y, stat)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 12)
        c.drawString(margin + 200, y + 5, desc)
        y -= 40

    y -= 20
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "The industry is DESPERATE for loss prevention technology.")

    # Footer watermark
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, 30, "CONFIDENTIAL - Prepared for Joe Hobart (jh@higbl.com)")

    c.showPage()

    # ========== PAGE 3: THE VALIDATION ==========
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 60, page_w, 60, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_w/2, page_h - 42, "THE VALIDATION")

    y = page_h - 110

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "This market is PROVEN:")
    y -= 40

    # Vivint box
    c.setFillColor(TEAL)
    c.roundRect(margin, y - 80, page_w - 2*margin, 90, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 32)
    c.drawCentredString(page_w/2, y - 25, "$2.8 BILLION")
    c.setFont("Helvetica", 14)
    c.drawCentredString(page_w/2, y - 50, "NRG Energy paid for Vivint Smart Home")
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(page_w/2, y - 72, "2023 Acquisition")

    y -= 120

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 12)
    validations = [
        "• Flo by Moen: 96% reduction in water claims (LexisNexis study)",
        "• Ting: 80% reduction in electrical fires (1M+ homes protected)",
        "• State Farm, Liberty Mutual, USAA all partnering with smart home tech",
        "• Tesla Powerwall has 1M+ installations but ZERO home sensor data",
    ]
    for v in validations:
        c.drawString(margin, y, v)
        y -= 22

    y -= 20
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(TEAL)
    c.drawString(margin, y, "Energy companies are buying home platforms. Tesla is next.")

    # Footer watermark
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, 30, "CONFIDENTIAL - Prepared for Joe Hobart (jh@higbl.com)")

    c.showPage()

    # ========== PAGE 4: THE SOLUTION (HIGH LEVEL) ==========
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 60, page_w, 60, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_w/2, page_h - 42, "THE SOLUTION")

    y = page_h - 100

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "I.H.P. - Intelligent Home Protection")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawString(margin, y, "A multi-peril home monitoring platform that protects against:")
    y -= 30

    perils = [
        ("WATER", "Leaks, pressure, flooding"),
        ("FIRE", "Smoke, heat, early detection"),
        ("ELECTRICAL", "Arc faults, power quality, surge"),
        ("STRUCTURAL", "Foundation, vibration, settlement"),
        ("HVAC", "Efficiency, failure prediction"),
    ]

    for peril, desc in perils:
        c.setFillColor(TEAL)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin + 20, y, peril)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 12)
        c.drawString(margin + 140, y, desc)
        y -= 28

    y -= 20
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "Unlike competitors who do ONE thing, I.H.P. does ALL of them -")
    y -= 18
    c.drawString(margin, y, "with cross-correlation that predicts failures before they happen.")

    y -= 40
    c.setFillColor(TEAL)
    c.roundRect(margin, y - 50, page_w - 2*margin, 60, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, y - 18, "THE SOFTWARE PLATFORM IS BUILT.")
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, y - 40, "Backend, ML pipeline, API - all done. We need hardware.")

    # Footer watermark
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, 30, "CONFIDENTIAL - Prepared for Joe Hobart (jh@higbl.com)")

    c.showPage()

    # ========== PAGE 5: WHAT WE NEED ==========
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 60, page_w, 60, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_w/2, page_h - 42, "WHAT WE NEED")

    y = page_h - 100

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "We need a hardware co-founder who can:")
    y -= 35

    needs = [
        "Design production-ready PCBs",
        "Select and validate sensors",
        "Write embedded firmware (Zephyr RTOS, Matter protocol)",
        "Navigate certifications (FCC, UL, Matter)",
        "Build manufacturing relationships",
    ]

    c.setFont("Helvetica", 12)
    for need in needs:
        c.setFillColor(TEAL)
        c.drawString(margin + 20, y, "•")
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 40, y, need)
        y -= 25

    y -= 30
    c.setFont("Helvetica-Bold", 14)
    c.drawString(margin, y, "What you get:")
    y -= 35

    gets = [
        "Co-founder equity (negotiable)",
        "Technical leadership of hardware division",
        "Ground floor on a Tesla acquisition play",
        "Real opportunity - not a side project",
    ]

    c.setFont("Helvetica", 12)
    for get in gets:
        c.setFillColor(TEAL)
        c.drawString(margin + 20, y, "•")
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 40, y, get)
        y -= 25

    y -= 30
    c.setFillColor(TEAL)
    c.roundRect(margin, y - 60, page_w - 2*margin, 70, 8, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w/2, y - 22, "Oklahoma-based. Your backyard.")
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, y - 45, "This isn't a cold call from Silicon Valley. This is local.")

    # Footer watermark
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, 30, "CONFIDENTIAL - Prepared for Joe Hobart (jh@higbl.com)")

    c.showPage()

    # ========== PAGE 6: NEXT STEPS ==========
    c.setFillColor(CHARCOAL)
    c.rect(0, page_h - 60, page_w, 60, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 22)
    c.drawCentredString(page_w/2, page_h - 42, "NEXT STEPS")

    y = page_h - 120

    steps = [
        ("1", "Sign the NDA", "Protects both of us"),
        ("2", "Review technical specs", "Full hardware requirements"),
        ("3", "Meet in person", "Coffee in Stillwater or OKC"),
        ("4", "Decide if you're in", "No pressure, real conversation"),
    ]

    for num, title, desc in steps:
        c.setFillColor(TEAL)
        c.circle(margin + 20, y - 5, 18, fill=1, stroke=0)
        c.setFillColor(white)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(margin + 20, y - 10, num)

        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin + 50, y, title)
        c.setFont("Helvetica", 11)
        c.setFillColor(CHARCOAL)
        c.drawString(margin + 50, y - 18, desc)
        y -= 55

    y -= 30

    # Contact box
    c.setFillColor(TEAL)
    c.roundRect(margin, y - 100, page_w - 2*margin, 110, 10, fill=1, stroke=0)
    c.setFillColor(white)
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_w/2, y - 30, "Eric De Loera")
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, y - 50, "partners@ihp-home.io")
    c.setFont("Helvetica-Bold", 14)
    c.drawCentredString(page_w/2, y - 80, "\"Let's grab coffee and talk.\"")

    # Footer watermark
    c.setFillColor(LIGHT_GRAY)
    c.setFont("Helvetica", 8)
    c.drawCentredString(page_w/2, 30, "CONFIDENTIAL - Prepared for Joe Hobart (jh@higbl.com)")

    c.save()
    print("Generated: IHP_Teaser_Deck.pdf")


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING PROTECTED DOCUMENTS FOR JOE HOBART")
    print("=" * 60)
    generate_nda()
    generate_teaser()
    print("=" * 60)
    print("\nSEND IN THIS ORDER:")
    print("  1. IHP_NDA_Joe_Hobart.pdf - He signs FIRST")
    print("  2. IHP_Teaser_Deck.pdf - After NDA is signed")
    print("  3. Technical specs - Only after he's committed")
    print("=" * 60)
