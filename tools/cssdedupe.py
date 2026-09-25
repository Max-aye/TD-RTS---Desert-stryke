#!/usr/bin/env python3
"""Drop declarations that a later rule in the same context fully overrides.

    python3 tools/cssdedupe.py parts/css/00-base.css            # report only
    python3 tools/cssdedupe.py parts/css/00-base.css --write    # rewrite in place

`00-base.css` is 241 KB of stylesheet layers stacked over several versions, so the
same selector is declared again and again. When a selector appears twice in the same
@media context and the later block declares every property the earlier one does, the
earlier block cannot affect rendering: equal selectors have equal specificity, so
source order decides, and the later one wins every property. Those blocks are removed.

Anything the tool cannot prove dead is left alone: a block carrying !important, a
block with even one property the later rules do not re-declare, and every at-rule
body (@keyframes, @font-face) are kept untouched. Comment bodies are masked before
parsing - a `{`, `}` or `@media` inside a comment would otherwise desync the context
stack and make the tool delete live rules.
"""
import collections, re, sys


def mask_comments(text):
    """Blank out comment bodies but keep every byte offset, so cuts stay accurate."""
    out, i, n = list(text), 0, len(text)
    while True:
        a = text.find('/*', i)
        if a < 0:
            break
        b = text.find('*/', a + 2)
        b = n if b < 0 else b + 2
        for k in range(a, b):
            if out[k] not in '\n\r':
                out[k] = ' '
        i = b
    return ''.join(out)


def parse(source):
    """Return [(media_context, selector, start, end, props)] for plain style rules."""
    text = mask_comments(source)
    rules, media, i, n = [], [], 0, len(text)
    while i < n:
        # at-rules must be recognised at the first non-blank byte: a newline in front of
        # @media used to send the scanner into the generic branch, which swallowed the
        # media's opening brace and desynced every context after it.
        if text[i] in ' \t\r\n':
            i += 1
            continue
        if text.startswith('@media', i) or text.startswith('@supports', i):
            head = text.index('{', i)
            media.append(text[i:head].strip())
            i = head + 1
            continue
        if text.startswith('@keyframes', i) or text.startswith('@font-face', i):
            depth, k = 0, text.index('{', i)
            while k < n:
                if text[k] == '{':
                    depth += 1
                elif text[k] == '}':
                    depth -= 1
                    if not depth:
                        break
                k += 1
            i = k + 1
            continue
        if text[i] == '}':
            if media:
                media.pop()
            i += 1
            continue
        brace = text.find('{', i)
        close = text.find('}', brace + 1) if brace >= 0 else -1
        if brace < 0 or close < 0:
            break
        selector, body = text[i:brace].strip(), text[brace + 1:close]
        props = {}
        for decl in body.split(';'):
            if ':' in decl:
                p, _, v = decl.partition(':')
                props[p.strip().lower()] = v.strip()
        if selector and props and '@' not in selector:
            rules.append((tuple(media), selector, i, close + 1, props))
        i = close + 1
    return rules


def dead_blocks(rules):
    groups = collections.defaultdict(list)
    for idx, r in enumerate(rules):
        groups[(r[0], r[1])].append(idx)
    dead = []
    for idxs in groups.values():
        if len(idxs) < 2:
            continue
        for pos, idx in enumerate(idxs[:-1]):
            props = rules[idx][4]
            if any('!important' in v for v in props.values()):
                continue
            later = set()
            for j in idxs[pos + 1:]:
                later |= set(rules[j][4])
            if set(props) <= later:
                dead.append(idx)
    return sorted(dead)


def main(path, write):
    text = open(path, encoding='utf-8').read()
    rules = parse(text)
    dead = dead_blocks(rules)
    removed = sum(rules[i][3] - rules[i][2] for i in dead)
    print(f'{path}: {len(rules)} rules, {len(dead)} fully overridden blocks, {removed} bytes')
    if not write:
        return 0
    out, cursor = [], 0
    for idx in dead:
        start, end = rules[idx][2], rules[idx][3]
        out.append(text[cursor:start])
        cursor = end
    out.append(text[cursor:])
    new = ''.join(out)
    open(path, 'w', encoding='utf-8').write(new)
    print(f'{path}: {len(text)} -> {len(new)} bytes')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    sys.exit(main(sys.argv[1], '--write' in sys.argv))
