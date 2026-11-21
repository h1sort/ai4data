#!/usr/bin/env python3
"""Export the deck to a PDF handout: one page per slide at its last build step,
plus every step of slides listed in ALL_STEPS. Speaker notes are not included.

Usage: deck/tools/pdf.py [out.pdf]   (needs playwright; set CHROME to use a local Chrome)
"""
import os, shutil, sys, tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright

DECK = Path(__file__).resolve().parents[1]
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else DECK / '.shots/deck.pdf').resolve()
ALL_STEPS = set()
EXTRA = {}
chrome = os.environ.get('CHROME') or shutil.which('google-chrome') or shutil.which('chromium')

with sync_playwright() as p, tempfile.TemporaryDirectory() as tmp:
    b = p.chromium.launch(executable_path=chrome, args=['--allow-file-access-from-files', '--no-sandbox'])
    pg = b.new_page(viewport={'width': 1920, 'height': 1080})
    url = (DECK / 'index.html').as_uri() + '?shot'
    pg.goto(url + '#/1/0'); pg.wait_for_timeout(800)
    slides = pg.evaluate("Deck.slides.map(s => [s.id, s.steps])")
    pngs = []
    for i, (sid, steps) in enumerate(slides, 1):
        for s in (range(1, steps + 1) if sid in ALL_STEPS else [*EXTRA.get(sid, []), steps]):
            pg.goto(f'{url}#/{i}/{s}'); pg.reload(); pg.wait_for_timeout(700)
            f = f'{tmp}/{len(pngs):03d}.png'; pg.screenshot(path=f); pngs.append(f)
    b.close()
    from PIL import Image
    ims = [Image.open(f).convert('RGB') for f in pngs]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    ims[0].save(OUT, save_all=True, append_images=ims[1:], resolution=144)
    print(OUT, len(ims), 'pages')
