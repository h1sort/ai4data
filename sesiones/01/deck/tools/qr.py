#!/usr/bin/env python3
"""Slides QR with the little presentation-screen icon in the middle (as in h1sort/datapub).
Usage: deck/tools/qr.py URL OUT.svg   (needs segno; error correction H so the cleared center still scans)"""
import sys, segno
url, out = sys.argv[1], sys.argv[2]
q = segno.make(url, error='h', boost_error=False)
m = [list(r) for r in q.matrix]; n = len(m)
c, half = n / 2, 3.0                      # clear a 6×6-module window around the center
lo, hi = int(c - half), int(c + half + 0.999)
cells = [f"M{x} {y}h1v1h-1z" for y in range(n) for x in range(n) if m[y][x] and not (lo <= x < hi and lo <= y < hi)]
s, t = 0.21666666666666667, c - 2.6
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges">'
       f'<path fill="#000" d="{"".join(cells)}"/>'
       f'<g shape-rendering="geometricPrecision" transform="translate({t:.2f} {t:.2f}) scale({s})"><g fill="#000">'
       '<rect x="1.5" y="2.5" width="21" height="14.5" rx="2"/><rect x="10.8" y="16" width="2.4" height="4.5"/>'
       '<rect x="7" y="19.5" width="10" height="2.4" rx="1.2"/><path d="M10 6.5l5.5 3.25-5.5 3.25z" fill="#fff"/></g></g></svg>')
open(out, 'w').write(svg); print(out, n, 'modules')
