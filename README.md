# Croconile One-Pagers

Static GitHub Pages site for the Croconile one-pagers, rebuilt as responsive web pages from the original PDFs.

| Page | Audience | PDF |
|---|---|---|
| [index.html](index.html) | Hub for all one-pagers | — |
| [croconile-for-all.html](croconile-for-all.html) | Everyone (full overview) | [pdf](pdf/croconile-for-all.pdf) |
| [croconile-for-all-v2.html](croconile-for-all-v2.html) | Everyone (condensed) | [pdf](pdf/croconile-for-all-v2.pdf) |
| [employed.html](employed.html) | People in a role | [pdf](pdf/employed.pdf) |
| [experienced-job-seekers.html](experienced-job-seekers.html) | Experienced job seekers | [pdf](pdf/experienced-job-seekers.pdf) |
| [first-time-job-seekers.html](first-time-job-seekers.html) | First-time job seekers | [pdf](pdf/first-time-job-seekers.pdf) |
| [leaders-and-managers.html](leaders-and-managers.html) | Leaders and managers | [pdf](pdf/leaders-and-managers.pdf) |
| [professors-and-trainers.html](professors-and-trainers.html) | Professors and trainers | [pdf](pdf/professors-and-trainers.pdf) |
| [students-and-trainees.html](students-and-trainees.html) | Students and trainees | [pdf](pdf/students-and-trainees.pdf) |

## Editing

Page content lives in `build/build.py` (one dict per audience). Edit it, then regenerate the HTML:

```bash
python3 build/build.py
```

Styles are in `assets/styles.css`. No build tooling or dependencies beyond Python 3.

## Publishing

Settings → Pages → Source: *Deploy from a branch*, Branch: `main`, folder `/ (root)`.

© 2026 Croconile. Proprietary and confidential. WorkCard™, DepthCard™ and Signal Space™ are trademarks of Croconile.
