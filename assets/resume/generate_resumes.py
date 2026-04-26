from __future__ import annotations

import json
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    HRFlowable,
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


BASE_DIR = Path(__file__).resolve().parent
SOURCE_PATH = BASE_DIR / "source" / "resumes.json"
CREATIVE_OUTPUT = BASE_DIR / "Madeline_Guzman_Creative_Resume.pdf"
ATS_OUTPUT = BASE_DIR / "Madeline_Guzman_ATS_Resume.pdf"


def load_data() -> dict:
    return json.loads(SOURCE_PATH.read_text(encoding="utf-8"))


def build_styles():
    sample = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=sample["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#111827"),
            spaceAfter=4,
        ),
        "title": ParagraphStyle(
            "Title",
            parent=sample["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=colors.HexColor("#374151"),
            spaceAfter=4,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#374151"),
        ),
        "brand": ParagraphStyle(
            "Brand",
            parent=sample["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=12,
            textColor=colors.HexColor("#111827"),
            alignment=TA_CENTER,
        ),
        "tagline": ParagraphStyle(
            "Tagline",
            parent=sample["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=9,
            leading=11,
            textColor=colors.HexColor("#4B5563"),
            alignment=TA_CENTER,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=sample["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=colors.HexColor("#111827"),
            spaceBefore=10,
            spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12.5,
            textColor=colors.HexColor("#111827"),
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=sample["BodyText"],
            fontName="Helvetica-Oblique",
            fontSize=8.5,
            leading=11,
            textColor=colors.HexColor("#4B5563"),
            spaceAfter=2,
        ),
        "role": ParagraphStyle(
            "Role",
            parent=sample["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9.5,
            leading=12,
            textColor=colors.HexColor("#111827"),
        ),
        "small": ParagraphStyle(
            "Small",
            parent=sample["BodyText"],
            fontName="Helvetica",
            fontSize=8.5,
            leading=10.5,
            textColor=colors.HexColor("#4B5563"),
        ),
    }


def bullet_list(items: list[str], styles: dict, left_indent: int = 12):
    return ListFlowable(
        [
            ListItem(Paragraph(item, styles["body"]), leftIndent=0)
            for item in items
        ],
        bulletType="bullet",
        start="circle",
        leftIndent=left_indent,
        bulletFontName="Helvetica",
        bulletFontSize=8,
        bulletColor=colors.HexColor("#111827"),
        spaceBefore=2,
        spaceAfter=4,
    )


def add_header(story: list, contact: dict, styles: dict, title: str):
    story.append(Paragraph(contact["name"].upper(), styles["name"]))
    story.append(Paragraph(title, styles["title"]))
    story.append(
        Paragraph(
            " · ".join(
                [
                    contact["location"],
                    contact["email"],
                    contact["phone"],
                    contact["linkedin"],
                    contact["website"],
                    contact["tools"],
                ]
            ),
            styles["contact"],
        )
    )
    story.append(Spacer(1, 0.08 * inch))
    story.append(HRFlowable(width="100%", color=colors.HexColor("#D1D5DB"), thickness=0.6))
    story.append(Spacer(1, 0.08 * inch))


def add_experience_block(story: list, item: dict, styles: dict):
    story.append(Paragraph(f"{item['role']} — {item['org']}", styles["role"]))
    story.append(Paragraph(item["meta"], styles["meta"]))
    story.append(bullet_list(item["bullets"], styles))


def build_creative(data: dict, styles: dict):
    creative = data["creative"]
    contact = data["contact"]
    story = []

    add_header(story, contact, styles, contact["title_creative"])
    story.append(Paragraph(creative["brand_name"].upper(), styles["brand"]))
    story.append(Paragraph(creative["brand_tagline"], styles["tagline"]))
    story.append(Spacer(1, 0.06 * inch))
    story.append(Paragraph(creative["availability"], styles["small"]))

    story.append(Paragraph("SUMMARY", styles["section"]))
    story.append(Paragraph(creative["summary"], styles["body"]))

    story.append(Paragraph("SKILLS", styles["section"]))
    skill_rows = [[Paragraph(f"<b>{row['label']}</b>", styles["body"]), Paragraph(row["items"], styles["body"])] for row in creative["skills"]]
    skill_table = Table(skill_rows, colWidths=[1.35 * inch, 5.55 * inch], hAlign="LEFT")
    skill_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )
    story.append(skill_table)

    story.append(Paragraph("EXPERIENCE", styles["section"]))
    for item in creative["experience"]:
        add_experience_block(story, item, styles)

    story.append(Paragraph("MILITARY SERVICE", styles["section"]))
    add_experience_block(story, creative["military"], styles)

    story.append(Paragraph("EDUCATION & CERTIFICATIONS", styles["section"]))
    story.append(bullet_list(creative["education"], styles))
    return story


def build_ats(data: dict, styles: dict):
    ats = data["ats"]
    contact = data["contact"]
    story = []

    add_header(story, contact, styles, "Game Audio Engineer · Sound Designer")

    story.append(Paragraph("SUMMARY", styles["section"]))
    story.append(Paragraph(ats["summary"], styles["body"]))

    story.append(Paragraph("SKILLS", styles["section"]))
    story.append(bullet_list(ats["skills"], styles, left_indent=10))

    story.append(Paragraph("EXPERIENCE", styles["section"]))
    for item in ats["experience"]:
        add_experience_block(story, item, styles)

    story.append(Paragraph("MILITARY SERVICE", styles["section"]))
    add_experience_block(story, ats["military"], styles)

    story.append(Paragraph("EDUCATION & CERTIFICATIONS", styles["section"]))
    story.append(bullet_list(ats["education"], styles, left_indent=10))

    story.append(Paragraph("ADDITIONAL", styles["section"]))
    story.append(Paragraph(ats["additional"], styles["body"]))
    return story


def render(path: Path, story: list):
    doc = SimpleDocTemplate(
        str(path),
        pagesize=LETTER,
        topMargin=0.45 * inch,
        bottomMargin=0.5 * inch,
        leftMargin=0.58 * inch,
        rightMargin=0.58 * inch,
        title=path.stem.replace("_", " "),
        author="Madeline Guzman",
    )
    doc.build(story)


def main():
    data = load_data()
    styles = build_styles()
    render(CREATIVE_OUTPUT, build_creative(data, styles))
    render(ATS_OUTPUT, build_ats(data, styles))
    print(f"Generated: {CREATIVE_OUTPUT.name}")
    print(f"Generated: {ATS_OUTPUT.name}")


if __name__ == "__main__":
    main()
