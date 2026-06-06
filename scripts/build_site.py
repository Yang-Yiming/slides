#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import os
import shutil
import subprocess
import sys
from contextlib import contextmanager
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "slides.toml"


def load_config() -> dict:
    config = parse_manifest(CONFIG_PATH.read_text(encoding="utf-8"))
    if not isinstance(config.get("deck"), list):
        raise ValueError("slides.toml must contain at least one [[deck]] entry")
    return config


def parse_manifest(text: str) -> dict:
    """Parse the small TOML subset used by slides.toml.

    This keeps the build script usable with the macOS system Python 3.9, which
    does not include tomllib.
    """
    config: dict = {}
    current: dict | None = None
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line == "[[deck]]":
            current = {}
            config.setdefault("deck", []).append(current)
            continue
        if "=" not in line:
            raise ValueError(f"slides.toml:{line_number}: expected key = value")
        key, value = [part.strip() for part in line.split("=", 1)]
        parsed = parse_value(value, line_number)
        target = current if current is not None else config
        target[key] = parsed
    return config


def parse_value(value: str, line_number: int) -> str | bool:
    if value in {"true", "false"}:
        return value == "true"
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return bytes(value[1:-1], "utf-8").decode("unicode_escape")
    raise ValueError(f"slides.toml:{line_number}: only quoted strings and booleans are supported")


def package_manager(source: Path) -> str:
    if (source / "bun.lock").exists() or (source / "bun.lockb").exists():
        return "bun"
    if (source / "pnpm-lock.yaml").exists():
        return "pnpm"
    if (source / "yarn.lock").exists():
        return "yarn"
    return "npm"


def run_build(deck: dict, base_url: str) -> None:
    source = ROOT / required(deck, "source")
    if not source.exists():
        raise FileNotFoundError(f"{deck['id']}: source directory does not exist: {source}")
    if not (source / "package.json").exists():
        raise FileNotFoundError(f"{deck['id']}: missing package.json in {source}")

    base = join_url(base_url, deck["id"]) + "/"
    manager = str(deck.get("manager") or package_manager(source))
    commands = {
        "bun": ["bun", "run", "build", "--", "--base", base, "--download", "false"],
        "npm": ["npm", "run", "build", "--", "--base", base, "--download", "false"],
        "pnpm": ["pnpm", "run", "build", "--", "--base", base, "--download", "false"],
        "yarn": ["yarn", "run", "build", "--base", base, "--download", "false"],
    }
    if manager not in commands:
        raise ValueError(f"{deck['id']}: unsupported package manager: {manager}")

    print(f"building {deck['id']} with {manager} (base {base})")
    with patched_slidev_frontmatter(source / "slides.md"):
        subprocess.run(commands[manager], cwd=source, check=True)


@contextmanager
def patched_slidev_frontmatter(slides_path: Path):
    if not slides_path.exists():
        yield
        return

    original = slides_path.read_text(encoding="utf-8")
    patched = original.replace("\nseoMeta:\n  ogImage: auto\n", "\n")
    if patched == original:
        yield
        return

    slides_path.write_text(patched, encoding="utf-8")
    try:
        yield
    finally:
        slides_path.write_text(original, encoding="utf-8")


def copy_tree(src: Path, dest: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(f"missing build output: {src}")
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dest)


def copy_static(deck: dict, dest: Path) -> None:
    source_value = deck.get("source")
    if not source_value:
        raise ValueError(f"{deck['id']}: {deck['kind']} deck requires source")
    source = ROOT / source_value
    if source.is_dir():
        copy_tree(source, dest)
        return
    dest.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest / source.name)


def required(deck: dict, key: str) -> str:
    value = deck.get(key)
    if not isinstance(value, str) or not value:
        raise ValueError(f"deck entry is missing required string field: {key}")
    return value


def join_url(base: str, *parts: str) -> str:
    url = base.rstrip("/")
    for part in parts:
        url += "/" + part.strip("/")
    return url or "/"


def deck_href(config: dict, deck: dict) -> str:
    base = str(config.get("base_url", "/"))
    href = join_url(base, deck["id"])
    entry = str(deck.get("entry", "index.html"))
    if entry != "index.html":
        href = join_url(href, entry)
    elif not href.endswith("/"):
        href += "/"
    return href


def render_index(config: dict, output_dir: Path) -> None:
    title = str(config.get("site_title", "Slides"))
    description = str(config.get("site_description", ""))
    decks = config["deck"]

    cards = []
    for deck in decks:
        deck_id = required(deck, "id")
        deck_title = html.escape(str(deck.get("title", deck_id)))
        deck_description = html.escape(str(deck.get("description", "")))
        kind = html.escape(str(deck.get("kind", "static")).upper())
        updated = html.escape(str(deck.get("updated", "")))
        href = html.escape(deck_href(config, deck))
        meta_parts = [f"<span>{kind}</span>"]
        if updated:
            meta_parts.append(f"<time>{updated}</time>")
        cards.append(
            f"""
      <article class="deck">
        <a class="deck-link" href="{href}">
          <div class="deck-meta">{''.join(meta_parts)}</div>
          <h2>{deck_title}</h2>
          <p>{deck_description}</p>
        </a>
      </article>""".rstrip()
        )

    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "index.html").write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --bg: #f6f7f9;
      --panel: #ffffff;
      --text: #171a1f;
      --muted: #606875;
      --line: #d9dde5;
      --accent: #1f6feb;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      background: var(--bg);
      color: var(--text);
      font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      line-height: 1.5;
    }}
    main {{
      width: min(960px, calc(100% - 32px));
      margin: 0 auto;
      padding: 56px 0;
    }}
    header {{
      margin-bottom: 28px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: clamp(2rem, 5vw, 3.6rem);
      line-height: 1;
      letter-spacing: 0;
    }}
    .intro {{
      margin: 0;
      max-width: 680px;
      color: var(--muted);
      font-size: 1rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 14px;
    }}
    .deck {{
      min-height: 160px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    .deck-link {{
      display: flex;
      height: 100%;
      flex-direction: column;
      padding: 18px;
      color: inherit;
      text-decoration: none;
    }}
    .deck-link:hover h2 {{
      color: var(--accent);
    }}
    .deck-meta {{
      display: flex;
      justify-content: space-between;
      gap: 12px;
      color: var(--muted);
      font-size: .78rem;
      text-transform: uppercase;
    }}
    h2 {{
      margin: 22px 0 8px;
      font-size: 1.15rem;
      line-height: 1.2;
      letter-spacing: 0;
    }}
    .deck p {{
      margin: 0;
      color: var(--muted);
      font-size: .94rem;
    }}
  </style>
</head>
<body>
  <main>
    <header>
      <h1>{html.escape(title)}</h1>
      <p class="intro">{html.escape(description)}</p>
    </header>
    <section class="grid" aria-label="Slide decks">
{chr(10).join(cards)}
    </section>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def validate_entries(config: dict, output_dir: Path) -> None:
    for deck in config["deck"]:
        deck_id = required(deck, "id")
        entry = str(deck.get("entry", "index.html"))
        path = output_dir / deck_id / entry
        if not path.exists():
            raise FileNotFoundError(f"{deck_id}: entry file not found after build: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the static slide index and managed deck outputs.")
    parser.add_argument("--skip-build", action="store_true", help="copy existing dist/static files and regenerate the index")
    parser.add_argument("--index-only", action="store_true", help="only regenerate site/index.html")
    parser.add_argument("--no-clean", action="store_true", help="do not remove the output directory first")
    args = parser.parse_args()

    config = load_config()
    output_dir = ROOT / str(config.get("output_dir", "site"))
    base_url = str(config.get("base_url", "/"))

    if output_dir.exists() and not args.no_clean and not args.index_only:
        shutil.rmtree(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if not args.index_only:
        for deck in config["deck"]:
            deck_id = required(deck, "id")
            kind = str(deck.get("kind", "static")).lower()
            dest = output_dir / deck_id
            if kind == "slidev":
                if not args.skip_build:
                    run_build(deck, base_url)
                copy_tree(ROOT / required(deck, "source") / "dist", dest)
            elif kind in {"html", "pdf", "static"}:
                copy_static(deck, dest)
            elif kind == "external":
                continue
            else:
                raise ValueError(f"{deck_id}: unsupported deck kind: {kind}")

    render_index(config, output_dir)
    if not args.index_only:
        validate_entries(config, output_dir)
    print(f"wrote {output_dir.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
