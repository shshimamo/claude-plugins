# skill-evolve

`~/.investigate/`・`~/.dev/`・`~/.repo-know/`・`~/.prompt-insight/` に蓄積されたデータを分析し、スキルを改善する `/skill-evolve` コマンドを提供します。

```
/skill-evolve を実行すると...

investigate_bug:
  ~/.investigate/bug/ の未解決不明点パターン
  + ~/.repo-know/<project>/ のプロジェクト知識
    ↓
  investigate_bug スキルのヒアリング項目・ガードレールを改善（EVOLVE セクション更新）

investigate_code:
  ~/.investigate/code/ の調査ログ
  + ~/.repo-know/<project>/ のプロジェクト知識
    ↓
  プロジェクトごとのスキル拡張ファイルを更新（gitignore 済み）

dev:
  ~/.investigate/bug/ + ~/.dev/ を横断集計
    ↓
  dev スキルの計画・実行フェーズを改善（EVOLVE セクション更新）

共通: ~/.prompt-insight/ のプロンプトログ（直近30日）
    ↓
  「繰り返し追加指示されていること」を各スキルに反映
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
│       └── SKILL.md                      # /skill-evolve コマンド本体
└── scripts/
    ├── collect_investigate.py            # ~/.investigate/bug/ の未解決パターンを集計
    ├── collect_investigate_code.py       # ~/.investigate/code/ + ~/.repo-know/ を集計
    ├── collect_cross_skill.py            # investigate/bug + dev を横断集計
    └── collect_prompt_insight.py         # ~/.prompt-insight/ のログを集計
```

---

## データの蓄積場所

| ディレクトリ | 書き込むスキル | 内容 |
|-------------|-------------|------|
| `~/.investigate/bug/<project>/` | investigate_bug | バグ調査ログ・未解決不明点 |
| `~/.investigate/code/<project>/` | investigate_code | コード調査ログ |
| `~/.repo-know/<project>/` | investigate_bug・investigate_code | プロジェクト固有の知識（tech/domain/decisions） |
| `~/.dev/<project>/` | dev | タスク管理ログ |
| `~/.prompt-insight/logs/` | （フック自動記録） | プロンプトログ |

---

## 使い方

Claude に話しかけるだけです:

```
/skill-evolve
```

「どのスキルを改善しますか？」と聞いてくるので選択してください。
Claude がデータ収集・分析・スキル更新・git commit まで行います。

---

## ローカル設定ファイルでターゲットをカスタマイズ（任意）

`.claude/claude-plugins/skill-evolve/skill-evolve.local.md` を作成すると、改善対象スキルと設定を環境ごとにカスタマイズできます。
このファイルは `.gitignore` に登録されているため、リポジトリには含まれません。

```markdown
## ターゲット

### investigate_bug
- データソース: investigate_bug
- SKILL.md: plugins/investigate/skills/investigate_bug/SKILL.md
- 改善観点: ヒアリング項目・ガードレール

### my-custom-skill
- データソース: investigate
- SKILL.md: plugins/my-plugin/skills/my-skill/SKILL.md
- 改善観点: ヒアリング項目を中心に改善

## 設定

- prompt_days: 30  # prompt-insight ログの収集日数（デフォルト: 30）
```

ファイルが存在しない場合はデフォルト（investigate_bug・investigate_code・dev、prompt_days: 30）が使われます。

---

## スキル拡張ファイル（investigate_code のみ・自動生成）

`investigate_code` ターゲットは、SKILL.md の EVOLVE セクションではなく
プロジェクトごとのスキル拡張ファイルを更新します。

```
~/.claude/claude-plugins/skill-evolve/
├── skill-evolve.local.md              # 改善プロセスのカスタマイズ
└── skill-extensions/
    └── <project>/
        └── investigate_code.local.md  # プロジェクトごとに自動生成
```

このファイルは `/investigate_code` 実行時に自動で読み込まれ、
そのプロジェクト固有の調査コンテキストとして活用されます。

このディレクトリ以下は `.gitignore` に登録されているため、リポジトリには含まれません。

---

## EVOLVE マーカーの追加（任意）

investigate_bug・dev スキルの SKILL.md を自動改善の対象にするには、改善したいセクションに以下を追加します。
マーカーがない SKILL.md はスキップされます（安全）。

```markdown
## ガードレール

<!-- EVOLVE:START -->
<!-- EVOLVE:END -->

- 推測禁止: ...（手動で書いた部分は変更されない）
```

---

## 更新されるファイル

| ファイル | 内容 | 更新方法 |
|---------|------|---------|
| `plugins/*/skills/*/SKILL.md` の EVOLVE セクション | investigate_bug・dev の改善結果（**主な出力**） | `/skill-evolve` 実行時に直接編集 |
| `~/.claude/claude-plugins/skill-evolve/skill-extensions/<project>/investigate_code.local.md` | investigate_code のプロジェクト別拡張（**主な出力**） | `/skill-evolve` 実行時に自動生成・更新 |
| `.claude/claude-plugins/skill-evolve/investigate-patterns.json` | 未解決の不明点パターン（中間ファイル） | `/skill-evolve` 実行時に上書き |
| `.claude/claude-plugins/skill-evolve/investigate-code-patterns.json` | コード調査パターン（中間ファイル） | `/skill-evolve` 実行時に上書き |
| `.claude/claude-plugins/skill-evolve/cross-skill-patterns.json` | 横断集計結果（中間ファイル） | `/skill-evolve` 実行時に上書き |
| `.claude/claude-plugins/skill-evolve/prompt-patterns.json` | プロンプトログ集計結果（中間ファイル） | `/skill-evolve` 実行時に上書き |

---

## よくある質問

**Q. データが蓄積されていない場合は？**
「データが不足しています」と表示してスキップします。各スキルを使い続けることでデータが蓄積されます。

**Q. prompt-insight を使っていない場合は？**
`~/.prompt-insight/logs/` が存在しない場合は自動的にスキップします。セットアップは `/prompt-insight setup` で行えます。

**Q. investigate_code の拡張ファイルはいつ反映される？**
次回 `/investigate_code` を実行したときにステップ0で自動読み込みされます。

**Q. 自動 commit を止めたい場合は？**
`/skill-evolve` 実行後に変更内容の確認を求めるので、その時点で断ることができます。investigate_code のスキル拡張ファイルはローカルのみのため commit されません。
