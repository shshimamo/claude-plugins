# Plan - feedback-collection

## 概要

**何を**: プラグイン使用後にユーザーがフィードバックを送れる `/feedback` プラグインを追加する。
**なぜ**: プラグインの品質改善のためにユーザーの生の声を収集する仕組みが必要。現状は改善点を把握する手段がない。

## 実装方針

- 既存プラグインのパターン（`todo`, `checkpoint`）に倣い、新規プラグインとして独立実装
- フィードバックはローカルファイル `~/.feedback/` に蓄積（外部送信なし）
- コマンド体系:
  - `/feedback` — 直近使ったプラグインへのフィードバック送信（省略時は対話で選択）
  - `/feedback <plugin-name>` — 指定プラグインへのフィードバック送信
  - `/feedback show` — 蓄積されたフィードバック一覧を表示
- 評価形式: ★1-5 の数値スコア + 任意のテキストコメント
- ファイル構造: `~/.feedback/<plugin-name>/YYYYMMDD_HHMMSS.md`
- マーケットプレイス（`marketplace.json`）と README にエントリを追加

## 影響範囲

| ファイル | 変更種別 |
|---------|---------|
| `.claude-plugin/marketplace.json` | 変更（feedbackエントリ追加） |
| `plugins/feedback/.claude-plugin/plugin.json` | 新規作成 |
| `plugins/feedback/skills/feedback/SKILL.md` | 新規作成 |
| `README.md` | 変更（feedbackプラグイン説明追加） |

## 考慮事項

- **後方互換性**: 既存プラグインへの変更なし。独立したプラグインとして追加
- **セキュリティ**: ローカル保存のみのためAPIキー等の秘密情報は不要
- **ユーザビリティ**: コマンドは簡潔に。`/feedback 5 とても使いやすい` のようなワンライナーで送れる設計
- **拡張性**: 将来的に外部送信や集計機能を追加できるよう、フォーマットを構造化

## トレーサビリティ

| 要件 | コンポーネント | API | データ |
|------|--------------|-----|--------|
| フィードバック送信 | `feedback` スキル（送信コマンド） | `/feedback [plugin] [score] [comment]` | `~/.feedback/<plugin>/YYYYMMDD.md` |
| フィードバック閲覧 | `feedback` スキル（showコマンド） | `/feedback show [plugin]` | `~/.feedback/<plugin>/` 配下の全ファイル |
| プラグイン選択 | `feedback` スキル（対話） | - | `~/.feedback/plugins.md`（プラグイン一覧） |
