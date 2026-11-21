#!/usr/bin/env python3
"""Slides QR with the little presentation-screen icon in the middle (as in h1sort/datapub).
Usage: deck/tools/qr.py URL OUT.svg [github]   (needs segno; error correction H so the cleared center still scans)
`github` puts the GitHub mark in the center instead of the screen icon."""
import sys, segno
url, out = sys.argv[1], sys.argv[2]
icon = sys.argv[3] if len(sys.argv) > 3 else 'slides'
q = segno.make(url, error='h', boost_error=False)
m = [list(r) for r in q.matrix]; n = len(m)
c, half = n / 2, (4.0 if icon == 'github' else 3.0)  # clear a window around the center for the icon
lo, hi = int(c - half), int(c + half + 0.999)
cells = [f"M{x} {y}h1v1h-1z" for y in range(n) for x in range(n) if m[y][x] and not (lo <= x < hi and lo <= y < hi)]
GITHUB = ('M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12')
if icon == 'github':
    s, t = 0.3, c - 3.6                    # 24-unit mark scaled to 7.2 modules, centered
    mark = f'<g shape-rendering="geometricPrecision" transform="translate({t:.2f} {t:.2f}) scale({s})"><path fill="#000" d="{GITHUB}"/></g>'
else:
    s, t = 0.21666666666666667, c - 2.6
    mark = (f'<g shape-rendering="geometricPrecision" transform="translate({t:.2f} {t:.2f}) scale({s})"><g fill="#000">'
            '<rect x="1.5" y="2.5" width="21" height="14.5" rx="2"/><rect x="10.8" y="16" width="2.4" height="4.5"/>'
            '<rect x="7" y="19.5" width="10" height="2.4" rx="1.2"/><path d="M10 6.5l5.5 3.25-5.5 3.25z" fill="#fff"/></g></g>')
svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {n} {n}" shape-rendering="crispEdges">'
       f'<path fill="#000" d="{"".join(cells)}"/>{mark}</svg>')
open(out, 'w').write(svg); print(out, n, 'modules')
