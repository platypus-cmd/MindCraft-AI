"""PDF export service for generated notes.

The export accepts an already generated NotesResponse and renders it to PDF
entirely in memory. It does not call Gemini, regenerate notes, or persist data.
"""

import io

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import ListFlowable, ListItem, Paragraph, SimpleDocTemplate, Spacer

from app.schemas.notes import DefinitionItem, NotesResponse


def generate_notes_pdf(notes_response: NotesResponse) -> bytes:
    """Render a complete NotesResponse to PDF bytes."""
    buffer = io.BytesIO()
    document = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=0.75 * inch,
        leftMargin=0.75 * inch,
        topMargin=0.75 * inch,
        bottomMargin=0.75 * inch,
        title="MindCraft Notes",
    )
    styles = _build_styles()
    story = _build_story(notes_response, styles)

    document.build(story)
    return buffer.getvalue()


def _build_styles() -> dict[str, ParagraphStyle]:
    base_styles = getSampleStyleSheet()
    return {
        "title": base_styles["Title"],
        "heading": base_styles["Heading2"],
        "subheading": base_styles["Heading3"],
        "body": base_styles["BodyText"],
        "bullet": base_styles["BodyText"],
    }


def _build_story(
    notes_response: NotesResponse,
    styles: dict[str, ParagraphStyle],
) -> list:
    notes = notes_response.notes
    story: list = []

    story.append(Paragraph(_escape(notes.title), styles["title"]))
    story.append(Spacer(1, 0.16 * inch))
    story.append(
        Paragraph(
            f"Estimated reading time: {notes_response.estimated_reading_time_minutes} minute(s)",
            styles["body"],
        )
    )

    _add_list_section(story, "Table of Contents", notes.table_of_contents, styles)

    for section in notes.sections:
        story.append(Spacer(1, 0.18 * inch))
        story.append(Paragraph(_escape(section.heading), styles["heading"]))
        _add_paragraph(story, section.content, styles)
        _add_list_section(story, "Key Points", section.key_points, styles)
        _add_definitions(story, section.definitions, styles)
        _add_list_section(story, "Examples", section.examples, styles)
        _add_list_section(story, "Exam Tips", section.exam_tips, styles)
        _add_list_section(story, "Memory Tricks", section.memory_tricks, styles)
        _add_list_section(story, "Common Mistakes", section.common_mistakes, styles)

    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph("Summary", styles["heading"]))
    _add_paragraph(story, notes.summary, styles)
    _add_list_section(story, "Key Takeaways", notes.key_takeaways, styles)

    story.append(Spacer(1, 0.18 * inch))
    story.append(Paragraph("One-Minute Revision", styles["heading"]))
    _add_paragraph(story, notes.one_minute_revision, styles)

    return story


def _add_paragraph(
    story: list,
    text: str,
    styles: dict[str, ParagraphStyle],
) -> None:
    if not text:
        return

    story.append(Spacer(1, 0.06 * inch))
    story.append(Paragraph(_escape(text), styles["body"]))


def _add_list_section(
    story: list,
    title: str,
    items: list[str],
    styles: dict[str, ParagraphStyle],
) -> None:
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(title, styles["subheading"]))

    if not items:
        story.append(Paragraph("None", styles["body"]))
        return

    story.append(
        ListFlowable(
            [
                ListItem(Paragraph(_escape(item), styles["bullet"]))
                for item in items
            ],
            bulletType="bullet",
            start="circle",
            leftIndent=18,
        )
    )


def _add_definitions(
    story: list,
    definitions: list[DefinitionItem],
    styles: dict[str, ParagraphStyle],
) -> None:
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("Definitions", styles["subheading"]))

    if not definitions:
        story.append(Paragraph("None", styles["body"]))
        return

    story.append(
        ListFlowable(
            [
                ListItem(
                    Paragraph(
                        f"<b>{_escape(item.term)}:</b> {_escape(item.definition)}",
                        styles["bullet"],
                    )
                )
                for item in definitions
            ],
            bulletType="bullet",
            start="circle",
            leftIndent=18,
        )
    )


def _escape(text: str) -> str:
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

import os
import asyncio
from playwright.sync_api import sync_playwright

def _generate_pdf_sync(html_content: str, theme_class: str) -> bytes:
    current_dir = os.path.dirname(__file__)
    style_path = os.path.abspath(os.path.join(current_dir, "../../../frontend/css/style.css"))
    
    css_content = ""
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            css_content = f.read()
            
    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            {css_content}
            body {{
                margin: 0;
                padding: 0;
                /* Force background graphics to print */
                -webkit-print-color-adjust: exact !important;
                print-color-adjust: exact !important;
            }}
        </style>
    </head>
    <body>
        <article id="notes-content" class="{theme_class}">
            {html_content}
        </article>
    </body>
    </html>
    """

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.set_content(full_html)
        page.evaluate("document.fonts.ready")
        pdf_bytes = page.pdf(
            format="A4",
            print_background=True,
            margin={"top": "0.5in", "bottom": "0.5in", "left": "0.5in", "right": "0.5in"}
        )
        browser.close()
        
    return pdf_bytes

async def generate_notes_pdf_playwright(html_content: str, theme_class: str) -> bytes:
    """Render HTML to PDF bytes using Playwright and Headless Chromium."""
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, _generate_pdf_sync, html_content, theme_class)
