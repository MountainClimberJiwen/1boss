<template>
  <DashboardLayout active="tasks">
    <div class="topbar">
      <div>
        <div style="font-size:28px;font-weight:700;">Task Page</div>
        <div class="subtitle">Track task sessions, status, timestamps, and operator notes.</div>
      </div>
      <button class="btn" @click="reload">Refresh</button>
    </div>

    <div class="grid-3" style="margin-bottom:12px;">
      <div class="card"><div class="kpi-label">Running Sessions</div><div class="kpi-value">{{ runningCount }}</div></div>
      <div class="card"><div class="kpi-label">Failed Tasks</div><div class="kpi-value">{{ failedCount }}</div></div>
      <div class="card"><div class="kpi-label">Completed Tasks</div><div class="kpi-value">{{ doneCount }}</div></div>
    </div>

    <div class="card">
      <div v-if="error" class="subtitle" style="color:#fca5a5;">{{ error }}</div>
      <div class="table-wrap">
        <table class="table">
          <thead><tr><th>Task</th><th>Agent Session</th><th>Status</th><th>Timestamp</th><th>Notes</th></tr></thead>
          <tbody>
            <tr v-if="loading"><td colspan="5">Loading...</td></tr>
            <tr v-else-if="tasks.length === 0"><td colspan="5">No tasks yet.</td></tr>
            <tr v-for="task in pagedTasks" :key="task.id">
              <td>
                <RouterLink :to="`/dashboard/task/${task.id}`">#{{ task.id }} {{ task.project_id }}</RouterLink>
              </td>
              <td>
                <div class="inline-actions" style="align-items:center;justify-content:flex-start;gap:6px;">
                  <span style="display:inline-block;min-width:170px;">{{ task.session_id || '-' }}</span>
                  <button
                    v-if="task.session_id"
                    class="btn small"
                    style="padding:2px 8px;"
                    @click="copySession(task.session_id)"
                  >
                    Copy
                  </button>
                </div>
              </td>
              <td>{{ task.run_status || task.status }}</td>
              <td>{{ formatTs(task.run_updated_at || task.started_at || task.created_at) }}</td>
              <td>{{ task.last_error || task.payload }}</td>
            </tr>
          </tbody>
        </table>
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
import { RouterLink } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getTasks } from '../api'

const tasks = ref([])
const loading = ref(false)
const error = ref('')
const pageSize = 10
const currentPage = ref(1)

const runningCount = computed(() => tasks.value.filter((x) => (x.run_status || x.status) === 'running').length)
const failedCount = computed(() => tasks.value.filter((x) => x.status === 'failed').length)
const doneCount = computed(() => tasks.value.filter((x) => x.status === 'done').length)
const totalPages = computed(() => Math.max(1, Math.ceil(tasks.value.length / pageSize)))
const pagedTasks = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return tasks.value.slice(start, start + pageSize)
})

function formatTs(value) {
  if (!value) return '-'
  const d = new Date(value)
  if (Number.isNaN(d.getTime())) return String(value)
  return d.toLocaleString()
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
    error.value = msg === 'unauthorized' ? '请先去 /auth 使用 admin/admin123 登录。' : msg
  } finally {
    loading.value = false
  }
}

onMounted(reload)

async function copySession(sessionId) {
  try {
    await navigator.clipboard.writeText(sessionId)
  } catch {
    // noop: ignore clipboard permission failures
  }
}
</script>
