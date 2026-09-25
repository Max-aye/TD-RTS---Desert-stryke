#!/usr/bin/env python3
"""Apply a versioned patch set to split parts (see tools/split.py).

    python3 tools/patch.py patches/v0_95_0 parts/

A patch set is a folder with spec.py defining:
  EDITS     = [dict(file='ui/controller.js', old='...', new='...', count=1, why='...')]
  NEW_PARTS = [dict(file='css/10-polish95.css', source='polish95.css', after='css/09-guide91.css',
                    glue_before='</style><style>')]
Rules that keep this safe in a 43 MB single file:
  * every `old` must occur exactly `count` times, otherwise nothing is written;
  * an edit whose `new` text is already present and whose `old` is gone counts as applied (idempotent);
  * `new` may contain {{FILE:name}} (contents of a file in the patch folder) and {{VERSION}}.
"""
import importlib.util, json, os, sys


def load_spec(folder):
    spec = importlib.util.spec_from_file_location('spec', os.path.join(folder, 'spec.py'))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    return mod


def expand(text, folder, version):
    while '{{FILE:' in text:
        a = text.index('{{FILE:'); b = text.index('}}', a)
        name = text[a + 7:b]
        text = text[:a] + open(os.path.join(folder, name), encoding='utf-8').read() + text[b + 2:]
    return text.replace('{{VERSION}}', version)


def main(folder, parts):
    spec = load_spec(folder)
    version = getattr(spec, 'VERSION', '0.0.0')
    cache, plan, problems = {}, [], []
    def read(f):
        if f not in cache:
            cache[f] = open(os.path.join(parts, f), encoding='utf-8', newline='').read()
        return cache[f]
    for e in spec.EDITS:
        text = read(e['file']); old = expand(e['old'], folder, version); new = expand(e['new'], folder, version)
        n, want = text.count(old), e.get('count', 1)
        if n == want:
            cache[e['file']] = text.replace(old, new); plan.append(f"edit  {e['file']}: {e.get('why', '')}")
        elif n == 0 and new in text:
            plan.append(f"skip  {e['file']}: already applied - {e.get('why', '')}")
        else:
            problems.append(f"{e['file']}: anchor found {n}x, expected {want} - {e.get('why', '')}\n    anchor: {old[:120]!r}")
    if problems:
        print('patch: NOTHING WRITTEN\n  ' + '\n  '.join(problems)); sys.exit(1)
    mpath = os.path.join(parts, 'manifest.json'); manifest = json.load(open(mpath, encoding='utf-8'))
    names = [p['file'] for p in manifest['parts']]
    for np in getattr(spec, 'NEW_PARTS', []):
        body = expand(open(os.path.join(folder, np['source']), encoding='utf-8').read(), folder, version)
        cache[np['file']] = body
        if np['file'] in names:
            plan.append(f"part  {np['file']}: refreshed"); continue
        i = names.index(np['after']) + 1
        entries = []
        if np.get('glue_before'):
            gname = np['file'].rsplit('.', 1)[0] + '.glue.html'
            cache[gname] = np['glue_before']; entries.append(gname)
        entries.append(np['file'])
        for k, name in enumerate(entries):
            names.insert(i + k, name)
        plan.append(f"part  {np['file']}: inserted after {np['after']}")
    for f, text in cache.items():
        p = os.path.join(parts, f); os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, 'w', encoding='utf-8', newline='') as fh:
            fh.write(text)
    manifest['parts'] = [{'file': n, 'bytes': len(open(os.path.join(parts, n), encoding='utf-8', newline='').read().encode())} for n in names]
    manifest['patched_to'] = version
    json.dump(manifest, open(mpath, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n'.join(plan)); print(f'patch: {version} applied ({len(plan)} steps)')


if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    main(sys.argv[1], sys.argv[2])
