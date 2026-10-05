---
layout: page
title: "The Crew"
eyebrow: "Roll call"
lede: "Thirty-four of us walked in. Here are the ones we're still in a group chat with."
margin_note: "add yourself!"
---

<div class="wrap">
  <p class="crew-intro">
    Index cards, exactly like the ones in the noticeboard outside the department
    office. Taped up, never taken down, always slightly curling at the corners.
  </p>
</div>

{%- assign groups = site.data.crew_groups -%}
{%- for g in groups -%}
  {%- comment -%}
    A person belongs to this group if their `group:` matches its key.
    Anyone with no `group:` at all falls into "everyone". Skip the
    whole heading if it would render empty.
  {%- endcomment -%}
  {%- assign members = "" | split: "" -%}
  {%- for person in site.data.crew -%}
    {%- assign pg = person.group -%}
    {%- if pg == nil or pg == "" -%}
      {%- if g.key == "everyone" -%}{%- assign members = members | push: person -%}{%- endif -%}
    {%- elsif pg == g.key -%}
      {%- assign members = members | push: person -%}
    {%- endif -%}
  {%- endfor -%}
  {%- if members.size > 0 -%}
<section class="wrap crew__section">
  <h2 class="crew__section-title">{{ g.title }}</h2>
  <ul class="crew">
    {%- for person in members -%}
      <li>
        <div class="crew__card" style="--tilt: {{ person.tilt | default: '0deg' }};">
          <span class="crew__pin" aria-hidden="true"></span>
          <h3 class="crew__name">{{ person.name }}</h3>
          {%- if person.role %}
          <p class="crew__role">{{ person.role }}</p>
          {%- endif %}
          <p class="crew__note">{{ person.note }}</p>
        </div>
      </li>
    {%- endfor -%}
  </ul>
</section>
  {%- endif -%}
{%- endfor %}

<div class="wrap">
  <div class="doc-block" style="margin-top:3rem;">
    <h3>Missing somebody?</h3>
    <p>
      The roster lives in one file &mdash; <code>_data/crew.yml</code>. Adding
      your own name is a five-line edit, and you don't need to know any of the
      rest of this site to do it.
    </p>
    <p>
      <a class="doodle-link" href="{{ '/about/#add-roster' | relative_url }}">Show me how</a>
    </p>
  </div>
</div>