#!/usr/bin/env python3
"""Build the English logo (assets/logo-en.svg and assets/logo-en-white.svg).

It uses the Mada Care mark from assets/logo-mark.svg, the name "Mada Care" set in
Thmanyah Bold and the motto in Thmanyah Medium. The text is turned into outlines,
so the logo looks the same without any font loaded.
"""
import os, re
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
NAVY, GREEN, WHITE = "#014359", "#4CB491", "#FFFFFF"


def text_path(font_file, text, size, x, baseline, tracking=0):
    f = TTFont(font_file)
    gs, cmap, hmtx, upm = f.getGlyphSet(), f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    s = size / upm
    pen = SVGPathPen(gs)
    for ch in text:
        g = cmap[ord(ch)]
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, x, baseline)))
        x += hmtx[g][0] * s + tracking
    return pen.getCommands(), x


mark = open("assets/logo-mark.svg", encoding="utf-8").read()
mark_body = mark[mark.index(">", mark.index("<svg")) + 1: mark.rindex("</svg>")]
mark_body = re.sub(r'\sid="[^"]*"', "", mark_body)

name, x1 = text_path("fonts/thmanyahsans-Bold.woff2", "Mada Care", 22, 46, 21, 0.2)
motto, x2 = text_path("fonts/thmanyahsans-Medium.woff2", "We care for you like family", 9.4, 46.5, 35)
width = round(max(x1, x2) + 1, 1)

for out, txt in (("assets/logo-en.svg", NAVY), ("assets/logo-en-white.svg", WHITE)):
    body = mark_body if txt == NAVY else mark_body.replace(NAVY, WHITE)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="40" viewBox="0 0 {width} 40" fill="none">\n'
           f'<svg x="0" y="0" width="37.254" height="40" viewBox="0 0 37.2592 40.0026">{body}</svg>\n'
           f'<path fill="{txt}" d="{name}"/>\n<path fill="{txt}" d="{motto}"/>\n</svg>\n')
    open(out, "w", encoding="utf-8").write(svg)
print("width", width)
