"""Render a synthetic handwritten student answer booklet (PNG pages -> PDF) for ANY exam.

Reusable test-data generator: give it a student name + {question_no: answer_text} and it writes a
ruled-notebook, handwriting-font PDF — same style as dataset/'Test Data'/page-1.pdf. Used to build
test cases for the format-agnostic general grader.

Usage: import build_booklet(name, roll, answers, out_pdf) or run the __main__ demo.
"""
import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT = os.path.join(BASE, "fonts", "Caveat.ttf")
PAGE_W, PAGE_H = 1240, 1754
LINE_H, MARGIN_L = 58, 120
INK, PAPER, RULE = (25, 25, 120), (250, 247, 241), (205, 214, 228)
WRAP = 48


def _page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)
    for y in range(150, PAGE_H, LINE_H):          # ruled lines
        d.line([(60, y), (PAGE_W - 40, y)], fill=RULE, width=1)
    d.line([(95, 0), (95, PAGE_H)], fill=(230, 150, 150), width=2)   # red margin
    return img, d


def build_booklet(name: str, roll: str, answers: dict[str, str], out_pdf: str):
    font = ImageFont.truetype(FONT, 34)
    pages, (img, d) = [], _page()
    y = 160

    def line(text, indent=0):
        nonlocal img, d, y
        if y > PAGE_H - 120:
            pages.append(img); img, d = _page(); y = 160
        d.text((MARGIN_L + indent, y), text, fill=INK, font=font)
        y += LINE_H

    line(f"Name: {name}    Roll No: {roll}")
    for qno in sorted(answers, key=lambda q: int(q)):
        for i, w in enumerate(textwrap.wrap(f"Q{qno}. {answers[qno]}", WRAP) or [f"Q{qno}."]):
            line(w, indent=0 if i == 0 else 40)
    pages.append(img)

    os.makedirs(os.path.dirname(out_pdf), exist_ok=True)
    pages[0].save(out_pdf, "PDF", resolution=150.0, save_all=True, append_images=pages[1:])
    print(f"  wrote {len(pages)}-page PDF -> {out_pdf}")


if __name__ == "__main__":
    demo = {"1": "b", "2": "A cell is the basic structural and functional unit of life."}
    build_booklet("Test Student", "001", demo, os.path.join(BASE, "dataset", "_demo", "demo.pdf"))
