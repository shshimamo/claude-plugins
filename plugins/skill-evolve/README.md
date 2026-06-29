# skill-evolve

`~/.investigate/` や `~/.dev/` に蓄積されたデータを分析し、スキルを改善する `/skill-evolve` コマンドを提供します。

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
│       └── SKILL.md             # /skill-evolve コマンド本体
└── scripts/
    ├── collect_investigate.py   # Case 2: ~/.investigate/ の未解決パターンを集計
    └── collect_cross_skill.py   # Case 3: investigate + dev を横断集計
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

`.claude/skill-evolve/skill-evolve.local.md` を作成すると、改善対象スキルを環境ごとにカスタマイズできます。
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
```

ファイルが存在しない場合はデフォルト（investigate_bug・dev）が使われます。

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

## 生成されるファイル

| ファイル | 内容 | 更新方法 |
|---------|------|---------|
| `.claude/skill-evolve/investigate-patterns.json` | 未解決の不明点パターン（中間ファイル） | `/skill-evolve` 実行時に上書き |
| `.claude/skill-evolve/cross-skill-patterns.json` | 横断集計結果（中間ファイル） | `/skill-evolve` 実行時に上書き |

---

## よくある質問

**Q. データが蓄積されていない場合は？**
「データが不足しています」と表示してスキップします。`investigate_bug` や `dev` スキルを使い続けることでデータが蓄積されます。

**Q. 自動 commit を止めたい場合は？**
`/skill-evolve` 実行後に変更内容の確認を求めるので、その時点で断ることができます。
