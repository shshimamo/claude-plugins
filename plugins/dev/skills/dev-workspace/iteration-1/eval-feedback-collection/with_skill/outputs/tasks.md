# Tasks - feedback-collection

## 基本情報
- ブランチ: `feature/feedback-collection`
- チケット: -
- 開始日: 2026-06-24

## 要件サマリー
- **背景**: プラグイン使用後のユーザーフィードバックを収集する仕組みがなく、品質改善のインプットが不足している
- **受入条件**:
  - `/feedback` でフィードバック送信ができる
  - `/feedback show` でフィードバック一覧を確認できる
  - `marketplace.json` と `README.md` に feedbackプラグインが追加されている
- **スコープ外**: 外部API連携、フィードバックの自動集計・分析、他プラグインからの自動呼び出し

---

## タスク

| # | タスク名 | 状態 | 対象ファイル | 実装詳細 | 依存 |
|---|---------|------|------------|---------|------|
| 1 | plugin.json 作成 | 未着手 | `plugins/feedback/.claude-plugin/plugin.json` | `name: feedback`, `description`, `author` を定義 | - |
| 2 | SKILL.md 作成 | 未着手 | `plugins/feedback/skills/feedback/SKILL.md` | フロントマター + 呼び出しパターン3種（引数なし・show・ワンライナー）を実装 | #1 |
| 3 | marketplace.json 更新 | 未着手 | `.claude-plugin/marketplace.json` | `plugins` 配列に feedback エントリを追加 | #1 |
| 4 | README.md 更新 | 未着手 | `README.md` | feedback プラグインのセクション追加（コマンド表・保存先・説明） | #2 |

**進捗**: 0 / 4 完了

---

## 作業再開ガイド
- **最後のタスク**: -
- **次のアクション**: タスク #1 から開始
- **メモ**: 既存の `checkpoint` スキルのファイル保存パターンを参考に実装する

---

## 作業ログ
- 2026-06-24: 調査・計画完了。タスクリスト作成。
