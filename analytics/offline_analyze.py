#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


def fetch_all(conn: sqlite3.Connection, sql: str, params: tuple = ()) -> list[sqlite3.Row]:
    cur = conn.execute(sql, params)
    return cur.fetchall()


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline analyze project/session/task status from task_queue.db")
    parser.add_argument(
        "--db",
        default="/Users/jiwen/PycharmProjects/task-queue-system/data/task_queue.db",
        help="sqlite db path (default: task-queue-system/data/task_queue.db)",
    )
    parser.add_argument("--json", action="store_true", help="print JSON output")
    args = parser.parse_args()

    db_path = Path(args.db)
    if not db_path.exists():
        raise SystemExit(f"db not found: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    project_rows = fetch_all(
        conn,
        """
        SELECT project_id,
               SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) AS pending,
               SUM(CASE WHEN status='running' THEN 1 ELSE 0 END) AS running,
               SUM(CASE WHEN status='done' THEN 1 ELSE 0 END) AS done,
               SUM(CASE WHEN status='failed' THEN 1 ELSE 0 END) AS failed,
               COUNT(*) AS total
        FROM tasks
        GROUP BY project_id
        ORDER BY project_id
        """,
    )

    session_rows = fetch_all(
        conn,
        """
        SELECT project_id,
               COUNT(*) AS run_count,
               SUM(CASE WHEN session_id IS NOT NULL AND session_id != '' THEN 1 ELSE 0 END) AS with_session_id,
               SUM(CASE WHEN run_status='running' THEN 1 ELSE 0 END) AS running_runs,
               SUM(CASE WHEN run_status='done' THEN 1 ELSE 0 END) AS done_runs,
               SUM(CASE WHEN run_status='failed' THEN 1 ELSE 0 END) AS failed_runs,
               MAX(updated_at) AS latest_updated_at
        FROM task_runs
        GROUP BY project_id
        ORDER BY project_id
        """,
    )

    task_latest_rows = fetch_all(
        conn,
        """
        SELECT t.id, t.project_id, t.status, t.created_at, t.started_at, t.finished_at,
               r.session_id, r.run_status, r.latest_progress
        FROM tasks t
        LEFT JOIN task_runs r ON r.task_id = t.id
        ORDER BY t.id DESC
        LIMIT 30
        """,
    )

    output = {
        "db": str(db_path),
        "projects": [dict(row) for row in project_rows],
        "sessions": [dict(row) for row in session_rows],
        "latest_tasks": [dict(row) for row in task_latest_rows],
    }

    if args.json:
        print(json.dumps(output, ensure_ascii=False, indent=2))
        return

    print(f"DB: {db_path}")
    print("\n== Project Status ==")
    for row in output["projects"]:
        print(
            f"- {row['project_id']}: total={row['total']} pending={row['pending']} "
            f"running={row['running']} done={row['done']} failed={row['failed']}"
        )

    print("\n== Session / Run Status ==")
    for row in output["sessions"]:
        print(
            f"- {row['project_id']}: runs={row['run_count']} with_session={row['with_session_id']} "
            f"running={row['running_runs']} done={row['done_runs']} failed={row['failed_runs']} "
            f"latest={row['latest_updated_at']}"
        )

    print("\n== Latest Tasks (30) ==")
    for row in output["latest_tasks"]:
        print(
            f"- task={row['id']} project={row['project_id']} status={row['status']} "
            f"run={row['run_status']} session={row['session_id']}"
        )


if __name__ == "__main__":
    main()
