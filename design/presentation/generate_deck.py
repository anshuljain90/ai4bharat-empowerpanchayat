#!/usr/bin/env python3
"""
Generate eGramSabha Hackathon Submission Deck.
Opens the template PPTX, replaces content on each of 14 slides.

Usage:
    python generate_deck.py
    # Outputs: ../../design/eGramSabha_Hackathon_Submission.pptx
"""
import os
import sys

# Add this directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

from styles import (
    DARK_TEXT, WHITE, GREEN_PRIMARY, GREEN_LIGHT, ORANGE_ACCENT,
    BLUE_AWS, BLUE_LIGHT, GRAY_MED, RED_URGENT, YELLOW_READY,
    TABLE_HEADER_BG, TABLE_ALT_BG, GRAY_LIGHT,
    FONT_TITLE, FONT_BODY, FONT_MONO,
    SIZE_SLIDE_TITLE, SIZE_SUBTITLE, SIZE_BODY, SIZE_BODY_SMALL,
    SIZE_TABLE, SIZE_TABLE_HEADER, SIZE_CAPTION, SIZE_BIG_STAT,
    CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, CONTENT_HEIGHT,
    set_font, add_titled_textbox, add_bullet_point, add_paragraph,
    style_table, set_cell_text,
)
from content import (
    SLIDE1, SLIDE2, SLIDE3A, SLIDE3B, SLIDE3C, SLIDE3D,
    SLIDE4, SLIDE5, SLIDE6, SLIDE7, SLIDE8, SLIDE9,
    SLIDE10, SLIDE11, SLIDE12, SLIDE13, SLIDE14,
)

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "..", ".."))
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "design", "Prototype Development Submission _ AWS AI for Bharat Hackathon.pptx")
OUTPUT_PATH = os.path.join(PROJECT_ROOT, "design", "eGramSabha_Hackathon_Submission.pptx")
LOGO_PATH = os.path.join(SCRIPT_DIR, "assets", "logo.png")
SCREENSHOTS_DIR = os.path.join(SCRIPT_DIR, "screenshots")
DIAGRAMS_DIR = os.path.join(SCRIPT_DIR, "diagrams")


def diagram_path(name):
    """Get path to a rendered diagram PNG."""
    p = os.path.join(DIAGRAMS_DIR, f"{name}.png")
    return p if os.path.exists(p) else None


def clear_slide_text(slide):
    """Remove all text boxes from a slide (keep background picture)."""
    shapes_to_remove = []
    for shape in slide.shapes:
        if shape.shape_type == 17:  # TEXT_BOX
            shapes_to_remove.append(shape)
    for shape in shapes_to_remove:
        sp = shape._element
        sp.getparent().remove(sp)


def add_textbox(slide, left, top, width, height, word_wrap=True):
    """Add a text box and return its text frame."""
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = word_wrap
    return tf


def add_table(slide, rows, cols, left, top, width, height):
    """Add a table to the slide."""
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    return table_shape.table


def add_flow_box(slide, left, top, width, height, text, fill_color=GREEN_PRIMARY, text_color=WHITE):
    """Add a rounded rectangle box for flow diagrams."""
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    tf = shape.text_frame
    tf.word_wrap = True
    tf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run = tf.paragraphs[0].add_run()
    run.text = text
    set_font(run, size=Pt(9), bold=True, color=text_color)
    return shape


def add_arrow(slide, left, top, width):
    """Add a right arrow connector."""
    shape = slide.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, left, top, width, Inches(0.25))
    shape.fill.solid()
    shape.fill.fore_color.rgb = GRAY_MED
    shape.line.fill.background()
    return shape


# ============================================================
# SLIDE BUILDERS
# ============================================================

def build_slide1(slide):
    """Team & Project Info."""
    clear_slide_text(slide)

    # Logo
    if os.path.exists(LOGO_PATH):
        slide.shapes.add_picture(LOGO_PATH, Inches(0.3), Inches(0.2), Inches(1.2), Inches(1.2))

    # Project name
    tf = add_textbox(slide, Inches(1.7), Inches(0.3), Inches(7.5), Inches(1.0))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "eGramSabha"
    set_font(run, size=Pt(36), bold=True, color=GREEN_PRIMARY)
    add_paragraph(tf, "AI-Powered Digital Gram Sabha Platform", size=Pt(16), color=GRAY_MED)

    # Team info boxes
    y_start = Inches(2.0)
    tf2 = add_textbox(slide, Inches(0.5), y_start, Inches(9.0), Inches(2.5))
    add_paragraph(tf2, "Team Name:  Empower Panchayat", size=Pt(18), bold=True, color=DARK_TEXT,
                  space_before=Pt(8), space_after=Pt(8))
    add_paragraph(tf2, "Team Leader Name:  (see submission form)", size=Pt(18), bold=True, color=DARK_TEXT,
                  space_before=Pt(8), space_after=Pt(8))
    add_paragraph(tf2, "Problem Statement:  AI-Powered Digital Gram Sabha Platform", size=Pt(18), bold=True, color=DARK_TEXT,
                  space_before=Pt(8), space_after=Pt(8))

    # Footer
    tf3 = add_textbox(slide, Inches(0.5), Inches(4.8), Inches(9.0), Inches(0.5))
    p = tf3.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "empowerpanchayat.org  |  Apache 2.0 Open Source  |  \"Sashakt Panchayat, Samriddh Bharat\""
    set_font(run, size=Pt(10), color=GRAY_MED, italic=True)


def build_slide2(slide):
    """Problem Statement."""
    clear_slide_text(slide)
    d = SLIDE2

    # Title
    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.5))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Headline
    tf2 = add_textbox(slide, CONTENT_LEFT, Inches(1.4), CONTENT_WIDTH, Inches(0.6))
    p = tf2.paragraphs[0]
    run = p.add_run()
    run.text = d["headline"]
    set_font(run, size=Pt(10), color=DARK_TEXT, italic=True)

    # Stats row
    stat_width = Inches(1.7)
    stat_height = Inches(0.8)
    stat_y = Inches(2.05)
    colors = [RED_URGENT, ORANGE_ACCENT, BLUE_LIGHT, GREEN_PRIMARY, RGBColor(0x75, 0x75, 0x75)]
    for i, (stat, label) in enumerate(d["stats"]):
        x = Inches(0.4 + i * 1.9)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, stat_y, stat_width, stat_height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = colors[i % len(colors)]
        shape.line.fill.background()
        tf_stat = shape.text_frame
        tf_stat.word_wrap = True
        p = tf_stat.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = stat
        set_font(run, size=Pt(20), bold=True, color=WHITE)
        p2 = tf_stat.add_paragraph()
        p2.alignment = PP_ALIGN.CENTER
        run2 = p2.add_run()
        run2.text = label
        set_font(run2, size=Pt(7), color=WHITE)

    # Barriers table
    table = add_table(slide, len(d["barriers"]) + 1, 2,
                       Inches(0.4), Inches(3.0), Inches(9.2), Inches(2.2))
    set_cell_text(table, 0, 0, "Barrier", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 1, "Impact", SIZE_TABLE_HEADER, True, WHITE)
    for i, (barrier, impact) in enumerate(d["barriers"]):
        set_cell_text(table, i + 1, 0, barrier)
        set_cell_text(table, i + 1, 1, impact)
    style_table(table)
    # Set column widths
    table.columns[0].width = Inches(4.0)
    table.columns[1].width = Inches(5.2)


def build_slide3(slide):
    """Brief About the Idea - Solution + Why AI."""
    clear_slide_text(slide)

    # Title
    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Brief About the Idea"
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Solution overview
    tf2 = add_textbox(slide, CONTENT_LEFT, Inches(1.35), Inches(4.4), Inches(1.0))
    p = tf2.paragraphs[0]
    run = p.add_run()
    run.text = "Solution Overview"
    set_font(run, size=Pt(14), bold=True, color=GREEN_PRIMARY)
    add_paragraph(tf2, SLIDE3A["overview"], size=Pt(9), color=DARK_TEXT)

    # Workflow diagram image
    wf = diagram_path("workflow")
    if wf:
        slide.shapes.add_picture(wf, Inches(0.3), Inches(2.3), Inches(9.3), Inches(0.7))
    else:
        tf_wf = add_textbox(slide, CONTENT_LEFT, Inches(2.3), CONTENT_WIDTH, Inches(0.4))
        add_paragraph(tf_wf, SLIDE3A["workflow"], size=Pt(10), bold=True, color=GREEN_PRIMARY)

    # Why AI section
    tf3 = add_textbox(slide, CONTENT_LEFT, Inches(3.15), CONTENT_WIDTH, Inches(2.3))
    p = tf3.paragraphs[0]
    run = p.add_run()
    run.text = "Why AI is Required"
    set_font(run, size=Pt(14), bold=True, color=GREEN_PRIMARY)
    for title, desc in SLIDE3B["points"]:
        p = tf3.add_paragraph()
        p.space_before = Pt(2)
        p.space_after = Pt(1)
        run = p.add_run()
        run.text = f"{title}: "
        set_font(run, size=Pt(8), bold=True, color=GREEN_PRIMARY)
        run2 = p.add_run()
        run2.text = desc
        set_font(run2, size=Pt(8), color=DARK_TEXT)


def build_slide4(slide):
    """AWS Services + Value AI Adds (continuation of Brief)."""
    clear_slide_text(slide)

    # Title
    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Brief About the Idea (continued)"
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # AWS Services - Left column
    tf2 = add_textbox(slide, Inches(0.3), Inches(1.35), Inches(4.6), Inches(3.7))
    p = tf2.paragraphs[0]
    run = p.add_run()
    run.text = "AWS Services (11 Active + 4 Code-Ready = 15)"
    set_font(run, size=Pt(12), bold=True, color=GREEN_PRIMARY)

    for svc, desc in SLIDE3C["active"]:
        p = tf2.add_paragraph()
        p.space_before = Pt(1)
        p.space_after = Pt(0)
        run = p.add_run()
        run.text = f"  {svc}: "
        set_font(run, size=Pt(7.5), bold=True, color=BLUE_LIGHT)
        run2 = p.add_run()
        run2.text = desc
        set_font(run2, size=Pt(7.5), color=DARK_TEXT)

    p = tf2.add_paragraph()
    p.space_before = Pt(4)
    run = p.add_run()
    run.text = "Code-Ready:"
    set_font(run, size=Pt(8), bold=True, color=YELLOW_READY)
    for svc, desc in SLIDE3C["code_ready"]:
        p = tf2.add_paragraph()
        p.space_before = Pt(0)
        run = p.add_run()
        run.text = f"  {svc}: "
        set_font(run, size=Pt(7.5), bold=True, color=YELLOW_READY)
        run2 = p.add_run()
        run2.text = desc
        set_font(run2, size=Pt(7.5), color=DARK_TEXT)

    # Value table - Right column
    table = add_table(slide, len(SLIDE3D["comparisons"]) + 1, 3,
                       Inches(5.0), Inches(1.35), Inches(4.7), Inches(3.5))
    set_cell_text(table, 0, 0, "User", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 1, "Without AI", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 2, "With AI", SIZE_TABLE_HEADER, True, WHITE)
    for i, (user, without, with_ai) in enumerate(SLIDE3D["comparisons"]):
        set_cell_text(table, i + 1, 0, user, Pt(7.5), True)
        set_cell_text(table, i + 1, 1, without, Pt(7.5), color=RED_URGENT)
        set_cell_text(table, i + 1, 2, with_ai, Pt(7.5), color=GREEN_PRIMARY)
    style_table(table)
    table.columns[0].width = Inches(1.2)
    table.columns[1].width = Inches(1.75)
    table.columns[2].width = Inches(1.75)


def build_slide5(slide):
    """List of Features."""
    clear_slide_text(slide)
    d = SLIDE4

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Two columns of features
    features = d["features"]
    mid = (len(features) + 1) // 2

    # Left column
    tf_left = add_textbox(slide, Inches(0.4), Inches(1.4), Inches(4.6), Inches(3.8))
    for i, (name, desc) in enumerate(features[:mid]):
        p = tf_left.paragraphs[0] if i == 0 else tf_left.add_paragraph()
        p.space_before = Pt(3)
        p.space_after = Pt(1)
        run = p.add_run()
        run.text = f"{name}: "
        set_font(run, size=Pt(8), bold=True, color=GREEN_PRIMARY)
        run2 = p.add_run()
        run2.text = desc
        set_font(run2, size=Pt(7.5), color=DARK_TEXT)

    # Right column
    tf_right = add_textbox(slide, Inches(5.1), Inches(1.4), Inches(4.6), Inches(3.8))
    for i, (name, desc) in enumerate(features[mid:]):
        p = tf_right.paragraphs[0] if i == 0 else tf_right.add_paragraph()
        p.space_before = Pt(3)
        p.space_after = Pt(1)
        run = p.add_run()
        run.text = f"{name}: "
        set_font(run, size=Pt(8), bold=True, color=GREEN_PRIMARY)
        run2 = p.add_run()
        run2.text = desc
        set_font(run2, size=Pt(7.5), color=DARK_TEXT)


def build_slide6(slide):
    """Visual Representations - Workflow & Governance Loop."""
    clear_slide_text(slide)

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Visual Representations"
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # 5-Step Workflow diagram image
    tf2 = add_textbox(slide, CONTENT_LEFT, Inches(1.35), Inches(4.0), Inches(0.3))
    p = tf2.paragraphs[0]
    run = p.add_run()
    run.text = "5-Step Gram Sabha Lifecycle"
    set_font(run, size=Pt(12), bold=True, color=GREEN_PRIMARY)

    wf = diagram_path("workflow")
    if wf:
        slide.shapes.add_picture(wf, Inches(0.2), Inches(1.7), Inches(9.6), Inches(1.2))

    # Governance loop diagram image
    tf3 = add_textbox(slide, CONTENT_LEFT, Inches(3.05), Inches(4.0), Inches(0.3))
    p = tf3.paragraphs[0]
    run = p.add_run()
    run.text = "Continuous Governance Loop"
    set_font(run, size=Pt(12), bold=True, color=GREEN_PRIMARY)

    gl = diagram_path("governance_loop")
    if gl:
        slide.shapes.add_picture(gl, Inches(0.2), Inches(3.35), Inches(9.6), Inches(1.2))

    # Caption
    tf4 = add_textbox(slide, Inches(0.2), Inches(4.65), Inches(9.5), Inches(0.3))
    p = tf4.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "Citizens can report issues at any time -- the cycle is continuous, not tied to meeting dates"
    set_font(run, size=Pt(8), color=GRAY_MED, italic=True)


def build_slide7(slide):
    """Process Flow - AI Pipelines."""
    clear_slide_text(slide)

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Process Flow: AI Pipelines"
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Pipeline diagram images — 4 pipelines stacked
    pipeline_diagrams = [
        ("Voice Issue Reporting", "voice_pipeline", "cronJobs.js:51-53"),
        ("MOM Generation", "mom_pipeline", "llm_service.py:763-791"),
        ("Agenda Generation", "agenda_pipeline", "llm_service.py, tts_service.py"),
        ("Face Authentication", "face_auth", "citizenAuthRoutes.js:210,335"),
    ]

    y_pos = Inches(1.4)
    img_h = Inches(0.85)

    for name, diagram_name, source in pipeline_diagrams:
        # Label
        tf_label = add_textbox(slide, Inches(0.2), y_pos, Inches(3.0), Inches(0.22))
        p = tf_label.paragraphs[0]
        run = p.add_run()
        run.text = name
        set_font(run, size=Pt(9), bold=True, color=GREEN_PRIMARY)
        # Source
        run2 = p.add_run()
        run2.text = f"  ({source.split(',')[0]})"
        set_font(run2, size=Pt(6), color=GRAY_MED, italic=True, name=FONT_MONO)

        # Diagram image
        dp = diagram_path(diagram_name)
        if dp:
            slide.shapes.add_picture(dp, Inches(0.2), y_pos + Inches(0.22), Inches(9.6), img_h)

        y_pos += img_h + Inches(0.28)


def build_slide8(slide):
    """Wireframes / Mock Diagrams - Screenshots."""
    clear_slide_text(slide)

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Wireframes / Prototype Screenshots"
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Check for screenshots
    screenshot_files = []
    if os.path.exists(SCREENSHOTS_DIR):
        screenshot_files = sorted([f for f in os.listdir(SCREENSHOTS_DIR)
                                    if f.endswith(('.png', '.jpg', '.jpeg'))])

    if screenshot_files:
        # Arrange screenshots in 2x3 grid
        positions = [
            (Inches(0.3), Inches(1.5)),  (Inches(3.5), Inches(1.5)),  (Inches(6.7), Inches(1.5)),
            (Inches(0.3), Inches(3.2)),  (Inches(3.5), Inches(3.2)),  (Inches(6.7), Inches(3.2)),
        ]
        img_w = Inches(3.0)
        img_h = Inches(1.6)
        labels = SLIDE7["screens"]

        for i, (fname, (x, y)) in enumerate(zip(screenshot_files[:6], positions)):
            fpath = os.path.join(SCREENSHOTS_DIR, fname)
            try:
                slide.shapes.add_picture(fpath, x, y, img_w, img_h)
            except Exception:
                # Fallback: placeholder box
                shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, img_w, img_h)
                shape.fill.solid()
                shape.fill.fore_color.rgb = GRAY_LIGHT
                shape.line.color.rgb = GRAY_MED
                tf_ph = shape.text_frame
                p = tf_ph.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                run = p.add_run()
                run.text = labels[i] if i < len(labels) else fname
                set_font(run, size=Pt(10), color=GRAY_MED)

            # Label
            if i < len(labels):
                tf_label = add_textbox(slide, x, y + img_h, img_w, Inches(0.25))
                p = tf_label.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                run = p.add_run()
                run.text = labels[i]
                set_font(run, size=Pt(7), color=GRAY_MED, italic=True)
    else:
        # No screenshots - show placeholder grid with labels
        tf2 = add_textbox(slide, CONTENT_LEFT, Inches(1.4), CONTENT_WIDTH, Inches(0.4))
        p = tf2.paragraphs[0]
        run = p.add_run()
        run.text = "Live at: https://empowerpanchayat.org/"
        set_font(run, size=Pt(10), color=BLUE_LIGHT, italic=True)

        positions = [
            (Inches(0.3), Inches(1.9)),  (Inches(3.5), Inches(1.9)),  (Inches(6.7), Inches(1.9)),
            (Inches(0.3), Inches(3.4)),  (Inches(3.5), Inches(3.4)),  (Inches(6.7), Inches(3.4)),
        ]
        img_w = Inches(3.0)
        img_h = Inches(1.3)

        for i, (x, y) in enumerate(positions):
            label = SLIDE7["screens"][i] if i < len(SLIDE7["screens"]) else ""
            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, img_w, img_h)
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(0xE8, 0xF5, 0xE9)
            shape.line.color.rgb = GREEN_LIGHT
            shape.line.width = Pt(1)
            tf_ph = shape.text_frame
            tf_ph.word_wrap = True
            p = tf_ph.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = f"[Screenshot]\n{label}"
            set_font(run, size=Pt(9), color=GREEN_PRIMARY)


def build_slide9(slide):
    """Architecture Diagram."""
    clear_slide_text(slide)
    d = SLIDE8

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Full-page architecture diagram image
    arch = diagram_path("architecture")
    if arch:
        slide.shapes.add_picture(arch, Inches(0.2), Inches(1.35), Inches(9.6), Inches(3.7))

    # Source
    tf_src = add_textbox(slide, Inches(0.3), Inches(5.1), Inches(9.5), Inches(0.3))
    p = tf_src.paragraphs[0]
    run = p.add_run()
    run.text = f"Source: {d['source']}  |  4 Docker containers on bridge network  |  11 Active + 4 Code-Ready AWS services"
    set_font(run, size=Pt(7), color=GRAY_MED, italic=True, name=FONT_MONO)


def build_slide10(slide):
    """Technologies Utilized."""
    clear_slide_text(slide)
    d = SLIDE9

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Technologies table
    table = add_table(slide, len(d["tech"]) + 1, 3,
                       Inches(0.3), Inches(1.4), Inches(9.4), Inches(3.8))
    set_cell_text(table, 0, 0, "Layer", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 1, "Technology", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 2, "Purpose", SIZE_TABLE_HEADER, True, WHITE)

    for i, (layer, tech, purpose) in enumerate(d["tech"]):
        set_cell_text(table, i + 1, 0, layer, Pt(8), True)
        set_cell_text(table, i + 1, 1, tech, Pt(8))
        set_cell_text(table, i + 1, 2, purpose, Pt(8))

    style_table(table)
    table.columns[0].width = Inches(1.3)
    table.columns[1].width = Inches(4.0)
    table.columns[2].width = Inches(4.1)


def build_slide11(slide):
    """Estimated Implementation Cost."""
    clear_slide_text(slide)
    d = SLIDE10

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Hackathon cost table
    tf2 = add_textbox(slide, Inches(0.3), Inches(1.35), Inches(4.5), Inches(0.3))
    p = tf2.paragraphs[0]
    run = p.add_run()
    run.text = f"Current Hackathon Cost: {d['total']}"
    set_font(run, size=Pt(12), bold=True, color=GREEN_PRIMARY)

    table = add_table(slide, len(d["hackathon_costs"]) + 2, 3,
                       Inches(0.3), Inches(1.7), Inches(4.5), Inches(2.8))
    set_cell_text(table, 0, 0, "Service", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 1, "Monthly Cost", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 2, "Notes", SIZE_TABLE_HEADER, True, WHITE)
    for i, (svc, cost, notes) in enumerate(d["hackathon_costs"]):
        set_cell_text(table, i + 1, 0, svc, Pt(8))
        set_cell_text(table, i + 1, 1, cost, Pt(8), True)
        set_cell_text(table, i + 1, 2, notes, Pt(7))
    # Total row
    last = len(d["hackathon_costs"]) + 1
    set_cell_text(table, last, 0, "TOTAL", Pt(8), True, GREEN_PRIMARY)
    set_cell_text(table, last, 1, d["total"], Pt(8), True, GREEN_PRIMARY)
    set_cell_text(table, last, 2, "", Pt(7))
    style_table(table)
    table.columns[0].width = Inches(1.8)
    table.columns[1].width = Inches(1.1)
    table.columns[2].width = Inches(1.6)

    # Scale projections table (right side)
    tf3 = add_textbox(slide, Inches(5.1), Inches(1.35), Inches(4.6), Inches(0.3))
    p = tf3.paragraphs[0]
    run = p.add_run()
    run.text = "Scale Projections"
    set_font(run, size=Pt(12), bold=True, color=GREEN_PRIMARY)

    table2 = add_table(slide, len(d["scale"]) + 1, 4,
                        Inches(5.1), Inches(1.7), Inches(4.6), Inches(1.5))
    set_cell_text(table2, 0, 0, "Phase", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table2, 0, 1, "Scale", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table2, 0, 2, "Monthly", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table2, 0, 3, "Per Citizen/Yr", SIZE_TABLE_HEADER, True, WHITE)
    for i, (phase, scale, cost, per_citizen) in enumerate(d["scale"]):
        set_cell_text(table2, i + 1, 0, phase, Pt(8), True)
        set_cell_text(table2, i + 1, 1, scale, Pt(7))
        set_cell_text(table2, i + 1, 2, cost, Pt(8))
        set_cell_text(table2, i + 1, 3, per_citizen, Pt(8), True, GREEN_PRIMARY if per_citizen.startswith("$") else DARK_TEXT)
    style_table(table2)
    table2.columns[0].width = Inches(1.0)
    table2.columns[1].width = Inches(1.4)
    table2.columns[2].width = Inches(1.0)
    table2.columns[3].width = Inches(1.2)

    # Comparison callout
    y_comp = Inches(3.4)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                    Inches(5.1), y_comp, Inches(4.6), Inches(0.6))
    shape.fill.solid()
    shape.fill.fore_color.rgb = GREEN_PRIMARY
    shape.line.fill.background()
    tf_comp = shape.text_frame
    tf_comp.word_wrap = True
    p = tf_comp.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "~100x Cost Reduction"
    set_font(run, size=Pt(14), bold=True, color=WHITE)
    p2 = tf_comp.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = "Rs 500+/meeting (physical) vs Rs 5/citizen/year (digital)"
    set_font(run2, size=Pt(9), color=WHITE)

    # Cost optimization notes
    tf4 = add_textbox(slide, Inches(5.1), Inches(4.1), Inches(4.6), Inches(1.0))
    p = tf4.paragraphs[0]
    run = p.add_run()
    run.text = "Cost Optimizations:"
    set_font(run, size=Pt(9), bold=True, color=DARK_TEXT)
    opts = ["S3 Intelligent-Tiering for auto storage class", "Polly S3 caching (generate once, serve many)",
            "API Gateway throttling (100 req/s)", "Bedrock low temperature (0.3) for efficiency"]
    for opt in opts:
        add_bullet_point(tf4, opt, size=Pt(7.5))


def build_slide12(slide):
    """Snapshots of the Prototype."""
    clear_slide_text(slide)

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = "Snapshots of the Prototype"
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Same as wireframes but with different emphasis
    screenshot_files = []
    if os.path.exists(SCREENSHOTS_DIR):
        screenshot_files = sorted([f for f in os.listdir(SCREENSHOTS_DIR)
                                    if f.endswith(('.png', '.jpg', '.jpeg'))])

    labels = SLIDE11["snapshots"]

    if screenshot_files:
        positions = [
            (Inches(0.3), Inches(1.5)),  (Inches(3.5), Inches(1.5)),  (Inches(6.7), Inches(1.5)),
            (Inches(0.3), Inches(3.2)),  (Inches(3.5), Inches(3.2)),  (Inches(6.7), Inches(3.2)),
        ]
        img_w = Inches(3.0)
        img_h = Inches(1.5)

        for i, (x, y) in enumerate(positions):
            if i < len(screenshot_files):
                fpath = os.path.join(SCREENSHOTS_DIR, screenshot_files[i])
                try:
                    slide.shapes.add_picture(fpath, x, y, img_w, img_h)
                except Exception:
                    pass
            if i < len(labels):
                tf_label = add_textbox(slide, x, y + img_h, img_w, Inches(0.3))
                p = tf_label.paragraphs[0]
                p.alignment = PP_ALIGN.CENTER
                run = p.add_run()
                run.text = labels[i]
                set_font(run, size=Pt(7.5), color=GREEN_PRIMARY, bold=True)
    else:
        # Placeholder
        tf2 = add_textbox(slide, CONTENT_LEFT, Inches(1.4), CONTENT_WIDTH, Inches(0.4))
        p = tf2.paragraphs[0]
        run = p.add_run()
        run.text = "Live at: https://empowerpanchayat.org/"
        set_font(run, size=Pt(10), color=BLUE_LIGHT, italic=True)

        positions = [
            (Inches(0.3), Inches(1.9)),  (Inches(3.5), Inches(1.9)),  (Inches(6.7), Inches(1.9)),
            (Inches(0.3), Inches(3.4)),  (Inches(3.5), Inches(3.4)),  (Inches(6.7), Inches(3.4)),
        ]
        for i, (x, y) in enumerate(positions):
            label = labels[i] if i < len(labels) else ""
            shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, Inches(3.0), Inches(1.3))
            shape.fill.solid()
            shape.fill.fore_color.rgb = RGBColor(0xE8, 0xF5, 0xE9)
            shape.line.color.rgb = GREEN_LIGHT
            shape.line.width = Pt(1)
            tf_ph = shape.text_frame
            tf_ph.word_wrap = True
            p = tf_ph.paragraphs[0]
            p.alignment = PP_ALIGN.CENTER
            run = p.add_run()
            run.text = f"[Screenshot]\n{label}"
            set_font(run, size=Pt(9), color=GREEN_PRIMARY)


def build_slide13(slide):
    """Performance Report / Benchmarking."""
    clear_slide_text(slide)
    d = SLIDE12

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Tatarpur subtitle
    tf2 = add_textbox(slide, CONTENT_LEFT, Inches(1.3), Inches(5.0), Inches(0.3))
    p = tf2.paragraphs[0]
    run = p.add_run()
    run.text = d["tatarpur_title"]
    set_font(run, size=Pt(11), bold=True, color=GREEN_PRIMARY)

    # Tatarpur metrics table
    table = add_table(slide, len(d["tatarpur_metrics"]) + 1, 4,
                       Inches(0.3), Inches(1.65), Inches(5.0), Inches(1.5))
    set_cell_text(table, 0, 0, "Metric", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 1, "National Avg", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 2, "Tatarpur Digital", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table, 0, 3, "Improvement", SIZE_TABLE_HEADER, True, WHITE)
    for i, (metric, avg, digital, improvement) in enumerate(d["tatarpur_metrics"]):
        set_cell_text(table, i + 1, 0, metric, Pt(8))
        set_cell_text(table, i + 1, 1, avg, Pt(8), color=RED_URGENT)
        set_cell_text(table, i + 1, 2, digital, Pt(8), bold=True, color=GREEN_PRIMARY)
        set_cell_text(table, i + 1, 3, improvement, Pt(9), bold=True, color=GREEN_PRIMARY)
    style_table(table)
    table.columns[0].width = Inches(1.3)
    table.columns[1].width = Inches(1.2)
    table.columns[2].width = Inches(1.3)
    table.columns[3].width = Inches(1.2)

    # Key outcomes
    tf3 = add_textbox(slide, Inches(0.3), Inches(3.2), Inches(5.0), Inches(0.4))
    p = tf3.paragraphs[0]
    run = p.add_run()
    run.text = d["tatarpur_outcomes"]
    set_font(run, size=Pt(8), color=DARK_TEXT, italic=True)

    # Impact table (right side)
    tf4 = add_textbox(slide, Inches(5.5), Inches(1.3), Inches(4.3), Inches(0.3))
    p = tf4.paragraphs[0]
    run = p.add_run()
    run.text = "Impact Summary"
    set_font(run, size=Pt(11), bold=True, color=GREEN_PRIMARY)

    table2 = add_table(slide, len(d["impact"]) + 1, 3,
                        Inches(5.5), Inches(1.65), Inches(4.3), Inches(2.5))
    set_cell_text(table2, 0, 0, "Impact Area", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table2, 0, 1, "Mechanism", SIZE_TABLE_HEADER, True, WHITE)
    set_cell_text(table2, 0, 2, "Outcome", SIZE_TABLE_HEADER, True, WHITE)
    for i, (area, mechanism, outcome) in enumerate(d["impact"]):
        set_cell_text(table2, i + 1, 0, area, Pt(7.5), True)
        set_cell_text(table2, i + 1, 1, mechanism, Pt(7))
        set_cell_text(table2, i + 1, 2, outcome, Pt(7.5), bold=True, color=GREEN_PRIMARY)
    style_table(table2)
    table2.columns[0].width = Inches(1.3)
    table2.columns[1].width = Inches(1.4)
    table2.columns[2].width = Inches(1.6)

    # Source
    tf5 = add_textbox(slide, Inches(0.3), Inches(5.0), Inches(9.5), Inches(0.3))
    p = tf5.paragraphs[0]
    run = p.add_run()
    run.text = "Source: IMPACT.md:14,330-340 | Tatarpur Digital Gram Sabha (April 2025)"
    set_font(run, size=Pt(7), color=GRAY_MED, italic=True, name=FONT_MONO)


def build_slide14(slide):
    """Additional Details / Future Development."""
    clear_slide_text(slide)
    d = SLIDE13

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Phase columns
    phase_colors = [GREEN_PRIMARY, BLUE_LIGHT, ORANGE_ACCENT, RGBColor(0x7B, 0x1F, 0xA2)]
    col_width = Inches(2.25)

    for i, ((phase_name, items), color) in enumerate(zip(d["phases"], phase_colors)):
        x = Inches(0.3) + i * (col_width + Inches(0.1))
        y = Inches(1.45)

        # Phase header
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, col_width, Inches(0.35))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        tf_h = shape.text_frame
        p = tf_h.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = phase_name
        set_font(run, size=Pt(11), bold=True, color=WHITE)

        # Items
        tf_items = add_textbox(slide, x, y + Inches(0.4), col_width, Inches(2.0))
        for j, item in enumerate(items):
            p = tf_items.paragraphs[0] if j == 0 else tf_items.add_paragraph()
            p.space_before = Pt(3)
            p.space_after = Pt(1)
            run = p.add_run()
            run.text = f">> {item}"
            set_font(run, size=Pt(8), color=DARK_TEXT)

    # Vision & alignment
    y_vision = Inches(3.8)
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,
                                    Inches(0.3), y_vision, Inches(9.4), Inches(0.8))
    shape.fill.solid()
    shape.fill.fore_color.rgb = GREEN_PRIMARY
    shape.line.fill.background()
    tf_v = shape.text_frame
    tf_v.word_wrap = True
    p = tf_v.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = d["vision"]
    set_font(run, size=Pt(14), bold=True, color=WHITE)
    p2 = tf_v.add_paragraph()
    p2.alignment = PP_ALIGN.CENTER
    run2 = p2.add_run()
    run2.text = d["alignment"]
    set_font(run2, size=Pt(9), color=WHITE, italic=True)

    # Prototype Assets row
    y_assets = Inches(4.7)
    d2 = SLIDE14
    asset_colors = [GREEN_PRIMARY, BLUE_LIGHT, ORANGE_ACCENT, RGBColor(0x7B, 0x1F, 0xA2)]
    for i, ((label, value), color) in enumerate(zip(d2["assets"], asset_colors)):
        x = Inches(0.3) + i * Inches(2.4)
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y_assets, Inches(2.25), Inches(0.45))
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        tf_a = shape.text_frame
        tf_a.word_wrap = True
        p = tf_a.paragraphs[0]
        run = p.add_run()
        run.text = f"{label}: "
        set_font(run, size=Pt(7), bold=True, color=WHITE)
        run2 = p.add_run()
        run2.text = value
        set_font(run2, size=Pt(6), color=WHITE)


def build_slide15(slide):
    """Prototype Assets (last content slide, mapped to template slide 14)."""
    clear_slide_text(slide)
    d = SLIDE14

    tf = add_textbox(slide, CONTENT_LEFT, CONTENT_TOP, CONTENT_WIDTH, Inches(0.4))
    p = tf.paragraphs[0]
    run = p.add_run()
    run.text = d["title"]
    set_font(run, size=SIZE_SLIDE_TITLE, bold=True, color=DARK_TEXT)

    # Logo centered
    if os.path.exists(LOGO_PATH):
        slide.shapes.add_picture(LOGO_PATH, Inches(4.0), Inches(1.4), Inches(1.8), Inches(1.8))

    # Assets as styled boxes
    y_pos = Inches(3.3)
    asset_colors = [GREEN_PRIMARY, BLUE_LIGHT, ORANGE_ACCENT, RGBColor(0x7B, 0x1F, 0xA2)]
    for i, ((label, value), color) in enumerate(zip(d["assets"], asset_colors)):
        x = Inches(0.3) + (i % 2) * Inches(4.9)
        y = y_pos + (i // 2) * Inches(0.7)
        box_w = Inches(4.6)
        box_h = Inches(0.55)

        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, x, y, box_w, box_h)
        shape.fill.solid()
        shape.fill.fore_color.rgb = color
        shape.line.fill.background()
        tf_asset = shape.text_frame
        tf_asset.word_wrap = True
        p = tf_asset.paragraphs[0]
        run = p.add_run()
        run.text = f"{label}: "
        set_font(run, size=Pt(10), bold=True, color=WHITE)
        run2 = p.add_run()
        run2.text = value
        set_font(run2, size=Pt(9), color=WHITE)

    # Footer
    tf2 = add_textbox(slide, Inches(0.3), Inches(5.0), Inches(9.4), Inches(0.3))
    p = tf2.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    run = p.add_run()
    run.text = "eGramSabha -- Empower Panchayat -- Apache 2.0 Open Source -- Digital Public Good"
    set_font(run, size=Pt(9), color=GRAY_MED, italic=True)


# ============================================================
# MAIN
# ============================================================

def main():
    print(f"Loading template: {TEMPLATE_PATH}")
    prs = Presentation(TEMPLATE_PATH)

    slides = list(prs.slides)
    assert len(slides) == 14, f"Expected 14 template slides, got {len(slides)}"

    # Map: template slides 1-14 -> our build functions
    # Template structure maps to our content as follows:
    # Slide 1:  Team/Project Info
    # Slide 2:  Brief (we use for Problem Statement since template has "Brief" label)
    # Slide 3:  Brief questions (we use for Brief + Why AI)
    # Slide 4:  Features (we use for AWS Services + Value table)
    # Slide 5:  Process flow (we use for Features)
    # Slide 6:  Wireframes (we use for Visual Representations)
    # Slide 7:  Architecture (we use for Process Flow / AI Pipelines)
    # Slide 8:  Technologies (we use for Wireframes/Screenshots)
    # Slide 9:  Cost (we use for Architecture)
    # Slide 10: Snapshots (we use for Technologies)
    # Slide 11: Performance (we use for Cost)
    # Slide 12: Future (we use for Snapshots)
    # Slide 13: Assets (we use for Performance)
    # Slide 14: Thank you (we use for Future + Assets)
    #
    # Actually, let's follow the EXACT template order from the plan:
    # Template Slide 1 -> Our Slide 1 (Team Info)
    # Template Slide 2 -> Our Slide 2 (Problem Statement) -- template says "Brief" but we put problem here
    # Template Slide 3 -> Our Slide 3 (Brief: Solution + Why AI)
    # Template Slide 4 -> Our Slide 4 (Brief continued: AWS + Value)
    # Template Slide 5 -> Our Slide 5 (Features)
    # Template Slide 6 -> Our Slide 6 (Visual Representations)
    # Template Slide 7 -> Our Slide 7 (Process Flow / AI Pipelines)
    # Template Slide 8 -> Our Slide 8 (Wireframes / Screenshots)
    # Template Slide 9 -> Our Slide 9 (Architecture)
    # Template Slide 10 -> Our Slide 10 (Technologies)
    # Template Slide 11 -> Our Slide 11 (Cost)
    # Template Slide 12 -> Our Slide 12 (Snapshots)
    # Template Slide 13 -> Our Slide 13 (Performance)
    # Template Slide 14 -> Our Slide 14 (Future + Assets)
    #
    # Wait - the template has 14 slides but we need:
    # 1. Team Info, 2. Problem Statement, 3. Brief (idea), 4. Brief (AWS+Value),
    # 5. Features, 6. Visual, 7. Process Flow, 8. Wireframes, 9. Architecture,
    # 10. Technologies, 11. Cost, 12. Snapshots, 13. Performance, 14. Future/Assets
    #
    # That's 14 content items for 14 slides. But the plan also wants "Prototype Assets"
    # as slide 14. Let's merge Future + Assets into slide 14 since the template
    # slide 14 appears to be a closing slide.
    #
    # Actually looking at the template more carefully:
    # Slide 1: Team Name / Problem Statement (TITLE)
    # Slide 2: Brief about the Idea (has label)
    # Slide 3: Brief continued (has 3 questions)
    # Slide 4: Features + Visual (has label)
    # Slide 5: Process flow (has label)
    # Slide 6: Wireframes (has label)
    # Slide 7: Architecture (has label)
    # Slide 8: Technologies (has label)
    # Slide 9: Cost (has label)
    # Slide 10: Snapshots (has label)
    # Slide 11: Performance (has label)
    # Slide 12: Future (has label)
    # Slide 13: Assets (has label)
    # Slide 14: Closing slide (just background)
    #
    # So 13 content slides + 1 closing.
    # We have more content than slides (14 content items for 13+1 slots).
    # Solution: Merge Problem Statement into slide 1 (it already has that field),
    # and use slide 14 for Assets.

    builders = [
        build_slide1,   # 1: Team & Project Info (includes problem statement)
        build_slide2,   # 2: Problem Statement detail
        build_slide3,   # 3: Brief - Solution + Why AI
        build_slide4,   # 4: Brief - AWS Services + Value
        build_slide5,   # 5: Features
        build_slide6,   # 6: Visual Representations
        build_slide7,   # 7: Process Flow / AI Pipelines
        build_slide8,   # 8: Wireframes / Screenshots
        build_slide9,   # 9: Architecture
        build_slide10,  # 10: Technologies
        build_slide11,  # 11: Cost
        build_slide12,  # 12: Snapshots
        build_slide13,  # 13: Performance / Benchmarking
        build_slide14,  # 14: Future + Assets (merged)
    ]

    for i, (slide_obj, builder) in enumerate(zip(slides, builders)):
        print(f"  Building slide {i + 1}: {builder.__doc__.strip()}")
        builder(slide_obj)

    print(f"\nSaving to: {OUTPUT_PATH}")
    prs.save(OUTPUT_PATH)
    print("Done! PPTX generated successfully.")
    print(f"\nTo convert to PDF:")
    print(f'  libreoffice --headless --convert-to pdf "{OUTPUT_PATH}"')


if __name__ == "__main__":
    main()
