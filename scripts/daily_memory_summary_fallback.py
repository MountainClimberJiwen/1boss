#!/usr/bin/env python3
import argparse
import datetime as dt
import glob
import json
import os
import re
from collections import Counter
from pathlib import Path

SESSION_ROOT = os.path.expanduser("~/.codex/sessions")
MEMORY_FILE = "/Users/jiwen/PycharmProjects/memory.md"
LOCAL_TZ = dt.datetime.now().astimezone().tzinfo


def parse_date(s: str) -> dt.date:
    return dt.datetime.strptime(s, "%Y-%m-%d").date()


def first_user_text(path: str):
    try:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                if obj.get("type") == "response_item":
                    item = obj.get("payload", {})
                    if item.get("type") == "message" and item.get("role") == "user":
                        out = []
                        for c in item.get("content", []):
                            if c.get("type") == "input_text" and c.get("text"):
                                out.append(c["text"])
                        txt = "\n".join(out).strip()
                        if txt:
                            return txt
    except Exception:
        return None
    return None


def classify(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["pr", "pull request", "review", "github", "ci"]):
        return "代码评审/PR"
    if any(k in t for k in ["cron", "launchd", "定时", "脚本", "automation", "自动"]):
        return "自动化与运维"
    if any(k in t for k in ["ios", "xcode", "swift", "simulator"]):
        return "iOS开发"
    if any(k in t for k in ["sql", "sqlite", "db", "database", "query"]):
        return "数据与查询"
    if any(k in t for k in ["wechat", "公众号", "adb", "phone", "android", "ollama"]):
        return "手机自动化/多模态"
    return "其他开发任务"


def get_session_files_for_day(target_day: dt.date):
    day_dir = os.path.join(
        SESSION_ROOT,
        target_day.strftime("%Y"),
        target_day.strftime("%m"),
        target_day.strftime("%d"),
    )
    if not os.path.isdir(day_dir):
        return []
    return sorted(glob.glob(os.path.join(day_dir, "*.jsonl")))


def get_existing_dates(memory_text: str):
    dates = set(re.findall(r"##\s+(\d{4}-\d{2}-\d{2})\s+Codex", memory_text))
    return dates


def build_summary_block(target_day: dt.date, prompts):
    groups = Counter(classify(p) for p in prompts)
    now = dt.datetime.now(tz=LOCAL_TZ).strftime("%Y-%m-%d %H:%M:%S %z")

    lines = []
    lines.append(f"\n## {target_day.isoformat()} Codex 事项分析（fallback）")
    lines.append(f"time: {now}")
    lines.append("source: local ~/.codex/sessions")
    lines.append("")

    idx = 1
    for cat, count in groups.most_common():
        lines.append(f"{idx}. {cat}")
        lines.append(f"- 做的事情：处理与“{cat}”相关的会话任务（{count} 条会话）。")
        lines.append("- 想解决的问题：推进对应事项落地并消除执行阻塞。")
        lines.append("- 使用的方法：读取本地 session 首条用户请求并按关键词归类汇总。")
        idx += 1

    lines.append("")
    return "\n".join(lines)


def append_for_day(target_day: dt.date) -> bool:
    mem_path = Path(MEMORY_FILE)
    mem_path.parent.mkdir(parents=True, exist_ok=True)
    existing = mem_path.read_text(encoding="utf-8") if mem_path.exists() else ""

    if target_day.isoformat() in get_existing_dates(existing):
        return False

    files = get_session_files_for_day(target_day)
    prompts = []
    for p in files:
        txt = first_user_text(p)
        if txt:
            prompts.append(txt)

    if not prompts:
        return False

    block = build_summary_block(target_day, prompts)
    with open(mem_path, "a", encoding="utf-8") as f:
        f.write(block)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target-date", help="YYYY-MM-DD")
    parser.add_argument("--start-date", help="YYYY-MM-DD")
    parser.add_argument("--end-date", help="YYYY-MM-DD")
    args = parser.parse_args()

    updated = 0
    if args.start_date and args.end_date:
        d = parse_date(args.start_date)
        end = parse_date(args.end_date)
        while d <= end:
            if append_for_day(d):
                updated += 1
            d += dt.timedelta(days=1)
    else:
        if args.target_date:
            target = parse_date(args.target_date)
        else:
            target = dt.datetime.now(tz=LOCAL_TZ).date() - dt.timedelta(days=1)
        if append_for_day(target):
            updated += 1

    print(f"UPDATED_BLOCKS={updated}")


if __name__ == "__main__":
    main()
