# Components - feedback-collection

## コンポーネント一覧

| コンポーネント | ファイル | 責務 |
|--------------|---------|------|
| プラグイン定義 | `plugins/feedback/.claude-plugin/plugin.json` | プラグイン名・説明・作者の宣言 |
| feedback スキル | `plugins/feedback/skills/feedback/SKILL.md` | /feedback / /feedback show / /feedback setup の処理定義 |
| フックスクリプト | `plugins/feedback/hooks/feedback-hook.sh` | セッション終了時にフィードバック収集を促すプロンプト出力 |
| データストア | `~/.feedback/<project>/YYYY-MM-DD.jsonl` | フィードバックデータの永続化（ランタイム生成） |

## データ形式

`~/.feedback/<project>/YYYY-MM-DD.jsonl` の1行フォーマット:

```json
{"timestamp": "2026-06-24T10:30:00+09:00", "plugin": "todo", "rating": 4, "comment": "タスク追加が直感的で使いやすい"}
```

| フィールド | 型 | 説明 |
|-----------|---|------|
| timestamp | ISO8601 文字列 | 記録日時 |
| plugin | 文字列 | 評価対象プラグイン名 |
| rating | 整数 (1-5) | 満足度評価 |
| comment | 文字列 \| null | 任意コメント |

## ディレクトリ構造

```
plugins/feedback/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── feedback/
│       └── SKILL.md
└── hooks/
    └── feedback-hook.sh

~/.feedback/                      # ランタイムデータ（gitignore対象外・ローカルのみ）
└── <project-name>/
    ├── 2026-06-24.jsonl
    └── 2026-06-25.jsonl
```

## 依存関係

```
feedback スキル
  └── フックスクリプト（/feedback setup 経由でオプションインストール）
      └── ~/.claude/settings.json（StopHook 登録）
```

既存プラグインへの依存・変更は一切なし。
