# Sora Bar — Ice派生版

Iceの実装とmacOS 27向け互換修正を取り込んだ、macOSネイティブのメニューバー管理アプリです。
仮称はSora Bar、初期バージョンは0.1.0です。Ice公式の製品ではありません。

**ソースコードを用意した検証用プレビューです。macOSでのコンパイル・起動・27.2の実機動作は未確認です。**
この環境はLinuxのため、インストール済みアプリや動作確認済みバイナリは提供していません。

## 取り込んだ機能

- 表示・非表示・常時非表示の区分、ホバー・クリック・スクロールでの表示、自動収納
- 区分へのドラッグ配置、アイコン検索、隠れた項目を表示する独立バー（Sora Panel）
- 単色・グラデーション・影・枠線・角丸などのメニューバー外観設定
- グローバルショートカット、ログイン時起動、設定保存
- macOS 27向けのアイコン取得・表示管理・クリック処理と既存の検証ツール

これらは継承した機能で、Sora Barとしての動作確認はまだ完了していません。
日本語環境では主要設定名と権限案内を日本語にしています。一部の詳細設定は英語です。

## macOS 27.2での制限

- **対応目標であり、動作保証済みではありません。** 27系の修正は公式Iceでは取り込み前のPRに基づきます。
- 表示区分はアプリ単位で保存します。区分内の実メニューバーの順序はmacOSが決定します。
- 27系ではアプリケーションメニューを隠す機能をスキップします。
- 既定の非表示方式は、macOSの「メニューバーへの表示を許可」に相当する設定を利用します。
  設定にアクセスできない場合には、非公開APIを使う代替方式に切り替わります。
- 代替方式ではシステム項目のクリックに遅延が生じることや、Developer ID署名のないビルドで
  自アプリのアイコンも隠れることがあります。Dock/FinderからSora Barを開き直すと設定画面を呼び出せます。
- 設定方式はOSの内部仕様に依存するため、OS更新後に再検証が必要です。
- 自動更新は無効です。元のIceを誤って配信しないよう、Sparkle・更新URL・公開鍵を除去しました。

## Macでビルドする

1. このソース一式をMacへ展開します。
2. フル版のXcodeをインストールし、初回起動のセットアップを済ませます。
   macOS 27.2を対象とする際は、そのOS向けSDKを備えたXcodeを使ってください。
3. ターミナルで展開先のフォルダーに移動し、次を実行します。

```bash
bash Scripts/build.sh
```

Swift Package Managerが依存ライブラリを取得するため、初回はインターネット接続が必要です。
ビルドログは`build/build.log`、アプリは
`build/DerivedData/Build/Products/Release/SoraBar.app`、
試用版ZIPは`dist/SoraBar-preview.zip`に出力します。

ビルド後にユーザーのApplicationsフォルダーへインストールして起動する場合：

```bash
bash Scripts/install.sh
```

既存のSoraBar.appは日時付きでバックアップします。Ice.appやIceの設定は置き換えません。
メニューバーの操作が競合するため、検証時はIceなど他のメニューバー管理アプリを終了してください。
初回起動でアクセシビリティを許可し、独立バーや外観変更には画面収録も許可します。
署名が変わるビルドでは、macOS側の許可を設定し直す必要がある場合があります。

Xcodeで開く場合は`Ice.xcodeproj`を開き、スキームに **SoraBar** を選びます。
コード内の型名・ディレクトリ名にIceが残っているのは、継承コードの変更を抑えるためです。
外部識別子は`local.sorabar.app`、XPCは`local.sorabar.app.MenuBarItemService`です。

### 署名

ビルドスクリプトの既定はローカル用のアドホック署名です。
手元の証明書を使用する場合は、設定済みのチームと証明書を明示できます。

```bash
DEVELOPMENT_TEAM=YOUR_TEAM_ID SIGNING_IDENTITY='Apple Development' bash Scripts/build.sh
```

このスクリプトはローカル検証用にHardened Runtimeを無効化します。
一般配布する際は、自分のBundle ID、Developer ID署名、Hardened Runtime、必要なentitlements、
公証、依存ライブラリのライセンス一式を別途整備・検証してください。
生成するプレビューZIPは公証済み配布版ではありません。

## 検証

Macで既存のコアロジックテストを実行：

```bash
swift test
```

Linuxでも実施できるプロジェクト・リソース・識別子の整合性確認：

```bash
python3 Scripts/verify-source.py
```

実機で確認する項目と現在の結果は[VALIDATION.ja.md](VALIDATION.ja.md)を参照してください。
`.github/workflows/build.yml`にmacOSでテスト・アドホック署名ビルド・DMG生成を行うCIを用意していますが、
この作業ではGitHubへの公開・CI実行は行っていません。

### Xcodeなしで使うための配布物

CIが成功すると`SoraBar-preview-Mac-download`という成果物に、アプリ入りZIP、
ApplicationsへドラッグしてインストールするDMG、対応するGPLソースZIPを保存します。
アプリ本体を受け取る利用者にはXcodeやターミナルは不要です。
`INSTALL.ja.txt`に利用者向けの手順を用意しています。

Macでアプリ入りZIPとDMGを両方作る場合は、`bash Scripts/package-preview.sh`を実行します。
この仕組みを用意しただけではビルド済みアプリは生成されません。

## ライセンスと出典

GPL-3.0。原著作権表示と[LICENSE](LICENSE)を保持しています。
上流は[Jordan BairdのIce](https://github.com/jordanbaird/Ice)、
取り込んだ互換修正は[PR #995](https://github.com/jordanbaird/Ice/pull/995)です。
取得元は`RabenkoYevhenii/Ice`の次のコミットに固定しました。

```
fa3f225f5967935459bcb68c637f863e62b2cbcd
```

取得ファイルと元のGitハッシュは[UPSTREAM.json](UPSTREAM.json)、
変更一覧は[CHANGES.ja.md](CHANGES.ja.md)に記録しています。
オリジナルREADMEは[README.upstream.md](README.upstream.md)、依存ライブラリの元の謝辞は
`Ice/Resources/Acknowledgements.rtf`です。Thaw・Barometer由来の注記も保持しています。
アプリアイコンなどの画像は独自の幾何学図形に置き換え、生成コードを同梱しています。
元のPDF・デザイン資料・宣伝動画は含めていません。
