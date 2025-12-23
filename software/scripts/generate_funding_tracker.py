#!/usr/bin/env python3
"""
Generate I.H.P. Funding Resources Tracker PDF
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
import os

OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "IHP_Funding_Tracker.pdf")

DARK_BLUE = HexColor('#1a365d')
TEAL = HexColor('#0d9488')
ORANGE = HexColor('#ea580c')
LIGHT_GRAY = HexColor('#f3f4f6')
MEDIUM_GRAY = HexColor('#6b7280')

def create_tracker():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        rightMargin=0.4*inch,
        leftMargin=0.4*inch,
        topMargin=0.4*inch,
        bottomMargin=0.4*inch
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle('Title', parent=styles['Heading1'], fontSize=20, textColor=DARK_BLUE, spaceAfter=4, alignment=1)
    subtitle_style = ParagraphStyle('Subtitle', parent=styles['Normal'], fontSize=10, textColor=MEDIUM_GRAY, spaceAfter=12, alignment=1)
    section_style = ParagraphStyle('Section', parent=styles['Heading2'], fontSize=12, textColor=TEAL, spaceBefore=10, spaceAfter=6)
    alert_style = ParagraphStyle('Alert', parent=styles['Heading2'], fontSize=12, textColor=ORANGE, spaceBefore=10, spaceAfter=6)
    body_style = ParagraphStyle('Body', parent=styles['Normal'], fontSize=9, spaceAfter=4, leading=11)
    small_style = ParagraphStyle('Small', parent=styles['Normal'], fontSize=8, textColor=MEDIUM_GRAY)

    story = []

    # Title
    story.append(Paragraph("I.H.P. FUNDING RESOURCES TRACKER", title_style))
    story.append(Paragraph(f"Created: {datetime.now().strftime('%B %d, %Y')} | Keep this updated!", subtitle_style))

    # STEP 1: SET UP ALERTS
    story.append(Paragraph("STEP 1: SET UP FREE GRANT ALERTS (Do This First!)", alert_style))

    alerts_data = [
        ["Service", "What It Does", "How to Sign Up"],
        ["Grants.gov", "Emails you new federal grants", "grants.gov → Create Account → Set Alerts"],
        ["SBIR.gov", "All SBIR opportunities", "sbir.gov → Create profile"],
        ["NSF SBIR", "NSF tech grants", "seedfund.nsf.gov"],
        ["DOE SBIR", "Energy/building grants", "Email: sbir-sttr@science.doe.gov"],
        ["i2E Oklahoma", "Oklahoma innovation funding", "i2e.org → Newsletter"],
    ]

    alerts_table = Table(alerts_data, colWidths=[1.2*inch, 2.3*inch, 3.5*inch])
    alerts_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(alerts_table)
    story.append(Spacer(1, 10))

    # GRANTS TO APPLY FOR NOW
    story.append(Paragraph("GRANTS TO APPLY FOR (You Qualify Now)", section_style))

    grants_now = [
        ["Grant", "Amount", "For", "Status"],
        ["Comcast RISE", "Varies", "Minority-owned biz", "[ ] Applied"],
        ["StitchCrew", "$25,000", "Startups", "[ ] Applied"],
        ["NSF SBIR Phase I", "$274,000", "Tech startups", "[ ] Need SAM.gov"],
        ["NASE Growth Grant", "$4,000/mo", "Small business members", "[ ] Check req"],
        ["Kiva OKC", "$15,000 @ 0%", "Any small business", "[ ] Consider"],
    ]

    grants_table = Table(grants_now, colWidths=[1.5*inch, 1*inch, 2*inch, 1.2*inch])
    grants_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(grants_table)
    story.append(Spacer(1, 10))

    # HISPANIC/MINORITY GRANTS
    story.append(Paragraph("HISPANIC & MINORITY SPECIFIC GRANTS", section_style))

    minority_grants = [
        ["Grant", "Amount", "When", "Status"],
        ["Support Latino Grant", "Varies", "Sept/Oct annually", "[ ] Watch 2025"],
        ["USHCC-Wells Fargo", "$5K-$15K", "Check ushcc.com", "[ ] Research"],
        ["Black Ambition Prize", "$15K-$1M", "Spring usually", "[ ] Watch 2025"],
        ["PepsiCo Hispanic Biz", "$10,000", "Annual", "[ ] Check fit"],
        ["MBDA Programs", "Varies", "Ongoing", "[ ] mbda.gov"],
    ]

    minority_table = Table(minority_grants, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1.2*inch])
    minority_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(minority_table)
    story.append(Spacer(1, 10))

    # OKLAHOMA GRANTS
    story.append(Paragraph("OKLAHOMA LOCAL GRANTS", section_style))

    ok_grants = [
        ["Grant", "Amount", "Notes", "Status"],
        ["OCAST Matching", "Up to $500K", "Need 51% work in OK", "[ ] Later"],
        ["Oklahoma OARS", "$50K-$500K", "Innovation projects", "[ ] Later"],
        ["STEP Export Fund", "Up to $24K", "For exporters", "[ ] Later"],
    ]

    ok_table = Table(ok_grants, colWidths=[1.5*inch, 1*inch, 2*inch, 1*inch])
    ok_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(ok_table)
    story.append(Spacer(1, 10))

    # REQUIRED REGISTRATIONS
    story.append(Paragraph("REQUIRED REGISTRATIONS (Do These First!)", alert_style))

    reg_data = [
        ["Registration", "Website", "Time", "Done?"],
        ["D-U-N-S Number", "dnb.com", "DONE", "[X] 136342147"],
        ["SAM.gov", "sam.gov", "2-4 weeks", "[ ]"],
        ["Login.gov", "login.gov", "1 hour", "[ ]"],
        ["Grants.gov", "grants.gov", "1 day", "[ ]"],
        ["SBIR.gov", "sbir.gov", "1 day", "[ ]"],
    ]

    reg_table = Table(reg_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 0.7*inch])
    reg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), ORANGE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
        ('ALIGN', (3, 0), (3, -1), 'CENTER'),
    ]))
    story.append(reg_table)
    story.append(Spacer(1, 10))

    # FREE HELP RESOURCES
    story.append(Paragraph("FREE HELP (No Money, Just Advice)", section_style))

    free_help = [
        ["Resource", "What They Do", "Contact"],
        ["Oklahoma SBDC", "Free business consulting", "Google 'Oklahoma SBDC'"],
        ["SCORE OKC", "Free mentorship", "score.org"],
        ["i2E", "Help find funding, commercialize", "i2e.org"],
        ["SBA Oklahoma", "Federal small biz help", "sba.gov/district/oklahoma"],
        ["US Hispanic Chamber", "Hispanic biz network", "ushcc.com"],
    ]

    free_table = Table(free_help, colWidths=[1.3*inch, 2.2*inch, 2*inch])
    free_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(free_table)
    story.append(Spacer(1, 10))

    # WEEKLY CHECK-IN
    story.append(Paragraph("WEEKLY CHECK-IN (Every Sunday, 15 min)", section_style))

    weekly_data = [
        ["Check These Sites Weekly:"],
        ["[ ] sbir.gov/topics - New federal tech grants"],
        ["[ ] grants.gov - Check your email alerts"],
        ["[ ] okcommerce.gov - Oklahoma opportunities"],
        ["[ ] ushcc.com - Hispanic business opportunities"],
        ["[ ] Your email - Look for grant alert emails"],
    ]

    weekly_table = Table(weekly_data, colWidths=[6*inch])
    weekly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BOX', (0, 0), (-1, -1), 1, DARK_BLUE),
    ]))
    story.append(weekly_table)
    story.append(Spacer(1, 10))

    # KEY DATES
    story.append(Paragraph("KEY DATES TO REMEMBER", section_style))

    dates_data = [
        ["Month", "What to Watch For"],
        ["September", "Support Latino Grant opens"],
        ["October", "Many SBIR solicitations release"],
        ["January", "New fiscal year grants"],
        ["Spring", "Black Ambition Prize"],
        ["Anytime", "NSF Project Pitch (rolling)"],
        ["Anytime", "Comcast RISE (rolling)"],
    ]

    dates_table = Table(dates_data, colWidths=[1.2*inch, 4*inch])
    dates_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(dates_table)
    story.append(Spacer(1, 15))

    # NOTES SECTION
    story.append(Paragraph("GRANTS YOU FIND (Write Them Here)", section_style))

    notes_data = [
        ["Date", "Grant Name", "Amount", "Deadline", "Notes"],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
        ["", "", "", "", ""],
    ]

    notes_table = Table(notes_data, colWidths=[0.8*inch, 1.8*inch, 0.8*inch, 0.9*inch, 2*inch])
    notes_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(notes_table)
    story.append(Spacer(1, 15))

    # Bottom tip
    tip_data = [
        ["TIP: Ask Claude 'grant check-in' weekly to search for new opportunities"]
    ]
    tip_table = Table(tip_data, colWidths=[7*inch])
    tip_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(tip_table)

    doc.build(story)
    print(f"PDF created: {OUTPUT_FILE}")
    return OUTPUT_FILE

if __name__ == "__main__":
    create_tracker()
