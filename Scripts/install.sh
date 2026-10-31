#!/bin/bash
# Modified for Sora Bar on 2026-10-31.
# Build and install Sora Bar for the current user. Modified 2026-10-31.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
bash "$ROOT/Scripts/build.sh"
DERIVED="${DERIVED:-$ROOT/build/DerivedData}"
APP="$DERIVED/Build/Products/${CONFIGURATION:-Release}/SoraBar.app"
DEST="$HOME/Applications/SoraBar.app"
mkdir -p "$HOME/Applications"
if pgrep -x SoraBar >/dev/null; then
    osascript -e 'tell application id "local.sorabar.app" to quit'
    for _ in {1..20}; do
        pgrep -x SoraBar >/dev/null || break
        sleep 0.25
    done
    if pgrep -x SoraBar >/dev/null; then
        echo "Sora Bar is still running. Quit it and try again." >&2
        exit 1
    fi
fi
if [[ -e "$DEST" ]]; then
    mv "$DEST" "$HOME/Applications/SoraBar-backup-$(date +%Y%m%d-%H%M%S)-$$.app"
fi
ditto "$APP" "$DEST"
codesign --verify --deep --strict "$DEST"
open "$DEST"
echo "Installed: $DEST"
