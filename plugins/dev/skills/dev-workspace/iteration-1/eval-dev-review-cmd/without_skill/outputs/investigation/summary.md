# Investigation Summary - dev-review-cmd

## 仕様の理解

devスキル（`/dev plan` / `/dev exec`）に新コマンド `/dev review` を追加する。
ユーザーが実装したコードをAIがレビューし、問題点・改善提案をまとめて出力するコマンド。

レビュー対象の特定方法:
- Gitの差分（`git diff`・`git diff HEAD`）を基本とする
- 対象ブランチ・コミット範囲はユーザーが指定可能

出力イメージ:
- 重大度別（Critical / Warning / Suggestion）の指摘リスト
- ファイル・行番号付きのコメント
- 改善後のコードスニペット（必要に応じて）

## 関連ファイル

- `plugins/dev/skills/dev/SKILL.md`: devスキル本体。`plan` / `exec` の仕様が記述されている。今回 `review` セクションを追記する主要ファイル。
- `plugins/dev/.claude-plugin/plugin.json`: プラグインメタ情報。コマンド追加の影響はないが確認済み。
- `plugins/dev/skills/dev/evals/evals.json`: evalの定義ファイル。`review` コマンドのevalを追加する可能性あり。

## 影響範囲

| ファイル | 変更内容 |
|---------|---------|
| `plugins/dev/skills/dev/SKILL.md` | `review` コマンドのセクションを追加 |
| `plugins/dev/skills/dev/evals/evals.json` | reviewコマンドのevalケースを追加（任意） |

## 不明点・リスク

| # | 内容 | 影響 | 状態 |
|---|------|------|------|
| 1 | レビュー対象の指定方法（git diff のみ？ファイル指定も？） | 中 | 未解決 |
| 2 | 既存フィーチャー情報（plan/tasks.md）との連携有無 | 低 | 未解決 |
| 3 | レビュー結果の保存先（`~/.dev/<project>/<feature>/review.md`？） | 中 | 未解決 |
