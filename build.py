#!/usr/bin/env python3
"""
Build the static site for alp simsek's personal page.

    python3 build.py

Reads  : content/site.json   (all editable content)
         assets/             (stylesheet, photo)
Writes : docs/               (the site that gets published)

Standard library only -- no dependencies, no build tools.
"""

import json
import os
import re
import shutil
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))
CONTENT = os.path.join(ROOT, "content", "site.json")
ASSETS = os.path.join(ROOT, "assets")
OUT = os.path.join(ROOT, "docs")

FONTS = ("https://fonts.googleapis.com/css2?"
         "family=Inter:wght@400;450;500;600&"
         "family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&display=swap")

NAV = [
    ("Home", "index.html"),
    ("Research", "research.html"),
    ("Teaching", "teaching.html"),
]


# ---------------------------------------------------------------- helpers

def md_links(text):
    """Turn [label](url) into an anchor. Everything else passes through."""
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', text)


def and_join(names):
    """'A', 'A and B', 'A, B, and C'."""
    if not names:
        return ""
    if len(names) == 1:
        return names[0]
    if len(names) == 2:
        return f"{names[0]} and {names[1]}"
    return ", ".join(names[:-1]) + f", and {names[-1]}"


def primary_url(paper):
    """The link the title should point at: prefer a PDF, else the first link."""
    links = paper.get("links") or []
    for wanted in ("PDF", "Journal", "Read"):
        for l in links:
            if l["label"] == wanted:
                return l["url"]
    return links[0]["url"] if links else None


def paper_html(paper, idx):
    """Render one entry in a paper list."""
    title = paper["title"]
    url = primary_url(paper)
    head = f'<a href="{url}">{title}</a>' if url else title

    # meta line: coauthors, outlet, year, citation
    bits = []
    co = paper.get("coauthors") or []
    if co:
        bits.append("with " + and_join(co))
    outlet = paper.get("outlet")
    if outlet:
        tail = f'<span class="outlet">{outlet}</span> ({paper["year"]})'
        if paper.get("cite"):
            tail += f', {paper["cite"]}'
        bits.append(tail)
    else:
        bits.append(paper["year"])

    parts = [
        '<li class="paper">',
        f'  <p class="paper-title">{head}</p>',
        '  <p class="paper-meta">' + '<span class="dot">·</span>'.join(bits) + '</p>',
    ]

    if paper.get("note"):
        parts.append(f'  <p class="paper-note">{paper["note"]}</p>')

    actions = []
    for l in (paper.get("links") or []):
        actions.append(f'<a href="{l["url"]}">{l["label"]}</a>')
    if actions:
        parts.append('  <div class="paper-links">' + "".join(actions) + "</div>")

    if paper.get("abstract"):
        parts.append(
            '  <details class="abstract">\n'
            '    <summary>Abstract</summary>\n'
            f'    <div class="abstract-body">{paper["abstract"]}</div>\n'
            '  </details>'
        )

    parts.append("</li>")
    return "\n".join(parts)


def paper_list(papers):
    return ('<ul class="papers">\n'
            + "\n".join(paper_html(p, i) for i, p in enumerate(papers))
            + "\n</ul>")


# ---------------------------------------------------------------- page chrome

def page(title, body, active, person, description):
    site_url = DATA["site"]["url"].rstrip("/")
    canonical = site_url + ("/" if active == "index.html" else "/" + active)
    nav = []
    for label, href in NAV:
        cur = ' aria-current="page"' if href == active else ""
        nav.append(f'<a href="{href}"{cur}>{label}</a>')
    cv = next((l["url"] for l in DATA["links"] if l["label"] == "CV"), "#")
    nav.append(f'<a href="{cv}">CV<span class="ext">↗</span></a>')

    year = date.today().year
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{description}">
<meta name="author" content="{person['name']}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta property="og:url" content="{canonical}">
<link rel="canonical" href="{canonical}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 100 100%22><text y=%22.9em%22 font-size=%2290%22 font-family=%22Georgia,serif%22>A</text></svg>">
</head>
<body>

<header class="site-header">
  <div class="wrap">
    <a class="brand" href="index.html">{person['name']}</a>
    <nav class="site-nav">{"".join(nav)}</nav>
  </div>
</header>

<main>
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <span>{person['name']} · {person['affiliation']}</span>
    <span><a href="mailto:{person['email']}">{person['email']}</a> · updated {date.today():%B %Y}</span>
  </div>
</footer>

</body>
</html>
"""


# ---------------------------------------------------------------- pages

def build_home():
    p = DATA["person"]

    bio = "\n".join(f"<p>{md_links(par)}</p>" for par in p["bio"])
    quick = "".join(f'<a href="{l["url"]}">{l["label"]}</a>' for l in DATA["links"])
    roles = "".join(f"<li>{r}</li>" for r in p["roles"])

    recent = paper_list(DATA["working_papers"][:3])

    addr = "<br>".join(p["address"])

    body = f"""
<section class="hero">
  <div class="wrap">
    <div class="hero-grid">
      <div>
        <h1>{p['name']}</h1>
        <p class="role">{p['title']}<span class="sep">/</span>{p['affiliation']}</p>
        <p class="tagline">{p['tagline']}</p>
        <div class="prose">
{bio}
        </div>
        <div class="quicklinks">{quick}</div>
      </div>
      <div>
        <div class="portrait-wrap">
          <img class="portrait" src="assets/photo.jpg" width="480" height="600"
               alt="{p['name']}" loading="eager">
        </div>
        <div class="sidecard"><ul>{roles}</ul></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <h2 class="section-title">Recent working papers</h2>
    {recent}
    <p style="margin-top:1.5rem"><a href="research.html">All research →</a></p>
  </div>
</section>

<section class="section" id="contact">
  <div class="wrap">
    <h2 class="section-title">Contact</h2>
    <div class="contact-grid">
      <div>
        <h4>Address</h4>
        <p>{addr}</p>
      </div>
      <div>
        <h4>Email</h4>
        <p><a href="mailto:{p['email']}">{p['email']}</a></p>
      </div>
    </div>
  </div>
</section>
"""
    return page(f"{p['name']}", body, "index.html", p,
                f"{p['name']}, {p['title']} at the {p['affiliation']}. "
                "Research on macroeconomics, finance, asset prices, and monetary policy.")


def build_research():
    p = DATA["person"]

    # Top-level groups drive the jump nav, so keep them few. Anything that is
    # not a working paper, publication, or policy piece lives under "Other".
    groups = [
        ("Working papers", [
            (None, DATA["working_papers"]),
            ("Earlier working papers", DATA["older_working_papers"]),
        ]),
        ("Publications", [
            (None, DATA["publications"]),
        ]),
        ("Policy and other writing", [
            (None, DATA["other_writing"]),
        ]),
        ("Other", [
            ("Books", DATA["books"]),
            ("Theses", DATA["theses"]),
            ("Publications in mathematics", DATA["math"]),
            ("Other writing", DATA.get("misc", [])),
        ]),
    ]

    blocks, jumps = [], []
    for title, subgroups in groups:
        if not any(items for _, items in subgroups):
            continue
        anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        jumps.append(f'<a href="#{anchor}">{title}</a>')
        blocks.append(f'<h3 class="group-title" id="{anchor}">{title}</h3>')
        for subtitle, items in subgroups:
            if not items:
                continue
            if subtitle:
                blocks.append(f'<h4 class="subgroup-title">{subtitle}</h4>')
            blocks.append(paper_list(items))

    body = f"""
<div class="wrap">
  <h1 class="page-title">Research</h1>
  <p class="page-intro">Working papers and publications in macroeconomics and finance.
     Most links point to PDFs; click <em>Abstract</em> to expand.</p>
  <nav class="jumps">{"".join(jumps)}</nav>
  {"".join(blocks)}
</div>
"""
    return page(f"Research — {p['name']}", body, "research.html", p,
                f"Working papers and publications by {p['name']}.")


def build_teaching():
    p = DATA["person"]
    t = DATA["teaching"]

    def course_rows(courses):
        rows = []
        for c in courses:
            detail = f'{c["level"]} <span class="dot">·</span> {c["school"]} <span class="dot">·</span> {c["years"]}'
            links = "".join(
                f' <span class="dot">·</span> <a href="{l["url"]}">{l["label"]}</a>'
                for l in (c.get("links") or [])
            )
            rows.append(
                '<li class="course">'
                f'<div class="code">{c["code"]}</div>'
                f'<div><p class="name">{c["title"]}</p>'
                f'<div class="detail">{detail}{links}</div></div>'
                "</li>"
            )
        return '<ul class="courses">' + "".join(rows) + "</ul>"

    students = "".join(
        f'<div class="students-group"><h4>{g["school"]}</h4>'
        f'<p>{", ".join(g["people"])}</p></div>'
        for g in DATA["students"]
    )

    honors = "".join(f"<li>{h}</li>" for h in DATA["honors"])

    body = f"""
<div class="wrap">
  <h1 class="page-title">Teaching &amp; advising</h1>
  <p class="page-intro">Courses I teach at Yale, together with courses taught previously
     at MIT and Harvard, and the doctoral students I have advised.</p>

  <h3 class="group-title">Current courses</h3>
  {course_rows(t["current"])}

  <h3 class="group-title">Previously taught</h3>
  {course_rows(t["past"])}

  <h3 class="group-title">Ph.D. students advised</h3>
  {students}

  <h3 class="group-title">Selected honors</h3>
  <ul class="honors">{honors}</ul>
</div>
"""
    return page(f"Teaching — {p['name']}", body, "teaching.html", p,
                f"Courses and doctoral advising by {p['name']} at Yale SOM, MIT, and Harvard.")


# ---------------------------------------------------------------- main

def main():
    global DATA
    with open(CONTENT, encoding="utf-8") as f:
        DATA = json.load(f)

    os.makedirs(OUT, exist_ok=True)

    pages = {
        "index.html": build_home,
        "research.html": build_research,
        "teaching.html": build_teaching,
    }
    for name, fn in pages.items():
        with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
            f.write(fn())
        print(f"  wrote docs/{name}")

    dest = os.path.join(OUT, "assets")
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(ASSETS, dest)
    print(f"  copied assets/ -> docs/assets/")

    # so GitHub Pages serves the files as-is instead of running Jekyll
    open(os.path.join(OUT, ".nojekyll"), "w").close()

    # tells GitHub Pages which custom domain to serve
    domain = DATA.get("site", {}).get("domain")
    if domain:
        with open(os.path.join(OUT, "CNAME"), "w", encoding="utf-8") as f:
            f.write(domain + "\n")
        print(f"  wrote docs/CNAME ({domain})")

    print("done.")


if __name__ == "__main__":
    DATA = {}
    main()
