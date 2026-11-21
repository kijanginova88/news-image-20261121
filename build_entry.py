#!/usr/bin/env python3
"""Build entry.png for news-image-20261121 — deterministic newspaper front page.
Run: python3 build_entry.py  (writes entry.png next to this script)
Uses only DejaVu / Liberation fonts shipped with the system; Pillow only.
No timestamps or random data are embedded, so repeated runs are byte-identical.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (17, 17, 17)
RED = (163, 18, 30)
BLUE = (28, 78, 138)
GREY = (90, 86, 78)
RULE = (17, 17, 17)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

def wrap(draw, text, fnt, width):
    """Greedy word wrap to pixel width."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def draw_story(d, x, y, w, kicker, headline, body, head_size=30, body_size=19,
               head_lines_max=3, body_lines_max=5, kicker_color=RED):
    f_kick = font(SANS_B, 19)
    f_head = font(SERIF, head_size)
    f_body = font(SANS, body_size)
    d.text((x, y), kicker, font=f_kick, fill=kicker_color)
    y += 26
    for line in wrap(d, headline, f_head, w)[:head_lines_max]:
        d.text((x, y), line, font=f_head, fill=INK)
        y += head_size + 6
    y += 4
    for line in wrap(d, body, f_body, w)[:body_lines_max]:
        d.text((x, y), line, font=f_body, fill=INK)
        y += body_size + 7
    return y

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36                      # margin
    R = W - M                   # right edge

    # ---- Masthead ----
    f_mast = font(SERIF_B, 62)
    title = "THE WORLD TODAY"
    tw = d.textlength(title, font=f_mast)
    d.text(((W - tw) / 2, 26), title, font=f_mast, fill=INK)
    f_date = font(SANS_B, 20)
    dateline = "SATURDAY, 21 NOVEMBER 2026  \u2022  WORLD NEWS IN ONE PAGE"
    dw = d.textlength(dateline, font=f_date)
    d.text(((W - dw) / 2, 104), dateline, font=f_date, fill=RED)
    d.line([(M, 134), (R, 134)], fill=RULE, width=3)
    d.line([(M, 140), (R, 140)], fill=RULE, width=1)

    # ---- Lead story: Poland ----
    y = draw_story(
        d, M, 156, R - M,
        "POLAND  \u2022  LEAD STORY",
        "Russian missiles land in Poland",
        "Two Russian missiles and a suspected drone came down in south-eastern Poland on "
        "Friday during a huge Russian attack on Ukraine. Prime Minister Donald Tusk called "
        "it an \u201cintentional provocation\u201d; NATO chief Mark Rutte called it a \u201cgrave "
        "violation\u201d of Polish airspace. No one in Poland was hurt.",
        head_size=46, body_size=20, head_lines_max=2, body_lines_max=3,
    )
    d.line([(M, 352), (R, 352)], fill=RULE, width=2)

    # ---- Two-column rows ----
    col_w = 464
    lx, rx = M, M + col_w + 24
    d.line([(M + col_w + 12, 366), (M + col_w + 12, 838)], fill=(180, 175, 164), width=1)

    # Row 1
    y1 = draw_story(
        d, lx, 368, col_w,
        "WALL STREET",
        "AI rout sinks US stocks",
        "The S&P 500 fell 3.7% and the Nasdaq 5.3% on Friday \u2014 wiping out the Nasdaq\u2019s "
        "gains for the year \u2014 as AI shares sold off. Nvidia fell 14%; Anthropic, a day "
        "after its $83-a-share IPO, fell 9.1%.",
        head_size=30, body_size=19, body_lines_max=5,
    )
    draw_story(
        d, rx, 368, col_w,
        "UKRAINE  \u2022  PEACE PUSH",
        "Trump wants deal by January, FT reports",
        "The White House told European and Ukrainian officials it wants a Russia\u2013Ukraine "
        "peace deal by early January 2027, the Financial Times reported. Envoy Jared "
        "Kushner said Russia was comfortable with NATO-style security guarantees for Kyiv.",
        head_size=30, body_size=19, body_lines_max=5,
    )
    d.line([(M, 612), (R, 612)], fill=(180, 175, 164), width=1)

    # Row 2
    draw_story(
        d, lx, 628, col_w,
        "THE HAGUE",
        "World court: Myanmar committed genocide",
        "The International Court of Justice ruled on Thursday that Myanmar committed "
        "genocide against the Rohingya in 2016\u201317 and ordered reparations \u2014 the first "
        "time the court has found a state guilty of genocide.",
        head_size=30, body_size=19, body_lines_max=4,
    )
    draw_story(
        d, rx, 628, col_w,
        "BRUSSELS",
        "Britain and EU seal food and youth deals",
        "Prime Minister Andy Burnham and EU leaders agreed deals easing food trade, "
        "linking carbon markets and letting 100,000 young people a year live and work on "
        "each side for up to three years.",
        head_size=30, body_size=19, body_lines_max=4,
    )
    d.line([(M, 852), (R, 852)], fill=RULE, width=2)

    # ---- Science, full width ----
    draw_story(
        d, M, 866, R - M,
        "SCIENCE",
        "Cancer pill shrinks pancreatic tumours in 44% of patients",
        "Erasca\u2019s ERAS-0015 shrank tumours in 11 of 25 previously treated pancreatic "
        "cancer patients in the Phase 1 AURORAS-1 trial, presented on Friday in Barcelona. "
        "It also showed a 60% response rate in lung cancer.",
        head_size=30, body_size=19, body_lines_max=2, kicker_color=BLUE,
    )

    # ---- Footer ----
    d.line([(M, 986), (R, 986)], fill=RULE, width=1)
    f_foot = font(SANS, 14)
    d.text((M, 994), "Sources: Reuters, AP, Financial Times, ICJ, EORTC-NCI-AACR, NPR",
           font=f_foot, fill=GREY)

    img.save("entry.png", format="PNG")
    print("saved entry.png")

if __name__ == "__main__":
    main()
