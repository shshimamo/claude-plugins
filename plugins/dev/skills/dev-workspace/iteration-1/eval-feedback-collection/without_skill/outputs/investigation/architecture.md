# Architecture - feedback-collection

## プラグイン構造の共通パターン

既存プラグインはすべて以下のディレクトリ構造を持つ:

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json      # プラグインメタデータ（name / description / author）
├── skills/
│   └── <skill-name>/
│       └── SKILL.md     # スキル定義（フロントマター + 呼び出しパターン）
└── hooks/               # 任意: フックスクリプト（prompt-insight のみ持つ）
    └── *.sh
```

## スキル呼び出しパターン

SKILL.md はフロントマター（name / description / version）＋Markdown 本文で構成。
呼び出しパターンごとにセクションを分けて「ステップ1〜N」形式で処理を記述する。

## データ保存パターン

- `~/.todo/` — todos.md 1ファイルに全データ
- `~/.checkpoint/` — タスク別ディレクトリ＋タイムスタンプファイル
- `~/.dev/` — プロジェクト/フィーチャー別ディレクトリ＋複数md
- `~/.repo-know/` — プロジェクト別ディレクトリ＋カテゴリ別md

feedback-collection は checkpoint と同様に「日付ベースのファイル分割」が適切。
`~/.feedback/<project-name>/YYYY-MM-DD.jsonl` に1フィードバック1行のJSONLで保存する設計とする。

## フックの仕組み（prompt-insight を参考）

`~/.claude/settings.json` の `hooks` セクションに `UserPromptSubmit` や `PostToolUse` を登録することで、
プラグイン独自のシェルスクリプトをフック実行できる。
feedback-collection では `StopHook`（セッション終了時）を利用してフィードバック収集を促すことを検討する。
