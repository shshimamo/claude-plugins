# skill-evolve

`~/.investigate/` や `~/.dev/` に蓄積されたデータ、および `~/.prompt-insight/` のプロンプトログを分析し、スキルを改善する `/skill-evolve` コマンドを提供します。

```
/skill-evolve を実行すると...

Case 2: ~/.investigate/ の調査ログ
    ↓ 集計
  「繰り返し未解決になる不明点」を Claude が分析
    ↓
  investigate_bug スキルのヒアリング項目・ガードレールを改善

Case 3: ~/.investigate/ + ~/.dev/ を横断集計
    ↓
  「繰り返しブロックされるタスクパターン」を Claude が分析
    ↓
  dev スキルの計画・実行フェーズを改善

共通: ~/.prompt-insight/ のプロンプトログ（直近30日）
    ↓
  「繰り返し追加指示されていること」を Claude が分析
    ↓
  各スキルに「最初からやるべきだった行動」として反映
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
│       └── SKILL.md                 # /skill-evolve コマンド本体
└── scripts/
    ├── collect_investigate.py       # Case 2: ~/.investigate/ の未解決パターンを集計
    ├── collect_cross_skill.py       # Case 3: investigate + dev を横断集計
    └── collect_prompt_insight.py    # ~/.prompt-insight/ のログを集計
```

---

## 使い方

Claude に話しかけるだけです:

```
/skill-evolve
```

「どのスキルを改善しますか？」と聞いてくるので選択してください。
Claude がデータ収集・分析・SKILL.md 編集・git commit まで行います。

---

## ローカル設定ファイルでターゲットをカスタマイズ（任意）

`.claude/claude-plugins/skill-evolve/skill-evolve.local.md` を作成すると、改善対象スキルと設定を環境ごとにカスタマイズできます。
このファイルは `.gitignore` に登録されているため、リポジトリには含まれません。

```markdown
## ターゲット

### investigate_bug
- データソース: investigate
- SKILL.md: plugins/investigate/skills/investigate_bug/SKILL.md
- 改善観点: ヒアリング項目・ガードレール

### my-custom-skill
- データソース: investigate
- SKILL.md: plugins/my-plugin/skills/my-skill/SKILL.md
- 改善観点: ヒアリング項目を中心に改善

## 設定

- prompt_days: 30  # prompt-insight ログの収集日数（デフォルト: 30）
```

ファイルが存在しない場合はデフォルト（investigate_bug・dev、prompt_days: 30）が使われます。

---

## スキル拡張ファイルでプロジェクト固有の手順を追加（任意）

`.claude/claude-plugins/skill-evolve/skill-extensions/<スキル名>.local.md` を作成すると、
スキルにプロジェクト固有の手順や観点を追加できます。
ベースの SKILL.md は変更せず、拡張内容のみローカルに管理できます。

```
~/.claude/
└── claude-plugins/
    └── skill-evolve/
        ├── skill-evolve.local.md       # 改善プロセスのカスタマイズ
        └── skill-extensions/
            ├── investigate_bug.local.md  # investigate_bug の拡張
            └── dev.local.md              # dev の拡張
```

例: `investigate_bug.local.md`

```markdown
## プロジェクト固有の調査手順

- DB のスロークエリログは `/var/log/mysql/slow.log` を確認する
- エラー発生時は Sentry のイベント ID を必ず記録する
- 本番環境のログは `kubectl logs` で取得する
```

このディレクトリ以下は `.gitignore` に登録されているため、リポジトリには含まれません。

---

## EVOLVE マーカーの追加（任意）

SKILL.md を自動改善の対象にするには、改善したいセクションに以下を追加します。
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
| `plugins/*/skills/*/SKILL.md` | 各スキルの EVOLVE セクション（**主な出力**） | `/skill-evolve` 実行時に直接編集 |
| `.claude/claude-plugins/skill-evolve/investigate-patterns.json` | 未解決の不明点パターン（中間ファイル） | `/skill-evolve` 実行時に上書き |
| `.claude/claude-plugins/skill-evolve/cross-skill-patterns.json` | 横断集計結果（中間ファイル） | `/skill-evolve` 実行時に上書き |
| `.claude/claude-plugins/skill-evolve/prompt-patterns.json` | プロンプトログ集計結果（中間ファイル） | `/skill-evolve` 実行時に上書き |

---

## よくある質問

**Q. データが蓄積されていない場合は？**
「データが不足しています」と表示してスキップします。`investigate_bug` や `dev` スキルを使い続けることでデータが蓄積されます。

**Q. prompt-insight を使っていない場合は？**
`~/.prompt-insight/logs/` が存在しない場合は自動的にスキップします。セットアップは `/prompt-insight setup` で行えます。

**Q. 自動 commit を止めたい場合は？**
`/skill-evolve` 実行後に変更内容の確認を求めるので、その時点で断ることができます。
