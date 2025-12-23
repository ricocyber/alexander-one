#!/usr/bin/env python3
"""
Generate PDF guides for LUXX LOFTS presentation materials
- AI Image Prompts Guide
- Billionaire Pitch Script
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import HexColor
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Colors
CHARCOAL = HexColor('#2C2C2C')
WARM_GRAY = HexColor('#6B6560')
GOLD = HexColor('#C9A962')
LIGHT_BG = HexColor('#FAF8F5')
WHITE = HexColor('#FFFFFF')

def draw_header(c, page_w, page_h, title, subtitle=""):
    """Draw page header"""
    # Gold bar
    c.setFillColor(GOLD)
    c.rect(0, page_h - 80, page_w, 80, fill=1, stroke=0)

    # Title
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(50, page_h - 45, title)

    if subtitle:
        c.setFont("Helvetica", 12)
        c.drawString(50, page_h - 65, subtitle)

def draw_footer(c, page_w, page_h, page_num):
    """Draw page footer"""
    c.setFillColor(WARM_GRAY)
    c.setFont("Helvetica", 8)
    c.drawString(50, 30, "© 2024 Eric De Loera | De Loera Development")
    c.drawRightString(page_w - 50, 30, f"Page {page_num}")

def generate_prompts_pdf():
    """Generate AI Image Prompts PDF"""
    page_w, page_h = letter
    c = canvas.Canvas("/Users/ericdeloera/Downloads/luxx-haus 5/LUXX_AI_Image_Prompts.pdf", pagesize=letter)

    # Prompts data
    prompts = [
        ("EXTERIOR HERO SHOTS", [
            ("1. Main Building - Golden Hour (COVER)",
             "Luxury 4-story industrial loft building, modern corten steel facade with weathered rust patina, exposed red brick walls, large floor-to-ceiling black steel windows, rooftop deck with string lights and people socializing, Oklahoma City downtown skyline in background, golden hour sunset with orange and pink sky, architectural photography, photorealistic, 8k resolution, magazine quality, warm lighting"),
            ("2. Street View - Blackwelder Avenue",
             "Modern industrial apartment building street view, 4 stories, corten steel and brick exterior, ground floor retail space with large storefront windows, mature trees lining sidewalk, vintage street lamps, people walking dogs and cycling, urban neighborhood setting, late afternoon sun casting long shadows, architectural digest style photography, photorealistic"),
            ("3. Dramatic Night Shot",
             "Luxury loft building at night, warm interior lights glowing through large industrial windows, corten steel facade illuminated by uplighting, rooftop deck with string lights and fire pit, city lights in background, moody urban atmosphere, architectural photography, cinematic lighting, 8k"),
            ("4. Aerial/Drone View",
             "Aerial drone photograph of modern 4-story loft building, corten steel and brick construction, rooftop deck with outdoor furniture and greenery, surrounded by urban Oklahoma City neighborhood, downtown skyline 1 mile away, birds eye view, golden hour, real estate marketing photography, 8k"),
            ("5. Corner Building Shot",
             "Corner view of industrial modern apartment building, weathered corten steel panels contrasting with restored red brick, black metal balconies with cable railings, large divided-light windows, street level entrance with modern canopy, urban streetscape, architectural photography, overcast soft lighting, photorealistic"),
        ]),
        ("INTERIOR - THE MINIMALIST (540 SF)", [
            ("6. Main Living Space - Hero Shot",
             "Minimalist industrial loft apartment interior, polished concrete floors, 12-foot exposed beam ceilings, floor-to-ceiling windows with black steel frames, open concept living and kitchen, modern minimalist furniture in neutral tones, exposed brick accent wall, pendant lighting, natural daylight streaming in, architectural digest style, photorealistic, 8k"),
            ("7. Kitchen Detail",
             "Modern minimalist kitchen in industrial loft, white quartz countertops, matte black cabinet hardware, stainless steel appliances, open shelving with plants, polished concrete floors, exposed ductwork ceiling, large window with city view, clean lines, Scandinavian influence, interior design photography, natural lighting"),
            ("8. Bedroom Nook",
             "Cozy bedroom area in open loft apartment, platform bed with white linen bedding, exposed brick wall behind headboard, large industrial window with sheer curtains, polished concrete floor with natural fiber rug, minimalist nightstands, warm morning light, hygge aesthetic, interior photography, 8k"),
            ("9. Bathroom",
             "Modern industrial bathroom, walk-in rain shower with black frame glass enclosure, white subway tile walls, concrete floor, floating wood vanity with vessel sink, matte black fixtures, round mirror with black frame, small window, spa-like minimalist design, interior photography"),
        ]),
        ("INTERIOR - THE PENTHOUSE (1,080 SF)", [
            ("10. Penthouse Main Living",
             "Luxurious double-height loft penthouse, 1000 square feet open floor plan, polished concrete floors, two walls of floor-to-ceiling industrial windows, custom built-in shelving, designer furniture in earth tones, statement lighting fixture, exposed steel beams, downtown city view, luxury real estate photography, golden hour interior light, 8k"),
            ("11. Penthouse Kitchen",
             "High-end chef's kitchen in industrial penthouse loft, large center island with waterfall quartz countertop, professional-grade stainless appliances, custom wood cabinetry, open to living space, 12-foot ceilings with exposed ductwork, pendant lights over island, entertaining space, luxury interior photography"),
            ("12. Penthouse Master Suite",
             "Spacious master bedroom in luxury loft penthouse, king bed with upholstered headboard, sitting area by large industrial windows, walk-in closet visible, en-suite bathroom entry, polished concrete floors with plush area rug, minimalist artwork, soft neutral palette, morning light, luxury real estate photography"),
        ]),
        ("ROOFTOP DECK & AMENITIES", [
            ("13. Rooftop Deck - Entertaining",
             "Luxury rooftop deck on industrial loft building, outdoor sectional sofa, fire pit table, string lights overhead, potted plants and greenery, built-in BBQ area, Oklahoma City downtown skyline view at sunset, people socializing with wine glasses, warm evening atmosphere, lifestyle photography, 8k"),
            ("14. Rooftop - Sunrise Yoga",
             "Rooftop deck at sunrise, person doing yoga on mat, minimalist outdoor furniture, city skyline silhouette, soft pink and orange sky, peaceful urban morning, wellness lifestyle, architectural rooftop space, lifestyle photography"),
            ("15. Rooftop Night Party",
             "Rooftop party scene on luxury loft building, stylish young professionals mingling, string lights and ambient lighting, fire pit glowing, city lights twinkling in background, DJ setup in corner, sophisticated urban nightlife, lifestyle photography, warm tones"),
        ]),
        ("LOCATION & NEIGHBORHOOD", [
            ("16. Downtown OKC Skyline Connection",
             "Split image showing industrial loft building in foreground connected to Oklahoma City downtown skyline, 1 mile distance indicated, urban neighborhood street scene, emphasizing proximity to downtown, real estate marketing style, golden hour, photorealistic"),
            ("17. Neighborhood Street Scene",
             "Charming urban neighborhood street in Oklahoma City, tree-lined sidewalks, mix of historic brick buildings and modern infill, people at outdoor cafe, cyclists, walkable community vibe, late afternoon sun, lifestyle real estate photography"),
            ("18. Walking Distance Map",
             "Stylized 3D map showing loft building location with walking distance circles, downtown Oklahoma City landmarks visible, Bricktown, Scissortail Park, highlighting 1-mile radius walkability, modern infographic style, clean design"),
        ]),
        ("LIFESTYLE SHOTS", [
            ("19. Young Professional Morning",
             "Young professional in minimalist loft apartment, standing by large window with coffee, city view, modern industrial interior, morning light, polished concrete floors, aspirational lifestyle, editorial photography style"),
            ("20. Remote Work Setup",
             "Home office setup in industrial loft apartment, minimal desk by large window, modern ergonomic chair, laptop and monitor, plants, exposed brick wall, natural light, productive creative workspace, lifestyle photography"),
            ("21. Couple Entertaining",
             "Stylish couple hosting dinner party in open loft apartment, friends gathered around dining table, industrial modern interior, warm lighting, wine and food on table, exposed brick and concrete, urban sophisticated lifestyle, editorial photography"),
            ("22. Artist/Creative in Residence",
             "Artist working in bright industrial loft studio apartment, large canvases, natural light from floor-to-ceiling windows, creative mess organized, polished concrete floors, exposed beams, authentic creative lifestyle, documentary style photography"),
        ]),
        ("DETAIL SHOTS", [
            ("23. Corten Steel Texture",
             "Close-up macro photograph of weathered corten steel facade panel, beautiful rust patina patterns, architectural detail, texture study, warm orange and brown tones, high detail, 8k"),
            ("24. Brick and Steel Junction",
             "Architectural detail where restored red brick wall meets modern corten steel panel, contrast of materials, industrial modern design, construction detail, texture, natural lighting, architectural photography"),
            ("25. Window Detail",
             "Large industrial window detail, black steel frame with divided lights, interior warm glow visible, exterior view, modern loft building, architectural detail photography"),
        ]),
        ("INFOGRAPHIC STYLE", [
            ("26. Investment Returns Visual",
             "Modern clean infographic showing real estate investment returns, 15% ROI highlighted, rising graph, money and building icons, professional financial presentation style, dark background with gold accents, corporate elegant design"),
            ("27. Unit Comparison",
             "Side-by-side comparison infographic, two loft floor plans, square footage numbers, pricing, modern minimal design, white background, architectural line drawings with lifestyle photos, real estate marketing style"),
            ("28. Location Benefits",
             "Infographic showing location benefits, icons for walking distance, downtown proximity, neighborhood amenities, cost savings percentage, modern clean design, real estate marketing, professional presentation style"),
        ]),
    ]

    page_num = 1

    # Cover page
    c.setFillColor(CHARCOAL)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(page_w/2, page_h - 200, "LUXX LOFTS")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 24)
    c.drawCentredString(page_w/2, page_h - 250, "AI IMAGE GENERATION GUIDE")

    c.setFont("Helvetica", 14)
    c.drawCentredString(page_w/2, page_h - 320, "28 Copy-Paste Prompts for")
    c.drawCentredString(page_w/2, page_h - 340, "Midjourney • Canva AI • DALL-E • Stable Diffusion")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w/2, 150, "DE LOERA DEVELOPMENT")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, 130, "Eric De Loera")

    c.showPage()
    page_num += 1

    # Content pages
    y = page_h - 120
    margin = 50

    for section_title, section_prompts in prompts:
        # Check if we need a new page
        if y < 200:
            draw_footer(c, page_w, page_h, page_num)
            c.showPage()
            page_num += 1
            y = page_h - 120

        # Section header
        c.setFillColor(GOLD)
        c.rect(margin - 10, y - 5, page_w - 2*margin + 20, 25, fill=1, stroke=0)
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin, y, section_title)
        y -= 40

        for prompt_title, prompt_text in section_prompts:
            # Check space
            lines_needed = len(prompt_text) // 70 + 3
            space_needed = lines_needed * 12 + 30

            if y < space_needed + 50:
                draw_footer(c, page_w, page_h, page_num)
                c.showPage()
                page_num += 1
                y = page_h - 100

            # Prompt title
            c.setFillColor(CHARCOAL)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(margin, y, prompt_title)
            y -= 18

            # Prompt text box
            c.setFillColor(HexColor('#F5F5F5'))
            box_height = lines_needed * 12 + 10
            c.rect(margin, y - box_height + 10, page_w - 2*margin, box_height, fill=1, stroke=0)

            # Prompt text
            c.setFillColor(WARM_GRAY)
            c.setFont("Courier", 8)

            # Word wrap
            words = prompt_text.split()
            line = ""
            text_y = y
            for word in words:
                test_line = line + " " + word if line else word
                if len(test_line) > 85:
                    c.drawString(margin + 5, text_y, line)
                    text_y -= 11
                    line = word
                else:
                    line = test_line
            if line:
                c.drawString(margin + 5, text_y, line)

            y = y - box_height - 15

    # Tips page
    draw_footer(c, page_w, page_h, page_num)
    c.showPage()
    page_num += 1

    draw_header(c, page_w, page_h, "PRO TIPS", "Get the best results from AI image generators")

    y = page_h - 130

    tips = [
        ("MIDJOURNEY", [
            "Add --ar 16:9 for widescreen presentation slides",
            "Add --ar 9:16 for phone/social media vertical",
            "Add --ar 1:1 for square Instagram posts",
            "Add --v 6 for latest version",
            "Add --style raw for more photorealistic results",
        ]),
        ("CANVA AI", [
            "Generate multiple versions and pick the best",
            "Use 'Enhance' feature after generation",
            "Combine with Canva's templates for polished layouts",
        ]),
        ("DALL-E 3", [
            "Be very specific about materials and lighting",
            "Request 'architectural photography style' for realism",
        ]),
        ("COLOR CONSISTENCY", [
            "Always mention: 'Corten steel rust orange'",
            "Always mention: 'Warm red brick'",
            "Always mention: 'Black steel frames'",
            "Always mention: 'Golden hour warm lighting'",
            "Always mention: 'Polished concrete gray'",
        ]),
    ]

    for section, items in tips:
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(margin, y, section)
        y -= 20

        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 10)
        for item in items:
            c.drawString(margin + 15, y, f"• {item}")
            y -= 15

        y -= 15

    draw_footer(c, page_w, page_h, page_num)
    c.save()
    print("Generated: LUXX_AI_Image_Prompts.pdf")

def generate_pitch_pdf():
    """Generate Billionaire Pitch Script PDF"""
    page_w, page_h = letter
    c = canvas.Canvas("/Users/ericdeloera/Downloads/luxx-haus 5/LUXX_Billionaire_Pitch.pdf", pagesize=letter)

    margin = 50
    page_num = 1

    # Cover
    c.setFillColor(CHARCOAL)
    c.rect(0, 0, page_w, page_h, fill=1, stroke=0)

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 48)
    c.drawCentredString(page_w/2, page_h - 200, "LUXX LOFTS")

    c.setFillColor(WHITE)
    c.setFont("Helvetica", 24)
    c.drawCentredString(page_w/2, page_h - 250, "BILLIONAIRE PITCH SCRIPT")

    c.setFont("Helvetica", 14)
    c.drawCentredString(page_w/2, page_h - 320, "16-Slide Presentation Guide")
    c.drawCentredString(page_w/2, page_h - 340, "with Delivery Tips & Social Media Strategy")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(page_w/2, 150, "DE LOERA DEVELOPMENT")
    c.setFillColor(WHITE)
    c.setFont("Helvetica", 12)
    c.drawCentredString(page_w/2, 130, "Eric De Loera")

    c.showPage()
    page_num += 1

    # Slides
    slides = [
        ("SLIDE 1: OPENING IMPACT", "[Image: Hero Shot - Golden Hour Exterior]",
         '"What you\'re looking at is not just a building. It\'s the future of urban living in Oklahoma City."',
         "PAUSE - Let the image speak"),

        ("SLIDE 2: THE VISIONARY", "[Image: Your photo or De Loera Development logo]",
         '"I\'m Eric De Loera, founder of De Loera Development. I don\'t build apartments. I build movements."',
         ""),

        ("SLIDE 3: THE PROBLEM", "[Image: Expensive downtown apartments]",
         '"Oklahoma City is booming. Young professionals are flooding in. But here\'s the problem... Downtown living costs $2.85 to $3.00 per square foot. That prices out the exact people who make cities vibrant."',
         ""),

        ("SLIDE 4: THE OPPORTUNITY", "[Image: Location map - 1 mile to downtown]",
         '"One mile from downtown. That\'s 5 minutes. But that one mile? It\'s a 30% discount. Same lifestyle. Same access. 30% less."',
         "Deep Deuce: $2.85/SF | Midtown: $2.92/SF | LUXX LOFTS: $2.59/SF"),

        ("SLIDE 5: THE VISION", "[Image: Building exterior - dramatic angle]",
         '"LUXX LOFTS. Industrial heritage meets minimalist future. Corten steel that ages like fine wine. Brick that tells a story. This isn\'t a building - it\'s a statement."',
         ""),

        ("SLIDE 6: THE EXPERIENCE", "[Image: Street view from Blackwelder]",
         '"From Blackwelder Avenue, this building commands attention. It doesn\'t blend in. It stands out."',
         ""),

        ("SLIDE 7: THE MINIMALIST", "[Image: Interior - 540 SF unit]",
         '"540 square feet of intentional living. Not small - curated. Polished concrete. 12-foot ceilings. Floor-to-ceiling glass. Everything you need. Nothing you don\'t."',
         "$1,400/month"),

        ("SLIDE 8: THE PENTHOUSE", "[Image: Penthouse interior - 1,080 SF]",
         '"For those who want more - The Penthouse. Two units combined. 1,080 square feet of pure luxury."',
         "$2,600/month"),

        ("SLIDE 9: THE LIFESTYLE", "[Image: Young professional by window]",
         '"Our residents aren\'t just tenants. They\'re a community of creators, entrepreneurs, dreamers."',
         ""),

        ("SLIDE 10: THE ROOFTOP", "[Image: Rooftop entertaining at sunset]",
         '"Oklahoma City sunsets. Downtown skyline. Your private rooftop. This is where deals get made."',
         ""),

        ("SLIDE 11: THE NUMBERS", "[Image: Clean infographic with financials]",
         '"This isn\'t speculation. This is math."',
         "Units: 4 | Monthly: $7,600 | Annual: $91,200 | Cost: $280K | 5-Year ROI: 15.2%"),

        ("SLIDE 12: THE MARKET", "[Image: OKC skyline / growth stats]",
         '"Oklahoma City is the fastest-growing market nobody\'s talking about."',
         "Metro: 1.4M | Downtown growth: 8%/yr | Occupancy: 98%"),

        ("SLIDE 13: THE COMPETITIVE EDGE", "[Image: Side-by-side comparison]",
         '"We\'re not competing with luxury high-rises. We\'re creating a new category."',
         "Price: $2.59 vs $2.85+ | Character: Authentic vs Generic | Community: Curated vs Anonymous"),

        ("SLIDE 14: THE EXIT STRATEGY", "[Image: Building with appreciation arrow]",
         '"Three paths to profit: 1) Hold & Cash Flow - 15% returns 2) Refinance - Pull equity, repeat 3) Sell - 40% appreciation in 5 years"',
         ""),

        ("SLIDE 15: THE ASK", "[Image: Hero shot or night shot]",
         '"I\'m raising $280,000 to bring LUXX LOFTS to life. This is your chance to own a piece of Oklahoma City\'s future."',
         ""),

        ("SLIDE 16: THE CLOSE", "[Your photo / contact info]",
         '"I don\'t need investors who write checks. I need partners who see what I see. The question isn\'t whether this building gets built. It\'s whether you\'re part of it."',
         "Eric De Loera | De Loera Development"),
    ]

    draw_header(c, page_w, page_h, "THE PRESENTATION", "16 Slides to Close the Deal")
    y = page_h - 130

    for i, (title, image, script, note) in enumerate(slides):
        # Check space
        if y < 180:
            draw_footer(c, page_w, page_h, page_num)
            c.showPage()
            page_num += 1
            y = page_h - 100

        # Slide box
        c.setFillColor(HexColor('#F8F8F8'))
        c.rect(margin, y - 100, page_w - 2*margin, 110, fill=1, stroke=0)

        # Title
        c.setFillColor(GOLD)
        c.setFont("Helvetica-Bold", 11)
        c.drawString(margin + 10, y - 5, title)

        # Image note
        c.setFillColor(WARM_GRAY)
        c.setFont("Helvetica-Oblique", 8)
        c.drawString(margin + 10, y - 20, image)

        # Script
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica", 9)

        # Word wrap script
        words = script.split()
        line = ""
        text_y = y - 38
        for word in words:
            test_line = line + " " + word if line else word
            if len(test_line) > 90:
                c.drawString(margin + 10, text_y, line)
                text_y -= 12
                line = word
            else:
                line = test_line
        if line:
            c.drawString(margin + 10, text_y, line)

        # Note
        if note:
            c.setFillColor(GOLD)
            c.setFont("Helvetica-Bold", 8)
            c.drawString(margin + 10, y - 90, note)

        y -= 120

    draw_footer(c, page_w, page_h, page_num)
    c.showPage()
    page_num += 1

    # Delivery Tips page
    draw_header(c, page_w, page_h, "DELIVERY TIPS", "How to Present to Billionaires")
    y = page_h - 130

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "THE RULES")
    y -= 20

    rules = [
        "Confidence, not arrogance - You're sharing an opportunity, not begging",
        "Numbers back everything - Billionaires respect math",
        "Less is more - Don't over-explain. Let them ask questions",
        "Silence is power - After key points, PAUSE. Let it land",
        "Know your numbers cold - They WILL ask detailed questions",
        "Have the answer to 'Why you?' - Your story matters",
    ]

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 10)
    for rule in rules:
        c.drawString(margin + 15, y, f"• {rule}")
        y -= 16

    y -= 20
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "QUESTIONS TO PREPARE FOR")
    y -= 20

    questions = [
        "What's your experience in development?",
        "Why Oklahoma City?",
        "What happens if you can't fill the units?",
        "Who's your contractor? What's their track record?",
        "What's the timeline?",
        "What's the worst-case scenario?",
        "How is my investment protected?",
        "What's your skin in the game?",
    ]

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica", 10)
    for q in questions:
        c.drawString(margin + 15, y, f"• \"{q}\"")
        y -= 16

    y -= 20
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "THE SECRET")
    y -= 20

    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-Oblique", 12)
    c.drawString(margin, y, "Billionaires don't invest in buildings. They invest in people.")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(margin, y, "Your conviction, your vision, your story - that's what closes the deal.")

    draw_footer(c, page_w, page_h, page_num)
    c.showPage()
    page_num += 1

    # Social Media page
    draw_header(c, page_w, page_h, "SOCIAL MEDIA STRATEGY", "The Road to 1 Million Followers")
    y = page_h - 130

    pillars = [
        ("THE BUILD (40%)", "Site visits, material selections, behind-the-scenes, problem solving"),
        ("THE VISION (30%)", "Why minimalism matters, future of urban living, OKC potential, your journey"),
        ("THE LIFESTYLE (20%)", "Renderings, design inspiration, resident lifestyle, neighborhood content"),
        ("THE EDUCATION (10%)", "Real estate basics, development process, market analysis, entrepreneurship"),
    ]

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "CONTENT PILLARS")
    y -= 20

    for title, desc in pillars:
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin + 15, y, title)
        y -= 14
        c.setFillColor(WARM_GRAY)
        c.setFont("Helvetica", 9)
        c.drawString(margin + 30, y, desc)
        y -= 18

    y -= 15
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "PLATFORM STRATEGY")
    y -= 20

    platforms = [
        ("Instagram", "Reels (30-60 sec), carousels, stories, highlights"),
        ("TikTok", "Raw content, day-in-the-life, comment responses"),
        ("LinkedIn", "Professional updates, investment philosophy, market analysis"),
        ("YouTube", "Long-form documentaries, Q&A sessions, market deep dives"),
    ]

    for platform, strategy in platforms:
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(margin + 15, y, platform)
        c.setFillColor(WARM_GRAY)
        c.setFont("Helvetica", 9)
        c.drawString(margin + 100, y, strategy)
        y -= 16

    y -= 20
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(margin, y, "WEEKLY CONTENT CALENDAR")
    y -= 20

    calendar = [
        ("Monday", "Motivation / Vision"),
        ("Tuesday", "Build Update"),
        ("Wednesday", "Design / Architecture"),
        ("Thursday", "Education / Tips"),
        ("Friday", "Behind the Scenes"),
        ("Saturday", "Lifestyle / OKC"),
        ("Sunday", "Week Recap / Plans"),
    ]

    for day, content in calendar:
        c.setFillColor(CHARCOAL)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(margin + 15, y, day)
        c.setFillColor(WARM_GRAY)
        c.setFont("Helvetica", 9)
        c.drawString(margin + 100, y, content)
        y -= 14

    y -= 25
    c.setFillColor(CHARCOAL)
    c.setFont("Helvetica-BoldOblique", 11)
    c.drawCentredString(page_w/2, y, '"The greatest creators don\'t just build buildings.')
    y -= 14
    c.drawCentredString(page_w/2, y, 'They build movements, communities, legacies."')

    draw_footer(c, page_w, page_h, page_num)
    c.save()
    print("Generated: LUXX_Billionaire_Pitch.pdf")

if __name__ == "__main__":
    generate_prompts_pdf()
    generate_pitch_pdf()
    print("\n✓ Both PDF guides generated successfully!")
