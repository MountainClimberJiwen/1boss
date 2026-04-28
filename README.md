# iboss

`iboss` 是一个聚合工程，用于把 `project-task-enqueue` 相关能力放到同一处管理，尽量不移动现有脚本。

## 目标
- 聚合 `project-task-enqueue` skill
- 聚合 Codex session 监控与钉钉通知
- 聚合 dashboard / backend 启动入口
- 提供离线分析 project / session / task 状态入口

## 目录

```text
iboss/
├── README.md
├── links/
│   ├── task-queue-system -> /Users/jiwen/PycharmProjects/task-queue-system
│   ├── skill-project-task-enqueue -> /Users/jiwen/PycharmProjects/openclaw/.cursor/skills/project-task-enqueue
│   ├── codex_approval_watcher.py -> /Users/jiwen/PycharmProjects/task-queue-system/data/codex_approval_watcher.py
│   └── tmux_auto_approve.py -> /Users/jiwen/PycharmProjects/task-queue-system/scripts/tmux_auto_approve.py
├── scripts/
│   ├── run_backend.sh
│   ├── run_dispatcher.sh
│   ├── run_session_watcher.sh
│   ├── enqueue_skill_task.sh
│   └── open_dashboard.sh
└── analytics/
    └── offline_analyze.py
```

## 入口说明

1. 启动 backend + dashboard（同一个 API 服务）

```bash
cd ~/PycharmProjects/iboss
./scripts/run_backend.sh
```

前端联调（Vue）：

```bash
./scripts/run_frontend.sh
# 默认: http://127.0.0.1:5173
```

说明：
- `vue` 开发服务器已通过 `vite proxy` 代理 `/api` 到 `http://127.0.0.1:8080`
- `scripts/run_backend.sh` 现在默认关闭本地鉴权（`TASK_QUEUE_DASHBOARD_AUTH_ENABLED=0`），方便联调；可自行覆盖该环境变量重新开启

2. 获取 dashboard 地址

```bash
./scripts/open_dashboard.sh
# 默认输出: http://127.0.0.1:8080/dashboard
```

2.1 开机后台自启动（launchd）

当前 dashboard 相关启动项：
- Backend/API: `/Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.backend-8080.plist`
- Frontend/Vite: `/Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.frontend-5173.plist`

对应脚本：
- `/Users/jiwen/PycharmProjects/iboss/scripts/run_backend_launchd.sh`
- `/Users/jiwen/PycharmProjects/iboss/scripts/run_frontend_launchd.sh`

常用维护命令：

```bash
launchctl print gui/$(id -u)/com.jiwen.iboss.backend-8080
launchctl print gui/$(id -u)/com.jiwen.iboss.frontend-5173

launchctl bootout gui/$(id -u) /Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.backend-8080.plist 2>/dev/null || true
launchctl bootstrap gui/$(id -u) /Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.backend-8080.plist
launchctl enable gui/$(id -u)/com.jiwen.iboss.backend-8080

launchctl bootout gui/$(id -u) /Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.frontend-5173.plist 2>/dev/null || true
launchctl bootstrap gui/$(id -u) /Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.frontend-5173.plist
launchctl enable gui/$(id -u)/com.jiwen.iboss.frontend-5173
```

3. 启动 dispatcher

```bash
./scripts/run_dispatcher.sh
```

4. 启动 Codex session 监控（包含钉钉消息发送逻辑）

```bash
./scripts/run_session_watcher.sh
```

5. 通过 skill 脚本入队任务

```bash
./scripts/enqueue_skill_task.sh "修复任务调度超时"
```

6. 离线分析 project/session/task 状态

```bash
python3 ./analytics/offline_analyze.py
python3 ./analytics/offline_analyze.py --json
```

## 关键事实
- 未移动原始代码路径，主要通过软链接和 wrapper 脚本聚合。
- `session` 监控与钉钉发送使用现有实现：
  - `/Users/jiwen/PycharmProjects/task-queue-system/data/codex_approval_watcher.py`
- `project-task-enqueue` skill 使用现有实现：
  - `/Users/jiwen/PycharmProjects/openclaw/.cursor/skills/project-task-enqueue`

## 可选环境变量
- `TASK_QUEUE_DB_PATH`
- `TASK_QUEUE_API_HOST`
- `TASK_QUEUE_API_PORT`
- `TASK_QUEUE_DISPATCHER_PROJECT_ID`

## Session 与 tmux 映射（SQLite 持久化）

已改为落库到 `task_queue.db` 的 `session_tmux_map` 表，字段：
- `session_id` (PK)
- `tmux_target`
- `source`
- `updated_at`

`codex_approval_watcher.py` 现在在路由时优先查这张表，再回退 `TMUX_TARGET_MAP_JSON`。

### 管理映射

新增脚本：`/Users/jiwen/PycharmProjects/iboss/scripts/session_tmux_map.py`

1. 设置映射

```bash
python3 /Users/jiwen/PycharmProjects/iboss/scripts/session_tmux_map.py set \
  --session-id "<codex_session_id>" \
  --tmux-target "%12" \
  --source manual
```

2. 查询单条

```bash
python3 /Users/jiwen/PycharmProjects/iboss/scripts/session_tmux_map.py get \
  --session-id "<codex_session_id>"
```

3. 列表查看

```bash
python3 /Users/jiwen/PycharmProjects/iboss/scripts/session_tmux_map.py list --limit 50
```

## 离线分析补充：crontab 的 Codex Session 总结

当前机器已有一个与 Codex session 总结相关的 crontab（每 3 小时）：

```cron
0 */3 * * * cd /Users/jiwen/PycharmProjects/openclaw/.cursor/skills/codex-openclaw-skill/skill-codex-openclaw && /Users/jiwen/.nvm/versions/node/v22.14.0/bin/codex exec --sandbox workspace-write "基于 /Users/jiwen/.codex/sessions 最近会话，更新 references/project-aliases.md 中的两个自动区块：Observed projects (auto) 和 Unmapped observed paths (auto)。保留 Active mappings 手工区块不改。输出简短摘要。" >> /tmp/codex-openclaw-weekly.log 2>&1
```

另外，`openclaw` 下还有“按脚本安装的 session 进展汇总 cron”能力：
- 脚本：`/Users/jiwen/PycharmProjects/openclaw/scripts/install_codex_progress_cron.sh`
- 汇总程序：`/Users/jiwen/PycharmProjects/openclaw/scripts/codex_session_progress_cron.py`
- 默认产出：`/Users/jiwen/PycharmProjects/openclaw/docs/codex_project_progress_latest.md`

说明：
- `iboss` 的 `analytics/offline_analyze.py` 负责离线统计 `task_queue.db` 中的 `project/session/task` 状态。
- 上述 crontab 与 `codex_session_progress_cron.py` 负责从 `~/.codex/sessions` 做会话级总结，二者互补。

## 定时任务：daily_memory_summary.sh

`iboss` 还有一个独立的“每日记忆汇总”任务，执行脚本：

- `/Users/jiwen/PycharmProjects/iboss/scripts/daily_memory_summary.sh`

当前使用 `launchd` 调度（不再使用 crontab），配置如下：

- LaunchAgent: `/Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.daily-memory-summary.plist`
- 调度时间：每天 `23:00`（`Hour=23`, `Minute=0`）
- 运行目录：`/Users/jiwen/PycharmProjects`

日志文件：

- 脚本日志：`/tmp/codex-daily-memory-summary.log`
- 审计日志：`/tmp/codex-daily-memory-summary-audit.log`
- launchd stdout：`/tmp/launchd-daily-memory-summary.out.log`
- launchd stderr：`/tmp/launchd-daily-memory-summary.err.log`

常用维护命令：

```bash
# 查看任务状态
launchctl print gui/$(id -u)/com.jiwen.iboss.daily-memory-summary

# 重新加载配置（修改 plist 后）
launchctl bootout gui/$(id -u) /Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.daily-memory-summary.plist 2>/dev/null || true
launchctl bootstrap gui/$(id -u) /Users/jiwen/Library/LaunchAgents/com.jiwen.iboss.daily-memory-summary.plist
launchctl enable gui/$(id -u)/com.jiwen.iboss.daily-memory-summary
```
