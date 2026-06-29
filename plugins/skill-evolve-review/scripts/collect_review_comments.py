#!/usr/bin/env python3
"""
Case 1: 過去N週間の PR レビューコメントを収集して JSON に保存する

GitHub Actions から実行される。
gh CLI（GitHub Actions に標準搭載）で GitHub API を叩き、
PR のインラインコメントを取得する。

入力（環境変数）:
  REPO       - リポジトリ名（例: myorg/my-app）
  WEEKS_BACK - 何週間前まで遡るか（デフォルト: 1）
  GH_TOKEN   - GitHub のアクセストークン（Actions が自動提供）

出力:
  .claude/skill-evolve/raw-comments.json
"""
import json
import os
import subprocess
import sys
from datetime import datetime, timedelta, timezone

weeks_back = int(os.environ.get('WEEKS_BACK', 1))
repo = os.environ.get('REPO', '')

if not repo:
    print("ERROR: REPO environment variable is required", file=sys.stderr)
    sys.exit(1)

# N週間前の日時を ISO 8601 形式で作成（GitHub API のフィルタに使う）
since = (datetime.now(timezone.utc) - timedelta(weeks=weeks_back)).strftime('%Y-%m-%dT%H:%M:%SZ')

print(f"Collecting PR review comments from {repo} since {since}...")

try:
    # gh api: GitHub の REST API を呼び出すコマンド
    # --paginate: コメントが多い場合に複数ページを自動取得
    # -q: jq 形式でフィルタ（指定日時以降のコメントのみ抽出）
    result = subprocess.run(
        [
            'gh', 'api',
            f'repos/{repo}/pulls/comments',
            '--paginate',
            '-q', f'[.[] | select(.created_at >= "{since}") | {{body: .body, path: .path, created_at: .created_at, pull_request_url: .pull_request_url}}]',
        ],
        capture_output=True,
        text=True,
        check=True,
        env={**os.environ, 'GH_TOKEN': os.environ.get('GH_TOKEN', '')},
    )
except subprocess.CalledProcessError as e:
    print(f"ERROR: gh command failed: {e.stderr}", file=sys.stderr)
    sys.exit(1)

# --paginate を使うと複数の JSON 配列が連結されて返ることがある（[[...][...]] 形式）
# そのためフラット化して1つの配列にまとめる
raw = result.stdout.strip()
if raw.startswith('[['):
    import re
    arrays = re.findall(r'\[.*?\]', raw, re.DOTALL)
    comments = []
    for a in arrays:
        try:
            comments.extend(json.loads(a))
        except json.JSONDecodeError:
            pass
else:
    comments = json.loads(raw or '[]')

# 次のスクリプト（improve_review_patterns.py）が読み込む中間ファイルとして保存
os.makedirs('.claude/skill-evolve', exist_ok=True)
with open('.claude/skill-evolve/raw-comments.json', 'w') as f:
    json.dump(comments, f, ensure_ascii=False, indent=2)

print(f"Collected {len(comments)} review comments")
