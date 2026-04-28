<template>
  <DashboardLayout active="tasks">
    <div class="topbar">
      <div>
        <div style="font-size:28px;font-weight:700;">Task #{{ route.params.id }}</div>
        <div class="subtitle">Review task metadata from backend queue store.</div>
      </div>
      <RouterLink class="btn" to="/dashboard/tasks">← Back to Task List</RouterLink>
    </div>

    <div class="detail-layout">
      <div class="card">
        <div style="font-weight:600;margin-bottom:8px;">Task Overview</div>
        <div v-if="loading" class="subtitle">Loading...</div>
        <div v-else-if="error" class="subtitle" style="color:#fca5a5;">{{ error }}</div>
        <div class="table-wrap">
          <table class="table">
            <tbody>
              <tr><td>Task ID</td><td>{{ task?.id ?? '-' }}</td></tr>
              <tr><td>Project</td><td>{{ task?.project_id ?? '-' }}</td></tr>
              <tr><td>Status</td><td>{{ task?.status ?? '-' }}</td></tr>
              <tr><td>Created</td><td>{{ formatTs(task?.created_at) }}</td></tr>
              <tr><td>Started</td><td>{{ formatTs(task?.started_at) }}</td></tr>
              <tr><td>Finished</td><td>{{ formatTs(task?.finished_at) }}</td></tr>
            </tbody>
          </table>
        </div>
        <div style="font-weight:600;margin:12px 0 8px;">Notes & History</div>
        <div class="subtitle" style="line-height:1.7;">
          Payload: {{ task?.payload || '-' }}<br/>
          Last Error: {{ task?.last_error || '-' }}
        </div>
      </div>
      <div class="side-stack">
        <div class="card"><div style="font-weight:600;margin-bottom:8px;">Actions</div><button class="btn" style="width:100%;" @click="reload">Reload</button></div>
        <div class="card"><div style="font-weight:600;margin-bottom:8px;">Session Notes</div><div class="subtitle">Session metadata is not included in this endpoint yet. For session-level info, use task list page joined run rows.</div></div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink, useRoute } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getTaskById } from '../api'

const route = useRoute()
const task = ref(null)
const loading = ref(false)
const error = ref('')

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
    const data = await getTaskById(route.params.id)
    task.value = data.task || null
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'load task failed'
  } finally {
    loading.value = false
  }
}

onMounted(reload)
</script>
