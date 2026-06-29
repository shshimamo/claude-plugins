---
name: skill-evolve
description: |
  蓄積された使用データをもとにスキルを自動改善する。
  ユーザーが「/skill-evolve」「スキルを改善して」「skill evolve 実行」などと言ったときに使う。
  ~/.investigate/ の未解決パターンから investigate_bug スキルを改善し、
  ~/.dev/ の保留タスクから dev スキルを改善する。
  ~/.investigate/code/ のドメイン知識から investigate_code のスキル拡張ファイルを更新する。
---

# skill-evolve

`~/.investigate/` と `~/.dev/` に蓄積されたデータ、および `~/.prompt-insight/` のプロンプトログを分析し、スキルを直接改善する。

## 手順

### 1. ローカル設定ファイルを確認

`.claude/claude-plugins/skill-evolve/skill-evolve.local.md` が存在する場合はそこに定義されたターゲットと設定を使う。
存在しない場合はデフォルトターゲット（investigate_bug・investigate_code・dev）と設定を使う。

ローカル設定ファイルのフォーマット:

```markdown
## ターゲット

### investigate_bug
- データソース: investigate_bug
- SKILL.md: plugins/investigate/skills/investigate_bug/SKILL.md
- 改善観点: ヒアリング項目・ガードレール

### my-custom-skill
- データソース: investigate
- SKILL.md: plugins/my-plugin/skills/my-skill/SKILL.md
- 改善観点: （自由記述）

## 設定

- prompt_days: 30  # prompt-insight ログの収集日数（デフォルト: 30）
```

設定を読み込んだら、対象スキルの一覧をユーザーに見せてから確認する:

> 以下のスキルを改善します。よろしいですか？
> 1. investigate_bug
> 2. investigate_code
> 3. dev
>
> 個別に選択する場合は番号を指定してください。

### 2. claude-plugins のルートパスを特定

この SKILL.md のパスは `plugins/skill-evolve/skills/skill-evolve/SKILL.md`。
4階層上がったディレクトリが claude-plugins のルート。

環境変数 `CLAUDE_PLUGINS_DIR` が設定されている場合はそちらを優先する。

### 3. カレントプロジェクトの repo-know を読み込む

`git remote get-url origin`（失敗した場合は `basename $(pwd)`）でカレントプロジェクト名を取得し、
`~/.repo-know/<project-name>/` の各ファイルを読み込む（存在しない場合はスキップ）。
読み込んだ内容をスキル改善の参考コンテキストとして活用する。

### 4. データ収集スクリプトを実行

claude-plugins ルートをカレントディレクトリにして、選択されたスキルに応じて実行する。

- investigate_bug を選んだ場合:
  ```bash
  cd <claude-plugins-root>
  python3 plugins/skill-evolve/scripts/collect_investigate.py
  ```
- investigate_code を選んだ場合:
  ```bash
  cd <claude-plugins-root>
  python3 plugins/skill-evolve/scripts/collect_investigate_code.py
  ```
- dev を選んだ場合:
  ```bash
  cd <claude-plugins-root>
  python3 plugins/skill-evolve/scripts/collect_cross_skill.py
  ```

### 5. prompt-insight ログを収集

`local.md` の `prompt_days` 設定（デフォルト: 30）を使って実行する:

```bash
cd <claude-plugins-root>
python3 plugins/skill-evolve/scripts/collect_prompt_insight.py <prompt_days>
```

`~/.prompt-insight/logs/` が存在しない場合はスキップ（エラーにしない）。

### 6. 収集データを読み込む

- investigate_bug 対象: `.claude/claude-plugins/skill-evolve/investigate-patterns.json`
- investigate_code 対象: `.claude/claude-plugins/skill-evolve/investigate-code-patterns.json`
- dev 対象: `.claude/claude-plugins/skill-evolve/cross-skill-patterns.json`
- 全ターゲット共通: `.claude/claude-plugins/skill-evolve/prompt-patterns.json`（存在する場合）

`items` や `stalled_tasks` が空なら「データが不足しています」と伝えてスキップ。

### 7. パターンを分析してスキルを更新

ターゲットによって更新方法が異なる。

#### investigate_bug / dev: SKILL.md の EVOLVE セクションを更新

各ターゲットについて、以下のデータをすべて合わせて SKILL.md の EVOLVE セクションを更新する:

- 収集データ（investigate / cross-skill）
- prompt-insight ログ（繰り返し追加指示されているパターン）

**データソースと改善観点の対応（デフォルト）:**

| ターゲット | データソース | 収集データ | 改善観点 |
|-----------|------------|----------|---------|
| investigate_bug | investigate/bug | 未解決の不明点パターン | ヒアリング項目・ガードレール |
| dev | dev + investigate/bug | 保留・ブロックタスク | 計画・実行フェーズのチェック項目 |

prompt-insight ログからは「スキル実行後にユーザーが繰り返し追加指示していること」を抽出し、
「最初から実行すべきだった行動」として EVOLVE セクションに反映する。

SKILL.md に `<!-- EVOLVE:START -->` / `<!-- EVOLVE:END -->` マーカーがある場合のみ更新する。
マーカーがない SKILL.md は変更しない。

```markdown
<!-- EVOLVE:START -->
<!-- updated: 2025-01-01 -->
- 追加した観点
<!-- EVOLVE:END -->
```

#### investigate_code: スキル拡張ファイルをプロジェクトごとに更新

`investigate-code-patterns.json` の各プロジェクトについて、
以下のパスのスキル拡張ファイルを更新する（なければ新規作成）:

```
~/.claude/claude-plugins/skill-evolve/skill-extensions/<project>/investigate_code.local.md
```

ディレクトリが存在しない場合は `mkdir -p` で作成する。

更新内容は `~/.repo-know/<project>/` と `summary.md` から抽出した以下の情報:
- アーキテクチャ・調査の起点
- ドメイン用語・注意点
- 繰り返し調査されている領域

`skill-evolve.local.md` でカスタムターゲットが定義されている場合は、そこに記載された「改善観点」をプロンプトとして使う。

共通の基準:
- 繰り返し登場しているパターンのみ対象
- 既存の項目と重複しないもののみ追加

### 8. 変更内容をユーザーに確認してから commit

編集した内容（どのファイルの何を変えたか）を要約して見せる。

**リポジトリに commit する変更**（investigate_bug / dev の EVOLVE セクション）:
```bash
git add plugins/investigate/skills/ plugins/dev/skills/
git commit -m "skill-evolve: auto-improve skills [$(date +%Y-%m-%d)]"
```

**ローカルのみの変更**（investigate_code のスキル拡張ファイル）:
`~/.claude/claude-plugins/skill-evolve/skill-extensions/` は gitignore 済みのためコミット不要。更新完了を伝えるだけ。

変更がなければ「改善すべきパターンが見つかりませんでした」と伝えて終了。

### 9. repo-know の更新

スキル改善を通じて判明した新しいプロジェクト知識を `~/.repo-know/<project-name>/` に保存する。

収集データ・改善パターンを振り返り、以下の観点で知識を抽出する:
- **tech**: 調査パターンから判明した技術スタック・アーキテクチャの傾向
- **domain**: 繰り返し登場するビジネスルール・ドメイン用語
- **decisions**: 繰り返し採用されている設計判断・修正方針

既存ファイルと重複しないもののみ候補として提示し、ユーザー確認後に追記する。
候補がない場合はスキップ。

## EVOLVE マーカーの追加方法

自動改善の対象にしたい SKILL.md のセクションに以下を追加する:

```markdown
## ガードレール
<!-- EVOLVE:START -->
<!-- EVOLVE:END -->
```

マーカー内の内容は毎回上書きされる（手動で書いた内容はマーカーの外に書くこと）。
