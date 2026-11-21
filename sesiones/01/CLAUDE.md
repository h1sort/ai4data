# Sesión 01 · deck y labs

Read `PLAN.md` first: run of show, timing and sources. The deck engine (`deck/engine.js`, `particles.js`, `styles.css`, `tools/`) is copied from h1sort/udlap (which copied cide and datapub); `CONTRACT.md` in h1sort/datapub documents the slide API.

## Working rules
- Slide text in Spanish with correct accents; code, file names and commit messages in English.
- Every number on a slide comes from a run of the labs in this folder or a source in `PLAN.md` §3. If you re-run a lab and the number changes, update the slide, the notes and `PLAN.md` together.
- Speaker notes: Spanish, first person, Carlos's spoken voice, end with the bridge to the next slide, stage directions in `<p class="dir">[…]</p>`.
- Students run everything with `uv run` from the repo root, one line per command (no shell variables, no `\` continuations): it must work in PowerShell and cmd. Python 3.14 via uv; avoid Node unless there is no Python option.
- No network at runtime. Projector rules: text ≥ 28px on the 1920×1080 stage, labels ≥ 20px, keep the bottom 140px free.
- Never cut `apuesta`, `sumas`, `filas` or `lab-marcador`.

## Publishing
The site copy lives in h1sort-website at `public/ai4data/01/`. From the root of this repo: `uv run herramientas/publicar.py <path to h1sort-website>` (copies `web/` and builds the deck without notes), then build, PR and merge in h1sort-website.
