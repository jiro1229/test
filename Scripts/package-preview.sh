#!/bin/bash
# Create an installable preview; created for Sora Bar on 2026-10-31.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ "$(uname -s)" != Darwin ]]; then
    echo "Packaging Sora Bar requires macOS and Xcode." >&2
    exit 1
fi
bash "$ROOT/Scripts/build.sh"
DERIVED="${DERIVED:-$ROOT/build/DerivedData}"
APP="$DERIVED/Build/Products/${CONFIGURATION:-Release}/SoraBar.app"
OUTPUT="$ROOT/dist"
codesign --verify --deep --strict "$APP"
STAGING="$(mktemp -d "$OUTPUT/.dmg.XXXXXX")"
trap 'rm -rf "$STAGING"' EXIT
ditto "$APP" "$STAGING/SoraBar.app"
ln -s /Applications "$STAGING/Applications"
cp "$ROOT/INSTALL.ja.txt" "$STAGING/最初にお読みください.txt"
hdiutil create -volname 'Sora Bar' -srcfolder "$STAGING" \
    -ov -format UDZO "$OUTPUT/SoraBar-preview.dmg"
hdiutil verify "$OUTPUT/SoraBar-preview.dmg"
echo "Disk image: $OUTPUT/SoraBar-preview.dmg"
