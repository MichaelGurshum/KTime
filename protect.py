#!/usr/bin/env python3
"""
protect.py — Regenerate protected HTML from source
Usage: python3 protect.py

Run this every time you update kabbalah-time.html.
Output: kabbalah-time-protected.html (deploy this to GitHub)
"""

import base64, json, re, sys, os

# ── CONFIG — edit this ──
GITHUB_USERNAME  = "YOUR_GITHUB_USERNAME"   # ← change this
SOURCE_FILE      = "kabbalah-time.html"
OUTPUT_FILE      = "kabbalah-time-protected.html"
AUTHOR_NAME      = "Michael Gurshumov"
YEAR             = "2025"
# ────────────────────────

def protect(source_path, output_path, github_username, author, year):
    if not os.path.exists(source_path):
        print(f"ERROR: {source_path} not found.")
        sys.exit(1)

    with open(source_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract JS
    js_start = html.find('<script>') + len('<script>')
    js_end   = html.rfind('</script>')
    if js_start < 0 or js_end < 0:
        print("ERROR: Could not find <script>...</script> in source file.")
        sys.exit(1)

    js_raw = html[js_start:js_end]

    # Base64 encode JS in chunks
    js_b64   = base64.b64encode(js_raw.encode('utf-8')).decode('ascii')
    chunks   = [js_b64[i:i+80] for i in range(0, len(js_b64), 80)]
    chunks_js = json.dumps(chunks)

    # Copyright header
    copyright_comment = f"""<!--
  ╔══════════════════════════════════════════════════════════════╗
  ║           מערכת זמן קבלית — KABBALISTIC TIME SYSTEM         ║
  ║                                                              ║
  ║  Copyright © {year} {author}. All rights reserved.   ║
  ║                                                              ║
  ║  This software is the exclusive intellectual property of     ║
  ║  the author. Unauthorized copying, reproduction, or use     ║
  ║  without express written permission is strictly prohibited.  ║
  ║                                                              ║
  ║  Protected under international copyright law.                ║
  ║  DMCA notices: contact owner via GitHub profile.             ║
  ╚══════════════════════════════════════════════════════════════╝
-->
"""

    # Protection wrapper
    protected_js = f"""
/* ©{year} {author} — All Rights Reserved. */
(function _protect() {{
  'use strict';

  const _allowed = [
    'localhost',
    '127.0.0.1',
    '{github_username}.github.io',
  ];
  const _host = (window.location.hostname || '').toLowerCase();
  const _ok   = _allowed.some(d => _host === d || _host.endsWith('.' + d));
  if (!_ok) {{
    document.body.innerHTML =
      '<div style="display:flex;align-items:center;justify-content:center;' +
      'height:100vh;background:#000;color:#c00;font-family:monospace;' +
      'font-size:14px;text-align:center;padding:20px">' +
      'This software is licensed and may only run on its authorized domain.<br>' +
      'Unauthorized use violates copyright law.<br><br>' +
      '© {year} {author} — All Rights Reserved.</div>';
    throw new Error('Domain not authorized.');
  }}

  let _devOpen = false;
  const _dt = new Image();
  Object.defineProperty(_dt, 'id', {{
    get: function () {{ _devOpen = true; return 'x'; }}
  }});
  setInterval(function () {{
    _devOpen = false;
    console.log('%c', _dt);
    if (_devOpen) {{
      console.clear();
      console.log(
        '%c© {year} {author} — Proprietary Software. Inspection prohibited.',
        'color:#FFD700;font-size:16px;font-weight:bold;background:#000;padding:8px 16px'
      );
    }}
  }}, 1500);

  document.addEventListener('contextmenu', function(e) {{ e.preventDefault(); }});

  document.addEventListener('keydown', function(e) {{
    if (
      (e.ctrlKey && (e.key === 'u' || e.key === 'U' ||
                     e.key === 's' || e.key === 'S')) ||
      (e.ctrlKey && e.shiftKey && (e.key === 'i' || e.key === 'I' ||
                                    e.key === 'j' || e.key === 'J' ||
                                    e.key === 'c' || e.key === 'C')) ||
      e.key === 'F12'
    ) {{
      e.preventDefault();
      e.stopPropagation();
      return false;
    }}
  }});

  const _chunks = {chunks_js};
  const _encoded = _chunks.join('');
  try {{
    const _fn = new Function(atob(_encoded));
    _fn();
  }} catch(e) {{
    console.error('Application error:', e.message);
  }}
}})();
"""

    result = (
        copyright_comment +
        html[:html.find('<!DOCTYPE')] +
        html[html.find('<!DOCTYPE'):js_start] +
        protected_js +
        html[js_end:]
    )

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(result)

    kb_in  = len(html) // 1024
    kb_out = len(result) // 1024
    print(f"✓ Protected file written: {output_path}")
    print(f"  Source:    {kb_in} KB  →  Protected: {kb_out} KB")
    print(f"  JS chunks: {len(chunks)} base64 pieces")
    print(f"  Domain lock: {github_username}.github.io")
    print(f"\nNext steps:")
    print(f"  1. Rename {output_path} to index.html")
    print(f"  2. Push index.html to your private GitHub repo")
    print(f"  3. GitHub Pages serves it — source stays private")

if __name__ == "__main__":
    protect(SOURCE_FILE, OUTPUT_FILE, GITHUB_USERNAME, AUTHOR_NAME, YEAR)
