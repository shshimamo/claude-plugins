# Tasks - dev-review-cmd

## 基本情報

- ブランチ: `feature/dev-review-cmd`
- 開始日: 2026-06-24

## 要件サマリー

- **背景**: `/dev exec` で実装後のコードレビューをAIに委ねることで、品質担保と手戻り削減を実現する
- **受入条件**:
  - `/dev review` を呼び出すと git diff を取得してレビューが実行される
  - 重大度別（Critical / Warning / Suggestion）に指摘が整理される
  - ファイル・行番号付きでコメントが出力される
  - レビュー結果が `review.md` に保存される
  - `plan.md` / `tasks.md` が存在する場合は設計意図を加味したレビューが実施される
- **スコープ外**:
  - CI/CD連携
  - 外部コードレビューツール（GitHub PRコメント等）との連携
  - git管理外プロジェクトへの対応

---

## タスク

| # | タスク名 | 状態 | 対象ファイル | 実装詳細 | 依存 |
|---|---------|------|------------|---------|------|
| 1 | SKILL.md に `review` セクション追記 | 未着手 | `plugins/dev/skills/dev/SKILL.md` | `exec` セクションの後に `review` コマンドのステップ定義（ステップ1〜4）と `review.md` テンプレートを追記 | - |
| 2 | SKILL.md フロントマターの description 更新 | 未着手 | `plugins/dev/skills/dev/SKILL.md` | フロントマターの `description` フィールドに `/dev review` の説明を追記 | #1 |
| 3 | plugin.json の description 更新 | 未着手 | `plugins/dev/.claude-plugin/plugin.json` | `description` フィールドに `review` コマンドの説明を追記 | #1 |

**進捗**: 0 / 3 完了

---

## 作業再開ガイド

- **最後のタスク**: -
- **次のアクション**: タスク#1 から着手（SKILL.md への `review` セクション追記）
- **メモ**: タスク#1 が最大の変更。SKILL.md の既存セクション構造（plan/exec）に合わせてステップ形式で記述する。#2・#3 は#1完了後に実施。

---

## 作業ログ

- 2026-06-24: 調査・計画フェーズ完了。SKILL.md・plugin.json・evals.json の構造を確認。evals.json には id:3 で review コマンドの eval がすでに定義済みのため変更不要と判断。
