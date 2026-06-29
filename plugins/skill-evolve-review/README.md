# skill-evolve-review

GitHub Actions で PR レビューコメントを週次集計し、`review-custom` スキルを自動改善する仕組みです。

```
あなたのリポジトリの PR レビューコメント
    ↓ 収集・集計（GitHub Actions / 週次）
Claude が「よく指摘されるパターン」を抽出
    ↓
.claude/skill-evolve/review-patterns.md に保存（自動 commit）
    ↓
review-custom スキルがレビュー時にこのファイルを読む
→ コードレビューの観点が自動で育っていく
```

---

## ファイル構成

```
plugins/skill-evolve-review/
├── README.md（このファイル）
├── .claude-plugin/
│   └── plugin.json
└── scripts/
    ├── collect_review_comments.py   # PR コメントを GitHub API で収集
    └── improve_review_patterns.py   # Claude で分析 → review-patterns.md を更新

.github/workflows/
└── skill-evolve.yml                 # Reusable Workflow（導入リポジトリから呼び出す）
```

---

## セットアップ

### ステップ1: あなたのリポジトリにワークフローを追加する

あなたのリポジトリ（例: Rails アプリ）に `.github/workflows/skill-evolve.yml` を作成します。

```yaml
name: Skill Evolve

on:
  schedule:
    - cron: '0 1 * * 1'  # 毎週月曜 1:00 UTC（日本時間 10:00）
  workflow_dispatch:       # 手動実行も可能

jobs:
  evolve:
    uses: shshimamo/claude-plugins/.github/workflows/skill-evolve.yml@main
    secrets:
      ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
```

### ステップ2: GitHub Secrets に API キーを登録する

リポジトリの **Settings → Secrets and variables → Actions** を開き、
`ANTHROPIC_API_KEY` という名前で Anthropic の API キーを登録します。

### ステップ3: review-custom スキルを導入する

`plugins/review/skills/review-custom/` のスキルをインストールします。
週次で `.claude/skill-evolve/review-patterns.md` が自動生成され、レビュー時に読み込まれます。

---

## 生成されるファイル

| ファイル | 内容 | 更新方法 |
|---------|------|---------|
| `.claude/skill-evolve/review-patterns.md` | PR レビューコメントから抽出したパターン | GitHub Actions が週次自動更新 |
| `.claude/skill-evolve/raw-comments.json` | 収集した生のコメントデータ（中間ファイル） | GitHub Actions が毎回上書き |

---

## よくある質問

**Q. PR コメントが少ない週は何が起きますか？**
コメントが 0 件の場合は `review-patterns.md` を更新せずに終了します。

**Q. `review-patterns.md` の内容がおかしかった場合は？**
ファイルを手動で編集するか削除してください。次の週次実行で再生成されます。

**Q. 自動 commit を止めたい場合は？**
ワークフローの最後のステップ（`Commit and push`）を削除してください。
