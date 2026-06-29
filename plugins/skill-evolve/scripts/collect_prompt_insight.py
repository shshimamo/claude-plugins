#!/usr/bin/env python3
"""
~/.prompt-insight/logs/ の JSONL ファイルを読み込み、
直近 N 日分のプロンプトログからパターンを抽出する。

出力:
  .claude/claude-plugins/skill-evolve/prompt-patterns.json
"""
import json
import sys
from pathlib import Path
from datetime import datetime, timedelta

# 引数で日数を指定可能（デフォルト: 30日）
days = int(sys.argv[1]) if len(sys.argv) > 1 else 30

logs_dir = Path.home() / '.prompt-insight' / 'logs'

if not logs_dir.exists():
    print("~/.prompt-insight/logs/ not found. Run /prompt-insight setup first.")
    exit(0)

cutoff = datetime.now() - timedelta(days=days)
prompts = []

for log_file in sorted(logs_dir.glob('*.jsonl')):
    # ファイル名（YYYY-MM-DD.jsonl）から日付を判定
    try:
        file_date = datetime.strptime(log_file.stem, '%Y-%m-%d')
    except ValueError:
        continue
    if file_date < cutoff:
        continue

    for line in log_file.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            prompts.append(json.loads(line))
        except json.JSONDecodeError:
            continue

output = {
    'days': days,
    'total_prompts': len(prompts),
    'prompts': prompts,
}

out_path = Path('.claude/claude-plugins/skill-evolve/prompt-patterns.json')
out_path.parent.mkdir(parents=True, exist_ok=True)
out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2))

print(f"Collected {len(prompts)} prompts from the last {days} days")
print(f"Saved to {out_path}")
