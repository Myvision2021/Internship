"""
generate_brochure_pdf.py
Generates an ultra-elegant, premium A4 PDF brochure for
Ikon Computer Education & Training Institute
"""
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

# ── Elegant Palette ───────────────────────────────────────────────────
CHARCOAL = HexColor("#1c1e21")
SLATE = HexColor("#2d3748")
GOLD = HexColor("#d4af37")
LIGHT_GOLD = HexColor("#f9f6ef")
GREY_TEXT = HexColor("#4a5568")
LIGHT_GREY = HexColor("#f7fafc")
BORDER_COLOR = HexColor("#e2e8f0")
WHITE = white

OUT_PATH = Path(__file__).parent / "brochure.pdf"
PAGE_W, PAGE_H = A4

def draw_background(canv, doc):
    canv.saveState()
    
    # Elegant top header block
    canv.setFillColor(CHARCOAL)
    canv.rect(0, PAGE_H - 120, PAGE_W, 120, fill=1, stroke=0)
    
    # Thin gold accent line below header
    canv.setFillColor(GOLD)
    canv.rect(0, PAGE_H - 123, PAGE_W, 3, fill=1, stroke=0)
    
    # Header Text
    canv.setFillColor(WHITE)
    canv.setFont("Helvetica-Bold", 18)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 50, "IKON COMPUTER EDUCATION & TRAINING INSTITUTE")
    
    canv.setFillColor(GOLD)
    canv.setFont("Helvetica", 10)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 72, "S U M M E R   I N T E R N S H I P   P R O G R A M   2 0 2 6")
    
    canv.setFillColor(HexColor("#a0aec0"))
    canv.setFont("Helvetica-Oblique", 9)
    canv.drawCentredString(PAGE_W / 2, PAGE_H - 95, "An ISO 9001:2015 & MSME Certified Institute")
    
    # Footer block
    canv.setFillColor(CHARCOAL)
    canv.rect(0, 0, PAGE_W, 50, fill=1, stroke=0)
    
    # Footer text
    canv.setFillColor(WHITE)
    canv.setFont("Helvetica", 8)
    canv.drawCentredString(PAGE_W / 2, 28, "29, Karbala Tank Lane, Kolkata – 700 006 (Near Punjab National Bank, Manicktala Branch)")
    
    canv.setFillColor(GOLD)
    canv.drawCentredString(PAGE_W / 2, 14, "Phone: +91 8240159300 / +91 8100789377   |   Email: pathakindra2006@gmail.com   |   Web: www.ikoncomp.co.in")
    
    # Page number
    canv.setFillColor(HexColor("#a0aec0"))
    canv.setFont("Helvetica", 7)
    canv.drawRightString(PAGE_W - 20, 20, f"Page {doc.page}")
    
    canv.restoreState()

def make_styles():
    st = getSampleStyleSheet()
    
    def s(name, **kw):
        return ParagraphStyle(name, **kw)
        
    return dict(
        h1 = s("H1", fontName="Helvetica-Bold", fontSize=14, textColor=CHARCOAL, spaceBefore=20, spaceAfter=10, leading=16, textTransform="uppercase", letterSpacing=1),
        course_title = s("CT", fontName="Helvetica-Bold", fontSize=12, textColor=SLATE, leading=16),
        course_desc = s("CD", fontName="Helvetica", fontSize=9, textColor=GREY_TEXT, leading=14),
        bullet = s("BL", fontName="Helvetica", fontSize=10, textColor=SLATE, leading=18, leftIndent=15, spaceBefore=4),
        contact_txt = s("CXT", fontName="Helvetica", fontSize=10, textColor=CHARCOAL, leading=18, alignment=TA_CENTER)
    )

def build_pdf():
    doc = SimpleDocTemplate(
        str(OUT_PATH), pagesize=A4,
        leftMargin=25*mm, rightMargin=25*mm,
        topMargin=135, bottomMargin=65,
        title="Ikon Internship Brochure",
        author="Ikon Computer Education"
    )
    
    st = make_styles()
    buf = []
    
    def section(title):
        buf.append(Paragraph(title, st["h1"]))
        buf.append(HRFlowable(width="100%", thickness=1, color=GOLD, spaceAfter=15, spaceBefore=0))

    # --- Courses ---
    section("COURSES OFFERED:")
    
    courses = [
        "1. Java Programming (30 Days)",
        "2. Python Development (30 Days)",
        "3. Database Management Systems (30 Days)",
        "4. Computer Networking (30 Days)"
    ]
    
    for c in courses:
        buf.append(Paragraph(c, st["course_title"]))
        buf.append(Spacer(1, 10))
        
    buf.append(Spacer(1, 15))

    # --- Highlights ---
    section("HIGHLIGHTS:")
    
    hl = [
        "MSME Verified & ISO Certified",
        "Offer Letter Provided",
        "Government-Recognized Certificate",
        "Expert Mentorship",
        "Major Project",
        "Placement Support"
    ]
    
    for h in hl:
        buf.append(Paragraph(f"- {h}", st["bullet"]))
        
    buf.append(Spacer(1, 40))
    
    # --- Contact ---
    section("CONTACT:")
    
    buf.append(Paragraph("Contact: +91 8240159300", st["course_title"]))
    buf.append(Paragraph("Email: pathakindra2006@gmail.com", st["course_title"]))
    buf.append(Paragraph("Website: www.ikoncomp.co.in", st["course_title"]))
    
    buf.append(Spacer(1, 40))
    buf.append(Paragraph("© 2026 Ikon Computer Education & Training Institute", st["course_desc"]))
    
    doc.build(buf, onFirstPage=draw_background, onLaterPages=draw_background)
    print(f"PDF saved -> {OUT_PATH}")

if __name__ == "__main__":
    build_pdf()

