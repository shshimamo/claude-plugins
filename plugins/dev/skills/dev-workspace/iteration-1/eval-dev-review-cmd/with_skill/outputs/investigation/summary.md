# Investigation Summary - dev-review-cmd

## 仕様の理解

devスキル（`/dev plan` / `/dev exec`）に新コマンド `/dev review` を追加する。
ユーザーが実装したコードをAIがレビューし、問題点・改善提案を構造化して出力するコマンド。

レビュー対象の特定方法:
- `git diff HEAD` をデフォルトとし、ユーザーがブランチ・コミット範囲を任意指定可能
- git管理外プロジェクトでは動作しない（エラーメッセージで案内）

出力イメージ:
- 重大度別（Critical / Warning / Suggestion）の指摘リスト
- ファイル・行番号付きのコメント
- 改善後のコードスニペット（必要に応じて）
- レビュー結果を `review.md` に保存

フィーチャー情報との連携:
- 対象フィーチャーの `plan.md` / `tasks.md` が存在すれば読み込み、設計意図を踏まえたレビューを実施
- フィーチャー情報がない場合もコードのみで動作可能

## 関連ファイル

- `plugins/dev/skills/dev/SKILL.md`: devスキル本体。`plan` / `exec` の仕様が定義されており、`review` セクションを追記する主要ファイル
- `plugins/dev/.claude-plugin/plugin.json`: プラグインメタ情報。description に `review` コマンドの説明を追記する
- `plugins/dev/skills/dev/evals/evals.json`: evalの定義ファイル。`review` コマンドのevalケース（id:3）がすでに存在している
- `plugins/review/skills/review-custom/SKILL.md`: 既存のレビュースキル。レビュー観点・出力フォーマットの参考になる

## 影響範囲

| ファイル | 変更内容 |
|---------|---------|
| `plugins/dev/skills/dev/SKILL.md` | `review` コマンドのセクションを追記。フロントマターの description も更新 |
| `plugins/dev/.claude-plugin/plugin.json` | description に `review` コマンドの説明を追記 |
| `plugins/dev/skills/dev/evals/evals.json` | 変更不要（id:3のevalケースがすでに定義済み） |

## 不明点・リスク

| # | 内容 | 影響 | 状態 |
|---|------|------|------|
| 1 | レビュー対象の指定方法（git diff のみ？ファイル指定も？） | 中 | 解決済（git diffベースで、ブランチ/コミット範囲をオプション指定可能とする） |
| 2 | 既存フィーチャー情報（plan/tasks.md）との連携有無 | 低 | 解決済（存在すれば読み込み、なくても単体動作可能） |
| 3 | レビュー結果の保存先 | 中 | 解決済（`~/.dev/<project>/<feature>/review.md` に保存） |
| 4 | 差分が大きい場合の対応 | 低 | 解決済（ファイル単位の分割レビューを推奨する旨をSKILL.mdに明示） |
