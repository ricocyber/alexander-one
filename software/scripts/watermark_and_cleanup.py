#!/usr/bin/env python3
"""
Watermark keeper PDFs and remove duplicate files
De Loera Development - File Cleanup
"""

import os
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor, Color
from io import BytesIO

BASE_DIR = "/Users/ericdeloera/Downloads/luxx-haus 5"

# Files to DELETE (duplicates/outdated)
FILES_TO_DELETE = [
    # I.H.P. duplicates (all merged into IHP_COMPLETE_SECURED.pdf)
    "IHP_Data_Sources.pdf",
    "IHP_Demo_Report.pdf",
    "IHP_Market_Research_Report.pdf",
    "IHP_Verified_Data_Report.pdf",
    "IHP_VERIFIED_Final.pdf",
    "IHP_Visual_Explainer.pdf",

    # Real Estate duplicates
    "DeLoera_Development_Concepts.pdf",
    "DeloeraDevelopement_4801 n blackwelder .pdf",
    "LUXX_LOFTS_4801_Blackwelder.pdf",
    "LUXX_LOFTS_CAD_Professional.pdf",
    "LUXX_HAUS_water_Demo_Report.pdf",
]

# Scripts to DELETE (old drafts - keeping only final versions)
SCRIPTS_TO_DELETE = [
    "scripts/generate_ihp_data_report.py",
    "scripts/generate_ihp_final_verified.py",
    "scripts/generate_ihp_sources.py",
    "scripts/generate_ihp_verified_data.py",
    "scripts/generate_ihp_visual.py",
    "scripts/generate_demo_report.py",
    "scripts/generate_standalone_report.py",
    "scripts/generate_luxx_lofts.py",
    "scripts/generate_luxx_lofts_enhanced.py",
    "scripts/generate_luxx_cad_professional.py",
    "scripts/generate_deloera_developments.py",
    "scripts/generate_professional_renderings.py",
]

# Files to WATERMARK (keep these)
IHP_FILES_TO_WATERMARK = [
    ("IHP_Hardware_Technical_Spec.pdf", "I.H.P. CONFIDENTIAL"),
    ("IHP_Tesla_Pitch.pdf", "I.H.P. CONFIDENTIAL"),
]

REAL_ESTATE_FILES_TO_WATERMARK = [
    ("LUXX_LOFTS_Complete_Package.pdf", "DE LOERA DEVELOPMENT - CONFIDENTIAL"),
    ("LUXX_LOFTS_Investor_Package.pdf", "DE LOERA DEVELOPMENT - CONFIDENTIAL"),
    ("LUXX_LOFTS_Tenant_Brochure.pdf", "LUXX LOFTS"),
    ("DeLoera_4801_Golden_Ratio.pdf", "DE LOERA DEVELOPMENT - CONFIDENTIAL"),
    ("LUXX_AI_Image_Prompts.pdf", "DE LOERA DEVELOPMENT"),
    ("LUXX_Billionaire_Pitch.pdf", "DE LOERA DEVELOPMENT - CONFIDENTIAL"),
]

def create_watermark_pdf(text, page_size):
    """Create a watermark PDF overlay"""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=page_size)

    page_w, page_h = page_size

    # Diagonal watermark - light gray, semi-transparent
    c.saveState()
    c.translate(page_w/2, page_h/2)
    c.rotate(45)
    c.setFillColor(Color(0.7, 0.7, 0.7, alpha=0.15))
    c.setFont("Helvetica-Bold", 40)
    c.drawCentredString(0, 0, text)
    c.restoreState()

    # Footer watermark
    c.setFillColor(Color(0.3, 0.3, 0.3, alpha=0.5))
    c.setFont("Helvetica", 8)
    c.drawString(40, 20, f"© 2024 De Loera Development | {text}")
    c.drawRightString(page_w - 40, 20, "Proprietary & Confidential")

    c.save()
    packet.seek(0)
    return PdfReader(packet)

def watermark_pdf(input_path, output_path, watermark_text):
    """Add watermark to existing PDF"""
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()

        for page in reader.pages:
            # Get page size
            page_box = page.mediabox
            page_size = (float(page_box.width), float(page_box.height))

            # Create watermark for this page
            watermark_pdf_obj = create_watermark_pdf(watermark_text, page_size)
            watermark_page = watermark_pdf_obj.pages[0]

            # Merge watermark onto page
            page.merge_page(watermark_page)
            writer.add_page(page)

        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

        return True
    except Exception as e:
        print(f"  ERROR watermarking {input_path}: {e}")
        return False

def main():
    print("=" * 70)
    print("DE LOERA DEVELOPMENT - FILE CLEANUP & WATERMARKING")
    print("=" * 70)

    # Step 1: Delete duplicate files
    print("\n📁 REMOVING DUPLICATE PDFs...")
    deleted_count = 0
    for filename in FILES_TO_DELETE:
        filepath = os.path.join(BASE_DIR, filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"  ✓ Deleted: {filename}")
            deleted_count += 1
        else:
            print(f"  - Not found: {filename}")

    # Step 2: Delete old scripts
    print("\n📜 REMOVING OLD SCRIPTS...")
    for script in SCRIPTS_TO_DELETE:
        filepath = os.path.join(BASE_DIR, script)
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"  ✓ Deleted: {script}")
            deleted_count += 1
        else:
            print(f"  - Not found: {script}")

    # Step 3: Watermark I.H.P. files
    print("\n🔒 WATERMARKING I.H.P. FILES...")
    watermarked_count = 0
    for filename, watermark_text in IHP_FILES_TO_WATERMARK:
        input_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(input_path):
            # Watermark in place (backup first)
            temp_path = input_path + ".tmp"
            if watermark_pdf(input_path, temp_path, watermark_text):
                os.replace(temp_path, input_path)
                print(f"  ✓ Watermarked: {filename}")
                watermarked_count += 1
        else:
            print(f"  - Not found: {filename}")

    # Step 4: Watermark Real Estate files
    print("\n🏠 WATERMARKING REAL ESTATE FILES...")
    for filename, watermark_text in REAL_ESTATE_FILES_TO_WATERMARK:
        input_path = os.path.join(BASE_DIR, filename)
        if os.path.exists(input_path):
            temp_path = input_path + ".tmp"
            if watermark_pdf(input_path, temp_path, watermark_text):
                os.replace(temp_path, input_path)
                print(f"  ✓ Watermarked: {filename}")
                watermarked_count += 1
        else:
            print(f"  - Not found: {filename}")

    # Summary
    print("\n" + "=" * 70)
    print("CLEANUP COMPLETE")
    print("=" * 70)
    print(f"\n  Files deleted: {deleted_count}")
    print(f"  Files watermarked: {watermarked_count}")

    print("\n📂 FINAL FILE STRUCTURE:")
    print("\n  I.H.P. (Intelligent Home Protection):")
    print("    • IHP_COMPLETE_SECURED.pdf (master document)")
    print("    • IHP_Hardware_Technical_Spec.pdf")
    print("    • IHP_Tesla_Pitch.pdf")

    print("\n  REAL ESTATE (LUXX LOFTS / 4801 Blackwelder):")
    print("    • LUXX_LOFTS_Complete_Package.pdf")
    print("    • LUXX_LOFTS_Investor_Package.pdf")
    print("    • LUXX_LOFTS_Tenant_Brochure.pdf")
    print("    • DeLoera_4801_Golden_Ratio.pdf")
    print("    • LUXX_AI_Image_Prompts.pdf")
    print("    • LUXX_Billionaire_Pitch.pdf")

    print("\n  SCRIPTS (Essential only):")
    print("    • generate_ihp_complete_secured.py")
    print("    • generate_luxx_complete_package.py")
    print("    • generate_investor_tenant_docs.py")
    print("    • generate_golden_ratio_building.py")
    print("    • generate_hardware_tech_doc.py")
    print("    • generate_tesla_pitch.py")
    print("    • generate_market_research_pdf.py")
    print("    • generate_presentation_guide.py")
    print("    • generate_hardware_renders.py")
    print("    • create_logo.py")
    print("    • watermark_and_cleanup.py")

    print("\n  SOURCE CODE (Backend):")
    print("    • cmd/, internal/, ml/, pkg/, web/")
    print("    • luxx-api (compiled binary)")
    print("    • configs/, migrations/, infrastructure/")

    print("\n  DOCS:")
    print("    • AI_IMAGE_PROMPTS.md")
    print("    • BILLIONAIRE_PITCH_SCRIPT.md")
    print("    • docs/DeLoera_Portfolio_Strategy.md")
    print("    • docs/IHP_Market_Research_Data.md")

    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
