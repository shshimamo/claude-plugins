---
name: investigate_code
description: コードリーディング・機能理解を支援するスキル。機能の構造・処理フロー・データフローをドキュメント化する。コードリーディング、機能理解、アーキテクチャ調査、仕様把握などに使う。「/investigate_code」または「この機能を理解したい」「コードを読んで」「処理の流れを教えて」で起動する。
version: 1.0.0
---

# Investigate Code スキル

保存先: `~/.investigate/<project-name>/<investigation-name>/`

```
~/.investigate/<project>/
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
