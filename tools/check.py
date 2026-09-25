#!/usr/bin/env python3
"""Syntax-check every <script> block of a built game with `node --check`.

    python3 tools/check.py TERRA2136_PLAY_v0_95_0.html
"""
import os, re, subprocess, sys, tempfile
html = open(sys.argv[1], encoding='utf-8').read()
bad = 0
for i, m in enumerate(re.finditer(r'<script\b[^>]*>(.*?)</script>', html, re.S)):
    with tempfile.NamedTemporaryFile('w', suffix='.js', delete=False, encoding='utf-8') as f:
        f.write(m.group(1)); path = f.name
    r = subprocess.run(['node', '--check', path], capture_output=True, text=True)
    os.unlink(path)
    status = 'ok' if r.returncode == 0 else 'SYNTAX ERROR'
    bad += r.returncode != 0
    print(f'script {i}: {len(m.group(1)):>11,} chars  {status}')
    if r.returncode:
        print(r.stderr[-1500:])
print('check: PASS' if not bad else f'check: FAIL ({bad} script blocks)')
sys.exit(1 if bad else 0)
