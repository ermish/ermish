# Regenerates chips/*.svg: python scripts/chips.py chips scripts/lightwrite-mark.svg
# Also writes chips-block.html (the README <picture> block) next to chips/; paste it in, then delete it.
import os, re, sys

out = sys.argv[1]
lw = open(sys.argv[2], encoding="utf-8").read()
lw_inner = re.sub(r"^<svg[^>]*>|</svg>\s*$", "", lw.strip())

FONT = "-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif"
MONO = "ui-monospace,SFMono-Regular,Consolas,monospace"

ICONS = {
    "hypergate": ("0 0 100 100", """
  <defs>
    <linearGradient id="hgRing" x1="0.08" y1="0.05" x2="0.92" y2="0.95">
      <stop offset="0" stop-color="#7c6bff"/><stop offset="0.3" stop-color="#6d5efc"/>
      <stop offset="0.6" stop-color="#22d3ee"/><stop offset="0.8" stop-color="#a5f3fc"/>
      <stop offset="1" stop-color="#6d5efc"/>
    </linearGradient>
    <radialGradient id="hgFeather">
      <stop offset="0.46" stop-color="#fff" stop-opacity="0"/><stop offset="0.58" stop-color="#fff" stop-opacity="0.5"/>
      <stop offset="0.7" stop-color="#fff" stop-opacity="1"/><stop offset="0.86" stop-color="#fff" stop-opacity="0.32"/>
      <stop offset="1" stop-color="#fff" stop-opacity="0"/>
    </radialGradient>
    <mask id="hgGate" maskContentUnits="userSpaceOnUse"><circle cx="50" cy="50" r="40" fill="url(#hgFeather)"/></mask>
  </defs>
  <rect x="4" y="4" width="92" height="92" rx="23" fill="#05060f"/>
  <circle cx="50" cy="50" r="40" fill="url(#hgRing)" mask="url(#hgGate)">
    <animateTransform attributeName="transform" type="rotate" from="0 50 50" to="360 50 50" dur="12s" repeatCount="indefinite"/>
  </circle>"""),
    "nekko-agent": ("0 0 512 512", """
  <defs><clipPath id="sq"><rect width="512" height="512" rx="114"/></clipPath></defs>
  <g clip-path="url(#sq)">
    <rect width="512" height="512" fill="#101714"/>
    <g transform="translate(-8 20.6) scale(22)" fill="none" stroke="#f2f1e9" stroke-width="1.5" stroke-miterlimit="8">
      <path d="M5 10l-1-6 5 3q3-1.1 6 0l5-3-1 6a7.4 7.4 0 0 1-14 0z"/>
    </g>
  </g>
  <rect x="3" y="3" width="506" height="506" rx="111" fill="none" stroke="#a7c8ac" stroke-opacity="0.72" stroke-width="10"/>"""),
    "vaizer": ("0 0 32 32", """
  <rect width="32" height="32" rx="7.5" fill="#5646d4"/>
  <path d="M4 9 V5 H8 M28 9 V5 H24 M4 23 V27 H8 M28 23 V27 H24" stroke="#fbfaf5" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" fill="none" opacity="0.55"/>
  <path d="M7 11 C7 8.5 9 7 16 7 C23 7 25 8.5 25 11 L25 15 C25 20 21 24 16 24 C11 24 7 20 7 15 Z" fill="#fbfaf5" fill-opacity="0.14" stroke="#fbfaf5" stroke-width="1.6" stroke-linejoin="round"/>
  <rect x="10" y="12.4" width="12" height="3.2" rx="1.6" fill="#5eead4">
    <animate attributeName="opacity" values="1;0.55;1" dur="3s" repeatCount="indefinite"/>
  </rect>
  <path d="M13 19 H19" stroke="#fbfaf5" stroke-width="1.6" stroke-linecap="round" opacity="0.55"/>"""),
    "getsu": ("0 0 100 100", """
  <defs>
    <mask id="cres" maskContentUnits="userSpaceOnUse">
      <rect width="100" height="100" fill="#fff"/><circle cx="62" cy="40" r="28" fill="#000"/>
    </mask>
  </defs>
  <rect width="100" height="100" rx="23" fill="#1c1a18"/>
  <circle cx="47" cy="50" r="33" fill="#d6ad55" mask="url(#cres)"/>
  <g fill="#2b2a28" stroke="#1c1a18" stroke-width="1">
    <path d="M38 70 C36 60 46 55 58 57 C64 58 68 60 70 63 C71 68 66 71 58 72 L44 73 C40 73 38 72 38 70 Z"/>
    <path d="M64 58 L66 50 L69 56 L74 54 L73 62 C71 65 66 65 64 62 Z"/>
    <path d="M58 70 C59 76 58 81 56 84" fill="none" stroke="#2b2a28" stroke-width="3.2" stroke-linecap="round"/>
  </g>
  <path d="M42 70 C38 74 40 79 46 78" fill="none" stroke="#2b2a28" stroke-width="3" stroke-linecap="round"/>
  <path d="M84 76 l1.4 3.6 3.6 1.4 -3.6 1.4 -1.4 3.6 -1.4 -3.6 -3.6 -1.4 3.6 -1.4z" fill="#fbf7f1">
    <animate attributeName="opacity" values="1;0.25;1" dur="4s" repeatCount="indefinite"/>
  </path>"""),
    "lightwrite": ("0 0 96 96", lw_inner),
}

CHIPS = [
    ("hypergate", "Hypergate", "One secure gateway for every MCP server", "https://hypergate.app", "hypergate.app",
     dict(dark=("#05060f", "#7c6bff", "#22d3ee", "#f4f4ff", "#a5b4d8", "#22d3ee"),
          light=("#f6f5ff", "#7c6bff", "#22d3ee", "#14132b", "#4b5275", "#5b4be8"))),
    ("nekko-agent", "Nekko Agent", "AI on your computer for code and everyday work", "https://nekkoagent.com", "nekkoagent.com",
     dict(dark=("#101714", "#a7c8ac", "#a7c8ac", "#f2f1e9", "#a9b8ac", "#a7c8ac"),
          light=("#f4f6f1", "#6f9a77", "#a7c8ac", "#101714", "#4d5c51", "#3f7a4b"))),
    ("vaizer", "Vaizer", "See how your agents work and what they focus on", "https://vaizer.app", "vaizer.app",
     dict(dark=("#0f0e1c", "#5646d4", "#0e7c72", "#f4f2ff", "#aaa6cc", "#5eead4"),
          light=("#ece9e1", "#5646d4", "#0e7c72", "#1a1730", "#57536b", "#0e7c72"))),
    ("getsu", "Getsu", "Calm, anti-streak monthly journaling and goals", "https://getsu.app", "getsu.app",
     dict(dark=("#1c1a18", "#d6ad55", "#6fb3c2", "#fbf7f1", "#a39a90", "#d6ad55"),
          light=("#fbf7f1", "#d6ad55", "#3e8fa0", "#1c1a18", "#7a726a", "#a67c22"))),
    ("lightwrite", "Lightwrite", "AI-first, local-first notes over files you own", "https://lightwrite.app", "lightwrite.app",
     dict(dark=("#131210", "#34b3ab", "#c4b5f5", "#f6f4ee", "#a8a196", "#79dcd8"),
          light=("#fffdf8", "#34b3ab", "#c4b5f5", "#1b1a18", "#6b655c", "#1f8a83"))),
]

def chip(slug, name, tag, label, theme, colors):
    bg, e1, e2, title, sub, link = colors
    vb, icon = ICONS[slug]
    ring = f'<rect x="16.5" y="16.5" width="55" height="55" rx="13" fill="none" stroke="{e1}" stroke-opacity="0.35"/>' if theme == "light" else ""
    glow = 0.26 if theme == "dark" else 0.14
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="400" height="88" viewBox="0 0 400 88" role="img" aria-label="{name}: {tag}">
  <defs>
    <linearGradient id="edge" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{e1}" stop-opacity="0.75"/><stop offset="1" stop-color="{e2}" stop-opacity="0.55"/>
    </linearGradient>
    <radialGradient id="glow" cx="0.1" cy="0.5" r="0.6">
      <stop offset="0" stop-color="{e1}" stop-opacity="{glow}"/><stop offset="1" stop-color="{e1}" stop-opacity="0"/>
    </radialGradient>
  </defs>
  <rect x="1" y="1" width="398" height="86" rx="20" fill="{bg}"/>
  <rect x="1" y="1" width="398" height="86" rx="20" fill="url(#glow)"/>
  <rect x="1" y="1" width="398" height="86" rx="20" fill="none" stroke="url(#edge)" stroke-width="1.5"/>
  <svg x="16" y="16" width="56" height="56" viewBox="{vb}">{icon}
  </svg>
  {ring}
  <text x="88" y="40" fill="{title}" font-family="{FONT}" font-size="22" font-weight="700" letter-spacing="0.2">{name}</text>
  <text x="88" y="62" fill="{sub}" font-family="{FONT}" font-size="13.5">{tag.replace('&', '&amp;')}</text>
  <text x="382" y="40" text-anchor="end" fill="{link}" font-family="{MONO}" font-size="11">{label} ↗</text>
</svg>
"""

os.makedirs(out, exist_ok=True)
for f in os.listdir(out):
    os.remove(os.path.join(out, f))
for slug, name, tag, url, label, themes in CHIPS:
    for theme, colors in themes.items():
        with open(os.path.join(out, f"{slug}-{theme}.svg"), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(chip(slug, name, tag, label, theme, colors))

rows = []
for slug, name, tag, url, label, _ in sorted(CHIPS, key=lambda c: ['nekko-agent', 'hypergate', 'vaizer', 'lightwrite', 'getsu'].index(c[0])):
    rows.append(f"""  <a href="{url}"><picture>
    <source media="(prefers-color-scheme: dark)" srcset="./chips/{slug}-dark.svg">
    <img src="./chips/{slug}-light.svg" height="72" alt="{name}: {tag}">
  </picture></a>""")
open(os.path.join(os.path.dirname(out), "chips-block.html"), "w", encoding="utf-8", newline="\n").write("<p>\n" + "\n".join(rows) + "\n</p>\n")
