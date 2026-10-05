# Campus & Chaos

The unofficial yearbook for **Loki** and the **ATSMU batch of 2023** — photos,
videos and the small moments that never made it into a real yearbook.

Live at: **https://imlokisenpai.github.io/campus-and-chaos**

Built with [Jekyll](https://jekyllrb.com), published by GitHub Pages. No
analytics, no trackers, no accounts, no database. It's a folder of files in a
repo, and that's the whole architecture.

---

## What's here

```
campus-and-chaos/
├── _config.yml            # site title, tagline, batch year, repo URL
├── _data/
│   ├── sections.yml       # the yearbook chapters
│   ├── crew.yml           # the roster  ← edit this to add your name
│   ├── crew_groups.yml    # roster headings
│   └── nav.yml            # header links
├── _memories/             # ← one .md file per memory
├── _includes/             # header, footer, polaroid, lightbox, card
├── _layouts/              # default, home, yearbook, memory, page
├── _sass/                 # the whole theme
│   ├── _variables.scss    # ← colours, fonts, spacing
│   ├── _base.scss         # paper texture, typography
│   ├── _layout.scss       # header, footer, page furniture
│   ├── _components.scss   # polaroids, tape, handwriting, lightbox
│   ├── _home.scss
│   └── _yearbook.scss
├── assets/
│   ├── css/main.scss      # entry point
│   ├── js/main.js         # lightbox + scroll-in (no dependencies)
│   ├── img/favicon.svg
│   └── memories/          # ← drop photos and videos here
├── about.md               # the guide your friends will actually read
├── yearbook.md
├── crew.md
└── script/
    └── make_placeholders.py
```

---

## Run it locally

Only needed if you want to preview before pushing. Friends don't need this.

```bash
bundle install
bundle exec jekyll serve
# → http://127.0.0.1:4000
```

Push to `main` and GitHub Actions rebuilds and deploys automatically — usually
within a minute.

---

## Adding a memory

**Full instructions with a copy-paste template are on the site's own
[About page](/about/#add).** Short version:

1. On GitHub: **Add file → Create new file**
2. Filename: `_memories/my-memory-slug.md`
3. Paste the frontmatter template from the About page, add your photo to
   `assets/memories/` via **Add file → Upload files**
4. Commit. Wait a minute. Done.

You don't need Jekyll, Ruby, or any local setup to contribute.

---

## Things you'll probably want to change first

| What | Where |
|---|---|
| Tagline | `tagline:` in `_config.yml` |
| Roster names | `_data/crew.yml` — **these are placeholders** |
| The chapters | `_data/sections.yml` |
| Colours & fonts | `_sass/_variables.scss` |
| Header links | `_data/nav.yml` |
| Repo URL in the footer | `github_repo:` in `_config.yml` |

The placeholder "photos" in `assets/memories/` are generated SVGs so a fresh
clone looks like a finished site instead of a wall of broken images. Replace
them with real photos as friends upload them — nothing else needs to change.
Regenerate them with:

```bash
python3 script/make_placeholders.py
```

### A note on the demo video

`lights-out-lights-on` references `assets/memories/roof-singing.mp4`, which
isn't in the repo. That page demonstrates how embedded video works — drop a
real clip in and it plays. Nothing else is broken.

---

## Notes

- **Photos are displayed at 900×1125** and stretched to their frame via
  `object-fit: cover`. That's a deliberate crop for the polaroid aesthetic, so
  portrait phone photos look best.
- **Everything is graded in CSS** (`.film`) — faded blacks, warm highlights,
  grain, vignette. If a photo looks muddy, it's usually because it was already
  heavily filtered before upload.
- **Videos** use `preload="none"` and never autoplay, because hostel Wi-Fi is
  not a thing.
- **`prefers-reduced-motion`** is respected — animations stop for anyone who
  has that set.