<template>
  <DashboardLayout active="projects">
    <div class="topbar">
      <div>
        <div class="eyebrow">Workspace</div>
        <div class="title">{{ displayProjectName(project) }}</div>
        <div v-if="displayProjectName(project) !== (project?.project_id || projectId)" class="subtitle" style="margin:4px 0 0;font-size:12px;color:var(--text-tertiary);">ID: {{ project?.project_id || projectId }}</div>
      </div>
      <div class="inline-actions">
        <button class="icon-btn" title="Commit & Push to Git" :disabled="commitLoading" @click="doCommit"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/></svg></button>
        <RouterLink class="icon-btn" to="/dashboard/projects" title="Back to Projects"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg></RouterLink>
        <RouterLink class="icon-btn" to="/dashboard/tasks" title="Tasks"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg></RouterLink>
        <RouterLink class="icon-btn" to="/dashboard/ideas" title="Ideas"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.9.27-1.48.27-2.23A4.88 4.88 0 0 0 12 7a4.88 4.88 0 0 0-3.36 4.77c0 .75.09 1.33.27 2.23"/><path d="M12 2v2"/><path d="M4.22 4.22l1.42 1.42"/><path d="M19.78 4.22l-1.42 1.42"/></svg></RouterLink>
      </div>
    </div>

    <div class="detail-layout">
      <div class="card">
        <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:10px;">
          <div>
            <div style="font-weight:600;">Agent Threads</div>
          </div>
          <button class="icon-btn" title="Reload" @click="reloadAll"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
        </div>

        <div class="thread-shell">
          <div class="thread-list-column">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
              <span class="subtitle" style="margin:0;">Threads ({{ threads.length }})</span>
              <button v-if="selectedThreadId" class="icon-btn" title="Clear selection" @click="startNewThread"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
            </div>
            <div v-if="threadsLoading" class="subtitle">Loading threads...</div>
            <div v-else-if="threads.length === 0" class="subtitle">No threads yet. Start with something like <code>@coder fix login flow</code>.</div>
            <button
              v-for="thread in threads"
              :key="thread.id"
              class="thread-row"
              :class="{ active: Number(selectedThreadId) === Number(thread.id) }"
              @click="selectThread(thread.id)"
            >
              <div style="font-weight:600;line-height:1.4;">{{ thread.title || `Thread #${thread.id}` }}</div>
              <div class="thread-row-meta">
                <span>#{{ thread.id }}</span>
                <span>{{ thread.message_count || 0 }} msgs</span>
              </div>
              <div class="subtitle" style="margin:6px 0 0;line-height:1.5;">{{ summarizeThread(thread) }}</div>
            </button>
          </div>

          <div class="thread-main-column">
            <div class="card">
              <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:12px;margin-bottom:10px;">
                <div>
                  <div style="font-weight:600;">Thread Timeline</div>
                </div>
                <span v-if="selectedThread" class="chip" style="margin-top:0;">#{{ selectedThread.id }} · {{ selectedThread.status || 'open' }}</span>
              </div>

              <div v-if="timelineLoading" class="subtitle">Loading timeline...</div>
              <div v-else-if="!selectedThreadId" class="subtitle">Select a thread to inspect its timeline.</div>
              <div v-else-if="timeline.length === 0" class="subtitle">This thread has no timeline events yet.</div>
              <div ref="timelineScrollRef" v-else class="chat-stack custom-scroll timeline-scroll-area" @scroll="onTimelineScroll">
                <div v-for="(item, idx) in timeline" :key="itemKey(item, idx)" :class="chatRowClass(item)">
                  <div style="max-width:82%;">
                    <div :class="chatBubbleClass(item)">{{ chatSummary(item) }}</div>
                    <div class="chat-meta">{{ chatMeta(item) }}</div>
                  </div>
                </div>
              </div>
            </div>

            <div class="card thread-composer-card">
              <div style="font-weight:600;margin-bottom:6px;">Send command</div>
              <div class="subtitle" style="margin:0 0 10px;">
                <code>@{{ activeAgent }}</code>
              </div>
              <textarea
                ref="textareaRef"
                v-model="instruction"
                class="input composer-textarea"
                placeholder="e.g. @coder fix the auth race condition and summarize root cause"
                @input="onInstructionInput"
                @keydown="onComposerKeydown"
              />
              <div
                v-if="mentionQuery !== null && filteredAgents.length > 0"
                style="background:#171c25;border:1px solid rgba(148,163,184,0.26);border-radius:10px;margin-top:4px;overflow:hidden;"
              >
                <div
                  v-for="(agent, idx) in filteredAgents"
                  :key="agent.agent_name"
                  :style="{ padding: '8px 12px', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '8px', borderBottom: '1px solid rgba(148,163,184,0.12)', background: idx === mentionIndex ? 'rgba(56,189,248,0.15)' : '' }"
                  @mousedown.prevent="insertMention(agent.agent_name)"
                >
                  <span style="font-weight:600;color:#38bdf8;">@{{ agent.agent_name }}</span>
                  <span class="subtitle" style="margin:0;">{{ agent.description || agent.role || agent.backend }}</span>
                </div>
              </div>
              <div style="display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin-top:10px;">
                <button class="icon-btn" :disabled="sending" title="Send" @click="sendCommand"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>
                <span class="chip mobile-hide-cmd" style="margin-top:0;">Cmd+Enter 发送 · Suggested: @hermes · @coder · @reviewer · @summary</span>
              </div>
              <div v-if="sendError" class="subtitle" style="margin:10px 0 0;color:#fca5a5;">{{ sendError }}</div>
              <div v-else-if="sendOk" class="subtitle" style="margin:10px 0 0;color:#86efac;">
                Task #{{ sendOk.task_id }} enqueued to thread #{{ sendOk.thread_id }} for @{{ sendOk.agent_name }}
                <span v-if="pollStatus">· {{ pollStatus }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="side-stack">
        <div class="card side-info-card">
          <div style="font-weight:700;margin-bottom:10px;font-size:14px;">Status</div>
          <div v-if="loading">
            <div class="skeleton skeleton-text" style="width:30%;margin-bottom:10px;"></div>
            <div class="skeleton skeleton-text medium"></div>
          </div>
          <div v-else-if="error" style="padding:10px 12px;background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.2);border-radius:8px;color:#fca5a5;font-size:12.5px;">{{ error }}</div>
          <div v-else>
            <div style="display:flex;align-items:center;gap:8px;margin-bottom:8px;flex-wrap:wrap;">
              <span class="chip" :style="statusChipStyle(projectStatus)">{{ projectStatus }}</span>
              <span class="subtitle" style="margin:0;">{{ project?.path || '-' }}</span>
            </div>
            <div style="font-size:12px;color:var(--muted);margin-bottom:8px;">Tasks: {{ project?.counts?.total || 0 }} (pending {{ project?.counts?.pending || 0 }} · running {{ project?.counts?.running || 0 }} · done {{ project?.counts?.done || 0 }} · failed {{ project?.counts?.failed || 0 }})</div>
            <div style="font-size:12px;color:var(--muted);">Latest Run: {{ project?.latest_run_status || '-' }}</div>
            <div style="font-size:12px;color:var(--muted);margin-top:4px;">Threads: {{ threads.length }}</div>
            <div v-if="commitResult" style="margin-top:10px;padding:8px 10px;border-radius:8px;font-size:12px;line-height:1.5;" :style="commitResult.ok ? 'background:rgba(52,211,153,0.08);border:1px solid rgba(52,211,153,0.15);color:#34d399;' : 'background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.15);color:#fca5a5;'">
              <div v-if="commitResult.ok">
                <div>✅ Task #{{ commitResult.task_id }} enqueued for @{{ commitResult.agent_name }}</div>
                <div class="subtitle" style="margin-top:4px;">Hermes will handle commit message, git profile, and push.</div>
              </div>
              <div v-else>❌ {{ commitResult.error }}</div>
            </div>
          </div>
        </div>

        <div class="card side-info-card">
          <div style="font-weight:600;margin-bottom:8px;">Configuration</div>
          <label style="display:flex;align-items:flex-start;justify-content:space-between;gap:12px;cursor:pointer;">
            <div>
              <div style="font-weight:600;">autoresearch</div>
              <div class="subtitle" style="margin:6px 0 0;">默认关闭。打开后，项目后续任务可读取到该项目开启了自主进化/autoresearch 配置。</div>
            </div>
            <input
              type="checkbox"
              :checked="Boolean(project?.autoresearch)"
              :disabled="loading || configSaving"
              @change="onAutoresearchToggle"
            />
          </label>
          <div class="subtitle" style="margin-top:10px;">
            当前状态：{{ project?.autoresearch ? '已开启' : '已关闭' }}
            <span v-if="configSaving"> · 保存中...</span>
          </div>
          <div v-if="configError" class="subtitle" style="margin-top:8px;color:#fca5a5;">{{ configError }}</div>
        </div>

        <div class="card side-info-card side-info-card--progress">
          <div style="font-weight:600;margin-bottom:8px;">Latest Progress</div>
          <div v-if="loading" class="subtitle">Loading...</div>
          <div v-else-if="!project?.latest_progress && !project?.latest_memory_summary" class="subtitle">No progress recorded yet.</div>
          <div v-else class="custom-scroll" style="font-size:12px;line-height:1.7;white-space:pre-wrap;max-height:200px;overflow-y:auto;">{{ progressSummary(project?.latest_progress || project?.latest_memory_summary) }}</div>
        </div>

        <div v-if="project?.autoresearch" class="card side-info-card side-info-card--proposals">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
            <div style="font-weight:600;">Research Proposals</div>
            <button class="icon-btn" title="Reload" @click="reloadProposals"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
          </div>
          <div v-if="proposalsLoading" class="subtitle">Loading proposals...</div>
          <div v-else-if="proposals.length === 0" class="subtitle">No proposals yet.</div>
          <div v-else class="side-stack" style="gap:8px;">
            <div
              v-for="p in proposals"
              :key="p.id"
              class="list-card"
            >
              <div style="display:flex;justify-content:space-between;align-items:center;gap:8px;">
                <span class="chip" style="margin-top:0;">{{ p.status }}</span>
                <span class="subtitle" style="margin:0;white-space:nowrap;">{{ formatTs(p.created_at) }}</span>
              </div>
              <div class="subtitle" style="margin:6px 0 0;white-space:pre-wrap;max-height:120px;overflow-y:auto;">{{ p.proposal }}</div>
              <div v-if="p.status === 'pending'" style="display:flex;gap:8px;margin-top:8px;">
                <button
                  class="btn small"
                  :disabled="proposalActionId === p.id"
                  @click="doApproveProposal(p.id)"
                >
                  Approve
                </button>
                <button
                  class="btn small"
                  style="background:#4a232a;border-color:#4a232a;"
                  :disabled="proposalActionId === p.id"
                  @click="doRejectProposal(p.id)"
                >
                  Reject
                </button>
              </div>
            </div>
          </div>
        </div>

        <div class="card side-info-card side-info-card--agents">
          <div style="font-weight:600;margin-bottom:8px;">Agent Roster</div>
          <div v-if="agentsLoading" class="subtitle">Loading agents...</div>
          <div v-else-if="agents.length === 0" class="subtitle">No agents configured.</div>
          <div v-else class="side-stack" style="gap:8px;">
            <div
              v-for="agent in agents"
              :key="agent.agent_name"
              class="list-card"
              :style="String(agent.agent_name) === String(activeAgent) ? 'border:1px solid #50617e;background:#1b2230;' : ''"
            >
              <div style="display:flex;justify-content:space-between;gap:8px;align-items:center;">
                <div style="font-weight:600;">@{{ agent.agent_name }}</div>
                <span class="chip" style="margin-top:0;">{{ agent.backend }}</span>
              </div>
              <div class="subtitle" style="margin:6px 0 0;">{{ agent.description || agent.role || 'Project agent' }}</div>
              <div class="thread-row-meta">
                <span>{{ agent.role || 'role n/a' }}</span>
                <span v-if="agent.toolsets">toolsets: {{ agent.toolsets }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="card side-info-card side-info-card--actions">
          <div style="font-weight:600;margin-bottom:8px;">Actions</div>
          <button class="btn" style="width:100%;margin-bottom:6px;" @click="reloadAll">Reload</button>
          <button class="btn" style="width:100%;margin-bottom:6px;" @click="startNewThread">Clear thread selection</button>
          <button class="btn" style="width:100%;background:#4a232a;border-color:#4a232a;" @click="doDelete">Delete Project</button>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import {
  approveResearchProposal,
  commitProjectToGit,
  deleteProject,
  getProjectAgents,
  getProjectById,
  getProjectThread,
  getProjectThreads,
  getResearchProposals,
  rejectResearchProposal,
  sendHermesFollowup,
  updateProjectConfig
} from '../api'

const route = useRoute()
const router = useRouter()
const project = ref(null)
const loading = ref(false)
const error = ref('')
const instruction = ref('')
const sending = ref(false)
const sendError = ref('')
const sendOk = ref(null)
const threads = ref([])
const threadsLoading = ref(false)
const selectedThreadId = ref(null)
const selectedThread = ref(null)
const timeline = ref([])
const timelineLoading = ref(false)
const agents = ref([])
const agentsLoading = ref(false)
const pollInterval = ref(null)
const pollStatus = ref('')
const configSaving = ref(false)
const configError = ref('')
const commitLoading = ref(false)
const commitResult = ref(null)
const proposals = ref([])
const proposalsLoading = ref(false)
const proposalActionId = ref(null)
const expandedKeys = ref(new Set())
const textareaRef = ref(null)
const timelineScrollRef = ref(null)
const mentionQuery = ref(null)
const mentionIndex = ref(0)
const syncInterval = ref(null)
let timelineRequestToken = 0
let userManuallyScrolled = false
let lastAutoScrollTime = 0

const projectId = computed(() => decodeURIComponent(route.params.id))

const projectStatus = computed(() => {
  const counts = project.value?.counts || {}
  if ((counts.running || 0) > 0) return 'running'
  if ((counts.pending || 0) > 0) return 'pending'
  if ((counts.failed || 0) > 0) return 'failed'
  if ((counts.done || 0) > 0) return 'done'
  return 'idle'
})

const activeAgent = computed(() => {
  const fromSend = sendOk.value?.agent_name
  if (fromSend) return String(fromSend)
  const text = instruction.value || ''
  const match = text.match(/@([a-zA-Z0-9_-]+)/)
  return match ? match[1] : 'hermes'
})

const filteredAgents = computed(() => {
  if (mentionQuery.value === null) return []
  const q = mentionQuery.value.toLowerCase()
  return agents.value.filter(a => (a.agent_name || '').toLowerCase().includes(q))
})

function statusChipStyle(status) {
  const map = {
    running: { background: 'rgba(56,189,248,0.1)', borderColor: 'rgba(56,189,248,0.15)', color: '#38bdf8' },
    pending: { background: 'rgba(251,191,36,0.1)', borderColor: 'rgba(251,191,36,0.15)', color: '#fbbf24' },
    failed:  { background: 'rgba(248,113,113,0.1)', borderColor: 'rgba(248,113,113,0.15)', color: '#f87171' },
    done:    { background: 'rgba(52,211,153,0.1)', borderColor: 'rgba(52,211,153,0.15)', color: '#34d399' },
    idle:    { background: 'var(--chip)', borderColor: 'rgba(255,255,255,0.04)', color: 'var(--text-secondary)' }
  }
  return map[status] || map.idle
}

function formatTs(value) {
  if (!value) return '-'
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return String(value)
  return d.toLocaleString()
}

function summarizeThread(thread) {
  const text = String(thread?.latest_message_excerpt || '').trim()
  if (!text) return 'No messages yet.'
  return text.length > 88 ? `${text.slice(0, 85)}...` : text
}

function itemKey(item, idx) {
  return `${item.type || 'item'}-${item.id || item.task_id || idx}`
}

function chatRowClass(item) {
  const sender = String(item?.sender_type || '')
  const eventType = String(item?.event_type || '')
  if (sender === 'human') return 'chat-row human'
  if (eventType === 'task_enqueued') return 'chat-row muted'
  if (eventType === 'task_run') return 'chat-row system'
  return 'chat-row agent'
}

function chatBubbleClass(item) {
  const sender = String(item?.sender_type || '')
  const eventType = String(item?.event_type || '')
  if (sender === 'human') return 'chat-bubble human'
  if (eventType === 'task_enqueued') return 'chat-bubble muted'
  if (eventType === 'task_run') return 'chat-bubble system'
  return 'chat-bubble agent'
}

function extractCodexIntent(text) {
  // Try to extract the human-readable intent from a codex payload
  if (!text) return ''
  const t = String(text)
  // Look for the first agent_message text
  const match = t.match(/"text":"([^"]+)"/)
  if (match) return match[1]
  // Look for error messages
  const errMatch = t.match(/"message":"([^"]+)"/)
  if (errMatch) return errMatch[1]
  return t.slice(0, 200)
}

function chatSummary(item) {
  const eventType = String(item?.event_type || '')
  const sender = String(item?.sender_type || '')

  // Human instruction
  if (sender === 'human') {
    return item?.content || ''
  }

  // Task enqueued notification
  if (eventType === 'task_enqueued') {
    const content = String(item?.content || '')
    // Convert English system message to concise Chinese
    const m = content.match(/Enqueued task #(\d+) for @([\w-]+)/)
    if (m) return `已分配任务 #${m[1]} 给 @${m[2]}`
    return content || `已分配任务 #${item?.task_id}`
  }

  // Task run result
  if (eventType === 'task_run') {
    const status = String(item?.run_status || item?.status || '')
    const summary = item?.summary || ''
    const error = item?.last_error || ''

    if (status === 'done') {
      if (summary) {
        const intent = extractCodexIntent(summary)
        return intent || '任务已完成'
      }
      return '任务已完成'
    }
    if (status === 'failed') {
      return error ? `执行失败：${String(error).slice(0, 120)}` : '执行失败'
    }
    if (status === 'running') {
      return '正在执行中...'
    }
    return `任务状态：${status}`
  }

  // Agent / system message
  return item?.content || item?.summary || ''
}

function chatMeta(item) {
  const sender = String(item?.sender_type || '')
  const eventType = String(item?.event_type || '')
  const name = item?.sender_name || ''
  const time = formatTs(item?.created_at)

  if (sender === 'human') {
    return `你 · ${time}`
  }
  if (eventType === 'task_enqueued') {
    return `系统 · ${time}`
  }
  if (eventType === 'task_run') {
    const status = String(item?.run_status || item?.status || '')
    return `${name || 'Agent'} · ${status} · ${time}`
  }
  return `${name || 'Agent'} · ${time}`
}

function displayProjectName(p) {
  if (!p) return projectId.value
  if (p.aliases) {
    const first = String(p.aliases).split(',')[0].trim()
    if (first && first !== p.project_id) return first
  }
  return p.project_id || projectId.value
}

function progressSummary(raw) {
  if (!raw) return ''
  const lines = String(raw).split('\n').filter(Boolean)
  const events = []
  for (const line of lines) {
    try {
      events.push(JSON.parse(line))
    } catch {
      // ignore non-JSON lines, keep as plain text
    }
  }

  // If no JSON events found, treat as plain text and truncate
  if (events.length === 0) {
    const t = String(raw).trim()
    return t.length > 400 ? t.slice(0, 400) + '...' : t
  }

  const parts = []
  for (const e of events) {
    if (e.type === 'item.completed' && e.item?.type === 'agent_message' && e.item?.text) {
      parts.push(String(e.item.text).trim())
    } else if (e.type === 'error' && e.message) {
      parts.push(`⚠️ ${String(e.message).trim()}`)
    } else if (e.type === 'item.completed' && e.item?.type === 'command_execution' && e.item?.exit_code !== null && e.item?.exit_code !== 0) {
      parts.push(`⚠️ Command failed (exit ${e.item.exit_code}): ${String(e.item.command || '').slice(0, 60)}`)
    }
  }

  const unique = []
  for (const p of parts) {
    if (!unique.includes(p)) unique.push(p)
  }
  return unique.slice(-5).join('\n\n') || String(raw).trim().slice(0, 400)
}

function isNearBottom(el, threshold = 30) {
  if (!el) return true
  return el.scrollHeight - el.scrollTop - el.clientHeight < threshold
}

function scrollToBottom(force = false) {
  if (!timelineScrollRef.value) return
  const el = timelineScrollRef.value
  if (!force && userManuallyScrolled && !isNearBottom(el)) return
  lastAutoScrollTime = Date.now()
  const doScroll = () => {
    if (timelineScrollRef.value === el) {
      el.scrollTo({ top: el.scrollHeight, behavior: 'auto' })
    }
  }
  doScroll()
  requestAnimationFrame(() => {
    doScroll()
    requestAnimationFrame(() => {
      doScroll()
    })
  })
}

function onTimelineScroll() {
  if (Date.now() - lastAutoScrollTime < 100) return
  const el = timelineScrollRef.value
  if (!el) return
  if (isNearBottom(el)) {
    userManuallyScrolled = false
  } else {
    userManuallyScrolled = true
  }
}

function onInstructionInput() {
  const el = textareaRef.value
  if (!el) {
    mentionQuery.value = null
    mentionIndex.value = 0
    return
  }
  const cursor = el.selectionStart
  const text = instruction.value
  const beforeCursor = text.slice(0, cursor)
  const match = beforeCursor.match(/@([a-zA-Z0-9_-]*)$/)
  if (match) {
    mentionQuery.value = match[1]
    mentionIndex.value = 0
  } else {
    mentionQuery.value = null
    mentionIndex.value = 0
  }
}

function onComposerKeydown(e) {
  if (e.key === 'Enter' && e.metaKey && !e.shiftKey && !e.altKey && !e.ctrlKey) {
    e.preventDefault()
    if (!sending.value) {
      sendCommand()
    }
    return
  }
  if (mentionQuery.value === null || filteredAgents.value.length === 0) return
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    mentionIndex.value = (mentionIndex.value + 1) % filteredAgents.value.length
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    mentionIndex.value = (mentionIndex.value - 1 + filteredAgents.value.length) % filteredAgents.value.length
  } else if (e.key === 'Enter') {
    e.preventDefault()
    const agent = filteredAgents.value[mentionIndex.value]
    if (agent) insertMention(agent.agent_name)
  } else if (e.key === 'Escape') {
    mentionQuery.value = null
    mentionIndex.value = 0
  }
}

function insertMention(agentName) {
  const el = textareaRef.value
  if (!el) return
  const cursor = el.selectionStart
  const text = instruction.value
  const beforeCursor = text.slice(0, cursor)
  const afterCursor = text.slice(cursor)
  const newBefore = beforeCursor.replace(/@[a-zA-Z0-9_-]*$/, `@${agentName} `)
  instruction.value = newBefore + afterCursor
  mentionQuery.value = null
  mentionIndex.value = 0
  nextTick(() => {
    el.focus()
    const pos = newBefore.length
    el.setSelectionRange(pos, pos)
  })
}

async function reloadProject() {
  loading.value = true
  error.value = ''
  try {
    const data = await getProjectById(projectId.value)
    project.value = data.project || null
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'load project failed'
  } finally {
    loading.value = false
  }
}

async function reloadThreads({ preserveSelection = true } = {}) {
  threadsLoading.value = true
  try {
    const data = await getProjectThreads(projectId.value, 100)
    threads.value = data.threads || []
    const hasCurrent = threads.value.some((thread) => Number(thread.id) === Number(selectedThreadId.value))
    if (!preserveSelection || !hasCurrent) {
      selectedThreadId.value = threads.value[0]?.id || null
    }
  } catch (err) {
    sendError.value = err instanceof Error ? err.message : 'load threads failed'
    threads.value = []
    selectedThreadId.value = null
  } finally {
    threadsLoading.value = false
  }
}

async function reloadAgents() {
  agentsLoading.value = true
  try {
    const data = await getProjectAgents(projectId.value)
    agents.value = data.agents || []
  } catch (err) {
    sendError.value = err instanceof Error ? err.message : 'load agents failed'
    agents.value = []
  } finally {
    agentsLoading.value = false
  }
}

async function reloadTimeline({ background = false } = {}) {
  if (!selectedThreadId.value) {
    selectedThread.value = null
    timeline.value = []
    return
  }
  const requestToken = ++timelineRequestToken
  const showLoading = !background || timeline.value.length === 0
  if (showLoading) {
    timelineLoading.value = true
  }
  try {
    const data = await getProjectThread(projectId.value, selectedThreadId.value)
    if (requestToken !== timelineRequestToken) return
    selectedThread.value = data.thread || null
    const raw = data.timeline || []
    timeline.value = raw.slice().sort((a, b) => new Date(a.created_at || 0) - new Date(b.created_at || 0))
    await nextTick()
    if (requestToken !== timelineRequestToken) return
    scrollToBottom(!background)
  } catch (err) {
    if (requestToken !== timelineRequestToken) return
    sendError.value = err instanceof Error ? err.message : 'load timeline failed'
    if (!background) {
      selectedThread.value = null
      timeline.value = []
    }
  } finally {
    if (requestToken === timelineRequestToken && showLoading) {
      timelineLoading.value = false
    }
  }
}

async function reloadProposals() {
  if (!projectId.value) return
  proposalsLoading.value = true
  try {
    const data = await getResearchProposals(projectId.value, null, 50)
    proposals.value = data.proposals || []
  } catch (err) {
    proposals.value = []
  } finally {
    proposalsLoading.value = false
  }
}

async function doApproveProposal(id) {
  proposalActionId.value = id
  try {
    await approveResearchProposal(projectId.value, id)
    await reloadProposals()
  } catch (err) {
    sendError.value = err instanceof Error ? err.message : 'approve failed'
  } finally {
    proposalActionId.value = null
  }
}

async function doRejectProposal(id) {
  proposalActionId.value = id
  try {
    await rejectResearchProposal(projectId.value, id)
    await reloadProposals()
  } catch (err) {
    sendError.value = err instanceof Error ? err.message : 'reject failed'
  } finally {
    proposalActionId.value = null
  }
}

async function reloadAll() {
  await reloadProject()
  await reloadAgents()
  await reloadThreads()
  await reloadTimeline()
  if (project.value?.autoresearch) {
    await reloadProposals()
  } else {
    proposals.value = []
  }
  // Mark this project as seen now that the latest state has been loaded
  localStorage.setItem(`project_last_seen_${projectId.value}`, String(Date.now()))
}

async function selectThread(threadId) {
  selectedThreadId.value = threadId
  userManuallyScrolled = false
  await reloadTimeline()
}

function startNewThread() {
  selectedThreadId.value = null
  selectedThread.value = null
  timeline.value = []
  sendOk.value = null
  sendError.value = ''
  stopPollTimeline()
  pollStatus.value = ''
}

async function doCommit() {
  commitLoading.value = true
  commitResult.value = null
  try {
    const data = await commitProjectToGit(projectId.value)
    commitResult.value = { ok: true, ...data }
  } catch (err) {
    commitResult.value = { ok: false, error: err instanceof Error ? err.message : 'commit failed' }
  } finally {
    commitLoading.value = false
  }
}

async function doDelete() {
  if (!confirm(`Delete project "${projectId.value}"? This will remove all related tasks and runs.`)) return
  try {
    await deleteProject(projectId.value)
    router.push('/dashboard/projects')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'delete failed'
  }
}

async function onAutoresearchToggle(event) {
  const checked = Boolean(event?.target?.checked)
  const previous = Boolean(project.value?.autoresearch)
  configSaving.value = true
  configError.value = ''
  if (project.value) {
    project.value = { ...project.value, autoresearch: checked }
  }
  try {
    const data = await updateProjectConfig(projectId.value, { autoresearch: checked })
    if (data?.project) {
      project.value = data.project
    }
  } catch (err) {
    if (project.value) {
      project.value = { ...project.value, autoresearch: previous }
    }
    configError.value = err instanceof Error ? err.message : 'update config failed'
  } finally {
    configSaving.value = false
  }
}

async function sendCommand() {
  if (!instruction.value.trim()) {
    sendError.value = '请输入指令后再发送'
    return
  }
  sending.value = true
  sendError.value = ''
  sendOk.value = null
  stopPollTimeline()
  try {
    const data = await sendHermesFollowup(
      projectId.value,
      instruction.value.trim(),
      undefined,
      selectedThreadId.value || undefined,
      true
    )
    sendOk.value = {
      task_id: data.task_id,
      session_id: data.session_id,
      thread_id: data.thread_id,
      message_id: data.message_id,
      agent_name: data.agent_name
    }
    instruction.value = ''
    mentionQuery.value = null
    mentionIndex.value = 0
    selectedThreadId.value = data.thread_id
    await reloadAll()
    scrollToBottom(true)
    startPollTimeline()
  } catch (err) {
    sendError.value = err instanceof Error ? err.message : 'send failed'
  } finally {
    sending.value = false
  }
}

function startPollTimeline() {
  stopPollTimeline()
  pollStatus.value = '等待执行...'
  let count = 0
  const maxPolls = 30
  pollInterval.value = setInterval(async () => {
    count++
    await reloadTimeline({ background: true })
    const runItem = timeline.value.find((item) => item.event_type === 'task_run' && item.task_id === sendOk.value?.task_id)
    if (runItem) {
      const status = runItem.run_status || runItem.status || 'queued'
      if (status === 'running') {
        pollStatus.value = '执行中...'
      } else if (status === 'done') {
        pollStatus.value = '已完成'
        stopPollTimeline()
      } else if (status === 'failed') {
        pollStatus.value = '执行失败'
        stopPollTimeline()
      }
    }
    if (count >= maxPolls) {
      pollStatus.value = '已停止轮询'
      stopPollTimeline()
    }
  }, 3000)
}

function stopPollTimeline() {
  if (pollInterval.value) {
    clearInterval(pollInterval.value)
    pollInterval.value = null
  }
}

onMounted(() => {
  reloadAll()
  syncInterval.value = setInterval(() => {
    if (selectedThreadId.value) {
      reloadTimeline({ background: true })
    }
  }, 5000)
})
onUnmounted(() => {
  stopPollTimeline()
  if (syncInterval.value) {
    clearInterval(syncInterval.value)
    syncInterval.value = null
  }
})
</script>
