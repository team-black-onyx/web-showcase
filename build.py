"""Dependency-free Markdown-to-static-HTML site generator."""
import html
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "dist"


def parse(path):
    _, front, body = path.read_text(encoding="utf-8").split("---", 2)
    data, key = {}, ""
    for line in front.strip().splitlines():
        if line.startswith("  - ") and key == "tags":
            data.setdefault(key, []).append(line[4:].strip())
        elif line.startswith("  ") and key == "technical" and ":" in line:
            subkey, value = line.strip().split(":", 1)
            if not isinstance(data.get("technical"), dict):
                data["technical"] = {}
            data.setdefault("technical", {})[subkey.strip()] = value.strip()
        elif ":" in line:
            key, value = line.split(":", 1)
            key, value = key.strip(), value.strip()
            data[key] = value.strip('"\'') if value else []
    if data.get("technical") == []:
        data["technical"] = {}
    data["slug"] = data.get("slug", path.stem)
    data["body"] = body.strip()
    return data


def inline(s):
    s = html.escape(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    return re.sub(r"\[([^]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', s)


def markdown(text):
    out, para, items = [], [], []
    def flush():
        if para:
            out.append("<p>" + " ".join(map(inline, para)) + "</p>"); para.clear()
        if items:
            out.append("<ul>" + "".join("<li>" + inline(x) + "</li>" for x in items) + "</ul>"); items.clear()
    for line in text.splitlines():
        if not line.strip(): flush()
        elif line.startswith("## "): flush(); out.append("<h2>" + inline(line[3:]) + "</h2>")
        elif line.startswith("### "): flush(); out.append("<h3>" + inline(line[4:]) + "</h3>")
        elif line.startswith("- "): items.append(line[2:])
        else: para.append(line)
    flush()
    return "\n".join(out)


def render(title, description, body, *, prefix="", home="./", active=""):
    shell = (ROOT / "templates/shell.html").read_text(encoding="utf-8")
    active_exp = 'aria-current="page"' if active else ""
    github = json.loads((ROOT / "site-config.json").read_text(encoding="utf-8")).get("github_url", "").strip()
    github_nav = f'<a class="nav-github" href="{html.escape(github, quote=True)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>' if github else '<span class="nav-github">GitHub <span class="soon">SOON</span></span>'
    github_footer = f'<a class="footer-github" href="{html.escape(github, quote=True)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>' if github else '<span class="footer-github">GitHub <span class="soon">SOON</span></span>'
    replacements = {"TITLE": html.escape(title), "DESCRIPTION": html.escape(description), "BODY": body,
                    "ASSET_PREFIX": prefix, "HOME": home, "ACTIVE_EXPERIMENTS": active_exp, "GITHUB_NAV": github_nav, "GITHUB_FOOTER": github_footer}
    for key, value in replacements.items():
        shell = shell.replace("{{" + key + "}}", value)
    return shell


def build():
    github = json.loads((ROOT / "site-config.json").read_text(encoding="utf-8")).get("github_url", "").strip()
    experiments = sorted((parse(p) for p in (ROOT / "experiments").glob("*.md")),
                         key=lambda e: e.get("date", ""), reverse=True)
    shutil.rmtree(OUT, ignore_errors=True)
    (OUT / "assets").mkdir(parents=True)
    for name in ("site.css", "site.js"):
        shutil.copy2(ROOT / "assets" / name, OUT / "assets" / name)
    cards = []
    for e in experiments:
        tags = "".join(f'<span class="tag">{html.escape(tag)}</span>' for tag in e.get("tags", []))
        cards.append(f'<a class="experiment-card reveal" href="experiments/{html.escape(e["slug"])}/"><div class="card-top"><span class="status"><i></i>{html.escape(e.get("status", "In Progress"))}</span><span class="mono">{html.escape(e.get("date", ""))}</span></div><h3>{html.escape(e["title"])}<span class="arrow" aria-hidden="true">↗</span></h3><p>{html.escape(e["description"])}</p><div class="tag-row">{tags}</div><div class="card-foot mono">RESEARCH NOTE <span>OPEN EXPERIMENT&nbsp; ↗</span></div></a>')
        meta = "".join(f'<div><dt>{label}</dt><dd>{html.escape(str(value)).upper()}</dd></div>' for label, value in (("Status", e.get("status", "In Progress")), ("Researchers", e.get("researchers", "2")), ("Started", e.get("date", ""))))
        tech = "".join(f'<div><dt>{html.escape(k)}</dt><dd>{html.escape(str(v))}</dd></div>' for k, v in e.get("technical", {}).items())
        code = f'<a class="text-link" href="{html.escape(e.get("code_url") or github, quote=True)}" target="_blank" rel="noopener noreferrer">View code ↗</a>' if e.get("code_url") or github else '<span class="muted-note mono">CODE REPOSITORY TO BE ADDED</span>'
        detail = f'<main id="main" class="detail wrap"><a class="back-link mono" href="../../#experiments">← ALL EXPERIMENTS</a><header class="detail-head"><div class="eyebrow"><span class="eyebrow-mark"></span> EXPERIMENT / {html.escape(e["slug"].upper())}</div><h1>{html.escape(e["title"])}</h1><p class="detail-lede">{html.escape(e["description"])}</p></header><dl class="meta-grid">{meta}</dl><dl class="tech-grid">{tech}</dl><article class="prose">{markdown(e["body"])}</article><div class="code-row">{code}</div><aside class="record-note"><span class="mono">FIELD NOTE</span><p>This record is updated as the experiment develops. Claims reflect the evidence currently available.</p></aside></main>'
        folder = OUT / "experiments" / e["slug"]
        folder.mkdir(parents=True)
        (folder / "index.html").write_text(render(e["title"] + " — Layercraft", e["description"], detail, prefix="../../", home="../../", active="experiments"), encoding="utf-8")
    github_cta = f'<a class="button button-quiet" href="{html.escape(github, quote=True)}" target="_blank" rel="noopener noreferrer">GitHub ↗</a>' if github else '<span class="button button-quiet disabled">GitHub <span class="mono">SOON</span></span>'
    home = f'''<main id="main"><section class="hero wrap" id="top"><div class="hero-grid" aria-hidden="true"></div><div class="hero-copy"><div class="eyebrow"><span class="eyebrow-mark"></span> INDEPENDENT RESEARCH / ENGINEERING</div><h1>Experiments at the layers<br class="desktop-break"> beneath <span>intelligence.</span></h1><p class="hero-lede">We build things, test ideas, investigate what happens under the hood, and document what we learn.</p><div class="hero-actions"><a class="button button-primary" href="#experiments">Explore experiments <span>↓</span></a>{github_cta}</div></div><div class="layer-illustration" aria-hidden="true"><span></span><span></span><span></span><span></span><span></span><div class="layer-caption mono">SYSTEM / 001<br>OBSERVE WHAT EMERGES</div></div><div class="hero-index mono"><span>01 — 03</span><span>BUILD · MEASURE · LEARN</span></div></section><section class="section experiments-section" id="experiments"><div class="wrap"><div class="section-heading reveal"><div><div class="eyebrow">THE WORK</div><h2>Experiments</h2></div><p>Questions become experiments.<br>Experiments become evidence.</p></div><div class="experiment-grid">{"".join(cards)}</div></div></section><section class="section about-section" id="about"><div class="wrap about-layout"><div class="about-intro reveal"><div class="eyebrow">A SMALL, OPEN LAB</div><h2>Two minds.<br><span>One lab.</span></h2><p>Two engineers, curious about what happens beneath the surface. Layercraft is where we turn that curiosity into experiments.</p></div><div class="principles"><article class="principle reveal"><span class="principle-num mono">01</span><div><h3>Build</h3><p>Turn ideas into working experiments.</p></div><span class="principle-glyph">＋</span></article><article class="principle reveal"><span class="principle-num mono">02</span><div><h3>Question</h3><p>Investigate assumptions instead of taking them for granted.</p></div><span class="principle-glyph">?</span></article><article class="principle reveal"><span class="principle-num mono">03</span><div><h3>Learn</h3><p>Results, including failures, become the next experiment.</p></div><span class="principle-glyph">↗</span></article></div></div></section><section class="method-section"><div class="wrap method-layout"><div class="eyebrow">HOW WE WORK</div><div><div class="method-line"><span>Build</span><b>→</b><span>Measure</span><b>→</b><span>Inspect</span><b>→</b><span>Learn</span></div><p>We publish what evidence supports, make failures legible, and follow observations wherever they lead.</p></div></div></section></main>'''
    (OUT / "index.html").write_text(render("Layercraft — Experiments beneath intelligence", "Experiments at the layers beneath intelligence. An independent AI research and engineering notebook.", home), encoding="utf-8")
    (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")
    print(f"Built {len(experiments)} experiments into {OUT}")


if __name__ == "__main__":
    build()
