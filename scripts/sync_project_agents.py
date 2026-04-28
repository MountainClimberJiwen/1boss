#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sqlite3
import subprocess
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

DB_PATH = Path('/Users/jiwen/PycharmProjects/task-queue-system/data/task_queue.db')
HERMES_SKILLS_ROOT = Path('/Users/jiwen/.hermes/skills/iboss-projects')
AUTO_REFRESH_PREFIX = '- Auto-refreshed by `iboss/scripts/sync_project_agents.py` at '
SEED_LATEST_NOTE = '- This file is a seed context; refresh it after real project work.'
SEED_MANUAL_NOTE = '- Add durable project-specific context here: current milestone, blocked issues, important commands, env quirks, deployment URLs, test commands.'

SKILL_OVERRIDES = {
    'project-task-enqueue-系统-url-内容自动总结功能开发': {
        'skill_name': 'task-queue-system',
        'title': 'Task Queue System / project-task-enqueue',
        'description': '维护 task-queue-system 与 project-task-enqueue 相关能力，优先在 /Users/jiwen/PycharmProjects/task-queue-system 中执行。',
    },
    '测试项目-仪表盘同步验证': {
        'skill_name': 'dashboard-sync-test',
        'title': '测试项目-仪表盘同步验证',
        'description': '维护用于验证 dashboard 同步链路的测试项目。',
    },
    '每日-idea-自动整理工具': {
        'skill_name': 'daily-idea-organizer',
        'title': '每日 idea 自动整理工具',
        'description': '维护每日 idea 自动整理与汇总项目。',
    },
    'twitter-analysis': {
        'skill_name': 'twitter-analysis-project',
        'title': 'twitter-analysis',
        'description': '维护 Twitter/X 抓取分析项目。',
    },
    'wewe-rss': {
        'skill_name': 'wewe-rss-project',
        'title': 'WeWe RSS',
        'description': '维护 WeWe RSS 相关项目。',
    },
    'n8n': {
        'skill_name': 'n8n-project',
        'title': 'n8n',
        'description': '维护 n8n 工作流自动化相关项目。',
    },
    'workspace-lobster-dingtalk': {
        'skill_name': 'lobster-dingtalk-project',
        'title': 'workspace-lobster-dingtalk',
        'description': '维护 lobster 钉钉工作区项目。',
    },
    'sorin-app': {
        'skill_name': 'sorin-app-project',
        'title': 'sorin-app',
        'description': '维护 Sorin app 桌面端项目。',
    },
    'ai-infra-defi-tools': {
        'skill_name': 'ai-infra-defi-tools-project',
        'title': 'ai-infra-defi-tools',
        'description': '维护 AI infra DeFi tools 仓库。',
    },
    'freecad-assembler': {
        'skill_name': 'freecad-assembler-project',
        'title': 'freecad-assembler',
        'description': '维护 FreeCAD assembler / STEP viewer 项目。',
    },
    'Execution-Layer': {
        'skill_name': 'execution-layer-project',
        'title': 'Execution-Layer',
        'description': '维护 Execution-Layer 项目。',
    },
}

KNOWN_TASK_PROJECT_ALIASES = {
    'project-task-enqueue-系统-url-内容自动总结功能开发': ['project-task-enqueue', 'task-queue-system'],
}

ROUTER_SKILL_NAME = 'project-router'
ROUTER_DESCRIPTION = '按项目名、project_id、别名或路径把需求路由到对应 iboss project skill。'


@dataclass
class ProjectRecord:
    project_id: str
    aliases: str
    path: str
    source: str
    updated_at: str
    progress: str
    task_counts: dict[str, int]
    latest_task: dict[str, str | int | None] | None
    matched_task_project_ids: list[str]
    readme_summary: str
    git_branch: str | None
    git_status: str | None
    git_last_commit: str | None
    skill_name: str
    title: str
    skill_description: str
    latest_notes: list[str]
    manual_notes: list[str]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')


def slugify_project(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r'[^a-z0-9]+', '-', value)
    value = re.sub(r'-+', '-', value).strip('-')
    return value or 'project'


def normalize_key(value: str) -> str:
    value = value.strip().casefold()
    return re.sub(r'[\W_]+', '', value, flags=re.UNICODE)


def split_aliases(value: str) -> list[str]:
    return [part.strip() for part in value.split(',') if part.strip()]


def fallback_skill_name(project_id: str) -> str:
    slug = slugify_project(project_id)
    return f'{slug}-project'[:64]


def run(command: list[str], cwd: Path) -> str:
    result = subprocess.run(command, cwd=str(cwd), capture_output=True, text=True)
    if result.returncode != 0:
        return ''
    return result.stdout.strip()


def readme_summary(project_path: Path) -> str:
    for name in ('README.md', 'readme.md', 'README.MD'):
        candidate = project_path / name
        if candidate.exists():
            lines = []
            for raw in candidate.read_text(encoding='utf-8', errors='ignore').splitlines():
                text = raw.strip()
                if not text:
                    continue
                lines.append(text)
                if len(lines) >= 6:
                    break
            return ' / '.join(lines)[:700]
    return 'README 未找到；首次使用时建议先检查仓库结构与入口脚本。'


def git_snapshot(project_path: Path) -> tuple[str | None, str | None, str | None]:
    if not (project_path / '.git').exists():
        return None, None, None
    branch = run(['git', 'branch', '--show-current'], project_path) or None
    status = run(['bash', '-lc', 'git status --short | head -20'], project_path) or None
    last_commit = run(['git', 'log', '-1', '--pretty=format:%h %cs %s'], project_path) or None
    return branch, status, last_commit


def extract_section_lines(text: str, title: str) -> list[str]:
    pattern = re.compile(rf'^## {re.escape(title)}\s*$', re.MULTILINE)
    match = pattern.search(text)
    if not match:
        return []
    start = match.end()
    next_match = re.search(r'^##\s+', text[start:], flags=re.MULTILINE)
    end = start + next_match.start() if next_match else len(text)
    block = text[start:end].strip('\n')
    if not block.strip():
        return []
    return [line.rstrip() for line in block.splitlines() if line.strip()]


def load_existing_notes(project_path: Path) -> tuple[list[str], list[str]]:
    agents_path = project_path / '.harness' / 'AGENTS.MD'
    if not agents_path.exists():
        return [], []
    text = agents_path.read_text(encoding='utf-8', errors='ignore')
    latest_notes = extract_section_lines(text, 'Latest Notes')
    manual_notes = extract_section_lines(text, 'Manual Notes')
    latest_notes = [line for line in latest_notes if not line.startswith(AUTO_REFRESH_PREFIX)]
    return latest_notes, manual_notes


def compute_match_keys(project_id: str, aliases: str, path: str) -> set[str]:
    keys: set[str] = set()
    raw_values = [project_id, path, Path(path).name]
    raw_values.extend(split_aliases(aliases))
    raw_values.extend(KNOWN_TASK_PROJECT_ALIASES.get(project_id, []))

    for value in raw_values:
        if not value:
            continue
        keys.add(value)
        normalized = normalize_key(value)
        if normalized:
            keys.add(normalized)
        slug = slugify_project(value)
        if slug:
            keys.add(slug)
            keys.add(slug.replace('-', ''))
    return {key for key in keys if key}


def task_project_matches(task_project_id: str, match_keys: set[str]) -> bool:
    if task_project_id in match_keys:
        return True
    normalized = normalize_key(task_project_id)
    slug = slugify_project(task_project_id)
    candidates = {task_project_id, normalized, slug, slug.replace('-', '')}
    return any(candidate and candidate in match_keys for candidate in candidates)


def load_task_stats(conn: sqlite3.Connection) -> tuple[dict[str, dict[str, int]], dict[str, dict[str, str | int | None]]]:
    task_stats = {
        row['project_id']: {
            'pending': row['pending'],
            'running': row['running'],
            'done': row['done'],
            'failed': row['failed'],
            'total': row['total'],
        }
        for row in conn.execute(
            """
            SELECT project_id,
                   SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) AS pending,
                   SUM(CASE WHEN status='running' THEN 1 ELSE 0 END) AS running,
                   SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) AS done,
                   SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed,
                   COUNT(*) AS total
            FROM tasks
            GROUP BY project_id
            """
        ).fetchall()
    }

    latest_tasks = {}
    for row in conn.execute(
        """
        SELECT t.project_id,
               t.id,
               t.status,
               t.created_at,
               t.started_at,
               t.finished_at,
               r.session_id,
               r.run_status,
               r.latest_progress,
               r.updated_at AS run_updated_at
        FROM tasks t
        LEFT JOIN task_runs r ON r.task_id = t.id
        WHERE t.id IN (
            SELECT MAX(id) FROM tasks GROUP BY project_id
        )
        ORDER BY t.project_id
        """
    ).fetchall():
        latest_tasks[row['project_id']] = dict(row)
    return task_stats, latest_tasks


def aggregate_task_view(project_id: str, aliases: str, path: str, task_stats: dict[str, dict[str, int]], latest_tasks: dict[str, dict[str, str | int | None]]) -> tuple[dict[str, int], dict[str, str | int | None] | None, list[str]]:
    match_keys = compute_match_keys(project_id, aliases, path)
    matched_ids = sorted(task_id for task_id in task_stats if task_project_matches(task_id, match_keys))
    if not matched_ids:
        return {'pending': 0, 'running': 0, 'done': 0, 'failed': 0, 'total': 0}, None, []

    counts = {'pending': 0, 'running': 0, 'done': 0, 'failed': 0, 'total': 0}
    latest_rows = []
    for task_project_id in matched_ids:
        stats = task_stats.get(task_project_id, {})
        for key in counts:
            counts[key] += int(stats.get(key, 0))
        row = latest_tasks.get(task_project_id)
        if row:
            latest_rows.append(row)

    latest_rows.sort(key=lambda row: ((row.get('run_updated_at') or ''), (row.get('created_at') or ''), int(row.get('id') or 0)), reverse=True)
    return counts, (latest_rows[0] if latest_rows else None), matched_ids


def load_projects(project_filter: str | None = None) -> list[ProjectRecord]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    project_rows = conn.execute(
        """
        SELECT project_id, aliases, path, source, updated_at, COALESCE(progress, '0%') AS progress
        FROM projects
        ORDER BY updated_at DESC, project_id
        """
    ).fetchall()

    task_stats, latest_tasks = load_task_stats(conn)
    records: list[ProjectRecord] = []
    filter_key = normalize_key(project_filter or '')

    for row in project_rows:
        project_path = Path(row['path']).expanduser()
        overrides = SKILL_OVERRIDES.get(row['project_id'], {})
        skill_name = overrides.get('skill_name') or fallback_skill_name(row['project_id'])
        title = overrides.get('title') or row['project_id']
        description = overrides.get('description') or f'维护 {row["project_id"]} 项目。'
        branch, status, last_commit = git_snapshot(project_path) if project_path.exists() else (None, None, None)
        latest_notes, manual_notes = load_existing_notes(project_path) if project_path.exists() else ([], [])
        counts, latest_task, matched_task_ids = aggregate_task_view(row['project_id'], row['aliases'], row['path'], task_stats, latest_tasks)

        record = ProjectRecord(
            project_id=row['project_id'],
            aliases=row['aliases'],
            path=row['path'],
            source=row['source'],
            updated_at=row['updated_at'],
            progress=row['progress'],
            task_counts=counts,
            latest_task=latest_task,
            matched_task_project_ids=matched_task_ids,
            readme_summary=readme_summary(project_path) if project_path.exists() else '项目路径不存在，需先确认仓库位置。',
            git_branch=branch,
            git_status=status,
            git_last_commit=last_commit,
            skill_name=skill_name,
            title=title,
            skill_description=description,
            latest_notes=latest_notes,
            manual_notes=manual_notes,
        )

        if filter_key:
            haystack = [record.project_id, record.aliases, record.path, record.skill_name, record.title]
            haystack.extend(record.matched_task_project_ids)
            if not any(filter_key in normalize_key(item) for item in haystack if item):
                continue
        records.append(record)

    conn.close()
    return records


def latest_task_block(project: ProjectRecord) -> str:
    matched_line = '- matched task project_ids: ' + (', '.join(project.matched_task_project_ids) if project.matched_task_project_ids else '(none)')
    if not project.latest_task:
        return '\n'.join([matched_line, '- latest task: none recorded in task_queue.db'])
    row = project.latest_task
    return '\n'.join([
        matched_line,
        f"- latest task id: {row.get('id')}",
        f"- latest task project_id: {row.get('project_id')}",
        f"- latest task status: {row.get('status')}",
        f"- latest run status: {row.get('run_status') or '-'}",
        f"- latest session id: {row.get('session_id') or '-'}",
        f"- latest progress text: {row.get('latest_progress') or '-'}",
        f"- created_at: {row.get('created_at') or '-'}",
        f"- started_at: {row.get('started_at') or '-'}",
        f"- finished_at: {row.get('finished_at') or '-'}",
        f"- run_updated_at: {row.get('run_updated_at') or '-'}",
    ])


def git_block(project: ProjectRecord) -> str:
    if not project.git_branch:
        return '- git repo: not detected'
    lines = [
        f'- branch: {project.git_branch}',
        f'- last commit: {project.git_last_commit or "-"}',
        '- dirty summary:',
    ]
    dirty = project.git_status or '(clean)'
    for line in dirty.splitlines() or ['(clean)']:
        lines.append(f'  - {line}')
    return '\n'.join(lines)


def refreshed_latest_notes(existing_notes: list[str]) -> list[str]:
    notes = [f'{AUTO_REFRESH_PREFIX}{now_iso()}']
    cleaned = [line for line in existing_notes if line.strip() and line != SEED_LATEST_NOTE]
    notes.extend(cleaned[:8])
    if SEED_LATEST_NOTE not in notes:
        notes.append(SEED_LATEST_NOTE)
    return notes


def preserved_manual_notes(existing_notes: list[str]) -> list[str]:
    cleaned = [line for line in existing_notes if line.strip() and line != SEED_MANUAL_NOTE]
    if not cleaned:
        cleaned = [SEED_MANUAL_NOTE]
    return cleaned


def render_agents_md(project: ProjectRecord) -> str:
    counts = project.task_counts
    latest_notes = '\n'.join(refreshed_latest_notes(project.latest_notes))
    manual_notes = '\n'.join(preserved_manual_notes(project.manual_notes))
    body = f"""
# {project.title} · Project Agent Context

This file is the local grounding context for skill `{project.skill_name}`.
The skill should read this file before answering project-specific questions or executing project-specific commands.
If `{project.path}/.harness/work-notes.md` exists, read it too for session-derived progress notes and lessons learned.

## Identity
- project_id: `{project.project_id}`
- skill_name: `{project.skill_name}`
- repo_path: `{project.path}`
- aliases: `{project.aliases}`
- source: `{project.source}`
- project_table_updated_at: `{project.updated_at}`
- last_synced_by_iboss: `{now_iso()}`

## Project Summary
- stored progress field: `{project.progress}`
- readme summary: {project.readme_summary}

## Task Queue Snapshot
- pending: {counts['pending']}
- running: {counts['running']}
- done: {counts['done']}
- failed: {counts['failed']}
- total: {counts['total']}
{latest_task_block(project)}

## Workspace Snapshot
{git_block(project)}

## Agent Operating Rules
1. When this project skill is invoked, start by reading this file and then run live checks in `{project.path}` if the user asks about current status.
2. Use `{project.path}` as the default working directory for shell commands, code inspection, and edits unless the user explicitly redirects elsewhere.
3. For progress questions, combine this file with live signals: `git status`, recent commits, relevant logs, tests, and task queue data.
4. When the user sends a new idea, design note, or command for this project, execute it in this repo context rather than giving generic advice.
5. After meaningful work, update this file's `Project Summary`, `Task Queue Snapshot`, `Workspace Snapshot`, and `Latest Notes` sections so the project skill stays stateful across sessions.
6. Do not overwrite the `Manual Notes` section unless the user asks or you are clearly appending a new durable fact.
7. To refresh this file without touching other projects, run `python3 /Users/jiwen/PycharmProjects/iboss/scripts/sync_project_agents.py --project {project.skill_name}`.

## Suggested First Checks
- `pwd`
- `git status --short`
- `git log -1 --oneline`
- inspect repo README and entry scripts
- inspect task queue / dashboard state if the question is about dispatcher progress

## Latest Notes
{latest_notes}

## Manual Notes
{manual_notes}
"""
    return dedent(body).strip() + '\n'


def render_skill(project: ProjectRecord) -> str:
    body = f"""
---
name: {project.skill_name}
description: {project.skill_description}
version: 0.2.0
---

# {project.title}

This skill owns project `{project.project_id}`.

Primary repo path: `{project.path}`
Primary context file: `{project.path}/.harness/AGENTS.MD`
Aliases: `{project.aliases}`

## When to use
- The user mentions `{project.project_id}`.
- The user refers to this project by one of its aliases.
- The user asks for this repo's progress, wants to send an idea to this project, or wants commands executed in this project context.

## Required workflow
1. Read `{project.path}/.harness/AGENTS.MD` first.
2. If `{project.path}/.harness/work-notes.md` exists, read it for accumulated session summaries and implementation experience.
3. Treat `{project.path}` as the default working directory.
4. If the user asks for current progress, verify with live checks (`git status`, recent commits, task queue or runtime status) instead of trusting stale notes.
5. If the user gives a task or idea, execute it in this project context and keep answers specific to this repo.
6. After meaningful progress, update `{project.path}/.harness/AGENTS.MD` so future sessions inherit the latest context.
7. If only this project's seed context needs refresh, run `python3 /Users/jiwen/PycharmProjects/iboss/scripts/sync_project_agents.py --project {project.skill_name}`.

## Default response style for this project
- Be concrete and repo-specific.
- Mention file paths, commands, and current status.
- Prefer acting in the repo over giving abstract recommendations.

## Seed context
- stored progress: `{project.progress}`
- task counts: pending={project.task_counts['pending']}, running={project.task_counts['running']}, done={project.task_counts['done']}, failed={project.task_counts['failed']}, total={project.task_counts['total']}
- matched task project_ids: {', '.join(project.matched_task_project_ids) if project.matched_task_project_ids else '(none)'}
- readme summary: {project.readme_summary}
"""
    return dedent(body).strip() + '\n'


def render_router_skill(projects: list[ProjectRecord]) -> str:
    rows = []
    for project in projects:
        rows.append(
            f"- `{project.project_id}` → skill `{project.skill_name}` → path `{project.path}` → aliases `{project.aliases}`"
        )
    mapping = '\n'.join(rows)
    body = f"""
---
name: {ROUTER_SKILL_NAME}
description: {ROUTER_DESCRIPTION}
version: 0.2.0
---

# project router

Use this skill when the user references a managed project but the exact project skill is not obvious.

## Routing rule
Match the user's project name, project_id, alias, or path to the closest project below, then load that specific skill and continue there.

## Current mapping
{mapping}

## Operating rule
After routing, the project-specific skill must read that repo's `.harness/AGENTS.MD` before continuing.
"""
    return dedent(body).strip() + '\n'


def write_project_agents(project: ProjectRecord) -> None:
    project_path = Path(project.path).expanduser()
    harness_dir = project_path / '.harness'
    harness_dir.mkdir(parents=True, exist_ok=True)
    content = render_agents_md(project)
    (harness_dir / 'AGENTS.MD').write_text(content, encoding='utf-8')
    (harness_dir / 'AGENTS.md').write_text(content, encoding='utf-8')


def write_skill_file(skill_name: str, content: str) -> None:
    skill_dir = HERMES_SKILLS_ROOT / skill_name
    skill_dir.mkdir(parents=True, exist_ok=True)
    (skill_dir / 'SKILL.md').write_text(content, encoding='utf-8')


def write_category_description() -> None:
    HERMES_SKILLS_ROOT.mkdir(parents=True, exist_ok=True)
    description = dedent(
        """
        iboss project skills

        Per-project routing and context skills for projects tracked by iboss/task_queue_system.
        Each skill points to a repo-local `.harness/AGENTS.MD` file that stores progress, path, and durable repo context.
        Run `python3 /Users/jiwen/PycharmProjects/iboss/scripts/sync_project_agents.py` to refresh all projects,
        or pass `--project <name>` to refresh one project incrementally.
        """
    ).strip() + '\n'
    (HERMES_SKILLS_ROOT / 'DESCRIPTION.md').write_text(description, encoding='utf-8')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Sync per-project AGENTS.MD files and Hermes skills for managed projects.')
    parser.add_argument('--project', help='Refresh one project by project_id, alias, title, skill name, or repo path substring.')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not DB_PATH.exists():
        raise SystemExit(f'DB not found: {DB_PATH}')
    projects = load_projects(project_filter=args.project)
    if args.project and not projects:
        raise SystemExit(f'No project matched filter: {args.project}')
    write_category_description()
    for project in projects:
        write_project_agents(project)
        write_skill_file(project.skill_name, render_skill(project))
    write_skill_file(ROUTER_SKILL_NAME, render_router_skill(load_projects()))
    print(json.dumps({
        'db': str(DB_PATH),
        'skills_root': str(HERMES_SKILLS_ROOT),
        'project_filter': args.project,
        'project_count': len(projects),
        'skills': [{
            'project_id': p.project_id,
            'skill_name': p.skill_name,
            'path': p.path,
            'matched_task_project_ids': p.matched_task_project_ids,
            'task_counts': p.task_counts,
        } for p in projects] + [{
            'project_id': '__router__',
            'skill_name': ROUTER_SKILL_NAME,
            'path': str(HERMES_SKILLS_ROOT / ROUTER_SKILL_NAME),
        }]
    }, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
