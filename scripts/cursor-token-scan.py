"""
FILE: scripts/cursor-token-scan.py
PURPOSE: Pull real per-message token counts out of Cursor's local SQLite store
         and emit JSON on stdout for scripts/token-report.js.

Cursor records tokenCount {inputTokens, outputTokens} on each stored message
("bubble"), and modelName on the ones where a specific model was pinned.
"default" means auto-select picked the model.

Read-only. Walks a few hundred thousand rows, so it takes a couple of minutes.
"""
import collections
import json
import os
import re
import sqlite3
import sys

DB = os.path.join(
    os.environ.get('APPDATA', ''),
    'Cursor', 'User', 'globalStorage', 'state.vscdb',
)

MODEL_RX = re.compile(r'"modelName"\s*:\s*"([^"]{2,45})"')


def main():
    if not os.path.exists(DB):
        json.dump({'error': 'Cursor state.vscdb not found', 'models': []}, sys.stdout)
        return

    con = sqlite3.connect('file:%s?mode=ro' % DB.replace('\\', '/'), uri=True)
    agg = collections.defaultdict(lambda: {'n': 0, 'in': 0, 'out': 0})

    rows = con.execute("select value from cursorDiskKV where key like 'bubbleId:%'")
    for (value,) in rows:
        s = value if isinstance(value, str) else (
            value.decode('utf8', 'ignore') if isinstance(value, bytes) else '')
        if '"tokenCount"' not in s:
            continue
        try:
            j = json.loads(s)
        except Exception:
            continue
        tc = j.get('tokenCount') or {}
        tin = tc.get('inputTokens') or 0
        tout = tc.get('outputTokens') or 0
        if not (tin or tout):
            continue
        m = MODEL_RX.search(s)
        key = m.group(1) if m else '(not recorded)'
        d = agg[key]
        d['n'] += 1
        d['in'] += tin
        d['out'] += tout

    models = [
        {'model': k, 'n': v['n'], 'in': v['in'], 'out': v['out']}
        for k, v in sorted(agg.items(), key=lambda kv: -(kv[1]['in'] + kv[1]['out']))
    ]
    json.dump({
        'models': models,
        'totalIn': sum(m['in'] for m in models),
        'totalOut': sum(m['out'] for m in models),
        'requests': sum(m['n'] for m in models),
    }, sys.stdout)


if __name__ == '__main__':
    main()
