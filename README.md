# alpsimsek.org

Source for my personal academic website and CV. All website content lives in one
JSON file; a small Python script turns it into the static site that gets
published. The CV is LaTeX.

Replaces the old Google Sites page, which now points here.

## Folder structure

```
website/
  content/site.json     -- ALL website content (bio, papers, teaching, links)
  assets/               -- stylesheet and photo
  build.py              -- generates docs/ from content/ + assets/
  docs/                 -- the generated site; GitHub Pages serves this
    cv.pdf              -- self-hosted copy of the CV
  cv/
    simsekCV.pdf        -- the file behind the Dropbox share link (see below)
    simsekCV_YYYY_MM.pdf-- dated snapshots
    publish.sh          -- build the CV and copy it everywhere it is served
    latex/              -- CV source
      simsekCV.tex      -- content
      cvstyle.sty       -- typography
      presentations.tex -- archived seminar list, not in the public CV
      build.sh
    cv old/             -- every prior version, including the Word originals
  CLAUDE.md             -- working notes
```

## Updating the website

1. Edit `content/site.json`.
2. `python3 build.py`
3. Preview: `cd docs && python3 -m http.server 8765`, then <http://localhost:8765>
4. `git push` — the live site updates in about fifteen seconds.

No dependencies; `build.py` uses only the Python standard library.

### Adding a paper

Add an entry to the relevant list in `content/site.json` (`working_papers`,
`publications`, `older_working_papers`, `other_writing`, `books`, `theses`,
`math`, `misc`). Lists render in file order, so new papers go at the top.

```json
{
  "title": "Title of the Paper",
  "coauthors": ["Ricardo Caballero"],
  "year": "2026",
  "outlet": "Journal of Finance",
  "cite": "79(3), 1719-1753",
  "note": "Optional line under the title. HTML allowed.",
  "links": [
    { "label": "PDF", "url": "https://www.dropbox.com/..." },
    { "label": "Slides", "url": "https://www.dropbox.com/..." }
  ],
  "abstract": "Optional. Shown behind an 'Abstract' toggle."
}
```

- `outlet` and `cite` are for published papers; omit for working papers.
- The title links to the first `PDF` link, else `Journal`, else the first link.
- Keep the Dropbox `?dl=0` pattern: replacing the PDF in Dropbox updates what
  visitors download with no rebuild.
- **Whatever changes here, change in the CV too** — see `CLAUDE.md`.

## Updating the CV

1. Edit `cv/latex/simsekCV.tex`.
2. `cv/publish.sh` — builds and writes the PDF to three places:
   - `cv/simsekCV.pdf`, the file the Dropbox share link serves
   - `cv/simsekCV_YYYY_MM.pdf`, a dated snapshot
   - `docs/cv.pdf`, served at alpsimsek.org/cv.pdf
3. `git push` so the self-hosted copy goes live. Dropbox syncs on its own.

`cv/latex/build.sh --long` produces `simsekCV_full.pdf`, which appends the
archived seminar and conference presentations. Useful for promotion cases and
award nominations; not the public version.

### The Dropbox link

`cv/simsekCV.pdf` is the file behind
`dropbox.com/s/v7c8ki8d0lcqtub/simsekCV.pdf`. That URL appears on the Yale SOM
faculty page and inside every circulated copy of the CV, so the file is
overwritten in place and never renamed or moved. `publish.sh` handles this.

## Hosting

GitHub Pages, from `/docs` on `main` in `alp-simsek/alp-simsek.github.io`.
Domain registered at Namecheap through 2036; DNS is four A records to
`185.199.108-111.153` plus a `www` CNAME, with HTTPS enforced.
