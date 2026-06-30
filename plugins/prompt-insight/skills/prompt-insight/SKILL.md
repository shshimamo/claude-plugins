---
name: prompt-insight
description: プロンプトログの分析。「/prompt-insight setup」で初期設定、「/prompt-insight」でパターン分析と改善提案。ユーザーが繰り返し指示のパターン確認・スキル化・CLAUDE.md追記を指示したときに使う。
version: 1.0.0
---

# Prompt Insight スキル

ログ保存先: `~/.claude-plugins/prompt-insight/logs/YYYY-MM-DD.jsonl`
フックスクリプト: `~/.claude-plugins/prompt-insight/hook.sh`

## 呼び出しパターン

### `setup`

以下の手順で初期設定を行う。

**1. ディレクトリ作成**

Bash で `mkdir -p ~/.claude-plugins/prompt-insight/logs` を実行する。

**2. フックスクリプトのコピー**

スキルのベースディレクトリから2階層上がったプラグインルートに `hooks/prompt-logger.sh` がある。
これを `~/.claude-plugins/prompt-insight/hook.sh` にコピーして実行権限を付与する:

~~~bash
# ベースディレクトリ（例: ~/.claude/plugins/cache/shshimamo-plugins/prompt-insight/<hash>/skills/prompt-insight）
# プラグインルートは2階層上
PLUGIN_ROOT="$(dirname "$(dirname "$BASE_DIR")")"
cp "$PLUGIN_ROOT/hooks/prompt-logger.sh" ~/.claude-plugins/prompt-insight/hook.sh
chmod +x ~/.claude-plugins/prompt-insight/hook.sh
~~~

`$BASE_DIR` はスキル呼び出し時に提供されるベースディレクトリのパスを使うこと。

**3. `~/.claude/settings.json` にフック追加**

以下の手順で設定する:

1. `~/.claude/settings.json` を読み込む（存在しない場合は `{}` として扱う）
2. `jq` を使って `hooks.UserPromptSubmit` 配列に以下のエントリを追加する:

~~~json
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "bash ~/.claude-plugins/prompt-insight/hook.sh"
    }
  ]
}
~~~

jq コマンド例（既存エントリを保持しつつ追加）:

~~~bash
jq '.hooks.UserPromptSubmit += [{"matcher": "", "hooks": [{"type": "command", "command": "bash ~/.claude-plugins/prompt-insight/hook.sh"}]}]' \
  ~/.claude/settings.json > /tmp/settings_tmp.json && mv /tmp/settings_tmp.json ~/.claude/settings.json
~~~

settings.json が存在しない場合:

~~~bash
echo '{"hooks":{"UserPromptSubmit":[{"matcher":"","hooks":[{"type":"command","command":"bash ~/.claude-plugins/prompt-insight/hook.sh"}]}]}}' \
  > ~/.claude/settings.json
~~~

**4. 完了報告**

設定後、`~/.claude/settings.json` の `hooks` セクションを表示して確認を促す。

---

### 引数なし（`/prompt-insight`）

**ステップ1: ログ読み込み**

Bash で以下を実行してログを取得する:

~~~bash
ls ~/.claude-plugins/prompt-insight/logs/*.jsonl 2>/dev/null
~~~

ファイルが存在しない場合は以下を伝えて終了:
「ログがまだありません。先に `/prompt-insight setup` を実行してください。」

存在する場合は全ファイルを結合して読み込む:

~~~bash
cat ~/.claude-plugins/prompt-insight/logs/*.jsonl
~~~

**ステップ2: 統計情報の把握**

- 分析対象期間（最初〜最後の日付）
- 総プロンプト数
- ファイル数（日数）

**ステップ3: パターン分析**

全プロンプトを分析し、以下の観点で繰り返しパターンを特定する:

- 言い回しが違っても**同じ意図・目的**であれば同一パターンと判定する
- 例: 「コミットしてPRも作って」「commit + PR作成お願い」「pushしてPR出して」→ 同一パターン
- 例: 「テストも書いて」「テストコードも追加して」「ユニットテストも」→ 同一パターン

**ステップ4: レポート出力**

3回以上繰り返されたパターンを回数の多い順に表示する:

~~~
## Prompt Insight レポート
分析期間: YYYY-MM-DD 〜 YYYY-MM-DD（N日間）
総プロンプト数: N件

### 繰り返しパターン（3回以上）

1. 「commit + PR作成」(23回)
   例: "コミットしてPRも作って"
   提案: `/ship` スキル化

2. 「テストも書いて」(12回)
   例: "テストコードも追加して"
   提案: CLAUDE.md に追記

3. 「日本語でコメント」(8回)
   例: "コメントは日本語で書いて"
   提案: CLAUDE.md に追記

---
対応しますか？番号を指定してください（複数可: "1 2"）。
~~~

パターンが3回未満のものしかない場合は「まだ繰り返しパターンは検出されていません」と伝える。

**ステップ5: 対応**

ユーザーが番号を指定した場合、提案アクションを実行する:

- **スキル化** → 対象プロジェクトの `.claude/skills/` にSKILL.mdの雛形を作成し、内容を提示する
- **CLAUDE.md 追記** → 現在のプロジェクトの CLAUDE.md（なければ `~/.claude/CLAUDE.md`）に適切な形で追記する
