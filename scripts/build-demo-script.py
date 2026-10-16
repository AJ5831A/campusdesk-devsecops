import re
from html import escape
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer


def inline(value):
    value = escape(value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", value)
    return re.sub(r"`([^`]+)`", r'<font name="Courier">\1</font>', value)


def build():
    root = Path(__file__).resolve().parents[1]
    styles = getSampleStyleSheet()
    styles["BodyText"].fontSize = 10.5
    styles["BodyText"].leading = 15
    styles["BodyText"].spaceAfter = 8
    styles["BodyText"].splitLongWords = True
    for name in ["Heading1", "Heading2", "Heading3"]:
        styles[name].textColor = colors.HexColor("#5146A0")
    styles["Heading1"].fontSize = 21
    styles["Heading1"].leading = 25
    styles["Heading2"].fontSize = 14
    styles["Heading2"].leading = 18
    styles["Code"].fontSize = 8
    styles["Code"].leading = 11
    styles["Code"].backColor = colors.HexColor("#F3F1F8")
    styles.add(
        ParagraphStyle(
            "Narration",
            parent=styles["BodyText"],
            leftIndent=12,
            rightIndent=8,
            backColor=colors.HexColor("#F6F4FA"),
            borderPadding=6,
        )
    )
    story = []
    code = None
    for line in (root / "demo/demo-script.md").read_text().splitlines():
        if line.startswith("```"):
            if code is None:
                code = []
            else:
                story.append(
                    Preformatted("\n".join(code), styles["Code"], maxLineLength=90)
                )
                story.append(Spacer(1, 8))
                code = None
        elif code is not None:
            code.append(line)
        elif line.strip():
            if line.startswith("> "):
                story.append(Paragraph(inline(line[2:]), styles["Narration"]))
                continue
            level = len(line) - len(line.lstrip("#"))
            style = (
                styles.get(f"Heading{level}", styles["BodyText"])
                if level
                else styles["BodyText"]
            )
            value = line.lstrip("# ") if level else line
            story.append(Paragraph(inline(value), style))
    if code is not None:
        raise ValueError("Unclosed code block")

    def footer(canvas, document):
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#536879"))
        canvas.drawString(
            0.65 * inch, 0.35 * inch, "CampusDesk | Aryan (AJ5831A) | Presenter guide"
        )
        canvas.drawRightString(A4[0] - 0.65 * inch, 0.35 * inch, str(document.page))

    SimpleDocTemplate(
        str(root / "demo/demo-script.pdf"),
        pagesize=A4,
        rightMargin=0.65 * inch,
        leftMargin=0.65 * inch,
        topMargin=0.55 * inch,
        bottomMargin=0.65 * inch,
        title="CampusDesk - Exact presentation and demonstration script",
        author="CampusDesk - prepared for Aryan",
    ).build(story, onFirstPage=footer, onLaterPages=footer)


if __name__ == "__main__":
    build()
