#!/usr/bin/env python3
"""
Case 2: ~/.claude-plugins/investigate/bug/ の調査ファイルを分析し、
繰り返し「未解決」になっている不明点パターンを抽出する

investigate_bug スキルが生成した summary.md を読み取り、
「不明点・リスク」テーブルの未解決行を集計する。

出力:
  .claude/claude-plugins/skill-evolve/investigate-patterns.json
"""
import json
from pathlib import Path

investigate_root = Path.home() / '.claude-plugins' / 'investigate' / 'bug'

if not investigate_root.exists():
    print("~/.claude-plugins/investigate/bug/ not found. No data to analyze.")
    exit(0)

unresolved = []

# ~/.claude-plugins/investigate/bug/<project>/<investigation-name>/investigation/summary.md を全件スキャン
for summary_path in investigate_root.glob('*/*/investigation/summary.md'):
    content = summary_path.read_text(encoding='utf-8')

    # パスの構造: ~/.claude-plugins/investigate/bug/<project>/<investigation>/investigation/summary.md
    project = summary_path.parts[-4]
    investigation = summary_path.parts[-3]

    # summary.md の「不明点・リスク」テーブルから「未解決」の行を抽出
    # テーブル形式: | # | 内容 | 影響 | 状態 |
    in_table = False
    for line in content.splitlines():
        if '不明点' in line or 'リスク' in line:
            in_table = True
        if in_table and '|' in line and '未解決' in line:
            cells = [c.strip() for c in line.split('|') if c.strip()]
            if len(cells) >= 3:
                unresolved.append({
                    'project': project,
                    'investigation': investigation,
                    'content': cells[1] if len(cells) > 1 else cells[0],
                    'impact': cells[2] if len(cells) > 2 else '',
                })

output = {
    'total_unresolved': len(unresolved),
    'items': unresolved,
}

out_path = Path('.claude/claude-plugins/skill-evolve/investigate-patterns.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))

print(f"Found {len(unresolved)} unresolved items across {investigate_root}")
print(f"Saved to {out_path}")
