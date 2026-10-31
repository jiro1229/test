#!/bin/bash
# Sora Bar local development build. Modified 2026-10-31.
set -euo pipefail
if [[ "$(uname -s)" != Darwin ]]; then
    echo "Sora Bar requires macOS and a full Xcode installation to build." >&2
    exit 1
fi
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DERIVED="${DERIVED:-$ROOT/build/DerivedData}"
OUTPUT="$ROOT/dist"
CONFIGURATION="${CONFIGURATION:-Release}"
mkdir -p "$ROOT/build" "$OUTPUT"
xcrun --find swift >/dev/null
xcodebuild -version
SIGNING=(CODE_SIGN_IDENTITY=- CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM=
    CODE_SIGNING_REQUIRED=YES CODE_SIGNING_ALLOWED=YES PROVISIONING_PROFILE_SPECIFIER=)
if [[ -n "${DEVELOPMENT_TEAM:-}" ]]; then
    SIGNING=(CODE_SIGN_STYLE=Manual DEVELOPMENT_TEAM="$DEVELOPMENT_TEAM"
        CODE_SIGN_IDENTITY="${SIGNING_IDENTITY:-Apple Development}")
fi
# Local preview only. Distribution needs separate Developer ID signing and notarization.
xcodebuild -project "$ROOT/Ice.xcodeproj" -scheme SoraBar \
    -configuration "$CONFIGURATION" -destination 'platform=macOS' \
    -derivedDataPath "$DERIVED" build \
    ENABLE_HARDENED_RUNTIME=NO "${SIGNING[@]}" \
    2>&1 | tee "$ROOT/build/build.log"
APP="$DERIVED/Build/Products/$CONFIGURATION/SoraBar.app"
[[ -d "$APP" ]] || { echo "Missing product: $APP" >&2; exit 1; }
codesign --verify --deep --strict "$APP"
/usr/libexec/PlistBuddy -c 'Print :CFBundleIdentifier' "$APP/Contents/Info.plist" \
    | grep -qx 'local.sorabar.app'
STAGING="$(mktemp -d "$OUTPUT/.sorabar.XXXXXX")"
trap 'rm -rf "$STAGING"' EXIT
ditto "$APP" "$STAGING/SoraBar.app"
ditto -c -k --sequesterRsrc --keepParent "$STAGING/SoraBar.app" "$OUTPUT/SoraBar-preview.zip"
echo "Build: $APP"
echo "Preview archive: $OUTPUT/SoraBar-preview.zip"
