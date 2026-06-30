#!/usr/bin/env python3
"""
~/.claude-plugins/investigate/code/ の調査ファイルと ~/.claude-plugins/repo-know/ のプロジェクト知識を分析し、
investigate_code スキルの改善データを収集する。

出力:
  .claude/claude-plugins/skill-evolve/investigate-code-patterns.json

skill-evolve はこのデータをもとに
.claude/claude-plugins/skill-evolve/skill-extensions/<project>/investigate_code.local.md
を更新する。
"""
import json
from pathlib import Path

investigate_root = Path.home() / '.claude-plugins' / 'investigate' / 'code'
repo_know_root = Path.home() / '.claude-plugins' / 'repo-know'

if not investigate_root.exists() and not repo_know_root.exists():
    print("~/.claude-plugins/investigate/code/ and ~/.claude-plugins/repo-know/ not found. No data to analyze.")
    exit(0)

projects = {}

# ~/.claude-plugins/investigate/code/ から調査データを収集
if investigate_root.exists():
    for project_dir in sorted(investigate_root.iterdir()):
        if not project_dir.is_dir():
            continue

        project = project_dir.name
        if project not in projects:
            projects[project] = {
                'repo_know': None,
                'investigations': [],
            }

        # 各調査の summary.md を読み込む
        for summary_path in sorted(project_dir.glob('*/investigation/summary.md')):
            investigation = summary_path.parts[-3]
            projects[project]['investigations'].append({
                'name': investigation,
                'summary': summary_path.read_text(encoding='utf-8'),
            })

# ~/.claude-plugins/repo-know/ からプロジェクト知識を収集
if repo_know_root.exists():
    for project_dir in sorted(repo_know_root.iterdir()):
        if not project_dir.is_dir():
            continue

        project = project_dir.name
        if project not in projects:
            projects[project] = {
                'repo_know': None,
                'investigations': [],
            }

        parts = []
        for filename in ('tech.md', 'domain.md', 'decisions.md'):
            path = project_dir / filename
            if path.exists():
                parts.append(path.read_text(encoding='utf-8'))
        if parts:
            projects[project]['repo_know'] = '\n\n'.join(parts)

# データがないプロジェクトを除外
projects = {k: v for k, v in projects.items()
            if v['repo_know'] or v['investigations']}

output = {
    'total_projects': len(projects),
    'projects': projects,
}

out_path = Path('.claude/claude-plugins/skill-evolve/investigate-code-patterns.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))

print(f"Found {len(projects)} projects with code investigation data")
for project, data in projects.items():
    has_rk = '✓' if data['repo_know'] else '-'
    inv_count = len(data['investigations'])
    print(f"  {project}: repo-know={has_rk}, investigations={inv_count}")
print(f"Saved to {out_path}")
