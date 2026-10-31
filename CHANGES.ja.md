# Sora Bar 0.1.0 の変更

変更日: 2026-10-31。GPL-3.0のIce派生版として作成。

- IceのmacOS 27対応PR #995のコミット`fa3f225f5967935459bcb68c637f863e62b2cbcd`を取得。
- 外部識別子を`local.sorabar.app`に変更。XPC・ログ・検証ツールも変更。
- 表示名をSora Bar、独立バーをSora Panel、生成アプリ名をSoraBar.appに変更。
- 元の更新サーバー、公開鍵、Sparkle依存と更新UIを削除し、手動更新へ変更。
- 元作者の開発チーム設定を除去。専用スキーム、ローカルビルドとバックアップ付きインストールを追加。
- アイコン17点を新規生成。元の画像・PDF・デザイン資料・宣伝動画は同梱しない。
- 元の謝辞RTFをアプリに同梱して開けるように変更。GPL・派生版の出典もアプリに同梱。
- 主要画面に46項目の日本語訳を追加（部分翻訳）。27.2未検証の案内を画面に表示。
- 元のテスト11ファイルはそのまま保持。ビルド用CI、静的検証、実機チェック表を追加。
- macOSでのコンパイル・単体テスト・実機検証は未実施。

## 変更した上流ファイル

画像の置き換えと新規追加ファイル以外の一覧。各コードファイルにも変更日を表示。

- `.gitignore`
- `Ice/Events/EventTap.swift`
- `Ice/Events/HIDEventManager.swift`
- `Ice/Main/Updates.swift`
- `Ice/MenuBar/Appearance/MenuBarAppearanceEditor/MenuBarAppearanceEditor.swift`
- `Ice/MenuBar/ControlItem/ControlItem.swift`
- `Ice/MenuBar/ControlItem/ControlItemImageSet.swift`
- `Ice/MenuBar/IceBar/IceBar.swift`
- `Ice/MenuBar/IceBar/IceBarColorManager.swift`
- `Ice/MenuBar/IceBar/IceBarLocation.swift`
- `Ice/MenuBar/MacOS27/Concealer27.swift`
- `Ice/MenuBar/MacOS27/Core/ConcealmentController27.swift`
- `Ice/MenuBar/MacOS27/Core/ItemClick27.swift`
- `Ice/MenuBar/MacOS27/Core/ItemImages27.swift`
- `Ice/MenuBar/MacOS27/ItemClicker27.swift`
- `Ice/MenuBar/MacOS27/ItemImageStore27.swift`
- `Ice/MenuBar/MacOS27/MenuBarItemProvider27.swift`
- `Ice/MenuBar/MenuBarItems/MenuBarItemImageCache.swift`
- `Ice/MenuBar/MenuBarItems/MenuBarItemTag.swift`
- `Ice/MenuBar/MenuBarManager.swift`
- `Ice/MenuBar/MenuBarSection.swift`
- `Ice/Permissions/PermissionsView.swift`
- `Ice/Resources/Info.plist`
- `Ice/Settings/Models/GeneralSettings.swift`
- `Ice/Settings/SettingsPanes/AboutSettingsPane.swift`
- `Ice/Settings/SettingsPanes/AdvancedSettingsPane.swift`
- `Ice/Settings/SettingsPanes/GeneralSettingsPane.swift`
- `Ice/Settings/SettingsPanes/HotkeysSettingsPane.swift`
- `Ice/Settings/SettingsPanes/MenuBarLayoutSettingsPane.swift`
- `Ice/Settings/SettingsView.swift`
- `Ice/UI/IceUI/IceWindow.swift`
- `Ice.xcodeproj/project.pbxproj`
- `Ice.xcodeproj/project.xcworkspace/xcshareddata/swiftpm/Package.resolved`
- `README.md`
- `REQUIREMENTS.ja.md`
- `Scripts/check-panels.swift`
- `Scripts/install.sh`
- `Scripts/macos27/clock-restore.swift`
- `Scripts/macos27/icebar-ax.swift`
- `Scripts/macos27/layout-ax.swift`
- `Scripts/macos27/new-windows.swift`
- `Scripts/macos27/reveal-window.swift`
- `Scripts/macos27/system-item-probe.swift`
- `Scripts/macos27/verify-clock.sh`
- `Scripts/macos27/verify-conceal.sh`
- `Scripts/macos27/verify-hover.sh`
- `Scripts/macos27/verify-icebar-click.sh`
- `Scripts/macos27/verify-icebar.sh`
- `Scripts/macos27/verify-layout.sh`
- `Shared/Services/MenuBarItemService.swift`
