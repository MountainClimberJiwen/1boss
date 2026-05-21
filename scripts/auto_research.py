#!/usr/bin/env python3
"""
Auto-research dispatcher for iboss projects with autoresearch enabled.

Runs nightly (01:00) to:
1. Query task_queue.db for projects with autoresearch=1.
2. Read each project's .harness/AGENTS.MD (goals/status) and work-notes.md (used solutions).
3. Call a local LLM (Ollama by default) to generate a NEW proposal that excludes used solutions.
4. Store the proposal in the research_proposals table as 'pending'.

Environment:
  TASK_QUEUE_DB_PATH  — path to task_queue.db (default: /Users/jiwen/PycharmProjects/task-queue-system/data/task_queue.db)
  OLLAMA_API_URL      — Ollama chat completions endpoint (default: http://127.0.0.1:11434/v1/chat/completions)
  OLLAMA_MODEL        — model name (default: deepseek-v4-flash:cloud)
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import Request, urlopen

DEFAULT_DB_PATH = "/Users/jiwen/PycharmProjects/task-queue-system/data/task_queue.db"
DEFAULT_OLLAMA_URL = "http://127.0.0.1:11434/v1/chat/completions"
DEFAULT_OLLAMA_MODEL = "qwen3.5:4b"


def _read_text(path: str, limit: int = 8000) -> str:
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore")
        return text[:limit] if limit else text
    except Exception:
        return ""


def _call_llm(prompt: str) -> str:
    url = os.environ.get("OLLAMA_API_URL", DEFAULT_OLLAMA_URL)
    model = os.environ.get("OLLAMA_MODEL", DEFAULT_OLLAMA_MODEL)
    body = json.dumps(
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
        },
        ensure_ascii=False,
    ).encode("utf-8")
    req = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urlopen(req, timeout=300) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data["choices"][0]["message"]["content"]
    except Exception as exc:
        return f"[LLM error: {exc}]"


def _build_prompt(project_id: str, aliases: str, path: str, agents_md: str, work_notes: str) -> str:
    return f"""You are an autonomous research assistant for a software project.

Project ID: {project_id}
Aliases: {aliases}
Repo path: {path}

--- Project context (from AGENTS.MD) ---
{agents_md}

--- Previously used solutions / work notes ---
{work_notes}

Instructions:
1. Analyze the project's current goal, progress, and difficulties.
2. Propose ONE concrete, actionable NEW solution or next step that has NOT been tried before.
3. Do NOT repeat anything already listed in the work notes.
4. If no clear new direction exists, say so explicitly.

Output strictly in this format:
PROPOSAL: <one-paragraph actionable proposal>
REASONING: <brief reasoning why this is new and appropriate>
"""


def _extract_proposal(text: str) -> str:
    text = text.strip()
    if "PROPOSAL:" in text:
        parts = text.split("PROPOSAL:", 1)[1]
        if "REASONING:" in parts:
            parts = parts.split("REASONING:", 1)[0]
        return parts.strip()
    return text


def _notify_hermes(conn: sqlite3.Connection, project_id: str, proposal_id: int, proposal_text: str) -> None:
    """Create a Hermes thread message to notify about a new auto-research proposal."""
    now = datetime.now(timezone.utc).isoformat()
    cur = conn.execute(
        "INSERT INTO threads(project_id, title, status, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
        (project_id, f"Auto Research Proposal #{proposal_id}", "open", now, now),
    )
    thread_id = cur.lastrowid
    content = f"🤖 Auto-research generated a new proposal (#{proposal_id}):\n\n{proposal_text}\n\nApprove or reject via API when ready."
    conn.execute(
        """
        INSERT INTO thread_messages(
            project_id, thread_id, sender_type, sender_name, content,
            event_type, mentions_json, task_id, session_id, created_at
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (project_id, thread_id, "system", "auto-research", content, "message", "[]", None, None, now),
    )
    conn.commit()
    print(f"  Notified hermes imchannel (thread #{thread_id})")


def main() -> int:
    db_path = os.environ.get("TASK_QUEUE_DB_PATH", DEFAULT_DB_PATH)
    if not Path(db_path).exists():
        print(f"Database not found: {db_path}", file=sys.stderr)
        return 1

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    rows = conn.execute(
        "SELECT project_id, aliases, path FROM projects WHERE autoresearch = 1 ORDER BY project_id"
    ).fetchall()

    if not rows:
        print("No autoresearch projects found.")
        conn.close()
        return 0

    created = 0
    for row in rows:
        project_id = row["project_id"]
        repo_path = row["path"] or ""
        aliases = row["aliases"] or ""

        agents_md = _read_text(f"{repo_path}/.harness/AGENTS.MD", limit=4000)
        work_notes = _read_text(f"{repo_path}/.harness/work-notes.md", limit=4000)

        print(f"[auto-research] Project: {project_id}")
        if not agents_md:
            print(f"  Skipped: no AGENTS.MD found at {repo_path}/.harness/AGENTS.MD")
            continue

        prompt = _build_prompt(project_id, aliases, repo_path, agents_md, work_notes)
        llm_output = _call_llm(prompt)
        proposal_text = _extract_proposal(llm_output)

        cur = conn.execute(
            """
            INSERT INTO research_proposals (project_id, context, proposal, used_solutions, status, created_at)
            VALUES (?, ?, ?, ?, 'pending', datetime('now'))
            """,
            (
                project_id,
                agents_md[:2000],
                proposal_text[:4000],
                work_notes[:2000],
            ),
        )
        conn.commit()
        proposal_id = cur.lastrowid
        created += 1
        print(f"  Stored proposal #{proposal_id} ({len(proposal_text)} chars)")
        _notify_hermes(conn, project_id, proposal_id, proposal_text)

    conn.close()
    print(f"[auto-research] Finished. Proposals created: {created}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
