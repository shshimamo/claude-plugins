# Architecture - dev-review-cmd

## devスキルの構成

devスキルは単一の `SKILL.md` によって定義されるプロンプトベースのスキル。
コマンド（`plan` / `exec`）はユーザーの呼び出し文字列で分岐し、各コマンドのステップが順に実行される。

```
/dev plan  → ヒアリング → 調査 → 計画 → アウトプット生成 → ブラッシュアップ
/dev exec  → 計画読み込み → 進捗確認 → タスク実行 → tasks.md更新
/dev review（新規）→ 対象特定 → コード取得 → レビュー → 結果出力
```

## ファイル保存構造

```
~/.dev/<project>/
└── <feature-name>/
    ├── investigation/
    ├── plan.md
    ├── tasks.md
    ├── artifacts/
    └── review.md   ← 新規追加（reviewコマンドの出力）
```

## SKILL.mdの構造パターン

各コマンドは以下のパターンで記述されている:

```
### `<command>`

#### ステップ1: ...
#### ステップ2: ...
...
```

`review` コマンドも同パターンで追記する。

## reviewコマンドの設計方針

1. **対象取得**: `git diff`・`git diff <base>..<head>` でレビュー対象コードを取得
2. **コンテキスト収集**: plan.md・tasks.md が存在すればレビューの文脈として活用
3. **AIレビュー実行**: 重大度・ファイル・行番号・指摘内容・改善提案を構造化
4. **結果保存**: `review.md` に保存（フィーチャーと紐付く場合は `~/.dev/<project>/<feature>/review.md`）
