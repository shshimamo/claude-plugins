#!/usr/bin/env python3
"""
Case 3: ~/.investigate/ と ~/.dev/ を横断して
「各スキルで何が足りなかったか」のパターンを集計する

ローカルの cron から実行される（local_evolve.sh 経由）。
複数スキルのデータを合わせて分析することで、
単一スキルでは気づけないパターンを発見することが目的。

出力:
  .claude/skill-evolve/cross-skill-patterns.json
  → improve_local_skills.py が読み込んで dev スキルを改善する
"""
import json
from pathlib import Path

investigate_root = Path.home() / '.investigate'
dev_root = Path.home() / '.dev'

patterns = {
    'investigate': {'unresolved_count': 0, 'common_unknowns': []},
    'dev': {'stalled_tasks': [], 'missing_plan_areas': []},
}

# --- investigate: 複数の調査をまたいで共通する未解決不明点を集計 ---
if investigate_root.exists():
    unknowns: dict[str, int] = {}  # 不明点の内容 → 出現回数

    for summary_path in investigate_root.glob('*/*/investigation/summary.md'):
        content = summary_path.read_text(encoding='utf-8')
        in_table = False
        for line in content.splitlines():
            if '不明点' in line or 'リスク' in line:
                in_table = True
            if in_table and '|' in line and '未解決' in line:
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if cells:
                    key = cells[1] if len(cells) > 1 else cells[0]
                    unknowns[key] = unknowns.get(key, 0) + 1

    patterns['investigate']['unresolved_count'] = sum(unknowns.values())

    # 2件以上の調査で共通して未解決になっているものを「よくある詰まりポイント」として抽出
    patterns['investigate']['common_unknowns'] = [
        {'content': k, 'count': v} for k, v in unknowns.items() if v >= 2
    ]

# --- dev: 保留・ブロック状態のまま残っているタスクを集計 ---
# dev スキルが生成する ~/.dev/<project>/tasks.md を全件スキャン
if dev_root.exists():
    stalled = []
    for tasks_path in dev_root.glob('*/tasks.md'):
        content = tasks_path.read_text(encoding='utf-8')
        project = tasks_path.parent.name
        for line in content.splitlines():
            # タスクテーブルで「保留」「ブロック」「blocked」の行を抽出
            if '|' in line and ('保留' in line or 'ブロック' in line or 'blocked' in line.lower()):
                cells = [c.strip() for c in line.split('|') if c.strip()]
                if cells:
                    stalled.append({'project': project, 'task': cells[0]})
    patterns['dev']['stalled_tasks'] = stalled

out_path = Path('.claude/skill-evolve/cross-skill-patterns.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(patterns, ensure_ascii=False, indent=2))

print(f"Cross-skill analysis saved to {out_path}")
print(f"  investigate unresolved: {patterns['investigate']['unresolved_count']}")
print(f"  dev stalled tasks: {len(patterns['dev']['stalled_tasks'])}")
