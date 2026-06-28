# skill-evolve

Claude のスキルを、実際の使用データから自動で育てる仕組みです。

PR のレビューコメントや調査ログを毎週集計し、Claude API で分析して、スキルファイルを自動で改善します。

---

## どういう仕組みか

```
【毎週自動実行】

Case 1（GitHub Actions）
  あなたのリポジトリの PR レビューコメント
      ↓ 収集・集計
  Claude が「よく指摘されるパターン」を抽出
      ↓
  .claude/skill-evolve/review-patterns.md に保存（自動 commit）
      ↓
  review-custom スキルがレビュー時にこのファイルを読む
  → コードレビューの観点が自動で育っていく

Case 2（ローカル cron）
  ~/.investigate/ に蓄積された調査ログ
      ↓ 集計
  「繰り返し未解決になる不明点」を Claude が分析
      ↓
  investigate_bug スキルのヒアリング項目・ガードレールを改善

Case 3（ローカル cron）
  ~/.investigate/ + ~/.dev/ を横断集計
      ↓
  「繰り返しブロックされるタスクパターン」を Claude が分析
      ↓
  dev スキルの計画・実行フェーズを改善
```

---

## ファイル構成

```
plugins/skill-evolve/
├── README.md（このファイル）
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   └── skill-evolve/
│       └── SKILL.md                 # Case 2&3: /skill-evolve コマンド
└── scripts/
    ├── github-actions/              # Case 1: GitHub Actions から実行されるスクリプト
    │   ├── collect_review_comments.py   # PR コメントを GitHub API で収集
    │   └── improve_review_patterns.py   # Claude で分析 → review-patterns.md を更新
    └── local-cron/                  # Case 2&3: データ収集スクリプト
        ├── collect_investigate.py       # Case 2: ~/.investigate/ の未解決パターンを集計
        └── collect_cross_skill.py       # Case 3: investigate + dev を横断集計

.github/workflows/
└── skill-evolve.yml                 # Case 1: Reusable Workflow（GitHub Actions）
```

---

## セットアップ

### Case 1: GitHub Actions でレビュースキルを育てる

#### ステップ1: あなたのリポジトリにワークフローを追加する

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

#### ステップ2: GitHub Secrets に API キーを登録する

リポジトリの **Settings → Secrets and variables → Actions** を開き、
`ANTHROPIC_API_KEY` という名前で Anthropic の API キーを登録します。

#### ステップ3: review-custom スキルを導入する

`plugins/review/skills/review-custom/` のスキルをインストールします。
週次で `.claude/skill-evolve/review-patterns.md` が自動生成され、レビュー時に読み込まれます。

---

### Case 2&3: /skill-evolve でスキルを育てる

`investigate_bug` や `dev` スキルを使い続けると `~/.investigate/` や `~/.dev/` にデータが蓄積されます。
任意のタイミングで `/skill-evolve` を実行すると、そのデータを分析してスキルを改善します。

#### 使い方

Claude に話しかけるだけです:

```
/skill-evolve
```

Claude が自動でデータ収集・分析・SKILL.md 編集・git commit まで行います。

#### EVOLVE マーカーを追加する（任意）

SKILL.md を自動改善の対象にするには、改善したいセクションに以下のマーカーを追加します。
マーカーがない SKILL.md はスキップされます（安全）。

```markdown
## ガードレール

<!-- EVOLVE:START -->
<!-- EVOLVE:END -->

- 推測禁止: ...（手動で書いた部分は変更されない）
```

---

## 生成されるファイル

| ファイル | 内容 | 更新方法 |
|---------|------|---------|
| `.claude/skill-evolve/review-patterns.md` | PR レビューコメントから抽出したパターン | GitHub Actions が週次自動更新 |
| `.claude/skill-evolve/raw-comments.json` | 収集した生のコメントデータ（中間ファイル） | GitHub Actions が毎回上書き |
| `.claude/skill-evolve/investigate-patterns.json` | 未解決の不明点パターン（中間ファイル） | ローカル cron が毎回上書き |
| `.claude/skill-evolve/cross-skill-patterns.json` | 横断集計結果（中間ファイル） | ローカル cron が毎回上書き |

---

## よくある質問

**Q. PR コメントが少ない週は何が起きますか？**
コメントが 0 件の場合は `review-patterns.md` を更新せずに終了します。

**Q. `review-patterns.md` の内容がおかしかった場合は？**
ファイルを手動で編集するか削除してください。次の週次実行で再生成されます。

**Q. 自動 commit を止めたい場合は？**
Case 1 はワークフローの最後のステップを削除してください。Case 2&3 は `/skill-evolve` 実行後に確認を求めるので、その時点で断ることができます。
