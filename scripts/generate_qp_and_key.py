import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "dataset", "answer_keys", "rendered")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ── page constants ───────────────────────────────────────────────────────
PAGE_W, PAGE_H = 1240, 1754          # A4 @ ~150 DPI
LINE_SPACING   = 50
MARGIN_LEFT    = 100
TEXT_X         = MARGIN_LEFT
INK_COLOR      = (0, 0, 0)           # Black ink for printed text
PAPER_COLOR    = (255, 255, 255)     # White paper
WRAP_WIDTH     = 70                  # chars per line for printed text

def _new_page():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER_COLOR)
    draw = ImageDraw.Draw(img)
    return img, draw

def render_text_file(input_filepath, output_prefix):
    print(f"Generating images for {output_prefix}...")
    try:
        font = ImageFont.truetype("arial.ttf", 36)
    except IOError:
        print("    [WARN] Could not load Arial font, falling back to default.")
        font = ImageFont.load_default()

    with open(input_filepath, "r", encoding="utf-8") as f:
        content = f.read()

    pages = []
    img, draw = _new_page()
    cur_y = 100
    page_num = 1

    def _flush_page():
        nonlocal img, draw, cur_y, page_num
        pages.append((img, page_num))
        page_num += 1
        img, draw = _new_page()
        cur_y = 100

    for line in content.split("\n"):
        wrapped = textwrap.wrap(line, width=WRAP_WIDTH)
        if not wrapped: # empty line
            cur_y += LINE_SPACING
            continue
            
        for w_line in wrapped:
            if cur_y > PAGE_H - 100:
                _flush_page()
            draw.text((TEXT_X, cur_y), w_line, fill=INK_COLOR, font=font)
            cur_y += LINE_SPACING
            
    pages.append((img, page_num))

    for page_img, pnum in pages:
        fname = os.path.join(OUTPUT_DIR, f"{output_prefix}_p{pnum}.png")
        page_img.save(fname)
        
    print(f"    [OK] Saved {len(pages)} page(s) for {output_prefix}")

if __name__ == "__main__":
    q_file = os.path.join(BASE_DIR, "dataset", "answer_keys", "Question.txt")
    a_file = os.path.join(BASE_DIR, "dataset", "answer_keys", "answerkey.txt")
    
    render_text_file(q_file, "Question_Paper")
    render_text_file(a_file, "Answer_Key")
    print(f"Output saved to {OUTPUT_DIR}")
