# alpsimsek — personal website

The source for my personal academic website. All content lives in one file;
a small Python script turns it into the static site that gets published.

Replaces the old Google Sites page at `sites.google.com/view/alpsimsek`.

## Folder structure

```
website/
  content/site.json     -- ALL editable content (bio, papers, teaching, links)
  assets/               -- stylesheet and photo
    style.css
    photo.jpg
  build.py              -- generates docs/ from content/ + assets/
  docs/                 -- the generated site (this is what gets published)
  cv/                   -- CV archive (not published; the site links to Dropbox)
  README.md
```

## Updating the site

1. Edit `content/site.json`.
2. Run the build:

   ```
   cd ~/Dropbox/Desktop/website
   python3 build.py
   ```

3. Preview locally:

   ```
   cd docs && python3 -m http.server 8765
   ```

   then open <http://localhost:8765>.

4. Publish (see *Publishing* below).

No dependencies -- `build.py` uses only the Python standard library.

## Adding a paper

Add an entry to the relevant list in `content/site.json`
(`working_papers`, `publications`, `older_working_papers`, `turkey`,
`other_writing`, `books`, `theses`, `math`). Lists are displayed in the
order they appear in the file, so put new papers at the top.

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

Notes:

- `outlet` and `cite` are for published papers; leave them out for working papers.
- The paper title links to the first `PDF` link, else `Journal`, else the first link.
- Dropbox links work as-is with `?dl=0`. Keep that pattern -- updating the PDF in
  Dropbox updates what visitors download, with no site rebuild needed.

## The CV

The nav "CV" button points at a fixed Dropbox link
(`dropbox.com/s/v7c8ki8d0lcqtub/simsekCV.pdf`). Replacing that file in Dropbox
updates the CV everywhere. The `cv/` folder here is just the local archive.

## Publishing

The `docs/` folder is a plain static site -- any static host serves it.
See the deployment notes below for the setup currently in use.
