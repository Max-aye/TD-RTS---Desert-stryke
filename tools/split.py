#!/usr/bin/env python3
"""TERRA 2136: split the single-file build into editable parts.

    python3 tools/split.py TERRA2136_PLAY_v0_94_0.html parts/

Everything is plain byte-for-byte concatenation, so tools/build.py
reproduces the input exactly (checked with sha256 at the end).
Cut points are text anchors that must occur exactly once; if a future
version moves them, the script stops with a clear message instead of
producing a broken split.
"""
import hashlib, json, os, re, sys

# (script index, [(anchor, part name for the text BEFORE the anchor)], name of the tail)
SCRIPT_PLAN = {
    0: ([('window.TERRA_ASSETS={', 'data/design-config.js')], 'data/assets-models.js'),
    1: ([('"/render/texture-data.js":function', 'engine/ark-visual-a.js'),
         ('"/render/turret-models.js":function', 'data/texture-data.js')], 'engine/ark-visual-b.js'),
    2: ([], 'game/content-sim.js'),
    3: ([], 'game/progress.js'),
    5: ([('/* TERRA 2136 / VISUAL-RISK 055.', 'data/ui-images.js'),
         ('/* VERSION-095:', 'ui/views.js', 'optional'),
         ('/* ICONS-095:', 'ui/version95.js', 'optional'),
         ('/* TERRA 2136 · DOM UI, input and lifecycle', 'ui/views.js|ui/icons95.js')], 'ui/controller.js'),
    6: ([], 'render/ground-motion.js'),
}
SCRIPT4_ANCHORS = [
    ('/* MORTARCH90: native assets derived from user source;', 'render/mortarch-motion.js'),
    ('/* MORTARCH90 thumbnail:', 'data/mortarch-models.js'),
]
SCRIPT4_TAIL = 'render/adapters.js'
STYLE_NAMES = ['css/00-base.css', 'css/01-crate78.css', 'css/02-crate81.css', 'css/03-release87.css',
               'css/04-journey88.css', 'css/05-expedition89.css', 'css/06-mortarch90.css',
               'css/07-weekly91.css', 'css/08-roster91.css', 'css/09-guide91.css', 'css/10-polish95.css']


def cut(text, anchors, tail):
    """Cut text exactly at each anchor; each anchor must occur exactly once."""
    out, pos, seen = [], 0, set()
    for anchor, name, *flags in anchors:
        n = text.count(anchor)
        if n == 0 and 'optional' in flags:
            continue
        if '|' in name:  # name depends on whether the optional anchors before it matched
            name = name.split('|')[1] if seen else name.split('|')[0]
        if 'optional' in flags:
            seen.add(anchor)
        if n != 1:
            sys.exit(f'split: anchor {anchor[:60]!r} found {n} times (expected 1)')
        i = text.index(anchor)
        if i < pos:
            sys.exit(f'split: anchor {anchor[:60]!r} is out of order')
        out.append((name, text[pos:i]))
        pos = i
    out.append((tail, text[pos:]))
    return out


def main(src, dst):
    raw = open(src, 'rb').read()
    s = raw.decode('utf-8')
    parts, pos, glue_n = [], 0, 0
    def glue(t):
        nonlocal glue_n
        parts.append((f'glue/{glue_n:02d}.html', t)); glue_n += 1
    tag_re = re.compile(r'<(style|script)\b[^>]*>', re.I)
    style_i = script_i = 0
    while True:
        m = tag_re.search(s, pos)
        if not m:
            break
        kind = m.group(1).lower()
        close = s.index(f'</{kind}>', m.end())
        glue(s[pos:m.end()])
        body = s[m.end():close]
        if kind == 'style':
            name = STYLE_NAMES[style_i] if style_i < len(STYLE_NAMES) else f'css/{style_i:02d}-extra.css'
            parts.append((name, body)); style_i += 1
        else:
            if script_i == 4:
                parts.extend(cut(body, SCRIPT4_ANCHORS, SCRIPT4_TAIL))
            elif script_i in SCRIPT_PLAN:
                anchors, tail = SCRIPT_PLAN[script_i]
                parts.extend(cut(body, anchors, tail))
            else:
                parts.append((f'js/script{script_i:02d}.js', body))
            script_i += 1
        pos = close
    glue(s[pos:])
    # give the two meaningful glue files readable names
    for k, (name, text) in enumerate(parts):
        if name.startswith('glue/') and '<head>' in text:
            parts[k] = ('markup/head.html', text)
        elif name.startswith('glue/') and '<body>' in text:
            parts[k] = ('markup/body.html', text)
    # the markup between the last </style> and the first <script> is the body UI
    os.makedirs(dst, exist_ok=True)
    manifest = []
    for name, text in parts:
        p = os.path.join(dst, name)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='') as f:
            f.write(text)
        manifest.append({'file': name, 'bytes': len(text.encode('utf-8'))})
    info = {'source': os.path.basename(src), 'sha256': hashlib.sha256(raw).hexdigest(), 'parts': manifest}
    json.dump(info, open(os.path.join(dst, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
    print(f'split: {len(parts)} parts, {len(raw):,} bytes -> {dst}')

if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
