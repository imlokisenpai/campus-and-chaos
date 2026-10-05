---
layout: page
title: "About This Yearbook"
eyebrow: "Colophon"
lede: >-
  What this is, who made it, and how to add the one photo we definitely forgot
  about.
margin_note: "read me"
hero_photo:
  src: /assets/memories/library-stack.svg
  alt: "A desk lamp over a stack of library books"
  caption: "assembled at 2am, obviously"
  tilt: tilt-r
  tape: tr
  dateback: "'19 ▸ 11 ▸ 03"
---

## Why this exists

Real yearbooks are expensive, slightly embarrassing, and printed once — with a
deadline. So none of us got one. What we got instead was a folder on someone's
laptop that half of us have been quietly adding to since first year.

This is that folder, but public.

It's not official. It's not curated to flatter anyone. It's just a place to put
things so that in ten years, when someone asks *"what was that trip in second
year again?"*, there's an answer with a date on it.

## The design

Everything here is a deliberate bit of nostalgia:

- **Warm paper** with visible grain, so it feels like a printed page rather
  than a screen.
- **Film photography** treatment on every photo — faded blacks, warm highlights,
  grain, and a vignette. Old rolls had none of this clarity and were better for it.
- **Polaroids and tape**, slightly rotated, because straight lines look like spreadsheets.
- **Yearbook typography** — high-contrast serif, chapter numbers, little
  handwritten years under each title.
- **Handwritten annotations** in the margins, because someone always scrawled
  on the class photo.

Edit the palette in `_sass/_variables.scss` if you'd rather it looked like
something else. It's all in one file.

## Add your memory {#add}

No coding, no installs, no local setup. Here's the whole process:

**1. Open the repo**

Go to `{{ site.github_repo }}` → the **Add file** button → **Create new file**.

**2. Name it**

In the filename box, type:

```
_memories/second-year-hostel-lights-out.md
```

The bit after `second-year` is just a name — use words instead of spaces.

**3. Fill in the template**

Delete everything in the editor and paste this:

```yaml
---
title: "Lights Out, Lights On"
date: 2021-03-14
section: second-year
place: "Hostel, room 214"
camera: "Rohan's Kodak"
people: ["Priya", "Kabir", "Dev"]
featured: false
cover:
  src: /assets/memories/hostel-night.svg
  alt: "A corridor lit by one bulb"
  tilt: tilt-l
  tape: tl
  dateback: "'21 ▸ 03 ▸ 14"
photos:
  - src: /assets/memories/hostel-night.svg
    alt: "The corridor at 2am"
    caption: "one bulb between all of us"
    tilt: tilt-r
    tape: tr
note: "the bulb survived. barely."
---

Then write what actually happened. A paragraph is plenty. The photos do most
of the work, but the caption is what makes it worth opening in five years.

**4. Add the photo file**

Same as before: **Add file → Upload files**, drag your photo into
`assets/memories/`, then write the commit message.

Use a descriptive filename (`hostel-corridor-2021.jpg`, not `IMG_4821.jpg`).
Big photos get re-compressed automatically by the build, but keeping them under
about **4 MB** keeps GitHub happy.

**5. Commit, and that's it**

About a minute later the site rebuilds and your memory is live. You'll get an
email when it goes up.

### What's in the template

| Field | What it does |
|---|---|
| `title` | The headline. Make it a bit funny. |
| `date` | The date it happened. Drives the ordering. |
| `section` | One of the chapter keys below. |
| `place` | Where. Shows up under the title. |
| `camera` | Optional. Who took it, or what with. |
| `people` | A list of names, in quotes. |
| `featured` | `true` puts it on the homepage. Use sparingly. |
| `cover` | The photo used on the card and the big hero print. |
| `photos` | The rest. `wide: true` makes one span the full row. |
| `video` | `src`, `poster` and `caption` — see below. |
| `note` | Your handwriting, pinned to the print. |
| `signatures` | A list of friends who "signed" this page. |

Each photo accepts: `src`, `alt`, `caption`, `tilt` (`tilt-l`, `tilt-r`,
`tilt-lb`, `tilt-rb`), `tape` (`tl`, `tr`, `bl`, `br` — or `false` for none),
and `dateback` (the orange stamp).

### The chapters

Use one of these for `section`:

`freshers` · `first-year` · `second-year` · `third-year` · `final-year` ·
`graduation` · `after` · `misc`

Chapters are defined in `_data/sections.yml`. Add a new one there and it'll
appear on the homepage and the yearbook index automatically.

### Adding a video

Keep clips short — under a minute is plenty. Drop an `.mp4` into
`assets/memories/` and add:

```yaml
video:
  src: /assets/memories/farewell-speech.mp4
  poster: /assets/memories/farewell.svg
  caption: "the speech nobody was ready for"
```

A **poster** image matters: it's the still people see before pressing play, so
use one of the placeholders or drop in a frame from the video.

Videos don't autoplay and we never load them until you click play — the site
stays fast on hostel Wi-Fi.

### Adding your name {#add-roster}

Same idea, one file: `_data/crew.yml`. Add yourself to the list:

```yaml
- name: "Your Name"
  role: "something short and true"
  note: "a scrawl in your own handwriting"
  group: witnesses
  tilt: tilt-l
```

`group` is one of `organisers`, `witnesses`, or `everyone` — leave it out and
you'll appear under "Everyone Else".

## Ground rules

1. **Photos over paragraphs.** Nobody's reading an essay.
2. **Blur faces you don't want immortalised.** It's a public URL. Do it before
   you upload, not after.
3. **Write the date.** Even "sometime in second year" beats leaving it blank.
4. **Don't upload other people's stuff without asking.** In particular, don't
   post someone's DMs, screenshots of results, or anything from a hospital
   visit.
5. **Anything can be deleted.** Say so on the group chat and it comes down.

## Credits

Built by **{{ site.curator }}** with help from everyone else in the batch of
{{ site.batch_year }}. Runs on [Jekyll](https://jekyllrb.com), hosted free by
[GitHub Pages](https://pages.github.com). No analytics, no trackers, no
accounts, no database.

Photos belong to the people who took them. If one of these is yours and you'd
rather it wasn't here, that's a completely reasonable request — make it and it
goes.

<div class="postit" style="max-width: 34ch; margin: 2.5rem 0 0;">
  <p>Made with genuine affection and an unreasonable number of untitled files
  called "final_final2.jpg".</p>
  <p style="font-size: 1.1rem;">&mdash; {{ site.curator }}</p>
</div>