---
name: investigate_code
description: コードリーディング・機能理解を支援するスキル。機能の構造・処理フロー・データフローをドキュメント化する。コードリーディング、機能理解、アーキテクチャ調査、仕様把握などに使う。「/investigate_code」または「この機能を理解したい」「コードを読んで」「処理の流れを教えて」で起動する。
version: 1.0.0
---

# Investigate Code スキル

保存先: `~/.claude-plugins/investigate/code/<project-name>/<investigation-name>/`

```
~/.claude-plugins/investigate/code/<project>/
└── <investigation-name>/
    ├── investigation/
    │   └── summary.md        # 調査サマリー・関連ファイル・全体像
    └── artifacts/
        ├── structure.md      # コード構造の説明
        ├── sequence.md       # シーケンス図（Mermaid）
        ├── components.md     # コンポーネント依存関係図（Mermaid）
        └── data_flow.md      # データフロー説明
```

---

## ガードレール

調査の信頼性を保つために以下を必ず守る:

- **推測禁止**: コードを読んで確認した事実のみを記録する。未検証の内容は「仮説:」と明記する
- **パス記録**: 調査した経路・確認したファイルは必ず記録する（同じ道を二度辿らないため）
- **3回失敗で停止**: エントリーポイントが見つからないなど同じ方向で3回詰まったらユーザーに報告して指示を待つ

---

## ステップ0: 対象リポジトリの確認とコンテキスト読み込み

`git remote get-url origin`（失敗した場合は `basename $(pwd)`）でプロジェクト名を自動取得し、ユーザーに確認する:

> 対象リポジトリ: `<自動取得したプロジェクト名>`
> このリポジトリで合っていますか？（違う場合は正しい名前を教えてください）

確定したプロジェクト名を以降のすべての操作（調査ログの保存先・skill-extensions・repo-know の読み書き）で使う。

プロジェクト名が確定したら以下を読み込む（存在しない場合はスキップ）:

- `~/.claude-plugins/skill-evolve/skill-extensions/<project>/investigate_code.local.md`（調査の優先順位・注意点）
- `~/.claude-plugins/repo-know/<project>/` の各ファイル（アーキテクチャ・ドメイン知識・設計判断）

読み込んだ内容を以降のステップで追加コンテキストとして活用する。

---

## ステップ1: ヒアリング

**質問1: 調査対象**
```
どの機能・処理を理解したいですか？
```

**質問2: 関連ファイル**
```
関連するファイルやディレクトリはわかりますか？（わからなければスキップOK）
```

関連ファイルがわかっている場合はそこから調査を開始する。わからない場合は Grep・Glob で探す。

**質問3: 関連リポジトリ**
```
関連するリポジトリはありますか？（複数ある場合はすべて教えてください）
```

**質問4: 関連リンク**
```
関連する URL・ドキュメント・チケットはありますか？（Confluenceページ、Asanaタスク、GitHubのIssue/PRなど）
```

リンクが提供された場合は以下の方針でアクセスする:

| サービス | アクセス方法 |
|---------|------------|
| GitHub（github.com） | `gh` コマンドで Issue / PR / コードを取得 |
| Confluence | MCP を使用して検索・取得 |
| Asana | MCP を使用してタスク情報を取得 |
| Grafana | MCP を使用してダッシュボード・クエリを取得 |
| Sentry | MCP を使用してエラー詳細・スタックトレースを取得 |
| その他 | 対応する MCP があれば使用。なければユーザーにアクセス方法を確認 |

## ステップ2: プロジェクト名・調査名の取得

プロジェクト名: `git remote get-url origin` からリポジトリ名を抽出。失敗した場合は `basename $(pwd)`。

調査名: 調査対象から短い名前を生成してユーザーに確認（例: `user-auth-flow`, `order-processing`）。英数字・ハイフン推奨。

## ステップ3: 並列調査

Agent ツールで以下を並列調査する:

- **エントリーポイント特定**: 機能のエントリーポイント（API エンドポイント・コマンド・イベントハンドラなど）を特定
- **処理フロー追跡**: エントリーポイントから処理を辿り、コールチェーンを記録
- **データ構造確認**: 扱うモデル・型・DB スキーマを調査
- **依存関係確認**: 外部サービス・ライブラリ・他コンポーネントとの接続を確認

## ステップ4: アウトプット生成

`investigation/summary.md` を作成する:

~~~markdown
# Investigation Summary - <investigation-name>

## 調査対象
（調査した機能・処理の概要）

## 関連ファイル
- `path/to/file`: （役割）

## 全体像
（処理の流れを一言で説明）

## 不明点・リスク

| # | 内容 | 影響 | 状態 |
|---|------|------|------|
| 1 | （不明点） | 高/中/低 | 未解決/解決済 |
~~~

`artifacts/structure.md` を作成する:

~~~markdown
# Structure - <investigation-name>

## 概要
（この機能が何をするか）

## レイヤー構成
（Controller / Service / Repository など各レイヤーの役割と対応ファイル）

## 主要なクラス・関数
（重要なクラス・関数とその責務）

## 処理の流れ
（テキストで処理ステップを説明）
~~~

`artifacts/sequence.md` を作成する（Mermaid sequenceDiagram 形式）:

~~~markdown
# Sequence - <investigation-name>

```mermaid
sequenceDiagram
    ...
```
~~~

`artifacts/components.md` を作成する（Mermaid classDiagram または graph 形式）:

~~~markdown
# Components - <investigation-name>

```mermaid
graph TD
    ...
```
~~~

`artifacts/data_flow.md` を作成する:

~~~markdown
# Data Flow - <investigation-name>

## データの流れ
（入力 → 変換 → 保存 → 出力 の流れを説明）

## 主要なデータ変換
（どこで何を変換しているか）

## データ保存先
（DB テーブル・キャッシュ・外部ストレージなど）
~~~

## ステップ5: 報告とフィードバック

作成したファイルを提示してユーザーにフィードバックを求める。
理解できなかった箇所・追加調査が必要な箇所を明示する。

---

## ステップ6: repo-know への知識保存

今回の調査で得られたプロジェクト固有の知識を `~/.claude-plugins/repo-know/<project-name>/` に保存する。

調査結果を振り返り、以下の観点で知識を抽出する:
- **tech**: アーキテクチャ・レイヤー構成・ファイル構造（例: Controller → Service → Repository の対応）
- **domain**: ドメイン固有の用語・概念・エンティティの意味（例: User.status は enum ではなく文字列定数）
- **decisions**: 注意点・落とし穴・調査のヒント（例: 認証は AuthMiddleware から入ると早い）

既存ファイルと重複しないもののみ候補として提示し、ユーザー確認後に追記する。
候補がない場合はスキップ。
