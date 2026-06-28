# Investigation Summary - fix-exec-error-msg

## 仕様の理解

`/dev exec` 実行時に、選択されたフィーチャーの `tasks.md` が存在しない場合、エラーメッセージが不明瞭でユーザーが何をすべきか分からなくなる。

現状の SKILL.md では `/dev exec` のステップ1（計画の読み込み）で `tasks.md` を読み込む処理が記述されているが、ファイルが存在しない場合のエラーハンドリング・メッセージが定義されていない。

修正方針: `tasks.md` が存在しない場合に明確なエラーメッセージ（原因・対処法）を表示するよう SKILL.md の `/dev exec` フローに追記する。

## 関連ファイル

- `/Users/shshimamo/devel/src/github.com/shshimamo/claude-plugins/plugins/dev/skills/dev/SKILL.md`: devスキルの定義ファイル。`/dev exec` のフローが記述されている（ステップ1〜4）
- `/Users/shshimamo/devel/src/github.com/shshimamo/claude-plugins/plugins/dev/skills/dev/evals/evals.json`: eval定義（このバグを再現するテストケース含む）

## 影響範囲

| ファイル | 変更内容 |
|---------|---------|
| `plugins/dev/skills/dev/SKILL.md` | `/dev exec` ステップ1に `tasks.md` 不在時のエラーハンドリングを追記 |

## 不明点・リスク

| # | 内容 | 影響 | 状態 |
|---|------|------|------|
| 1 | tasks.md が存在しない原因は `/dev plan` 未実行か途中終了が想定されるが、他のケースがあるか | 低 | 解決済 |
| 2 | plan.md も存在しない場合の挙動も同様に不明瞭な可能性がある | 低 | 未解決 |
