#!/usr/bin/env python3
"""
Case 1: 収集した PR レビューコメントを Claude API で分析し、
.claude/skill-evolve/review-patterns.md を更新する

GitHub Actions から実行される。
collect_review_comments.py の後に実行すること。

入力:
  .claude/skill-evolve/raw-comments.json（前スクリプトの出力）

出力:
  .claude/skill-evolve/review-patterns.md
  → review-custom スキルがコードレビュー時に読み込む
"""
import json
import os
import sys
from datetime import date
from pathlib import Path

import anthropic

raw_path = Path('.claude/skill-evolve/raw-comments.json')
patterns_path = Path('.claude/skill-evolve/review-patterns.md')

# 前スクリプトの出力が存在するか確認
if not raw_path.exists():
    print("No raw-comments.json found. Run collect_review_comments.py first.", file=sys.stderr)
    sys.exit(1)

with open(raw_path) as f:
    comments = json.load(f)

if not comments:
    print("No comments to analyze")
    sys.exit(0)

# 既存のパターンファイルを読み込む（初回は空文字になる）
existing_patterns = patterns_path.read_text(encoding='utf-8') if patterns_path.exists() else ""

# Claude に渡すためにコメントをテキスト形式に変換
# 例: "- [app/models/user.rb] メソッドが長すぎます"
comments_text = "\n".join([f"- [{c.get('path', '?')}] {c['body']}" for c in comments])
today = date.today().isoformat()

client = anthropic.Anthropic()

# Claude に分析を依頼するプロンプト
# 既存パターンとの重複を除外し、繰り返しパターンのみ抽出するよう指示
response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=2048,
    messages=[{
        "role": "user",
        "content": f"""以下はこのプロジェクトの過去のPRレビューコメントです:

{comments_text}

これらを分析し、繰り返し指摘されているパターンやプロジェクト固有の重要なレビュー観点を抽出してください。

既存パターンファイル:
{existing_patterns if existing_patterns else "（まだありません）"}

以下のルール:
- 既存パターンと重複するものは出力しない
- 1回しか出てこない指摘は除外する
- ファイルパスからわかる場合はレイヤー（controller/model等）を明記する

出力形式（Markdownのみ、説明文不要）:
```
## {today}

### 頻出パターン
- （内容）

### プロジェクト固有の観点
- （内容）
```

追加すべき新しいパターンがなければ「変更なし」とだけ出力してください。
""",
    }],
)

output = response.content[0].text.strip()

if output == "変更なし":
    print("No new patterns found")
    sys.exit(0)

# Claude がコードブロック（```）で囲んで返した場合は除去する
if output.startswith("```"):
    lines = output.split("\n")
    output = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])

# 既存ファイルの末尾に追記（初回は新規作成）
updated = (existing_patterns.rstrip() + "\n\n" + output.strip() if existing_patterns else output.strip()) + "\n"
patterns_path.write_text(updated, encoding='utf-8')
print(f"Updated {patterns_path}")
