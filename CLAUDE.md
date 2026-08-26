# Working on this project

Alp Simsek's personal website (alpsimsek.org) and CV. Both live in this folder.

## The rule that matters most

**When a piece of writing enters the record or changes status on the website,
make the same change to the CV in the same session.**

Alp gives instructions in terms of the website, with the understanding that the
CV follows. Do not wait to be asked. The rule covers exactly three things:

- A new working paper appears → add to **Working Papers** in the CV
- A paper is accepted or published → move it in **both** (`working_papers` →
  `publications` in `content/site.json`; Working Papers → the numbered
  Publications list in `simsekCV.tex`, with outlet, volume and pages)
- A new opinion piece, VoxEU column, or policy essay appears → add to the
  site's `other_writing` **and** to *Other Publications* in the CV

That is the whole rule. It is about what exists and what status it holds, not
about presentation. Website-only edits do **not** propagate: adding a link,
writing or revising an abstract, adding a note under a title, reordering a
section, renaming a heading. The CV lists papers with outlets; it does not
carry the site's links or blurbs.

CV-only items — editorships, honors, PhD students, service, affiliations — come
as explicit instructions. Don't invent them. The annual Yale review is a
backstop that catches whatever slipped through, so a missed CV-only item is not
a crisis; a missed paper is.

After changing the CV, run `cv/publish.sh` so all three copies stay in step.

## Do not touch

- **`cv/simsekCV.pdf`** — this *is* the file behind the Dropbox share link
  `dropbox.com/s/v7c8ki8d0lcqtub/simsekCV.pdf`, which is printed on the Yale SOM
  faculty page and inside every circulated copy of the CV. Overwrite it in place
  via `publish.sh`. Never rename, move, or delete it.
- **The Google Sites pages** at `sites.google.com/view/alpsimsek` — they are
  signposts pointing here, and they stay live indefinitely so old citations keep
  resolving. Don't propose deleting them.

## How things build

```
python3 build.py        # content/site.json + assets/ -> docs/
cv/publish.sh           # CV -> cv/simsekCV.pdf, dated snapshot, docs/cv.pdf
git push                # GitHub Pages redeploys in ~15 seconds
```

`build.py` is standard library only — keep it that way. The CV needs xelatex
(TeX Live is installed at `/Library/TeX/texbin`).

## Facts worth not rediscovering

- Repo is `alp-simsek/alp-simsek.github.io`, public, serving `/docs` from `main`.
  Pushes authenticate through the macOS keychain; no SSH key needed.
- Domain is registered at Namecheap through 2036, DNS is four A records to
  `185.199.108–111.153` plus a `www` CNAME. HTTPS is enforced.
- `cv/` is gitignored: it holds ~25 historical CV versions and the repo is
  public. `docs/cv.pdf` is tracked; the LaTeX source deliberately is not —
  nothing depends on it being in git and Dropbox already versions it.
- Paper PDFs are Dropbox links, by preference. Keep that pattern; updating a PDF
  in Dropbox then needs no site rebuild.
- The seminar and conference presentation list was removed from the CV in August
  2026. It is archived in `cv/latex/presentations.tex` and still builds into
  `simsekCV_full.pdf` via `cv/publish.sh`-adjacent `latex/build.sh --long`.

## Style

Match the existing code. `build.py` and `cvstyle.sty` are commented at the level
a reader needs and no more. No frameworks, no build tooling, no dependencies.
