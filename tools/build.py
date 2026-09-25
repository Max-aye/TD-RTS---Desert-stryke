#!/usr/bin/env python3
"""TERRA 2136: concatenate parts/ back into one playable HTML file.

    python3 tools/build.py parts/ TERRA2136_PLAY_v0_95_0.html [--verify]

--verify: the output must equal the sha256 stored in parts/manifest.json
(use it right after split.py to prove the round trip is lossless).
"""
import hashlib, json, os, sys

def main(src, out, verify=False):
    info = json.load(open(os.path.join(src, 'manifest.json'), encoding='utf-8'))
    chunks = [open(os.path.join(src, p['file']), encoding='utf-8', newline='').read() for p in info['parts']]
    data = ''.join(chunks).encode('utf-8')
    open(out, 'wb').write(data)
    digest = hashlib.sha256(data).hexdigest()
    print(f'build: {len(info["parts"])} parts -> {out} ({len(data):,} bytes, sha256 {digest[:12]})')
    if verify and digest != info['sha256']:
        sys.exit('build: VERIFY FAILED - output differs from the split source')
    if verify:
        print('build: verify OK, byte-identical round trip')

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    if len(a) != 2:
        sys.exit(__doc__)
    main(a[0], a[1], '--verify' in sys.argv)
