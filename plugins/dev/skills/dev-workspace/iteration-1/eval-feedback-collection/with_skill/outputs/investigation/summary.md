# Investigation Summary - feedback-collection

## 仕様の理解

プラグインを使用した後にユーザーが簡単にフィードバックを送れる機能を追加する。
具体的には、各プラグインのスキル実行後に評価（★/👍/👎 など）とコメントを送信できるコマンド `/feedback` を新規プラグインとして追加する。
フィードバックはローカルファイルに蓄積し、集計・閲覧もできる。

## 関連ファイル

- `.claude-plugin/marketplace.json`: マーケットプレイス全体の設定。新プラグインのエントリを追加する場所
- `plugins/todo/.claude-plugin/plugin.json`: plugin.json の構造例（name / description / author）
- `plugins/todo/skills/todo/SKILL.md`: スキルファイルの構造例。フロントマター（name / description / version）+ 呼び出しパターン定義
- `plugins/checkpoint/skills/checkpoint/SKILL.md`: ファイル保存パターンの参考実装（`~/.checkpoint/` への保存）
- `plugins/dev/skills/dev/SKILL.md`: 複数コマンドパターン（plan / exec）の参考実装
- `README.md`: プラグイン一覧とインストール手順のドキュメント

## 影響範囲

| ファイル | 変更種別 | 理由 |
|---------|---------|------|
| `.claude-plugin/marketplace.json` | 変更 | feedback プラグインのエントリ追加 |
| `plugins/feedback/.claude-plugin/plugin.json` | 新規作成 | プラグイン定義 |
| `plugins/feedback/skills/feedback/SKILL.md` | 新規作成 | フィードバックスキルの実装 |
| `README.md` | 変更 | feedback プラグインの説明追加 |

## 不明点・リスク

| # | 内容 | 影響 | 状態 |
|---|------|------|------|
| 1 | フィードバックの送信先がローカルファイルのみか、外部APIにも送るかが未定 | 中 | 解決済（ローカルのみとする） |
| 2 | どのプラグインを使ったかの識別をどう行うか（手動入力 or 自動検知） | 中 | 解決済（手動指定 or 省略可能にする） |
| 3 | フィードバックの形式（評価スコア + テキスト か テキストのみか） | 低 | 解決済（★1-5 + 任意コメントとする） |
