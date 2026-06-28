# Tasks - dev-review-cmd

## 基本情報

- ブランチ: `feature/dev-review-cmd`
- 開始日: 2026-06-24

## 要件サマリー

- **背景**: `/dev exec` で実装後のコードレビューをAIに委ねることで、品質担保と手戻り削減を実現する
- **受入条件**:
  - `/dev review` を呼び出すとgit diffを取得してレビューが実行される
  - 重大度別（Critical / Warning / Suggestion）に指摘が整理される
  - ファイル・行番号付きでコメントが出力される
  - レビュー結果が `review.md` に保存される
- **スコープ外**:
  - CI/CD連携
  - 外部コードレビューツール（GitHub PRコメント等）との連携
  - plan/execフロー以外のコードへの適用（今回はgit diffベースのみ）

---

## タスク

| # | タスク名 | 状態 | 対象ファイル | 実装詳細 | 依存 |
|---|---------|------|------------|---------|------|
| 1 | SKILL.md に `review` セクション追記 | 未着手 | `plugins/dev/skills/dev/SKILL.md` | `plan` / `exec` セクションの後に `review` コマンドのステップ定義（ステップ1〜4）を追記 | - |
| 2 | SKILL.md の description 更新 | 未着手 | `plugins/dev/skills/dev/SKILL.md` | フロントマターの `description` フィールドに `/dev review` の説明を追記 | #1 |
| 3 | plugin.json の description 更新 | 未着手 | `plugins/dev/.claude-plugin/plugin.json` | `description` フィールドに `review` コマンドの説明を追記 | #1 |
| 4 | review.md のテンプレート定義 | 未着手 | `plugins/dev/skills/dev/SKILL.md` | SKILL.md内に `review.md` の出力フォーマット（テンプレート）を定義 | #1 |
| 5 | evalケースの追加 | 未着手 | `plugins/dev/skills/dev/evals/evals.json` | `/dev review` を呼び出すevalシナリオを追加 | #1, #2 |

**進捗**: 0 / 5 完了

---

## 作業再開ガイド

- **最後のタスク**: -
- **次のアクション**: タスク#1 から着手（SKILL.mdへの `review` セクション追記）
- **メモ**: タスク#1 が最大の変更。#2〜#4 は#1の内容を確認してから実施。#5は最後。

---

## 作業ログ

- 2026-06-24: 調査・計画フェーズ完了。SKILL.mdの構造を確認し、reviewセクションの追記方針を決定。
