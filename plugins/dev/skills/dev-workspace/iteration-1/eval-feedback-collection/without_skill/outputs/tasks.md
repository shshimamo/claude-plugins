# Tasks - feedback-collection

## 基本情報

- ブランチ: `feature/feedback-collection`
- チケット: -
- 開始日: 2026-06-24

## 要件サマリー

- **背景**: プラグイン使用後のユーザーフィードバックを収集する仕組みがなく、改善サイクルを回せない
- **受入条件**:
  - `/feedback` でフィードバック（評価＋コメント）を登録できる
  - `/feedback show` で蓄積済みフィードバックを一覧・集計できる
  - 既存プラグインへの変更がない
  - README.md に feedback プラグインの説明が追加されている
- **スコープ外**: 外部サービスへの送信、フィードバックの自動収集フック（MVP後に検討）

---

## タスク

| # | タスク名 | 状態 | 対象ファイル | 実装詳細 | 依存 |
|---|---------|------|------------|---------|------|
| 1 | plugin.json 作成 | 未着手 | `plugins/feedback/.claude-plugin/plugin.json` | name: "feedback"、description・author を記述 | - |
| 2 | SKILL.md 作成（/feedback） | 未着手 | `plugins/feedback/skills/feedback/SKILL.md` | フロントマター＋フィードバック登録フロー（ステップ1〜6）を記述 | #1 |
| 3 | SKILL.md 追記（/feedback show） | 未着手 | `plugins/feedback/skills/feedback/SKILL.md` | 一覧・集計表示フロー（ステップ1〜3）を追記 | #2 |
| 4 | SKILL.md 追記（/feedback setup） | 未着手 | `plugins/feedback/skills/feedback/SKILL.md` | フック設定フロー（オプション機能）を追記 | #2 |
| 5 | フックスクリプト作成 | 未着手 | `plugins/feedback/hooks/feedback-hook.sh` | セッション終了時にフィードバックを促すシェルスクリプト | #4 |
| 6 | README.md 追記 | 未着手 | `README.md` | feedback プラグインのセクションを既存フォーマットに合わせて追加 | #1 |

**進捗**: 0 / 6 完了

---

## 作業再開ガイド

- **最後のタスク**: -
- **次のアクション**: タスク #1 から開始（plugin.json 作成）
- **メモ**: SKILL.md は既存の todo / checkpoint を参考にフォーマットを揃えること

---

## 作業ログ

- 2026-06-24: 調査・計画フェーズ完了。investigation/ と plan.md / tasks.md を生成。
