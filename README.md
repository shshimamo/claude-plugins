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

### dev

仕様をもとにコードを調査・計画・実行する開発スキル。計画と実行の2コマンド構成。

```
/plugin install dev@shshimamo-plugins
```

| コマンド | 説明 |
|---------|------|
| `/dev plan <仕様>` | コード調査・計画立案・アウトプット生成 |
| `/dev exec` | 計画に従って実装を実行 |

**`/dev plan` の流れ:**
1. タスク種別を判断（new / feature / bugfix / refactor）
2. 既存コードを調査（Grep + 参照追跡で芋づる式に理解）
3. 調査結果を `investigation.md` に記録
4. 仕様と調査結果をもとに計画を精緻化
5. スコープに応じてシーケンス図・DB設計・タスクリストを生成

保存先: `~/.dev/<project-name>/<feature-name>/`

---

### repo-know

会話からプロジェクトの技術・ドメイン知識を抽出して蓄積する。セッションをまたいで知識を育てていける。

```
/plugin install repo-know@shshimamo-plugins
```

| コマンド | 説明 |
|---------|------|
| `/repo-know` | 会話から知識を抽出・保存 |
| `/repo-know show` | 蓄積された知識を表示 |

保存先: `~/.repo-know/<project-name>/`（tech.md / domain.md / decisions.md）

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
