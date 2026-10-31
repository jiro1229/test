#!/usr/bin/env python3
"""Validate source packaging without claiming compilation or OS compatibility."""
from pathlib import Path
import hashlib
import json
import plistlib
import re
import struct
import subprocess
import xml.etree.ElementTree as ET
import zlib

ROOT = Path(__file__).resolve().parents[1]


def openstep(text):
    pattern = r'\s+|//[^\n]*|/\*.*?\*/|"(?:\\.|[^"\\])*"|[{}()=;,]|[^\s{}()=;,]+'
    tokens = [m.group() for m in re.finditer(pattern, text, re.S)
              if not m.group().isspace() and not m.group().startswith(('//', '/*'))]
    index = 0

    def take(expected=None):
        nonlocal index
        token = tokens[index]
        index += 1
        if expected is not None:
            assert token == expected, (expected, token, index)
        return token

    def value():
        nonlocal index
        if tokens[index] == '{':
            take('{')
            result = {}
            while tokens[index] != '}':
                key = value()
                assert key not in result, f'Duplicate project key: {key}'
                take('=')
                result[key] = value()
                take(';')
            take('}')
            return result
        if tokens[index] == '(':
            take('(')
            result = []
            while tokens[index] != ')':
                result.append(value())
                if tokens[index] == ',':
                    take(',')
            take(')')
            return result
        token = take()
        return json.loads(token) if token.startswith('"') else token

    result = value()
    assert index == len(tokens), 'Trailing project tokens'
    return result


def check_png(path):
    data = path.read_bytes()
    assert data[:8] == b'\x89PNG\r\n\x1a\n', path
    offset = 8
    compressed = b''
    dimensions = None
    while offset < len(data):
        length = struct.unpack('>I', data[offset:offset + 4])[0]
        kind = data[offset + 4:offset + 8]
        payload = data[offset + 8:offset + 8 + length]
        checksum = struct.unpack('>I', data[offset + 8 + length:offset + 12 + length])[0]
        assert checksum == zlib.crc32(kind + payload), path
        if kind == b'IHDR':
            dimensions = struct.unpack('>II', payload[:8])
        elif kind == b'IDAT':
            compressed += payload
        offset += length + 12
    assert dimensions and compressed, path
    raw = zlib.decompress(compressed)
    assert len(raw) == dimensions[1] * (1 + dimensions[0] * 4), path
    return dimensions


def main():
    project = openstep((ROOT / 'Ice.xcodeproj/project.pbxproj').read_text())
    objects = project['objects']

    def references(value):
        if isinstance(value, dict):
            for item in value.values():
                references(item)
        elif isinstance(value, list):
            for item in value:
                references(item)
        elif re.fullmatch('[0-9A-F]{24}', value):
            assert value in objects, f'Dangling Xcode reference: {value}'

    references(project)
    app_configs = []
    xpc_configs = []
    for obj in objects.values():
        settings = obj.get('buildSettings', {})
        identifier = settings.get('PRODUCT_BUNDLE_IDENTIFIER')
        if identifier == 'local.sorabar.app':
            app_configs.append(settings)
            assert settings['PRODUCT_NAME'] == 'SoraBar'
            assert settings['INFOPLIST_KEY_CFBundleDisplayName'] == 'Sora Bar'
        elif identifier == 'local.sorabar.app.MenuBarItemService':
            xpc_configs.append(settings)
    assert len(app_configs) == len(xpc_configs) == 2
    for path in ROOT.rglob('*.plist'):
        plistlib.loads(path.read_bytes())
    for suffix in ('*.xcscheme', '*.xcworkspacedata', '*.xcsettings'):
        for path in ROOT.rglob(suffix):
            ET.parse(path)
    scheme = ET.parse(ROOT / 'Ice.xcodeproj/xcshareddata/xcschemes/SoraBar.xcscheme')
    for ref in scheme.findall('.//BuildableReference'):
        assert ref.attrib['BuildableName'] == 'SoraBar.app'
        assert ref.attrib['BlueprintIdentifier'] in objects

    assets = 0
    for path in ROOT.rglob('*.json'):
        document = json.loads(path.read_text())
        if path.name != 'Contents.json':
            continue
        for entry in document.get('images', []):
            if 'filename' not in entry:
                continue
            dimensions = check_png(path.parent / entry['filename'])
            if 'size' in entry:
                size = int(float(entry['size'].split('x')[0]) * float(entry['scale'][:-1]))
                assert dimensions == (size, size), path
            assets += 1
    assert assets == 17
    info = plistlib.loads((ROOT / 'Ice/Resources/Info.plist').read_bytes())
    assert 'SUFeedURL' not in info and 'SUPublicEDKey' not in info
    assert info['SUEnableAutomaticChecks'] is False
    for folder in ('Ice', 'Shared', 'MenuBarItemService'):
        for path in (ROOT / folder).rglob('*.swift'):
            source = path.read_text()
            assert 'com.jordanbaird.Ice' not in source, path
            assert 'import Sparkle' not in source, path
    assert 'Sparkle' not in (ROOT / 'Ice.xcodeproj/project.pbxproj').read_text()
    xpc = (ROOT / 'Shared/Services/MenuBarItemService.swift').read_text()
    assert 'local.sorabar.app.MenuBarItemService' in xpc
    assert (ROOT / 'LICENSE').read_bytes() == (ROOT / 'Ice/Resources/LICENSE.txt').read_bytes()
    assert (ROOT / 'Ice/Resources/Acknowledgements.rtf').is_file()
    for path in (ROOT / 'Scripts').rglob('*.sh'):
        subprocess.run(['bash', '-n', str(path)], check=True)
    translations = (ROOT / 'Ice/Resources/ja.lproj/Localizable.strings').read_text()
    pairs = re.findall(r'("(?:\\.|[^"\\])*")\s*=\s*("(?:\\.|[^"\\])*")\s*;', translations)
    assert len(pairs) >= 40
    keys = [json.loads(key) for key, _ in pairs]
    assert len(keys) == len(set(keys)), 'Duplicate translation keys'
    for _, value in pairs:
        json.loads(value)
    # Preserve inherited tests exactly; they are executed separately on macOS.
    manifest = json.loads((ROOT / 'UPSTREAM.json').read_text())
    for entry in manifest['files']:
        if entry['path'].startswith('Tests/'):
            content = (ROOT / entry['path']).read_bytes()
            digest = hashlib.sha1(b'blob ' + str(len(content)).encode() + b'\0' + content).hexdigest()
            assert digest == entry['sha'], entry['path']
    print(f'PASS: {len(objects)} Xcode objects, app/XPC identity, {assets} PNG assets,')
    print(f'      plist/XML/JSON, {len(pairs)} Japanese translations, shell syntax, offline updates,')
    print('      bundled license and unchanged inherited tests.')
    print('Not run: Swift compilation, unit tests, signing or macOS 27.2 hardware checks.')


if __name__ == '__main__':
    main()
