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

| コマンド | 説明 |
|---------|------|
| `/prompt-insight setup` | フック設定・初期化 |
| `/prompt-insight` | パターン分析・改善提案 |

分析結果例:
```
1. 「commit + PR作成」(23回) → /ship スキル化を提案
2. 「テストも書いて」(12回)  → CLAUDE.md 追記を提案
```
