#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sqlite3
from datetime import datetime, timezone

DEFAULT_DB = "/Users/jiwen/PycharmProjects/task-queue-system/data/task_queue.db"


def ensure_table(conn: sqlite3.Connection) -> None:
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS session_tmux_map (
            session_id TEXT PRIMARY KEY,
            tmux_target TEXT NOT NULL,
            source TEXT NOT NULL DEFAULT 'manual',
            updated_at TEXT NOT NULL
        )
        """
    )
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_session_tmux_map_updated_at
        ON session_tmux_map(updated_at DESC)
        """
    )
    conn.commit()


def cmd_set(conn: sqlite3.Connection, args: argparse.Namespace) -> int:
    now = datetime.now(timezone.utc).isoformat()
    conn.execute(
        """
        INSERT INTO session_tmux_map(session_id, tmux_target, source, updated_at)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(session_id) DO UPDATE SET
            tmux_target=excluded.tmux_target,
            source=excluded.source,
            updated_at=excluded.updated_at
        """,
        (args.session_id.strip(), args.tmux_target.strip(), args.source.strip(), now),
    )
    conn.commit()
    print(f"ok: {args.session_id.strip()} -> {args.tmux_target.strip()} (source={args.source.strip()})")
    return 0


def cmd_get(conn: sqlite3.Connection, args: argparse.Namespace) -> int:
    row = conn.execute(
        "SELECT session_id, tmux_target, source, updated_at FROM session_tmux_map WHERE session_id = ? LIMIT 1",
        (args.session_id.strip(),),
    ).fetchone()
    if not row:
        print("not found")
        return 1
    print(f"session_id={row['session_id']}")
    print(f"tmux_target={row['tmux_target']}")
    print(f"source={row['source']}")
    print(f"updated_at={row['updated_at']}")
    return 0


def cmd_list(conn: sqlite3.Connection, args: argparse.Namespace) -> int:
    rows = conn.execute(
        """
        SELECT session_id, tmux_target, source, updated_at
        FROM session_tmux_map
        ORDER BY updated_at DESC
        LIMIT ?
        """,
        (args.limit,),
    ).fetchall()
    for row in rows:
        print(f"{row['updated_at']} | {row['session_id']} -> {row['tmux_target']} ({row['source']})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage session_id <-> tmux_target mapping in sqlite")
    parser.add_argument("--db", default=DEFAULT_DB)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_set = sub.add_parser("set")
    p_set.add_argument("--session-id", required=True)
    p_set.add_argument("--tmux-target", required=True)
    p_set.add_argument("--source", default="manual")

    p_get = sub.add_parser("get")
    p_get.add_argument("--session-id", required=True)

    p_list = sub.add_parser("list")
    p_list.add_argument("--limit", type=int, default=50)

    args = parser.parse_args()

    conn = sqlite3.connect(args.db)
    conn.row_factory = sqlite3.Row
    try:
        ensure_table(conn)
        if args.cmd == "set":
            return cmd_set(conn, args)
        if args.cmd == "get":
            return cmd_get(conn, args)
        return cmd_list(conn, args)
    finally:
        conn.close()


if __name__ == "__main__":
    raise SystemExit(main())
