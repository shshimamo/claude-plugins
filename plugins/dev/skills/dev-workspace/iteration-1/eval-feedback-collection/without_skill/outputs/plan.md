# Plan - feedback-collection

## 概要

プラグイン使用後にユーザーが簡単にフィードバックを送れる新プラグイン `feedback` を追加する。
ユーザーが `/feedback` コマンドを実行すると、使用したプラグイン・評価・コメントを対話形式で入力し、
ローカルファイル（JSONL）に保存する。蓄積したフィードバックは `/feedback show` で一覧・集計できる。

## 実装方針

- **新規プラグインとして独立実装**: 既存プラグインを変更しない
- **データ保存**: `~/.feedback/<project-name>/YYYY-MM-DD.jsonl` に1行1JSON で保存
- **評価形式**: 5段階（1〜5）＋任意コメント
- **呼び出し方式**: 手動コマンド（`/feedback`）をメインとし、自動プロンプトはオプション
- **コマンド体系**:
  - `/feedback` — フィードバック登録（対話形式）
  - `/feedback show` — 一覧・集計表示
  - `/feedback setup` — 自動プロンプト用フック設定（オプション）

## 影響範囲

| ファイル | 変更種別 | 内容 |
|---------|---------|------|
| `plugins/feedback/.claude-plugin/plugin.json` | 新規作成 | プラグインメタデータ |
| `plugins/feedback/skills/feedback/SKILL.md` | 新規作成 | スキル定義（3コマンド） |
| `plugins/feedback/hooks/feedback-hook.sh` | 新規作成 | セッション終了時フック（setup用） |
| `README.md` | 追記 | feedback プラグインの説明追加 |

## 考慮事項

- **プライバシー**: フィードバックはローカル保存のみ。外部送信は行わない（MVP スコープ外）
- **後方互換性**: 既存プラグインへの変更なし
- **データ形式**: JSONL を選択（checkpoint の md 形式より集計が容易）
- **プロジェクト名**: `git remote get-url origin` から取得、失敗時は `basename $(pwd)`（既存パターン踏襲）

## トレーサビリティ

| 要件 | コンポーネント | API | データ |
|------|--------------|-----|--------|
| フィードバック登録 | feedback スキル（`/feedback`） | - | `~/.feedback/<project>/YYYY-MM-DD.jsonl` |
| 一覧・集計表示 | feedback スキル（`/feedback show`） | - | 同上（読み取り） |
| 自動プロンプト | feedback-hook.sh + settings.json | StopHook | - |
