#!/usr/bin/env python3
"""
Generate all application documents as PDFs
Cielo Azul LLC / I.H.P.
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, ListFlowable, ListItem
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

# Brand Colors
TEAL = HexColor('#0D9488')
DARK_TEAL = HexColor('#0F766E')
BLACK = HexColor('#0A0A0A')
WHITE = white
GRAY = HexColor('#6B7280')
LIGHT_GRAY = HexColor('#F3F4F6')
RED = HexColor('#DC2626')

BASE_DIR = "/Users/ericdeloera/Downloads/luxx-haus 5"
OUTPUT_DIR = f"{BASE_DIR}/docs"

def get_styles():
    """Return common styles"""
    styles = getSampleStyleSheet()

    return {
        'title': ParagraphStyle(
            'Title', parent=styles['Heading1'],
            fontSize=22, textColor=TEAL, spaceAfter=20,
            alignment=TA_CENTER, fontName='Helvetica-Bold'
        ),
        'h1': ParagraphStyle(
            'H1', parent=styles['Heading1'],
            fontSize=16, textColor=TEAL, spaceBefore=20,
            spaceAfter=10, fontName='Helvetica-Bold'
        ),
        'h2': ParagraphStyle(
            'H2', parent=styles['Heading2'],
            fontSize=13, textColor=DARK_TEAL, spaceBefore=15,
            spaceAfter=8, fontName='Helvetica-Bold'
        ),
        'body': ParagraphStyle(
            'Body', parent=styles['Normal'],
            fontSize=10, textColor=BLACK, spaceAfter=8,
            alignment=TA_JUSTIFY, leading=14
        ),
        'bullet': ParagraphStyle(
            'Bullet', parent=styles['Normal'],
            fontSize=10, textColor=BLACK, leftIndent=20,
            spaceAfter=4, leading=13
        ),
        'code': ParagraphStyle(
            'Code', parent=styles['Normal'],
            fontSize=9, textColor=BLACK, fontName='Courier',
            leftIndent=20, spaceAfter=8, backColor=LIGHT_GRAY
        ),
        'center': ParagraphStyle(
            'Center', parent=styles['Normal'],
            fontSize=10, alignment=TA_CENTER, textColor=GRAY
        )
    }

def create_table(data, col_widths, header_color=TEAL):
    """Create a styled table"""
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), header_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), WHITE),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, GRAY),
        ('BACKGROUND', (0, 1), (-1, -1), WHITE),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    return table


def create_federal_registration_guide():
    """Create Federal Registration Guide PDF"""
    filename = f"{OUTPUT_DIR}/Federal_Registration_Guide.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = get_styles()
    story = []

    # Title
    story.append(Paragraph("FEDERAL REGISTRATION GUIDE", styles['title']))
    story.append(Paragraph("SAM.gov | SBIR.gov | Grants.gov", styles['center']))
    story.append(Paragraph("Cielo Azul LLC", styles['center']))
    story.append(Spacer(1, 0.3*inch))

    # SAM.gov Section
    story.append(Paragraph("1. SAM.gov REGISTRATION (Required First)", styles['h1']))
    story.append(Paragraph("System for Award Management - required for ALL federal grants and contracts.", styles['body']))

    story.append(Paragraph("Before You Start - Gather These:", styles['h2']))
    sam_docs = [
        ['Document', 'Notes'],
        ['D-U-N-S Number', 'You have this ✓'],
        ['EIN (Tax ID)', 'IRS letter'],
        ['Bank account info', 'Cielo Azul LLC business account'],
        ['Bank routing number', 'On checks or statement'],
    ]
    story.append(create_table(sam_docs, [2.5*inch, 3.5*inch]))
    story.append(Spacer(1, 0.2*inch))

    story.append(Paragraph("Step-by-Step:", styles['h2']))
    steps = [
        "1. Go to sam.gov → Click 'Sign In' → Create Login.gov account",
        "2. Set up 2-factor authentication (required)",
        "3. Click 'Register Your Entity' → Select federal business",
        "4. Enter: Legal Name, Address, Start Date, Fiscal Year End",
        "5. Enter D-U-N-S number (system validates)",
        "6. Enter NAICS codes (Primary: 541715 - R&D)",
        "7. Enter banking info for ACH payments",
        "8. Add Points of Contact (you as owner)",
        "9. Complete Representations & Certifications",
        "10. Submit and wait 7-10 days for activation",
    ]
    for step in steps:
        story.append(Paragraph(step, styles['bullet']))

    story.append(Paragraph("NAICS Codes to Use:", styles['h2']))
    naics_data = [
        ['Code', 'Description'],
        ['541715', 'R&D in Physical Sciences (PRIMARY)'],
        ['334290', 'Communications Equipment Manufacturing'],
        ['541512', 'Computer Systems Design'],
        ['236220', 'Commercial Building Construction'],
    ]
    story.append(create_table(naics_data, [1.5*inch, 4.5*inch]))

    story.append(PageBreak())

    # SBIR.gov Section
    story.append(Paragraph("2. SBIR.gov REGISTRATION", styles['h1']))
    story.append(Paragraph("Portal for SBIR/STTR opportunities. Time: 10 minutes.", styles['body']))

    story.append(Paragraph("Steps:", styles['h2']))
    sbir_steps = [
        "1. Go to sbir.gov → Click 'Register'",
        "2. Create account with business email",
        "3. Complete company profile (name, D-U-N-S, address)",
        "4. Subscribe to email alerts for: DOE, NSF, DHS, HHS",
        "5. Save profile and bookmark opportunities",
    ]
    for step in sbir_steps:
        story.append(Paragraph(step, styles['bullet']))

    # Grants.gov Section
    story.append(Paragraph("3. GRANTS.gov REGISTRATION", styles['h1']))
    story.append(Paragraph("Central portal for ALL federal grants. Requires active SAM.gov first.", styles['body']))

    story.append(Paragraph("Steps:", styles['h2']))
    grants_steps = [
        "1. Go to grants.gov → Click 'Register'",
        "2. Select 'Organization Applicant'",
        "3. Enter UEI (from SAM.gov registration)",
        "4. System pulls organization info from SAM.gov",
        "5. Create Authorized Organization Representative (AOR)",
        "6. Subscribe to relevant opportunity categories",
    ]
    for step in grants_steps:
        story.append(Paragraph(step, styles['bullet']))

    # Checklist
    story.append(Paragraph("REGISTRATION CHECKLIST", styles['h1']))
    checklist_data = [
        ['Step', 'Task', 'Time', 'Status'],
        ['1', 'SAM.gov registration', '30-45 min', '☐'],
        ['2', 'Wait for SAM.gov activation', '7-10 days', '☐'],
        ['3', 'SBIR.gov registration', '10 min', '☐'],
        ['4', 'Grants.gov registration', '15 min', '☐'],
    ]
    story.append(create_table(checklist_data, [0.5*inch, 2.5*inch, 1.2*inch, 0.8*inch]))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("HELP CONTACTS", styles['h2']))
    contacts = [
        ['Service', 'Phone', 'Hours'],
        ['SAM.gov', '1-866-606-8220', 'M-F 8am-8pm ET'],
        ['SBIR.gov', '1-800-827-5722', 'M-F 9am-5pm ET'],
        ['Grants.gov', '1-800-518-4726', '24/7'],
    ]
    story.append(create_table(contacts, [2*inch, 2*inch, 2*inch]))

    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph("Prepared for Cielo Azul LLC | December 2024", styles['center']))

    doc.build(story)
    return filename


def create_comcast_rise():
    """Create Comcast RISE Application PDF"""
    filename = f"{OUTPUT_DIR}/Comcast_RISE_Application.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = get_styles()
    story = []

    story.append(Paragraph("COMCAST RISE APPLICATION", styles['title']))
    story.append(Paragraph("$10,000 Grant + Marketing Services", styles['center']))
    story.append(Paragraph("Cielo Azul LLC / I.H.P.", styles['center']))
    story.append(Spacer(1, 0.3*inch))

    # Business Info
    story.append(Paragraph("SECTION 1: BUSINESS INFORMATION", styles['h1']))
    biz_info = [
        ['Field', 'Response'],
        ['Legal Business Name', 'Cielo Azul LLC'],
        ['DBA', 'I.H.P. - Intelligent Home Protection'],
        ['Address', '4801 N Blackwelder Ave, OKC, OK 73118'],
        ['Employees', '1-5'],
        ['Revenue Range', 'Under $500,000'],
    ]
    story.append(create_table(biz_info, [2*inch, 4*inch]))

    story.append(Paragraph("SECTION 2: OWNER INFORMATION", styles['h1']))
    owner_info = [
        ['Field', 'Response'],
        ['Owner Name', 'Eric De Loera'],
        ['Title', 'Founder & CEO'],
        ['Race/Ethnicity', 'Hispanic/Latino'],
    ]
    story.append(create_table(owner_info, [2*inch, 4*inch]))

    story.append(Paragraph("SECTION 3: BUSINESS DESCRIPTION", styles['h1']))
    story.append(Paragraph("<b>What does your business do?</b>", styles['body']))
    desc = """Cielo Azul LLC is developing I.H.P. (Intelligent Home Protection), a revolutionary smart home platform that prevents property damage before it happens. Unlike existing solutions that monitor only one risk (water OR fire OR electrical), I.H.P. is the first platform to correlate multiple perils simultaneously—water leaks, electrical faults, structural issues, HVAC failures, and environmental hazards—to detect dangerous failure patterns before catastrophic loss occurs.

The problem is massive: American homeowners suffer $150 billion in property damage annually. Water damage alone costs $15 billion per year, with 14,000 incidents happening every single day. Insurance carriers are desperate for solutions—they've passed $21 billion in premium increases to consumers since 2021.

Our technology uses Matter 1.4-compliant sensors with Thread mesh networking, designed to integrate seamlessly with Tesla Powerwall, Apple HomeKit, Google Home, and Amazon Alexa."""
    story.append(Paragraph(desc, styles['body']))

    story.append(PageBreak())

    story.append(Paragraph("SECTION 4: COMMUNITY IMPACT", styles['h1']))
    story.append(Paragraph("<b>How has your business impacted your community?</b>", styles['body']))
    impact = """As a Hispanic entrepreneur in Oklahoma City, I'm building I.H.P. to protect working families who can least afford catastrophic home damage. A single water leak averaging $14,000 can devastate a family's finances and potentially lead to displacement or foreclosure.

My background in construction (LUXX BUILDZ / De Loera Development) showed me firsthand how preventable most home disasters are—if homeowners had the right technology and information.

I.H.P. will make comprehensive home protection affordable and accessible. By partnering with insurance carriers, we can offer devices at reduced cost while lowering premiums for participating homeowners.

My goal is to prevent 10,000 home disasters in Oklahoma within our first five years."""
    story.append(Paragraph(impact, styles['body']))

    story.append(Paragraph("SECTION 5: USE OF GRANT", styles['h1']))
    story.append(Paragraph("<b>How would the Comcast RISE grant help your business?</b>", styles['body']))
    use = """The $10,000 Comcast RISE grant would accelerate three critical areas:

1. PROTOTYPE DEVELOPMENT: Fund initial sensor hardware for our first 10-home pilot program in Oklahoma City.

2. MARKETING & AWARENESS: Build our digital presence to attract insurance carrier partners and early adopter homeowners.

3. TECHNOLOGY INFRASTRUCTURE: Establish cloud computing infrastructure for our data platform.

The marketing services and technology upgrades from Comcast RISE are equally valuable—we need professional creative assets and reliable connectivity to demonstrate credibility to insurance industry partners.

This grant represents seed funding that positions us for larger SBIR federal grants ($274,000+) currently in application."""
    story.append(Paragraph(use, styles['body']))

    story.append(Paragraph("SUBMISSION CHECKLIST", styles['h1']))
    checklist = [
        "☐ Business license (Cielo Azul LLC Articles)",
        "☐ Government-issued ID",
        "☐ Proof of business address",
        "☐ W-9 form",
    ]
    for item in checklist:
        story.append(Paragraph(item, styles['bullet']))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Apply at:</b> comcastrise.com/apply", styles['body']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Prepared for Cielo Azul LLC | December 2024", styles['center']))

    doc.build(story)
    return filename


def create_stitchcrew():
    """Create StitchCrew Latino Accelerator Application PDF"""
    filename = f"{OUTPUT_DIR}/StitchCrew_Latino_Application.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = get_styles()
    story = []

    story.append(Paragraph("STITCHCREW LATINO ACCELERATOR", styles['title']))
    story.append(Paragraph("8-Week Program | Up to $15,000 Grant", styles['center']))
    story.append(Paragraph("Cielo Azul LLC / I.H.P.", styles['center']))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("FOUNDER INFORMATION", styles['h1']))
    founder = [
        ['Field', 'Response'],
        ['Name', 'Eric De Loera'],
        ['Hispanic/Latino Descent', 'Yes'],
        ['Ownership %', '100%'],
        ['Location', 'Oklahoma City, OK'],
    ]
    story.append(create_table(founder, [2*inch, 4*inch]))

    story.append(Paragraph("COMPANY OVERVIEW", styles['h1']))
    company = [
        ['Field', 'Response'],
        ['Business Name', 'Cielo Azul LLC (dba I.H.P.)'],
        ['Industry', 'Technology / Smart Home / InsurTech'],
        ['Stage', 'Pre-revenue / Prototype development'],
        ['Employees', '1-5'],
    ]
    story.append(create_table(company, [2*inch, 4*inch]))

    story.append(Paragraph("THE PROBLEM", styles['h1']))
    problem = """American homeowners lose $150 billion annually to property damage. Water damage alone costs $15 billion per year—that's 14,000 incidents every single day.

Current smart home solutions are fragmented: Flo by Moen monitors water only, Ting monitors electrical only, Nest Protect detects smoke/CO only.

These single-peril devices miss dangerous cross-system failures. Insurance carriers are desperate for solutions—they've had consecutive years of underwriting losses and passed $21 billion in premium increases to consumers."""
    story.append(Paragraph(problem, styles['body']))

    story.append(Paragraph("THE SOLUTION", styles['h1']))
    solution = """I.H.P. (Intelligent Home Protection) is the first platform to correlate multiple home perils simultaneously.

HARDWARE: Five sensor modules monitoring water, electrical, structural, HVAC, and environmental risks.

SOFTWARE: Cloud-based correlation engine that identifies compound failure patterns.

INTEGRATION: Matter 1.4 protocol—works with Apple, Google, Amazon, Tesla.

BUSINESS MODEL: Hardware ($500-800) + Subscription ($15-25/mo) + Insurance data licensing ($3-5/mo per home)."""
    story.append(Paragraph(solution, styles['body']))

    story.append(PageBreak())

    story.append(Paragraph("MARKET & COMPETITION", styles['h1']))
    market = """TARGET CUSTOMERS:
• Primary: Insurance carriers (Nationwide, State Farm, Liberty Mutual)
• Secondary: Homeowners (94M US households with security systems)
• Tertiary: Contractors (LUXX BUILDZ Tech platform)

COMPETITORS & DIFFERENTIATION:
• Flo by Moen: Water only (96% claim reduction) - No electrical/structural
• Ting: Electrical only (80% fire prevention) - No water/HVAC
• Phyn: Water only (99% leak reduction) - No correlation

I.H.P. is the ONLY platform correlating 5 perils simultaneously."""
    story.append(Paragraph(market, styles['body']))

    story.append(Paragraph("USE OF $15,000 GRANT", styles['h1']))
    use_data = [
        ['Category', 'Amount', 'Purpose'],
        ['Prototype Components', '$8,000', 'Dev kits, sensors, PCBs'],
        ['Cloud Infrastructure', '$3,000', 'AWS/Azure, database'],
        ['Pilot Program', '$2,500', '5-10 home installation'],
        ['Legal/IP', '$1,500', 'Provisional patent, trademark'],
    ]
    story.append(create_table(use_data, [2*inch, 1*inch, 3*inch]))

    story.append(Paragraph("WHY STITCHCREW", styles['h1']))
    why = """1. FINANCIAL FUNDAMENTALS: Strengthen financial modeling and investor materials.

2. CAPITAL ACCESS: Connections to investors and funding sources.

3. MENTORSHIP: Guidance from entrepreneurs who've scaled hardware businesses.

4. NETWORK: Connections to Latino entrepreneurs and OKC innovation ecosystem.

5. ACCOUNTABILITY: 8-week structure to hit milestones.

6. CREDIBILITY: Program graduation adds legitimacy with insurance carriers."""
    story.append(Paragraph(why, styles['body']))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Contact:</b> The Alliance for Economic Development of Oklahoma City", styles['body']))
    story.append(Paragraph("<b>Website:</b> theallianceokc.org", styles['body']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Prepared for Cielo Azul LLC | December 2024", styles['center']))

    doc.build(story)
    return filename


def create_gbeta():
    """Create gBETA OKC Application PDF"""
    filename = f"{OUTPUT_DIR}/gBETA_OKC_Application.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = get_styles()
    story = []

    story.append(Paragraph("gBETA OKLAHOMA CITY APPLICATION", styles['title']))
    story.append(Paragraph("7-Week Accelerator | FREE | No Equity", styles['center']))
    story.append(Paragraph("Cielo Azul LLC / I.H.P.", styles['center']))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("COMPANY OVERVIEW", styles['h1']))
    story.append(Paragraph("<b>One-line description:</b>", styles['body']))
    story.append(Paragraph("I.H.P. is a multi-peril smart home platform that prevents property damage by correlating water, electrical, structural, HVAC, and environmental sensor data to detect failure cascades before catastrophic loss.", styles['body']))

    overview = [
        ['Field', 'Response'],
        ['Company', 'Cielo Azul LLC (dba I.H.P.)'],
        ['Stage', 'Pre-revenue / Prototype'],
        ['Industry', 'Smart Home / InsurTech / IoT'],
        ['Founder', 'Eric De Loera'],
    ]
    story.append(create_table(overview, [2*inch, 4*inch]))

    story.append(Paragraph("THE PROBLEM (100-200 words)", styles['h1']))
    problem = """American homeowners lose $150 billion annually to property damage. Water damage alone costs $15 billion per year—that's 14,000 incidents every single day.

Current smart home solutions are fragmented and incomplete: Flo by Moen monitors water only, Ting monitors electrical only, Nest Protect detects smoke/CO only.

These single-peril devices miss dangerous cross-system failures. Example: An aging HVAC compressor draws excess current (electrical), causing refrigerant leak (environmental), leading to condensation backup (water), eventually damaging the foundation (structural). Current devices detect NONE of this cascade until it's too late.

Insurance carriers are desperate for solutions—they've had consecutive years of underwriting losses and passed $21 billion in premium increases to consumers since 2021."""
    story.append(Paragraph(problem, styles['body']))

    story.append(Paragraph("THE SOLUTION (100-200 words)", styles['h1']))
    solution = """I.H.P. is the first platform to correlate multiple home perils simultaneously.

HARDWARE: Five sensor modules—Water (pressure/flow/moisture), Electrical (arc faults/power quality), Structural (vibration/tilt), HVAC (compressor health), Environmental (smoke/CO/humidity).

SOFTWARE: Cloud-based correlation engine analyzing multi-sensor data to identify compound failure patterns.

INTEGRATION: Matter 1.4 protocol with Thread mesh networking. Works with Apple HomeKit, Google Home, Amazon Alexa, Samsung SmartThings, Tesla Powerwall.

BUSINESS MODEL: Hardware sales ($500-800), monthly subscription ($15-25), insurance data licensing ($3-5/home from carriers).

Competitor single-peril devices achieve 70-99% claim reduction. By correlating all five perils, I.H.P. can exceed these results."""
    story.append(Paragraph(solution, styles['body']))

    story.append(PageBreak())

    story.append(Paragraph("MARKET SIZE", styles['h1']))
    market = [
        ['Segment', '2024', '2033', 'CAGR'],
        ['Smart Home Insurance', '$3.67B', '$13.47B', '18.25%'],
        ['Smart Home Security', '$35.02B', '$145.54B', '15.31%'],
        ['Home Insurance Total', '$234.6B', '$576B', '7.6%'],
    ]
    story.append(create_table(market, [2*inch, 1.2*inch, 1.2*inch, 1*inch]))

    story.append(Paragraph("TRACTION", styles['h1']))
    traction = """COMPLETED:
• Market research (insurance data, competitor analysis, Matter 1.4 specs)
• Technical architecture (Nordic nRF5340, Thread networking)
• Hardware engineering partnership in discussion
• SBIR Phase I application drafted ($274K)
• Real estate collateral ($140K+) available

NEXT 90 DAYS:
• Complete working prototype
• Deploy 5-10 home pilot in OKC
• Submit SBIR application
• Secure first insurance carrier LOI"""
    story.append(Paragraph(traction, styles['body']))

    story.append(Paragraph("WHAT I WANT FROM gBETA", styles['h1']))
    wants = """1. CUSTOMER DISCOVERY - Validate assumptions through direct conversations
2. BUSINESS MODEL REFINEMENT - Optimize pricing and go-to-market
3. PITCH DEVELOPMENT - Translate technology into compelling investor pitch
4. MENTOR NETWORK - Access to hardware/enterprise sales expertise
5. PATHWAY TO GENER8TOR - $100K investment accelerator
6. OKC ECOSYSTEM - Deep local connections"""
    story.append(Paragraph(wants, styles['body']))

    story.append(Paragraph("WHY gBETA SPECIFICALLY", styles['h1']))
    why = """1. NO EQUITY - Protective of cap table this early
2. PATHWAY TO GENER8TOR - Clear path to $100K investment
3. LOCAL FOCUS - Building in Oklahoma, need OKC advice not Silicon Valley

I'm 100% committed to the full 7-week program."""
    story.append(Paragraph(why, styles['body']))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Website:</b> gbeta.org/oklahoma-city", styles['body']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Prepared for Cielo Azul LLC | December 2024", styles['center']))

    doc.build(story)
    return filename


def create_omfa():
    """Create Oklahoma Minority Founders Accelerator Application PDF"""
    filename = f"{OUTPUT_DIR}/OMFA_Application.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = get_styles()
    story = []

    story.append(Paragraph("OKLAHOMA MINORITY FOUNDERS", styles['title']))
    story.append(Paragraph("ACCELERATOR APPLICATION", styles['title']))
    story.append(Paragraph("OCAST / SSBCI Funded", styles['center']))
    story.append(Paragraph("Cielo Azul LLC / I.H.P.", styles['center']))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("FOUNDER DEMOGRAPHICS", styles['h1']))
    demo = [
        ['Field', 'Response'],
        ['Name', 'Eric De Loera'],
        ['BIPOC Status', 'Yes - Hispanic/Latino'],
        ['Ownership', '100% (Majority Owner)'],
        ['Location', 'Oklahoma City, OK'],
    ]
    story.append(create_table(demo, [2*inch, 4*inch]))

    story.append(Paragraph("COMPANY INFORMATION", styles['h1']))
    company = [
        ['Field', 'Response'],
        ['Legal Name', 'Cielo Azul LLC'],
        ['DBA', 'I.H.P. - Intelligent Home Protection'],
        ['State', 'Oklahoma'],
        ['Industry', 'Smart Home / InsurTech / IoT'],
        ['Stage', 'Pre-revenue'],
        ['Employees', '1-5'],
    ]
    story.append(create_table(company, [2*inch, 4*inch]))

    story.append(Paragraph("THE PROBLEM", styles['h1']))
    problem = """$150 BILLION in annual property damage. $15 billion in water claims. 14,000 water incidents PER DAY. 344,600 house fires annually.

Current solutions (Flo, Ting, Phyn, Nest) monitor only ONE peril each. They miss dangerous cross-system failures.

Insurance carriers have had consecutive underwriting losses. $21 billion passed to consumers in premium increases (2021-2024). They're desperate for solutions."""
    story.append(Paragraph(problem, styles['body']))

    story.append(Paragraph("THE SOLUTION", styles['h1']))
    solution = """I.H.P. correlates 5 home perils simultaneously:
• WTR-X1: Water pressure, flow, moisture
• ELC-X1: Arc faults, power quality
• STR-X1: Vibration, tilt, settlement
• HVC-X1: HVAC health, efficiency
• ENV-X1: Smoke, CO, temperature, humidity

Built on Nordic nRF5340 MCU with Thread mesh networking and Matter 1.4 protocol. Works with Apple, Google, Amazon, Tesla ecosystems.

Business Model: Hardware ($500-800) + Subscription ($15-25/mo) + Insurance licensing ($3-5/mo per home)."""
    story.append(Paragraph(solution, styles['body']))

    story.append(PageBreak())

    story.append(Paragraph("MARKET OPPORTUNITY", styles['h1']))
    market = [
        ['Segment', '2024', '2033', 'CAGR'],
        ['Smart Home Insurance', '$3.67B', '$13.47B', '18.25%'],
        ['Target 5-Year SOM', '100K homes', '$60M ARR', '-'],
    ]
    story.append(create_table(market, [2*inch, 1.2*inch, 1.2*inch, 1*inch]))

    story.append(Paragraph("COMPETITIVE ADVANTAGE", styles['h1']))
    comp = [
        ['Feature', 'Competitors', 'I.H.P.'],
        ['Multi-peril correlation', '✗', '✓'],
        ['Insurance-grade data', '✗', '✓'],
        ['Matter 1.4 native', 'Partial', '✓'],
        ['Contractor platform', '✗', '✓'],
    ]
    story.append(create_table(comp, [2.5*inch, 1.5*inch, 1.5*inch]))

    story.append(Paragraph("FUNDING REQUEST", styles['h1']))
    funding = [
        ['Category', '%', 'Use'],
        ['Prototype Development', '50%', 'Components, PCBs, dev kits'],
        ['Pilot Program', '25%', '10-25 home installation'],
        ['Cloud Infrastructure', '15%', 'AWS/Azure, 12mo hosting'],
        ['Legal/IP', '10%', 'Patent, trademark'],
    ]
    story.append(create_table(funding, [2*inch, 0.8*inch, 3.2*inch]))

    story.append(Paragraph("WHY OMFA", styles['h1']))
    why = """1. OKLAHOMA-FOCUSED - Building here, for Oklahoma first
2. MINORITY FOUNDER SUPPORT - SSBCI set-aside addresses capital barriers
3. OCAST ECOSYSTEM - Access to Industry Innovation grants, Catalyst, gener8tor
4. HIGH-GROWTH POTENTIAL - Venture-scale opportunity ($13B+ market)
5. CREDIBILITY - Program graduation signals validation to carriers/investors"""
    story.append(Paragraph(why, styles['body']))

    story.append(Paragraph("GROWTH POTENTIAL", styles['h1']))
    growth = """• MASSIVE MARKET: $150B losses, carriers desperate
• PROVEN DEMAND: Competitors show 70-99% claim reduction
• ACQUISITION PRECEDENT: NRG paid $2.8B for Vivint
• FIRST-MOVER: No one else building multi-peril correlation
• REGULATORY TAILWINDS: Carriers will require smart home devices"""
    story.append(Paragraph(growth, styles['body']))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("<b>Contact:</b> OCAST | oklahoma.gov/ocast | (405) 319-8400", styles['body']))
    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Prepared for Cielo Azul LLC | December 2024", styles['center']))

    doc.build(story)
    return filename


def create_business_credit():
    """Create Business Credit Building Plan PDF"""
    filename = f"{OUTPUT_DIR}/Business_Credit_Plan.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter,
                           rightMargin=0.75*inch, leftMargin=0.75*inch,
                           topMargin=0.75*inch, bottomMargin=0.75*inch)
    styles = get_styles()
    story = []

    story.append(Paragraph("BUSINESS CREDIT BUILDING PLAN", styles['title']))
    story.append(Paragraph("EIN Only | No Personal Credit Pulls", styles['center']))
    story.append(Paragraph("Cielo Azul LLC", styles['center']))
    story.append(Spacer(1, 0.3*inch))

    story.append(Paragraph("GOAL: Paydex 80+ in 6 months, $50K+ credit in 12 months", styles['body']))

    story.append(Paragraph("PHASE 1: FOUNDATION (Week 1-2)", styles['h1']))
    foundation = [
        ['Task', 'Status'],
        ['LLC registered with Oklahoma', '☐'],
        ['EIN obtained', '✓'],
        ['D-U-N-S number', '✓'],
        ['Business bank account', '☐'],
        ['Business phone (listed)', '☐'],
        ['Claim D&B profile at dnb.com', '☐'],
        ['Create Experian Business profile', '☐'],
    ]
    story.append(create_table(foundation, [4*inch, 1.5*inch]))

    story.append(Paragraph("PHASE 2: STARTER TRADELINES (Week 2-4)", styles['h1']))
    story.append(Paragraph("Net-30 accounts that report to credit bureaus. Pay EARLY to build Paydex.", styles['body']))

    story.append(Paragraph("Tier 1 - Apply First (Easy Approval):", styles['h2']))
    tier1 = [
        ['Vendor', 'Sells', 'Reports To', 'Website'],
        ['Uline', 'Shipping supplies', 'D&B', 'uline.com'],
        ['Quill', 'Office supplies', 'D&B', 'quill.com'],
        ['Grainger', 'Industrial', 'D&B', 'grainger.com'],
    ]
    story.append(create_table(tier1, [1.5*inch, 1.5*inch, 1.2*inch, 1.8*inch]))

    story.append(Paragraph("Tier 2 - After 2-3 Tier 1 Accounts:", styles['h2']))
    tier2 = [
        ['Vendor', 'Reports To', 'Website'],
        ['Crown Office Supplies', 'D&B + Experian', 'crownofficesupplies.com'],
        ['Strategic Network Solutions', 'D&B + Experian', 'snsllc.com'],
    ]
    story.append(create_table(tier2, [2.5*inch, 1.5*inch, 2*inch]))

    story.append(PageBreak())

    story.append(Paragraph("PHASE 3: FUEL CARDS (Week 4-6)", styles['h1']))
    story.append(Paragraph("No personal credit check, reports to business bureaus:", styles['body']))
    fuel = [
        ['Card', 'Reports To', 'Personal Guarantee'],
        ['Shell Fleet Plus', 'D&B + Experian', 'Soft check only'],
        ['WEX Fleet Card', 'D&B', 'No'],
        ['Fuelman', 'D&B', 'No'],
    ]
    story.append(create_table(fuel, [2*inch, 2*inch, 2*inch]))

    story.append(Paragraph("PHASE 4: BUSINESS CREDIT CARDS (Month 2-3)", styles['h1']))
    story.append(Paragraph("After 3-5 tradelines and 60-90 days payment history:", styles['body']))
    cards = [
        ['Card', 'Credit Check', 'Personal Guarantee'],
        ['Nav Prime Card', 'NO', 'NO'],
        ['Brex Corporate', 'NO (checks bank)', 'NO'],
        ['Rho Card', 'NO', 'NO'],
        ['Rippling Corporate', 'NO', 'NO'],
    ]
    story.append(create_table(cards, [2*inch, 2*inch, 2*inch]))

    story.append(Paragraph("PHASE 5: LINES OF CREDIT (Month 6-12)", styles['h1']))
    story.append(Paragraph("After Paydex 80+ established:", styles['body']))
    loc = [
        ['Lender', 'Amount', 'Website'],
        ['Fundbox', 'Up to $150K', 'fundbox.com'],
        ['Kabbage (Amex)', 'Up to $250K', 'kabbage.com'],
        ['BlueVine', 'Up to $250K', 'bluevine.com'],
    ]
    story.append(create_table(loc, [2*inch, 1.5*inch, 2.5*inch]))

    story.append(Paragraph("PAYDEX SCORING", styles['h1']))
    paydex = [
        ['Payment Timing', 'Points'],
        ['30+ days early', '100'],
        ['20-30 days early', '90'],
        ['On time', '80'],
        ['1-14 days late', '70'],
        ['15-30 days late', '60'],
    ]
    story.append(create_table(paydex, [3*inch, 1.5*inch]))
    story.append(Paragraph("<b>Strategy:</b> Pay ALL invoices at least 20 days early.", styles['body']))

    story.append(Paragraph("12-MONTH TIMELINE", styles['h1']))
    timeline = [
        ['Month', 'Action', 'Result'],
        ['1-2', 'Apply for 3 Tier 1 Net-30 accounts', 'First tradelines'],
        ['2-3', 'Apply for Tier 2 accounts', '5 tradelines'],
        ['3-4', 'Apply for fuel cards', 'Paydex building'],
        ['4-5', 'Apply for Nav Prime or Brex', 'First credit card'],
        ['6', 'Check Paydex score', 'Target 80+'],
        ['6-9', 'Apply for Fundbox/BlueVine', '$25K-$50K line'],
        ['9-12', 'Apply for larger lines', '$50K-$100K+ available'],
    ]
    story.append(create_table(timeline, [1*inch, 2.5*inch, 2.5*inch]))

    story.append(Paragraph("CRITICAL RULES", styles['h1']))
    rules = """DO:
✓ Pay EARLY (20+ days before due)
✓ Use each account monthly
✓ Keep utilization under 30%
✓ Monitor D&B profile monthly

DON'T:
✗ Give personal SSN unless required
✗ Miss any payment deadlines
✗ Max out credit lines
✗ Apply for too many accounts at once"""
    story.append(Paragraph(rules, styles['body']))

    story.append(Spacer(1, 0.3*inch))
    story.append(Paragraph("Prepared for Cielo Azul LLC | December 2024", styles['center']))

    doc.build(story)
    return filename


if __name__ == "__main__":
    print("=" * 60)
    print("GENERATING ALL APPLICATION DOCUMENTS")
    print("Cielo Azul LLC / I.H.P.")
    print("=" * 60)
    print()

    files = []

    print("Creating Federal Registration Guide...")
    files.append(create_federal_registration_guide())

    print("Creating Comcast RISE Application...")
    files.append(create_comcast_rise())

    print("Creating StitchCrew Latino Accelerator Application...")
    files.append(create_stitchcrew())

    print("Creating gBETA OKC Application...")
    files.append(create_gbeta())

    print("Creating OMFA Application...")
    files.append(create_omfa())

    print("Creating Business Credit Building Plan...")
    files.append(create_business_credit())

    print()
    print("=" * 60)
    print("ALL DOCUMENTS CREATED")
    print("=" * 60)
    print()
    for f in files:
        print(f"  ✓ {os.path.basename(f)}")
    print()
    print(f"Location: {OUTPUT_DIR}")
    print()
    print("Opening folder...")
    os.system(f'open "{OUTPUT_DIR}"')
