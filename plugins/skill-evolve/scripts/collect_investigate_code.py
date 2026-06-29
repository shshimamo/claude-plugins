#!/usr/bin/env python3
"""
~/.investigate/code/ の調査ファイルとドメイン知識を分析し、
investigate_code スキルの改善データを収集する。

出力:
  .claude/claude-plugins/skill-evolve/investigate-code-patterns.json

skill-evolve はこのデータをもとに
.claude/claude-plugins/skill-evolve/skill-extensions/<project>/investigate_code.local.md
を更新する。
"""
import json
from pathlib import Path

investigate_root = Path.home() / '.investigate' / 'code'

if not investigate_root.exists():
    print("~/.investigate/code/ not found. No data to analyze.")
    exit(0)

projects = {}

for project_dir in sorted(investigate_root.iterdir()):
    if not project_dir.is_dir():
        continue

    project = project_dir.name
    projects[project] = {
        'domain_knowledge': None,
        'investigations': [],
    }

    # domain-knowledge.md を読み込む
    dk_path = project_dir / 'domain-knowledge.md'
    if dk_path.exists():
        projects[project]['domain_knowledge'] = dk_path.read_text(encoding='utf-8')

    # 各調査の summary.md を読み込む
    for summary_path in sorted(project_dir.glob('*/investigation/summary.md')):
        investigation = summary_path.parts[-3]
        projects[project]['investigations'].append({
            'name': investigation,
            'summary': summary_path.read_text(encoding='utf-8'),
        })

# データがないプロジェクトを除外
projects = {k: v for k, v in projects.items()
            if v['domain_knowledge'] or v['investigations']}

output = {
    'total_projects': len(projects),
    'projects': projects,
}

out_path = Path('.claude/claude-plugins/skill-evolve/investigate-code-patterns.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))

print(f"Found {len(projects)} projects with code investigation data")
for project, data in projects.items():
    has_dk = '✓' if data['domain_knowledge'] else '-'
    inv_count = len(data['investigations'])
    print(f"  {project}: domain-knowledge={has_dk}, investigations={inv_count}")
print(f"Saved to {out_path}")
