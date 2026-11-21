#!/usr/bin/env python3
"""Build the public web copy of the deck: no speaker notes, flat paths.

Usage: deck/tools/public-build.py <out_dir> [--skip ID ...] [--noindex]

<out_dir>/index.html is the deck; assets/ holds only the files the slides
reference. --skip drops slides by id, --noindex keeps the copy out of search engines.
Adapted from h1sort/datapub (this deck has no video).
"""
import argparse, re, shutil, subprocess, sys
from pathlib import Path

DECK = Path(__file__).resolve().parents[1]
REPO = DECK.parent
SOURCES = ['index.html', 'styles.css', 'particles.js', 'engine.js', 'acts']
NOTES = re.compile(r'\n[ \t]*notes:\s*`(?:\\.|[^`\\])*`,?')

ap = argparse.ArgumentParser()
ap.add_argument('out')
ap.add_argument('--skip', nargs='*', default=[])
ap.add_argument('--noindex', action='store_true')
args = ap.parse_args()
out = Path(args.out).resolve()
if out.exists():
    shutil.rmtree(out)
out.mkdir(parents=True)

for name in SOURCES:
    src = DECK / name
    (shutil.copytree if src.is_dir() else shutil.copy2)(src, out / name)

refs = set()
for f in [*out.rglob('*.js'), *out.rglob('*.html'), *out.rglob('*.css')]:
    t = f.read_text()
    t = NOTES.sub('', t)
    refs |= set(re.findall(r'\.\./assets/([^\'"`)\s]+)', t))
    t = t.replace('../assets/', 'assets/')
    if f.name == 'index.html':
        skip = f' data-skip="{" ".join(args.skip)}"' if args.skip else ''
        t = t.replace('<html lang="es">', f'<html lang="es" data-public{skip}>')
        if args.noindex:
            t = t.replace('<meta charset="utf-8">', '<meta charset="utf-8">\n  <meta name="robots" content="noindex, nofollow">')
    f.write_text(t)

# Stills are named in a JS table (`${f}`); copy that folder whole.
for r in sorted(refs):
    src = REPO / 'assets' / r
    if '${' in r:
        src = src.parent
        shutil.copytree(src, out / 'assets' / src.relative_to(REPO / 'assets'), dirs_exist_ok=True)
    else:
        (out / 'assets' / r).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, out / 'assets' / r)


# Guards: no notes left, every script still parses.
leftover = [str(f) for f in out.rglob('*.js') if re.search(r'\bnotes:\s*`', f.read_text())]
if leftover:
    sys.exit(f'notes left in: {leftover}')
for f in out.rglob('*.js'):
    subprocess.run(['node', '--check', str(f)], check=True)
print(out, f'{sum(1 for _ in out.rglob("*") if _.is_file())} files',
      f'skip={args.skip}', f'noindex={args.noindex}')
