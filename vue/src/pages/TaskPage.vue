<template>
  <DashboardLayout active="tasks">
    <div class="topbar">
      <div>
        <div class="eyebrow">Execution</div>
        <div class="title">Tasks</div>
      </div>
      <div class="inline-actions">
        <RouterLink class="icon-btn" to="/dashboard/projects" title="Projects"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></RouterLink>
        <button class="icon-btn" title="Refresh" @click="reload"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-row">
      <div class="kpi-pill kpi-pill--running">
        <span class="kpi-pill-label">Running</span>
        <span class="kpi-pill-value">{{ runningCount }}</span>
      </div>
      <div class="kpi-pill kpi-pill--failed">
        <span class="kpi-pill-label">Failed</span>
        <span class="kpi-pill-value">{{ failedCount }}</span>
      </div>
      <div class="kpi-pill kpi-pill--auto">
        <span class="kpi-pill-label">Done</span>
        <span class="kpi-pill-value">{{ doneCount }}</span>
      </div>
      <div class="kpi-pill">
        <span class="kpi-pill-label">Total</span>
        <span class="kpi-pill-value">{{ tasks.length }}</span>
      </div>
    </div>

    <!-- Backend Stats -->
    <div v-if="backendStats.length > 0" class="card" style="margin-bottom:12px;padding:12px 16px;">
      <div style="font-weight:600;margin-bottom:8px;font-size:13px;color:var(--text-secondary);">Backend Performance (Thompson Sampling)</div>
      <div style="display:flex;flex-wrap:wrap;gap:8px;">
        <div v-for="s in backendStats" :key="`${s.project_id}-${s.backend}`" class="chip" :style="agentChipStyle(s.backend)" style="display:flex;align-items:center;gap:6px;padding:4px 10px;">
          <span style="font-weight:600;">{{ s.backend }}</span>
          <span style="opacity:0.7;font-size:11px;">{{ s.project_id }}</span>
          <span style="font-family:var(--font-mono);font-size:11px;opacity:0.9;">{{ s.success }}/{{ s.total }}</span>
          <span v-if="s.success_rate != null" style="font-family:var(--font-mono);font-size:10px;opacity:0.8;">{{ Math.round(s.success_rate * 100) }}%</span>
        </div>
      </div>
    </div>

    <!-- Enqueue Composer -->
    <div class="card" style="margin-bottom:12px;">
      <div style="font-weight:600;margin-bottom:10px;font-size:13px;">New Task</div>
      <div style="display:flex;flex-direction:column;gap:10px;">
        <div>
          <label class="idea-draft-label">Project <span style="color:#f87171;">*</span></label>
          <input v-model="selectedProject" class="input" list="project-list" placeholder="Select or type a project_id" style="width:100%;" />
          <datalist id="project-list">
            <option v-for="p in projects" :key="p.project_id" :value="p.project_id">{{ p.project_id }}</option>
          </datalist>
        </div>
        <div>
          <label class="idea-draft-label">Instruction</label>
          <textarea
            v-model="taskPayload"
            class="input composer-textarea"
            placeholder="Describe what Hermes should do..."
            @keydown="onComposerKeydown"
          />
        </div>
        <div class="inline-actions" style="justify-content:space-between;align-items:center;">
          <button class="btn light" :disabled="enqueueLoading || !taskPayload.trim()" @click="doEnqueue">
            <span v-if="enqueueLoading">Sending...</span>
            <span v-else>Enqueue</span>
          </button>
          <div class="subtitle" style="margin:0;" :style="{ color: enqueueError ? '#fca5a5' : enqueueOk ? '#86efac' : 'var(--text-tertiary)' }">
            {{ enqueueError || enqueueOk || 'Cmd+Enter to send' }}
          </div>
        </div>
      </div>
    </div>

    <!-- Table Card -->
    <div class="card">
      <div v-if="error" class="subtitle" style="color:#fca5a5;margin-bottom:12px;">{{ error }}</div>

      <div class="table-wrap">
        <table class="table">
          <thead>
            <tr>
              <th>Task</th>
              <th>Agent</th>
              <th>Session</th>
              <th>Status</th>
              <th>Timestamp</th>
              <th>Notes</th>
            </tr>
          </thead>
          <tbody>
            <!-- Skeleton loading -->
            <template v-if="loading">
              <tr v-for="i in 5" :key="i">
                <td><div class="skeleton skeleton-text" style="width:80%;"></div></td>
                <td><div class="skeleton skeleton-text short"></div></td>
                <td><div class="skeleton skeleton-text" style="width:60%;"></div></td>
                <td><div class="skeleton skeleton-text short"></div></td>
                <td><div class="skeleton skeleton-text" style="width:70%;"></div></td>
                <td><div class="skeleton skeleton-text medium"></div></td>
              </tr>
            </template>

            <!-- Empty state -->
            <tr v-else-if="tasks.length === 0">
              <td colspan="6" style="border-bottom:none;padding:0;">
                <div class="empty-state">
                  <div class="empty-state-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg></div>
                  <div class="empty-state-title">No tasks yet</div>
                  <div class="empty-state-desc">Tasks will appear here once agents start processing work. Create a project first to generate tasks.</div>
                  <RouterLink class="btn light small" to="/dashboard/projects" style="margin-top:4px;">Go to Projects</RouterLink>
                </div>
              </td>
            </tr>

            <!-- Data rows -->
            <tr v-for="task in pagedTasks" :key="task.id">
              <td>
                <RouterLink :to="`/dashboard/task/${task.id}`" style="font-weight:500;transition:color var(--duration-fast) var(--ease-out-expo);" onmouseover="this.style.color='var(--accent)'" onmouseout="this.style.color=''">
                  #{{ task.id }} {{ task.project_id }}
                </RouterLink>
              </td>
              <td>
                <span class="chip" :style="agentChipStyle(task.backend)">{{ agentLabel(task.backend) }}</span>
              </td>
              <td>
                <div class="inline-actions" style="align-items:center;justify-content:flex-start;gap:6px;">
                  <span style="display:inline-block;max-width:140px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;font-family:var(--font-mono);font-size:11px;color:var(--text-secondary);">{{ task.session_id || '-' }}</span>
                  <button v-if="task.session_id" class="icon-btn" title="Copy session ID" @click="copySession(task.session_id)"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg></button>
                </div>
              </td>
              <td>
                <span class="chip" :style="statusChipStyle(task.run_status || task.status)">{{ task.run_status || task.status }}</span>
              </td>
              <td class="mono" style="color:var(--text-secondary);font-size:11px;">{{ formatTs(task.run_updated_at || task.started_at || task.created_at) }}</td>
              <td>
                <div style="max-width:200px;max-height:4.5em;overflow:hidden;text-overflow:ellipsis;display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;color:var(--text-secondary);font-size:11.5px;line-height:1.6;">
                  {{ task.last_error || task.payload }}
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="pagination-bar">
        <button class="icon-btn" :disabled="currentPage === 1" title="Previous page" @click="currentPage -= 1"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg></button>
        <span class="subtitle" style="margin:0;">Page {{ currentPage }} / {{ totalPages }}</span>
        <button class="icon-btn" :disabled="currentPage >= totalPages" title="Next page" @click="currentPage += 1"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></button>
      </div>
    </div>

    <!-- Memory Feedback History -->
    <div v-if="memoryFeedback.length > 0" class="card" style="margin-top:12px;padding:12px 16px;">
      <div style="font-weight:600;margin-bottom:8px;font-size:13px;color:var(--text-secondary);">Memory Feedback (ELO Learning)</div>
      <div style="display:flex;flex-direction:column;gap:6px;">
        <div v-for="m in memoryFeedback" :key="m.id" style="display:flex;align-items:center;gap:8px;padding:6px 8px;border-radius:8px;background:var(--panel);border:1px solid rgba(255,255,255,0.04);">
          <span style="font-size:11px;opacity:0.6;min-width:40px;">{{ formatTs(m.ts) }}</span>
          <span style="font-size:11px;font-family:var(--font-mono);opacity:0.7;max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ m.memory_id }}</span>
          <span style="font-size:11px;opacity:0.8;flex:1;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">{{ m.query }}</span>
          <span class="chip" :style="feedbackChipStyle(m.reward)" style="font-size:10px;padding:2px 8px;">{{ m.reward > 0 ? '👍' : '👎' }} {{ m.action }}</span>
          <span style="font-family:var(--font-mono);font-size:11px;opacity:0.7;min-width:36px;text-align:right;">{{ Math.round(m.score || 1500) }}</span>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getTasks, getProjectState, enqueueTask, getApiBase, getBackendStats, getMemoryFeedback } from '../api'

const tasks = ref([])
const projects = ref([])
const loading = ref(false)
const error = ref('')
const pageSize = 10
const currentPage = ref(1)
const backendStats = ref([])
const memoryFeedback = ref([])

const selectedProject = ref('')
const taskPayload = ref('')
const enqueueLoading = ref(false)
const enqueueError = ref('')
const enqueueOk = ref('')

const runningCount = computed(() => tasks.value.filter((x) => (x.run_status || x.status) === 'running').length)
const failedCount = computed(() => tasks.value.filter((x) => x.status === 'failed').length)
const doneCount = computed(() => tasks.value.filter((x) => x.status === 'done').length)
const totalPages = computed(() => Math.max(1, Math.ceil(tasks.value.length / pageSize)))
const pagedTasks = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return tasks.value.slice(start, start + pageSize)
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

function agentLabel(backend) {
  const map = { hermes: 'Hermes', codex: 'Codex', kimi: 'Kimi' }
  return map[backend] || (backend ? backend.charAt(0).toUpperCase() + backend.slice(1) : '-')
}

function agentChipStyle(backend) {
  const map = {
    hermes: { background: 'rgba(56,189,248,0.1)', borderColor: 'rgba(56,189,248,0.15)', color: '#38bdf8' },
    codex:  { background: 'rgba(52,211,153,0.1)', borderColor: 'rgba(52,211,153,0.15)', color: '#34d399' },
    kimi:   { background: 'rgba(167,139,250,0.1)', borderColor: 'rgba(167,139,250,0.15)', color: '#a78bfa' },
  }
  return map[backend] || { background: 'var(--chip)', borderColor: 'rgba(255,255,255,0.04)', color: 'var(--text-secondary)' }
}

function feedbackChipStyle(reward) {
  if (reward > 0) {
    return { background: 'rgba(52,211,153,0.1)', borderColor: 'rgba(52,211,153,0.15)', color: '#34d399' }
  }
  return { background: 'rgba(248,113,113,0.1)', borderColor: 'rgba(248,113,113,0.15)', color: '#f87171' }
}

function formatTs(value) {
  if (!value) return '-'
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return String(value)
  return d.toLocaleString()
}

async function loadProjects() {
  try {
    const data = await getProjectState()
    projects.value = (data.projects || []).sort((a, b) => {
      const aTs = Math.max(
        a.latest_run_updated_at ? new Date(a.latest_run_updated_at).getTime() : 0,
        a.latest_memory_updated_at ? new Date(a.latest_memory_updated_at).getTime() : 0
      )
      const bTs = Math.max(
        b.latest_run_updated_at ? new Date(b.latest_run_updated_at).getTime() : 0,
        b.latest_memory_updated_at ? new Date(b.latest_memory_updated_at).getTime() : 0
      )
      return bTs - aTs
    })
  } catch {
    // ignore project load errors
  }
}

async function doEnqueue() {
  if (!selectedProject.value.trim() || !taskPayload.value.trim()) {
    enqueueError.value = 'Project and instruction are required'
    return
  }
  enqueueLoading.value = true
  enqueueError.value = ''
  enqueueOk.value = ''
  try {
    const data = await enqueueTask(selectedProject.value.trim(), taskPayload.value.trim())
    enqueueOk.value = `Task #${data.task_id} enqueued`
    taskPayload.value = ''
    selectedProject.value = ''
    await reload()
  } catch (err) {
    enqueueError.value = err instanceof Error ? err.message : 'enqueue failed'
  } finally {
    enqueueLoading.value = false
  }
}

function onComposerKeydown(e) {
  if (e.key === 'Enter' && e.metaKey && !e.shiftKey && !e.altKey && !e.ctrlKey) {
    e.preventDefault()
    if (!enqueueLoading.value) doEnqueue()
  }
}

async function reload() {
  loading.value = true
  error.value = ''
  try {
    const data = await getTasks({ limit: 100 })
    tasks.value = data.tasks || []
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
    if (currentPage.value < 1) currentPage.value = 1
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'load tasks failed'
    if (msg === 'unauthorized') {
      error.value = 'Please log in at /auth with admin/admin123.'
    } else if (!getApiBase()) {
      error.value = 'Backend URL not set. Go to Profile to configure API server address (e.g. http://192.168.x.x:8080).'
    } else {
      error.value = msg
    }
  } finally {
    loading.value = false
  }
  // Load optional data separately so failures don't break the main task list
  try {
    const statsData = await getBackendStats()
    backendStats.value = statsData.stats || []
  } catch {
    backendStats.value = []
  }
  try {
    const memData = await getMemoryFeedback(20)
    memoryFeedback.value = memData.memory_feedback || []
  } catch {
    memoryFeedback.value = []
  }
}

onMounted(() => {
  reload()
  loadProjects()
})

async function copySession(sessionId) {
  try {
    await navigator.clipboard.writeText(sessionId)
  } catch {
    // noop: ignore clipboard permission failures
  }
}
</script>
