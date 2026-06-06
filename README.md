# Slides

Published site: <https://yang-yiming.github.io/slides/>

`slides.toml` is the source of truth for the decks shown on the site. The
generated static site lives in `site/`, and GitHub Actions only publishes that
folder to GitHub Pages.

## Local build

Build all managed decks and regenerate the index:

```bash
python3 scripts/build_site.py
```

Regenerate only the root index after editing metadata:

```bash
python3 scripts/build_site.py --index-only
```

Use `kind = "slidev"` for Slidev projects, and add future PDF or static HTML
decks to `slides.toml` with their own `kind`, `source`, and `entry`.

## Content List

| link | description | updated |
|------|-------------|---------|
| [make_gyx](https://yang-yiming.github.io/slides/make_gyx/) | Simple tutorial for Makefile & CMake. | 2025-09-09 |
| [share_rust](https://yang-yiming.github.io/slides/share_rust/) | Share for the SUSTCSC competition - Rust. | 2025-09-12 |
| [fcy_papers](https://yang-yiming.github.io/slides/fcy_papers/) | Short summary of Prof. Fu Chaoyou's papers (2024-2025). | 2025-10-13 |
| [spark-proj-2](https://yang-yiming.github.io/slides/spark-proj-2/) | Slides of my Spark course project 2. | 2026-06-01 |
