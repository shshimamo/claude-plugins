# prompt-insight

プロンプトログを自動収集・分析し、繰り返しパターンをスキル化・CLAUDE.md化する提案を行う。

## セットアップ（必須）

ログを収集するには `UserPromptSubmit` フックを有効にする必要がある。
**セットアップをしないとログが記録されない。**

---

### 方法A: `/prompt-insight setup` で自動設定（推奨）

Claude に話しかけるだけで設定が完了する:

```
/prompt-insight setup
```

以下を自動で行う:
1. `~/.claude-plugins/prompt-insight/logs/` ディレクトリを作成
2. フックスクリプトを `~/.claude-plugins/prompt-insight/hook.sh` にコピー
3. `~/.claude/settings.json` にフックを登録

---

### 方法B: 手動設定

#### 1. ディレクトリ作成

```bash
mkdir -p ~/.claude-plugins/prompt-insight/logs
```

#### 2. フックスクリプトのコピー

このリポジトリのフックスクリプトを所定の場所にコピーして実行権限を付与する:

```bash
cp <このリポジトリのパス>/plugins/prompt-insight/hooks/prompt-logger.sh \
   ~/.claude-plugins/prompt-insight/hook.sh
chmod +x ~/.claude-plugins/prompt-insight/hook.sh
```

#### 3. `~/.claude/settings.json` にフックを追加

**settings.json が存在する場合:**

```bash
jq '.hooks.UserPromptSubmit += [{"matcher": "", "hooks": [{"type": "command", "command": "bash ~/.claude-plugins/prompt-insight/hook.sh"}]}]' \
  ~/.claude/settings.json > /tmp/settings_tmp.json && mv /tmp/settings_tmp.json ~/.claude/settings.json
```

**settings.json が存在しない場合:**

```bash
echo '{"hooks":{"UserPromptSubmit":[{"matcher":"","hooks":[{"type":"command","command":"bash ~/.claude-plugins/prompt-insight/hook.sh"}]}]}}' \
  > ~/.claude/settings.json
```

#### 4. 確認

```bash
cat ~/.claude/settings.json
```

`hooks.UserPromptSubmit` に以下のエントリが含まれていれば設定完了:

```json
{
  "matcher": "",
  "hooks": [
    {
      "type": "command",
      "command": "bash ~/.claude-plugins/prompt-insight/hook.sh"
    }
  ]
}
```

---

## 使い方

セットアップ後、Claude に話しかけるだけでログが蓄積される。
一定期間たったら `/prompt-insight` で分析を実行する:

```
/prompt-insight
```

繰り返しパターンを検出し、スキル化・CLAUDE.md追記の提案を行う。

---

## ファイル構成

```
plugins/prompt-insight/
├── README.md（このファイル）
├── .claude-plugin/
│   └── plugin.json
├── hooks/
│   └── prompt-logger.sh    # UserPromptSubmit フックスクリプト
└── skills/
    └── prompt-insight/
        └── SKILL.md        # /prompt-insight コマンド本体
```

ログの保存先:

```
~/.claude-plugins/prompt-insight/
├── logs/
│   ├── 2026-01-01.jsonl
│   └── 2026-01-02.jsonl
└── hook.sh                 # setup でコピーされるフックスクリプト
```
