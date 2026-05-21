<template>
  <DashboardLayout active="tasks">
    <div class="topbar">
      <div>
        <div class="eyebrow">Execution</div>
        <div class="title">Task #{{ route.params.id }}</div>
      </div>
      <RouterLink class="icon-btn" to="/dashboard/tasks" title="Back to Tasks"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg></RouterLink>
    </div>

    <div class="detail-layout">
      <div class="card">

        <div v-if="loading">
          <div class="skeleton skeleton-title" style="width:40%;margin-bottom:16px;"></div>
          <div v-for="i in 6" :key="i" class="skeleton skeleton-text" style="margin-bottom:10px;"></div>
        </div>

        <div v-else-if="error" style="padding:12px;background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.2);border-radius:8px;color:#fca5a5;font-size:12.5px;">
          {{ error }}
        </div>

        <div v-else>
          <div class="table-wrap">
            <table class="table">
              <tbody>
                <tr>
                  <td style="color:var(--text-tertiary);width:120px;">Task ID</td>
                  <td style="font-weight:500;font-family:var(--font-mono);">{{ task?.id ?? '-' }}</td>
                </tr>
                <tr>
                  <td style="color:var(--text-tertiary);">Project</td>
                  <td style="font-weight:500;">{{ task?.project_id ?? '-' }}</td>
                </tr>
                <tr>
                  <td style="color:var(--text-tertiary);">Agent</td>
                  <td>
                    <span class="chip" :style="agentChipStyle(task?.backend)">{{ agentLabel(task?.backend) }}</span>
                  </td>
                </tr>
                <tr>
                  <td style="color:var(--text-tertiary);">Session</td>
                  <td style="font-family:var(--font-mono);font-size:12px;">
                    <div class="inline-actions" style="justify-content:flex-start;gap:6px;">
                      <span>{{ task?.session_id || '-' }}</span>
                      <button v-if="task?.session_id" class="icon-btn" title="Copy session ID" @click="copySession(task.session_id)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg></button>
                    </div>
                  </td>
                </tr>
                <tr>
                  <td style="color:var(--text-tertiary);">Status</td>
                  <td>
                    <span class="chip" :style="statusChipStyle(task?.status)">{{ task?.status ?? '-' }}</span>
                    <span v-if="task?.run_status && task.run_status !== task.status" class="chip" :style="statusChipStyle(task.run_status)" style="margin-left:6px;">{{ task.run_status }}</span>
                  </td>
                </tr>
                <tr>
                  <td style="color:var(--text-tertiary);">Created</td>
                  <td class="mono" style="color:var(--text-secondary);font-size:11px;">{{ formatTs(task?.created_at) }}</td>
                </tr>
                <tr>
                  <td style="color:var(--text-tertiary);">Started</td>
                  <td class="mono" style="color:var(--text-secondary);font-size:11px;">{{ formatTs(task?.started_at) }}</td>
                </tr>
                <tr>
                  <td style="color:var(--text-tertiary);">Finished</td>
                  <td class="mono" style="color:var(--text-secondary);font-size:11px;">{{ formatTs(task?.finished_at) }}</td>
                </tr>
              </tbody>
            </table>
          </div>

          <div v-if="task?.latest_progress" style="margin-top:16px;">
            <div style="font-weight:700;margin-bottom:10px;font-size:14px;">Latest Progress</div>
            <div style="background:var(--panel-2);border:1px solid var(--line);border-radius:10px;padding:14px;">
              <div style="font-size:12.5px;color:var(--text-secondary);line-height:1.7;font-family:var(--font-mono);white-space:pre-wrap;word-break:break-word;">{{ task.latest_progress }}</div>
            </div>
          </div>

          <div style="font-weight:700;margin:16px 0 10px;font-size:14px;">Notes & History</div>
          <div style="background:var(--panel-2);border:1px solid var(--line);border-radius:10px;padding:14px;">
            <div style="font-size:12px;color:var(--text-tertiary);margin-bottom:6px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">Payload</div>
            <div style="font-size:12.5px;color:var(--text-secondary);line-height:1.7;font-family:var(--font-mono);word-break:break-word;">{{ task?.payload || '-' }}</div>
          </div>
          <div v-if="task?.last_error || task?.run_error" style="background:rgba(248,113,113,0.06);border:1px solid rgba(248,113,113,0.15);border-radius:10px;padding:14px;margin-top:10px;">
            <div style="font-size:12px;color:#f87171;margin-bottom:6px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;">Error</div>
            <div style="font-size:12.5px;color:#fca5a5;line-height:1.7;font-family:var(--font-mono);word-break:break-word;">{{ task?.run_error || task?.last_error }}</div>
          </div>
        </div>
      </div>

      <div class="side-stack">
        <div class="card">
          <button class="btn" style="width:100%;" @click="reload">Reload</button>
        </div>
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

async function copySession(sessionId) {
  try {
    await navigator.clipboard.writeText(sessionId)
  } catch {
    // noop
  }
}

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
