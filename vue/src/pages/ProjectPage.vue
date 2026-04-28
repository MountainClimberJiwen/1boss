<template>
  <DashboardLayout active="projects">
    <div class="topbar">
      <div>
        <div style="font-size:28px;font-weight:700;">Project Page</div>
        <div class="subtitle">Track project status, latest progress, and linked work items.</div>
      </div>
      <div style="display:flex;gap:8px;"><button class="btn" @click="reload">Refresh</button></div>
    </div>

    <div class="grid-3" style="margin-bottom:12px;">
      <div class="card"><div class="kpi-label">Active Projects</div><div class="kpi-value">{{ projects.length }}</div><span class="chip">Synced from backend</span></div>
      <div class="card"><div class="kpi-label">With Running Tasks</div><div class="kpi-value">{{ runningProjects }}</div><span class="chip" style="background:#163148;">Now processing</span></div>
      <div class="card"><div class="kpi-label">With Failed Tasks</div><div class="kpi-value">{{ failedProjects }}</div><span class="chip" style="background:#4a232a;">Needs attention</span></div>
    </div>

    <div class="card" style="margin-bottom:12px;">
      <div style="font-weight:600;margin-bottom:8px;">Latest Progress</div>
      <div v-if="error" class="subtitle" style="margin:0;color:#fca5a5;">{{ error }}</div>
      <div v-else-if="latestProgressRows.length === 0" class="subtitle" style="margin:0;line-height:1.8;">No progress records yet.</div>
      <div v-else class="subtitle" style="margin:0;line-height:1.8;">
        <div v-for="item in latestProgressRows" :key="item.project_id">
          {{ item.project_id }}: {{ item.latest_progress || item.latest_run_status || 'No recent run data' }}
        </div>
      </div>
    </div>

    <div class="card">
      <div class="topbar" style="margin-bottom:10px;">
        <div><div style="font-weight:600;">Projects</div><div class="subtitle" style="margin:0;">Status, latest progress, and linked task volume</div></div>
        <button class="btn" @click="reload">+ Reload</button>
      </div>
      <div v-if="loading" class="subtitle">Loading...</div>
      <div v-else-if="projects.length === 0" class="subtitle">No project records.</div>
      <div v-else class="project-card-grid">
        <div v-for="row in pagedProjects" :key="row.project_id" class="card list-card">
          <div style="display:flex;justify-content:space-between;align-items:flex-start;gap:8px;">
            <div style="font-size:14px;font-weight:600;word-break:break-word;">{{ row.project_id }}</div>
            <span class="chip" :style="statusChipStyle(projectStatus(row))">{{ projectStatus(row) }}</span>
          </div>
          <div :title="row.path || ''" style="font-size:12px;color:var(--muted);margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
            {{ row.path || '-' }}
          </div>
          <div style="display:flex;gap:12px;margin-top:8px;font-size:12px;">
            <div style="flex:1;min-width:0;">
              <div style="color:var(--muted);font-size:11px;">Latest Progress</div>
              <div style="white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{{ row.latest_progress || row.latest_run_status || '-' }}</div>
            </div>
            <div style="text-align:right;">
              <div style="color:var(--muted);font-size:11px;">Tasks</div>
              <div style="font-weight:600;">{{ row.counts?.total || 0 }}</div>
            </div>
          </div>
        </div>
      </div>
      <div style="display:flex;justify-content:flex-end;align-items:center;gap:8px;margin-top:10px;">
        <button class="btn small" :disabled="currentPage === 1" @click="currentPage -= 1">Prev</button>
        <span class="subtitle" style="margin:0;">Page {{ currentPage }} / {{ totalPages }}</span>
        <button class="btn small" :disabled="currentPage >= totalPages" @click="currentPage += 1">Next</button>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getProjectState } from '../api'

const projects = ref([])
const loading = ref(false)
const error = ref('')
const pageSize = 10
const currentPage = ref(1)

const runningProjects = computed(() => projects.value.filter((x) => (x.counts?.running || 0) > 0).length)
const failedProjects = computed(() => projects.value.filter((x) => (x.counts?.failed || 0) > 0).length)
const latestProgressRows = computed(() => projects.value.slice(0, 3))
const totalPages = computed(() => Math.max(1, Math.ceil(projects.value.length / pageSize)))
const pagedProjects = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return projects.value.slice(start, start + pageSize)
})

function projectStatus(row) {
  const counts = row.counts || {}
  if ((counts.running || 0) > 0) return 'running'
  if ((counts.pending || 0) > 0) return 'pending'
  if ((counts.failed || 0) > 0) return 'failed'
  if ((counts.done || 0) > 0) return 'done'
  return 'idle'
}

function statusChipStyle(status) {
  const map = {
    running: { background: '#163148' },
    pending: { background: '#2a2a14' },
    failed:  { background: '#4a232a' },
    done:    { background: '#1a3a1a' },
    idle:    { background: 'var(--chip)' }
  }
  return map[status] || map.idle
}

async function reload() {
  loading.value = true
  error.value = ''
  try {
    const data = await getProjectState()
    projects.value = data.projects || []
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
    if (currentPage.value < 1) currentPage.value = 1
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'load projects failed'
    error.value = msg === 'unauthorized' ? '请先去 /auth 使用 admin/admin123 登录。' : msg
  } finally {
    loading.value = false
  }
}

onMounted(reload)
</script>
