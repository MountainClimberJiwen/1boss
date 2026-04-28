#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import glob
import json
import os
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

DEFAULT_SESSIONS_GLOB = os.path.expanduser('~/.codex/sessions/**/*.jsonl')
DEFAULT_PROJECTS_DB = Path('/Users/jiwen/PycharmProjects/task-queue-system/data/task_queue.db')
DEFAULT_STATE_PATH = Path('/Users/jiwen/PycharmProjects/iboss/state/codex-worknotes-sync-state.json')
DEFAULT_LOOKBACK_HOURS = 24 * 30
AUTO_NOTE = '> Auto-appended from Codex session sync. Do not edit old entries in place; add follow-up notes below.'

KNOWN_ALIASES = {
    'project-task-enqueue-系统-url-内容自动总结功能开发': ['project-task-enqueue', 'task-queue-system'],
}


@dataclass
class ProjectRecord:
    project_id: str
    aliases: str
    path: str
    skill_name: str


@dataclass
class SessionSummary:
    session_id: str
    file_path: str
    cwd: str
    project: ProjectRecord
    session_start: dt.datetime
    last_event: dt.datetime
    completion_type: str
    summary_text: str


def parse_iso8601(ts: str) -> dt.datetime | None:
    if not ts:
        return None
    try:
        return dt.datetime.fromisoformat(ts.replace('Z', '+00:00'))
    except ValueError:
        return None


def now_utc() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc)


def normalize_key(value: str) -> str:
    return re.sub(r'[\W_]+', '', (value or '').casefold())


def slugify(value: str) -> str:
    value = re.sub(r'[^a-z0-9]+', '-', (value or '').lower())
    return re.sub(r'-+', '-', value).strip('-')


def split_aliases(value: str) -> list[str]:
    return [part.strip() for part in (value or '').split(',') if part.strip()]


def fallback_skill_name(project_id: str) -> str:
    slug = slugify(project_id)
    return f'{slug}-project'[:64]


def iter_session_files(pattern: str) -> Iterable[str]:
    files = glob.glob(pattern, recursive=True)
    files.sort(key=lambda p: os.path.getmtime(p), reverse=True)
    return files


def load_projects(db_path: Path) -> list[ProjectRecord]:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    rows = conn.execute(
        '''
        SELECT project_id, aliases, path
        FROM projects
        ORDER BY updated_at DESC, project_id
        '''
    ).fetchall()
    conn.close()

    overrides = {
        'project-task-enqueue-系统-url-内容自动总结功能开发': 'task-queue-system',
        '测试项目-仪表盘同步验证': 'dashboard-sync-test',
        '每日-idea-自动整理工具': 'daily-idea-organizer',
        'twitter-analysis': 'twitter-analysis-project',
        'wewe-rss': 'wewe-rss-project',
        'n8n': 'n8n-project',
        'workspace-lobster-dingtalk': 'lobster-dingtalk-project',
        'sorin-app': 'sorin-app-project',
        'ai-infra-defi-tools': 'ai-infra-defi-tools-project',
        'freecad-assembler': 'freecad-assembler-project',
        'Execution-Layer': 'execution-layer-project',
    }

    return [
        ProjectRecord(
            project_id=str(row['project_id']),
            aliases=str(row['aliases'] or ''),
            path=str(row['path']),
            skill_name=overrides.get(str(row['project_id'])) or fallback_skill_name(str(row['project_id'])),
        )
        for row in rows
    ]


def project_match_keys(project: ProjectRecord) -> set[str]:
    keys: set[str] = set()
    raw_values = [project.project_id, project.path, Path(project.path).name]
    raw_values.extend(split_aliases(project.aliases))
    raw_values.extend(KNOWN_ALIASES.get(project.project_id, []))
    for value in raw_values:
        if not value:
            continue
        keys.add(value)
        keys.add(normalize_key(value))
        slug = slugify(value)
        if slug:
            keys.add(slug)
            keys.add(slug.replace('-', ''))
    return {key for key in keys if key}


def resolve_project(cwd: str, projects: list[ProjectRecord]) -> ProjectRecord | None:
    cwd_path = Path(cwd or '').expanduser()
    cwd_str = str(cwd_path)

    direct_matches = []
    for project in projects:
        project_path = Path(project.path).expanduser()
        try:
            if cwd_path == project_path or cwd_path.is_relative_to(project_path):
                direct_matches.append((len(str(project_path)), project))
        except Exception:
            continue
    if direct_matches:
        direct_matches.sort(key=lambda item: item[0], reverse=True)
        return direct_matches[0][1]

    normalized_cwd = normalize_key(cwd_str)
    slug_cwd = slugify(Path(cwd_str).name or cwd_str)
    for project in projects:
        keys = project_match_keys(project)
        if cwd_str in keys or normalized_cwd in keys or slug_cwd in keys or slug_cwd.replace('-', '') in keys:
            return project
    return None


def extract_message_text(payload: dict) -> str:
    content = payload.get('content')
    if not isinstance(content, list):
        return ''
    parts: list[str] = []
    for item in content:
        if not isinstance(item, dict):
            continue
        item_type = item.get('type')
        if item_type in {'input_text', 'output_text', 'text'}:
            text = item.get('text')
            if isinstance(text, str) and text.strip():
                parts.append(text.strip())
    return '\n'.join(parts)


def sanitize_summary(text: str, limit: int = 1400) -> str:
    text = (text or '').strip()
    if not text:
        return ''
    lines = [line.rstrip() for line in text.splitlines() if line.strip()]
    compact = '\n'.join(lines)
    if len(compact) <= limit:
        return compact
    return compact[: limit - 3].rstrip() + '...'


def parse_session_file(path: str, projects: list[ProjectRecord], since: dt.datetime) -> SessionSummary | None:
    session_id = ''
    cwd = ''
    session_start: dt.datetime | None = None
    last_event: dt.datetime | None = None
    latest_assistant = ''
    completion_type = ''

    try:
        with open(path, 'r', encoding='utf-8') as fh:
            for raw in fh:
                raw = raw.strip()
                if not raw:
                    continue
                try:
                    event = json.loads(raw)
                except json.JSONDecodeError:
                    continue

                ts = parse_iso8601(str(event.get('timestamp', '')))
                if ts and (last_event is None or ts > last_event):
                    last_event = ts

                event_type = event.get('type')
                payload = event.get('payload') or {}
                payload_type = payload.get('type')

                if event_type == 'session_meta':
                    session_id = str(payload.get('id') or session_id)
                    cwd = str(payload.get('cwd') or cwd)
                    sstart = parse_iso8601(str(payload.get('timestamp', '')))
                    if sstart:
                        session_start = sstart
                elif event_type == 'turn_context':
                    cwd = str(payload.get('cwd') or cwd)
                elif event_type == 'response_item' and payload_type == 'message' and payload.get('role') == 'assistant':
                    text = extract_message_text(payload)
                    if text:
                        latest_assistant = text
                elif event_type == 'event_msg' and payload_type in {'task_complete', 'turn_aborted'}:
                    completion_type = payload_type

    except OSError:
        return None

    if not session_id or not completion_type or not last_event or last_event < since:
        return None

    project = resolve_project(cwd, projects)
    if not project:
        return None

    summary_text = sanitize_summary(latest_assistant)
    if not summary_text:
        return None

    return SessionSummary(
        session_id=session_id,
        file_path=path,
        cwd=cwd,
        project=project,
        session_start=session_start or last_event,
        last_event=last_event,
        completion_type=completion_type,
        summary_text=summary_text,
    )


def load_state(path: Path) -> dict:
    if not path.exists():
        return {'processed_sessions': {}, 'last_run_at': None}
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except Exception:
        return {'processed_sessions': {}, 'last_run_at': None}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding='utf-8')


def ensure_work_notes(path: Path, project: ProjectRecord) -> None:
    if path.exists():
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    header = [
        f'# {project.project_id} work notes',
        '',
        f'- repo_path: `{project.path}`',
        f'- skill_name: `{project.skill_name}`',
        '',
        AUTO_NOTE,
        '',
    ]
    path.write_text('\n'.join(header), encoding='utf-8')


def append_work_note(summary: SessionSummary) -> Path:
    notes_path = Path(summary.project.path).expanduser() / '.harness' / 'work-notes.md'
    ensure_work_notes(notes_path, summary.project)
    block = [
        f'## {summary.last_event.astimezone().isoformat(timespec="seconds")} · Codex session `{summary.session_id}`',
        f'- completion: `{summary.completion_type}`',
        f'- session_start: `{summary.session_start.astimezone().isoformat(timespec="seconds")}`',
        f'- last_event: `{summary.last_event.astimezone().isoformat(timespec="seconds")}`',
        f'- cwd: `{summary.cwd}`',
        f'- source: `{summary.file_path}`',
        '- summary:',
    ]
    block.extend([f'  {line}' if line.startswith('- ') else f'  {line}' for line in summary.summary_text.splitlines()])
    block.append('')
    with notes_path.open('a', encoding='utf-8') as fh:
        fh.write('\n'.join(block))
    return notes_path


def render_result(processed: list[tuple[SessionSummary, Path]], skipped_count: int, state_path: Path) -> dict:
    return {
        'processed_count': len(processed),
        'skipped_count': skipped_count,
        'state_path': str(state_path),
        'items': [
            {
                'session_id': item.session_id,
                'project_id': item.project.project_id,
                'skill_name': item.project.skill_name,
                'notes_path': str(notes_path),
                'last_event': item.last_event.isoformat(),
            }
            for item, notes_path in processed
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description='Append deduplicated Codex session summaries into per-project .harness/work-notes.md files.')
    parser.add_argument('--sessions-glob', default=DEFAULT_SESSIONS_GLOB)
    parser.add_argument('--projects-db', default=str(DEFAULT_PROJECTS_DB))
    parser.add_argument('--state-path', default=str(DEFAULT_STATE_PATH))
    parser.add_argument('--lookback-hours', type=int, default=DEFAULT_LOOKBACK_HOURS)
    parser.add_argument('--limit', type=int, default=500)
    args = parser.parse_args()

    since = now_utc() - dt.timedelta(hours=max(1, args.lookback_hours))
    projects = load_projects(Path(args.projects_db))
    state_path = Path(args.state_path)
    state = load_state(state_path)
    processed_sessions = state.setdefault('processed_sessions', {})

    processed: list[tuple[SessionSummary, Path]] = []
    skipped_count = 0

    for idx, path in enumerate(iter_session_files(args.sessions_glob)):
        if idx >= args.limit:
            break
        summary = parse_session_file(path, projects=projects, since=since)
        if not summary:
            skipped_count += 1
            continue
        fingerprint = summary.last_event.isoformat()
        if processed_sessions.get(summary.session_id) == fingerprint:
            skipped_count += 1
            continue
        notes_path = append_work_note(summary)
        processed_sessions[summary.session_id] = fingerprint
        processed.append((summary, notes_path))

    state['last_run_at'] = now_utc().isoformat()
    save_state(state_path, state)
    print(json.dumps(render_result(processed, skipped_count, state_path), ensure_ascii=False, indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
