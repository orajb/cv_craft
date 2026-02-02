"""Generate an HTML preview of all icons"""
import sys
sys.path.insert(0, 'src')

from icons import get_icon, TAB_ICONS

# List of all icon names
ICON_NAMES = [
    "dashboard", "file-text", "briefcase", "palette", "sparkles", "folder", "settings",
    "plus", "save", "trash", "edit", "copy", "external-link", "refresh",
    "check", "check-circle", "x-circle", "clock", "send", "award",
    "cpu", "zap", "user", "link", "graduation-cap", "award-star", "code", "bar-chart", "target"
]

html = '''<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: system-ui; background: #1a1a2e; color: white; padding: 2rem; }
        .grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 1.5rem; }
        .icon-card { background: #252540; border-radius: 8px; padding: 1rem; text-align: center; }
        .icon-card svg { width: 32px; height: 32px; }
        .icon-name { font-size: 0.75rem; margin-top: 0.5rem; color: #888; }
    </style>
</head>
<body>
    <h1>CV Crafter Icons</h1>
    <div class="grid">
'''

for name in ICON_NAMES:
    svg = get_icon(name, size=32, color='#00d4aa')
    html += f'<div class="icon-card">{svg}<div class="icon-name">{name}</div></div>\n'

html += '</div></body></html>'

with open('/tmp/icons_preview.html', 'w') as f:
    f.write(html)

print('Created /tmp/icons_preview.html')
print('Opening in browser...')

import webbrowser
webbrowser.open('file:///tmp/icons_preview.html')
