# shshimamo-plugins

Claude Code plugins by shshimamo

## インストール

### マーケットプレイス登録（初回のみ）

```
/plugin marketplace add shshimamo/claude-plugins
```

### プラグインインストール

```
/plugin install <plugin-name>@shshimamo-plugins
```

---

## プラグイン一覧

### todo

日々のTodo管理スキル。登録・完了・現状確認ができる。

```
/plugin install todo@shshimamo-plugins
```

| コマンド | 説明 |
|---------|------|
| `/todo` | 一覧表示・提案 |
| `/todo add タスク名` | タスク追加 |
| `/todo done: 1` | タスク完了 |
| `/todo rm: 1` | タスクをゴミ箱へ |
| `/todo memo add: 1 内容` | メモ追加 |

---

### review

カスタムルールを加えたコードレビュースキル。プロジェクト固有・共通のレビュー観点をmdで管理し育てていける。

```
/plugin install review@shshimamo-plugins
```

| コマンド | 説明 |
|---------|------|
| `/review-custom` | カスタムルールでコードレビュー |
| `/review-update` | レビュールールを更新 |

---

### checkpoint

セッションの作業状況をタスクごとにファイル保存し、次のセッションで再開できる。セッションが途切れやすい環境で有効。

```
/plugin install checkpoint@shshimamo-plugins
```

| コマンド | 説明 |
|---------|------|
| `/checkpoint` | 現在の作業状況を保存 |
| `/checkpoint resume` | 過去のチェックポイントから再開 |

保存先: `~/.checkpoint/<task-name>/yyyymmddhhmm.md`

---

### prompt-insight

プロンプトログを自動収集・分析し、繰り返しパターンをスキル化・CLAUDE.md化する提案を行う。

```
/plugin install prompt-insight@shshimamo-plugins
```

**セットアップ（初回のみ）**

```
/prompt-insight setup
```

`UserPromptSubmit` フックを自動設定し、以降のプロンプトを `~/.prompt-insight/logs/` に記録する。

手動でセットアップする場合:

```bash
# ログディレクトリ作成
mkdir -p ~/.prompt-insight/logs

# hook.sh をコピー（プラグインキャッシュのパスは適宜調整）
cp ~/.claude/plugins/cache/shshimamo-plugins/prompt-insight/<hash>/hooks/prompt-logger.sh ~/.prompt-insight/hook.sh
chmod +x ~/.prompt-insight/hook.sh
```

`~/.claude/settings.json`（または `settings.local.json`）に以下を追加:

```json
"hooks": {
  "UserPromptSubmit": [
    {
      "matcher": "",
      "hooks": [
        {
          "type": "command",
          "command": "bash ~/.prompt-insight/hook.sh"
        }
      ]
    }
  ]
}
```

| コマンド | 説明 |
|---------|------|
| `/prompt-insight setup` | フック設定・初期化 |
| `/prompt-insight` | パターン分析・改善提案 |

分析結果例:
```
1. 「commit + PR作成」(23回) → /ship スキル化を提案
2. 「テストも書いて」(12回)  → CLAUDE.md 追記を提案
```
