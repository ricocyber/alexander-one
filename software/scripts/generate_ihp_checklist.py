#!/usr/bin/env python3
"""
Generate I.H.P. Action Checklist PDF for Eric
Simple, printable checklist to stay organized
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
import os

# Output path
OUTPUT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "IHP_Action_Checklist.pdf")

# Colors
DARK_BLUE = HexColor('#1a365d')
TEAL = HexColor('#0d9488')
LIGHT_GRAY = HexColor('#f3f4f6')
MEDIUM_GRAY = HexColor('#6b7280')

def create_checklist():
    doc = SimpleDocTemplate(
        OUTPUT_FILE,
        pagesize=letter,
        rightMargin=0.5*inch,
        leftMargin=0.5*inch,
        topMargin=0.5*inch,
        bottomMargin=0.5*inch
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'Title',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=DARK_BLUE,
        spaceAfter=6,
        alignment=1  # Center
    )

    subtitle_style = ParagraphStyle(
        'Subtitle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=MEDIUM_GRAY,
        spaceAfter=20,
        alignment=1
    )

    section_style = ParagraphStyle(
        'Section',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=TEAL,
        spaceBefore=15,
        spaceAfter=8,
        borderPadding=5
    )

    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=11,
        spaceAfter=6,
        leading=14
    )

    small_style = ParagraphStyle(
        'Small',
        parent=styles['Normal'],
        fontSize=9,
        textColor=MEDIUM_GRAY,
        spaceAfter=4
    )

    story = []

    # Title
    story.append(Paragraph("I.H.P. ACTION CHECKLIST", title_style))
    story.append(Paragraph("Your Step-by-Step Guide to Getting Funded", subtitle_style))
    story.append(Paragraph(f"Created: {datetime.now().strftime('%B %d, %Y')}", small_style))
    story.append(Spacer(1, 10))

    # Current Status Box
    status_data = [
        ["YOUR CURRENT STATUS"],
        ["Money for I.H.P.: $0"],
        ["Grants Received: $0"],
        ["Applications Ready: 3 (Comcast RISE, StitchCrew, NSF SBIR)"],
    ]
    status_table = Table(status_data, colWidths=[7*inch])
    status_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, DARK_BLUE),
    ]))
    story.append(status_table)
    story.append(Spacer(1, 15))

    # PHASE 0: THIS WEEK
    story.append(Paragraph("PHASE 0: THIS WEEK (All Free)", section_style))

    week1_tasks = [
        ["Done", "Task", "Website/Notes"],
        ["[X]", "Get D-U-N-S Number", "DONE: 136342147"],
        ["[ ]", "Start SAM.gov Registration", "sam.gov (need D-U-N-S first)"],
        ["[ ]", "Contact Joe Hobart - Get YES or NO", "Need hardware partner decision"],
        ["[ ]", "Submit Comcast RISE Application", "Check if ready, find submit button"],
        ["[ ]", "Submit StitchCrew Application", "Check if ready, find submit button"],
        ["[ ]", "Call Oklahoma SBDC", "Free business help - google 'Oklahoma SBDC'"],
    ]

    task_table = Table(week1_tasks, colWidths=[0.5*inch, 2.5*inch, 4*inch])
    task_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(task_table)
    story.append(Spacer(1, 15))

    # PHASE 1: AFTER SAM.GOV (2-4 weeks)
    story.append(Paragraph("PHASE 1: AFTER SAM.GOV APPROVED (2-4 Weeks)", section_style))

    phase1_tasks = [
        ["Done", "Task", "Notes"],
        ["[ ]", "Submit NSF Project Pitch", "seedfund.nsf.gov - copy/paste from your doc"],
        ["[ ]", "Join SCORE.org for mentorship", "score.org - FREE mentors"],
        ["[ ]", "Research Flo by Moen (competitor)", "Understand what they do"],
        ["[ ]", "Research Ting/Whisker Labs", "Understand electrical monitoring"],
        ["[ ]", "Make list of insurance contacts", "Anyone you know in insurance?"],
    ]

    phase1_table = Table(phase1_tasks, colWidths=[0.5*inch, 2.5*inch, 4*inch])
    phase1_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(phase1_table)
    story.append(Spacer(1, 15))

    # PHASE 2: WAITING FOR NSF RESPONSE
    story.append(Paragraph("PHASE 2: WAITING FOR NSF (1-2 Months)", section_style))

    phase2_tasks = [
        ["Done", "Task", "Notes"],
        ["[ ]", "Keep talking to hardware partners", "Don't stop at just Joe"],
        ["[ ]", "Learn Matter/Thread basics", "YouTube videos, free resources"],
        ["[ ]", "Visit local hardware store", "Look at smart home products"],
        ["[ ]", "Talk to any insurance agents you know", "Get their perspective"],
        ["[ ]", "Review your SBIR full application outline", "Be ready if NSF invites you"],
    ]

    phase2_table = Table(phase2_tasks, colWidths=[0.5*inch, 2.5*inch, 4*inch])
    phase2_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('ALIGN', (0, 0), (0, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(phase2_table)
    story.append(Spacer(1, 15))

    # GRANT TRACKER
    story.append(Paragraph("GRANT TRACKER", section_style))

    grant_data = [
        ["Grant", "Amount", "Status", "Deadline", "Submitted?"],
        ["Comcast RISE", "$25,000", "App Ready", "Check website", "[ ]"],
        ["StitchCrew", "$25,000", "App Ready", "Check website", "[ ]"],
        ["NSF SBIR Phase I", "$274,000", "Need SAM.gov", "Rolling", "[ ]"],
        ["DOE SBIR", "$274,000", "Outline done", "Check SBIR.gov", "[ ]"],
        ["DHS SBIR", "$274,000", "Outline done", "Check SBIR.gov", "[ ]"],
    ]

    grant_table = Table(grant_data, colWidths=[1.5*inch, 1*inch, 1.2*inch, 1.3*inch, 1*inch])
    grant_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(grant_table)
    story.append(Spacer(1, 15))

    # IMPORTANT REGISTRATIONS
    story.append(Paragraph("REQUIRED REGISTRATIONS", section_style))

    reg_data = [
        ["Registration", "Website", "Status", "Date Done"],
        ["D-U-N-S Number", "dnb.com", "[X] Done", "136342147"],
        ["SAM.gov", "sam.gov", "[ ] Done", "_________"],
        ["SBIR.gov Account", "sbir.gov", "[ ] Done", "_________"],
        ["NSF Account", "seedfund.nsf.gov", "[ ] Done", "_________"],
        ["Grants.gov", "grants.gov", "[ ] Done", "_________"],
    ]

    reg_table = Table(reg_data, colWidths=[1.5*inch, 2*inch, 1*inch, 1.5*inch])
    reg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ALIGN', (2, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(reg_table)
    story.append(Spacer(1, 15))

    # KEY CONTACTS
    story.append(Paragraph("KEY CONTACTS TO TRACK", section_style))

    contact_data = [
        ["Who", "Role", "Phone/Email", "Status"],
        ["Joe Hobart", "Hardware Partner?", "_____________", "[ ] Yes [ ] No"],
        ["Oklahoma SBDC", "Free Business Help", "_____________", "[ ] Called"],
        ["SCORE Mentor", "Free Mentorship", "_____________", "[ ] Assigned"],
        ["___________", "Insurance Contact", "_____________", "[ ] Contacted"],
        ["___________", "Other HW Engineer", "_____________", "[ ] Contacted"],
    ]

    contact_table = Table(contact_data, colWidths=[1.5*inch, 1.5*inch, 2*inch, 1.5*inch])
    contact_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), DARK_BLUE),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.gray),
        ('PADDING', (0, 0), (-1, -1), 5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, LIGHT_GRAY]),
    ]))
    story.append(contact_table)
    story.append(Spacer(1, 20))

    # QUICK REFERENCE - What is I.H.P.?
    story.append(Paragraph("QUICK REFERENCE: WHAT IS I.H.P.?", section_style))

    ihp_summary = """
    <b>The Problem:</b> Houses get damaged by water, fire, electrical issues = $27 BILLION/year in losses<br/><br/>
    <b>Your Solution:</b> 5 sensors that talk to each other and predict problems BEFORE they happen<br/><br/>
    <b>Why It's Different:</b> Competitors only watch ONE thing. You watch EVERYTHING and connect the dots.<br/><br/>
    <b>Who Pays:</b> Insurance companies (they're desperate - 7 years of losses)<br/><br/>
    <b>Your Edge:</b> You actually BUILD houses. Most tech people don't understand how homes fail.
    """
    story.append(Paragraph(ihp_summary, body_style))
    story.append(Spacer(1, 15))

    # Bottom reminder
    reminder_data = [
        ["REMEMBER: You only need to do 3 things right now"],
        ["1. Get D-U-N-S and SAM.gov registered (FREE)"],
        ["2. Submit your grant applications"],
        ["3. Get a YES or NO from a hardware partner"],
        ["Everything else can wait until you have money."],
    ]
    reminder_table = Table(reminder_data, colWidths=[7*inch])
    reminder_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), TEAL),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BACKGROUND', (0, 1), (-1, -1), LIGHT_GRAY),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('BOX', (0, 0), (-1, -1), 1, TEAL),
    ]))
    story.append(reminder_table)

    # Build PDF
    doc.build(story)
    print(f"PDF created: {OUTPUT_FILE}")
    return OUTPUT_FILE

if __name__ == "__main__":
    create_checklist()
