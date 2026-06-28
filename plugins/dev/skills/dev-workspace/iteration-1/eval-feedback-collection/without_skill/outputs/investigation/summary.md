# Investigation Summary - feedback-collection

## 仕様の理解

プラグイン使用後にユーザーが簡単にフィードバックを送れる新機能。
Claude Code の `/plugin` エコシステム上に乗る形で、`/feedback` コマンドとして提供する。
フィードバックは評価（星・絵文字など）＋任意コメントをローカルファイルに保存し、将来的な集計・エクスポートも想定する。

## 関連ファイル

- `README.md`: プラグイン一覧・インストール方法の全体像
- `plugins/todo/.claude-plugin/plugin.json`: plugin.json のフォーマット基準
- `plugins/todo/skills/todo/SKILL.md`: SKILL.md の書き方（コマンドパターン・ファイル管理）
- `plugins/checkpoint/.claude-plugin/plugin.json`: シンプルなプラグイン定義の例
- `plugins/checkpoint/skills/checkpoint/SKILL.md`: ファイル保存・読み込みパターンの参考
- `plugins/review/skills/review-custom/SKILL.md`: ステップ構造・出力フォーマットの参考
- `plugins/prompt-insight/hooks/prompt-logger.sh`: フックスクリプトの実装例
- `plugins/prompt-insight/.claude-plugin/plugin.json`: フック連携プラグインの定義例
- `plugins/dev/skills/dev/SKILL.md`: plan.md / tasks.md の生成フォーマット基準

## 影響範囲

新規プラグインとして追加するため、既存プラグインへの変更は不要。
以下を新規作成する:

- `plugins/feedback/.claude-plugin/plugin.json`
- `plugins/feedback/skills/feedback/SKILL.md`
- `plugins/feedback/hooks/feedback-submitter.sh`（任意: PostToolUse フック経由で自動プロンプト）
- `README.md` への追記（既存ファイルへの変更あり）

## 不明点・リスク

| # | 内容 | 影響 | 状態 |
|---|------|------|------|
| 1 | フィードバックの送信先（ローカル保存のみ vs 外部サービス連携） | 高 | 未解決 |
| 2 | 評価形式（星5段階 / 絵文字 / Good-Bad のみ） | 中 | 未解決 |
| 3 | どのタイミングで促すか（コマンド手動呼び出し vs セッション終了時自動） | 中 | 未解決 |
| 4 | フィードバック一覧の閲覧・集計機能をどこまでスコープに含めるか | 低 | 未解決 |
