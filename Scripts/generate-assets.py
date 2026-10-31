#!/usr/bin/env python3
"""Draw Sora Bar's original geometric artwork; no external packages required.

Modified/created 2026-10-31. GPL-3.0. Original Ice artwork is not used.
Asset keys are retained so the inherited Swift code can load these replacements.
"""
from pathlib import Path
import json
import math
import struct
import zlib

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'Ice/Resources/Assets.xcassets'


def rounded(x, y, left, top, right, bottom, radius):
    dx = max(left + radius - x, 0, x - (right - radius))
    dy = max(top + radius - y, 0, y - (bottom - radius))
    return dx * dx + dy * dy <= radius * radius


def artwork(kind, x, y):
    if kind == 'app':
        if not rounded(x, y, .07, .07, .93, .93, .19):
            return 0, 0, 0, 0
        color = (int(26 + 24 * y), int(80 + 58 * x), int(174 + 45 * y), 255)
        if any(rounded(x, y, .25, top, right, top + .075, .0375)
               for top, right in [(.30, .75), (.465, .61), (.63, .75)]):
            return 245, 250, 255, 255
        if (x - .71) ** 2 + (y - .5025) ** 2 < .04 ** 2:
            return 132, 231, 221, 255
        return color
    if kind == 'warning':
        inside = .08 <= y <= .91 and abs(x - .5) <= (y - .08) * .52
        if not inside:
            return 0, 0, 0, 0
        if (.47 <= x <= .53 and .39 <= y <= .64) or (x - .5) ** 2 + (y - .76) ** 2 < .035 ** 2:
            return 62, 42, 0, 255
        return 245, 184, 42, 255
    fill = kind.endswith('Fill')
    if kind.startswith('Dot'):
        d = math.hypot(x - .5, y - .5)
        inside = d < .24 and (fill or d > .15)
    elif kind.startswith('Ellipsis'):
        d = min(math.hypot(x - cx, y - .5) for cx in [.2, .5, .8])
        inside = d < .09 and (fill or d > .047)
    else:
        inside = any(rounded(x, y, .13, top, right, top + .1, .04)
                     for top, right in [(.21, .87), (.45, .65), (.69, .87)])
        if not fill:
            inside = inside and not any(rounded(x, y, .16, top + .025, right - .03, top + .075, .018)
                                        for top, right in [(.21, .87), (.45, .65), (.69, .87)])
    return (0, 0, 0, 255) if inside else (0, 0, 0, 0)


def png(kind, size):
    rows = bytearray()
    # Supersample small assets so their template edges stay smooth.
    samples = 3 if size <= 128 else 1
    for y in range(size):
        rows.append(0)
        for x in range(size):
            colors = [artwork(kind, (x + (sx + .5) / samples) / size,
                              (y + (sy + .5) / samples) / size)
                      for sy in range(samples) for sx in range(samples)]
            alpha = sum(c[3] for c in colors)
            rgb = [round(sum(c[i] * c[3] for c in colors) / alpha) if alpha else 0 for i in range(3)]
            rows.extend((*rgb, round(alpha / len(colors))))

    def chunk(name, payload):
        return struct.pack('>I', len(payload)) + name + payload + struct.pack('>I', zlib.crc32(name + payload))

    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', size, size, 8, 6, 0, 0, 0))
            + chunk(b'IDAT', zlib.compress(rows, 9)) + chunk(b'IEND', b''))


def main():
    count = 0
    cache = {}
    for metadata in sorted(ASSETS.rglob('Contents.json')):
        data = json.loads(metadata.read_text())
        for entry in data.get('images', []):
            if 'filename' not in entry:
                continue
            if metadata.parent.suffix == '.appiconset':
                kind = 'app'
                size = int(float(entry['size'].split('x')[0]) * float(entry['scale'][:-1]))
            else:
                kind = 'warning' if metadata.parent.stem == 'Warning' else metadata.parent.stem
                size = 36
            key = kind, size
            if key not in cache:
                cache[key] = png(kind, size)
            (metadata.parent / entry['filename']).write_bytes(cache[key])
            count += 1
    print(f'Generated {count} original PNG assets.')


if __name__ == '__main__':
    main()
