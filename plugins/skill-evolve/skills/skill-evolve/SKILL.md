---
name: skill-evolve
description: |
  蓄積された使用データをもとにスキルを自動改善する。
  ユーザーが「/skill-evolve」「スキルを改善して」「skill evolve 実行」などと言ったときに使う。
  ~/.investigate/ の未解決パターンから investigate_bug スキルを改善し、
  ~/.dev/ の保留タスクから dev スキルを改善する。
---

# skill-evolve

`~/.investigate/` と `~/.dev/` に蓄積されたデータを分析し、スキルを直接改善する。

## 手順

### 1. 対象スキルをユーザーに確認

まず以下を聞く:

> どのスキルを改善しますか？
> 1. investigate_bug（調査スキル）
> 2. dev（開発スキル）
> 3. 両方

選択に応じて以降の手順を実行する。

### 2. claude-plugins のルートパスを特定

この SKILL.md のパスは `plugins/skill-evolve/skills/skill-evolve/SKILL.md`。
4階層上がったディレクトリが claude-plugins のルート。

環境変数 `CLAUDE_PLUGINS_DIR` が設定されている場合はそちらを優先する。

### 3. データ収集スクリプトを実行

claude-plugins ルートをカレントディレクトリにして、選択されたスキルに応じて実行する。

- investigate_bug を選んだ場合:
  ```bash
  cd <claude-plugins-root>
  python3 plugins/skill-evolve/scripts/collect_investigate.py
  ```
- dev を選んだ場合:
  ```bash
  cd <claude-plugins-root>
  python3 plugins/skill-evolve/scripts/collect_cross_skill.py
  ```
- 両方の場合は両方実行する。

### 4. 収集データを読み込む

- investigate_bug 対象: `.claude/skill-evolve/investigate-patterns.json`
- dev 対象: `.claude/skill-evolve/cross-skill-patterns.json`

`items` や `stalled_tasks` が空なら「データが不足しています」と伝えてスキップ。

### 5. パターンを分析して SKILL.md を直接更新

#### investigate_bug の改善

`investigate-patterns.json` の未解決パターンをもとに、
`plugins/investigate/skills/investigate_bug/SKILL.md` の EVOLVE セクションを更新する。

追加する観点の基準:
- 「未解決」のまま繰り返し登場している不明点に対応するヒアリング項目やガードレール
- 既存の項目と重複しないもののみ

#### dev の改善

`cross-skill-patterns.json` の保留・ブロックタスクパターンをもとに、
`plugins/dev/skills/dev/SKILL.md` の EVOLVE セクションを更新する。

追加する観点の基準:
- 繰り返しブロックされているタスクに対応する計画・実行フェーズのチェック項目
- 既存の項目と重複しないもののみ

#### EVOLVE セクションの書き方

SKILL.md に `<!-- EVOLVE:START -->` / `<!-- EVOLVE:END -->` マーカーがある場合のみ更新する。
マーカーがない SKILL.md は変更しない。

```markdown
<!-- EVOLVE:START -->
<!-- updated: 2025-01-01 -->
- 追加した観点
- 追加した観点
<!-- EVOLVE:END -->
```

### 6. 変更内容をユーザーに確認してから commit

編集した内容（どのファイルの何を変えたか）を要約して見せる。
ユーザーが OK したら commit する:

```bash
git add plugins/investigate/skills/ plugins/dev/skills/ .claude/skill-evolve/
git commit -m "skill-evolve: auto-improve skills [$(date +%Y-%m-%d)]"
```

変更がなければ「改善すべきパターンが見つかりませんでした」と伝えて終了。

## EVOLVE マーカーの追加方法

自動改善の対象にしたい SKILL.md のセクションに以下を追加する:

```markdown
## ガードレール
<!-- EVOLVE:START -->
<!-- EVOLVE:END -->
```

マーカー内の内容は毎回上書きされる（手動で書いた内容はマーカーの外に書くこと）。
