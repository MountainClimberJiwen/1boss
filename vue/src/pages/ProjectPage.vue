<template>
  <DashboardLayout active="projects">
    <div class="topbar">
      <div>
        <div class="eyebrow">Workspaces</div>
        <div class="title">Projects</div>
      </div>
      <div class="inline-actions">
        <RouterLink class="icon-btn" to="/dashboard/tasks" title="Tasks"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg></RouterLink>
        <RouterLink class="icon-btn" to="/dashboard/ideas" title="Ideas"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18h6"/><path d="M10 22h4"/><path d="M15.09 14c.18-.9.27-1.48.27-2.23A4.88 4.88 0 0 0 12 7a4.88 4.88 0 0 0-3.36 4.77c0 .75.09 1.33.27 2.23"/><path d="M12 2v2"/><path d="M4.22 4.22l1.42 1.42"/><path d="M19.78 4.22l-1.42 1.42"/></svg></RouterLink>
        <button class="icon-btn" title="Refresh" @click="reload"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
      </div>
    </div>

    <!-- KPI Cards -->
    <div class="kpi-row">
      <div class="kpi-pill">
        <span class="kpi-pill-label">All</span>
        <span class="kpi-pill-value">{{ projects.length }}</span>
      </div>
      <div class="kpi-pill kpi-pill--running">
        <span class="kpi-pill-label">Run</span>
        <span class="kpi-pill-value">{{ runningProjects }}</span>
      </div>
      <div class="kpi-pill kpi-pill--failed">
        <span class="kpi-pill-label">Fail</span>
        <span class="kpi-pill-value">{{ failedProjects }}</span>
      </div>
      <div class="kpi-pill kpi-pill--auto">
        <span class="kpi-pill-label">Auto</span>
        <span class="kpi-pill-value">{{ autoResearchProjects }}</span>
      </div>
    </div>

    <!-- Projects Card -->
    <div class="card">
      <div class="topbar" style="margin-bottom:12px;">
        <div></div>
        <div class="inline-actions">
          <button class="icon-btn" :title="showAdd ? 'Cancel' : 'Add Project'" @click="showAdd = !showAdd">
            <svg v-if="showAdd" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="5" y1="12" x2="19" y2="12"/></svg>
            <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>
          </button>
          <button class="icon-btn" title="Refresh" @click="reload"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
        </div>
      </div>

      <!-- Add Project Form -->
      <div v-if="showAdd" class="card" style="margin-bottom:14px;background:var(--panel-2);border-color:var(--line);">
        <div style="font-weight:700;margin-bottom:12px;font-size:14px;">New Project</div>
        <div style="display:flex;flex-direction:column;gap:10px;">
          <div>
            <label class="subtitle" style="margin:0;display:block;font-weight:500;font-size:11.5px;">Project name <span style="color:#f87171;">*</span></label>
            <input v-model="addName" class="input" placeholder="e.g. my-project" />
          </div>
          <div>
            <label class="subtitle" style="margin:0;display:block;font-weight:500;font-size:11.5px;">Project path <span style="color:#f87171;">*</span></label>
            <input v-model="addPath" class="input" placeholder="e.g. /Users/name/projects/my-project" />
          </div>
          <div>
            <label class="subtitle" style="margin:0;display:block;font-weight:500;font-size:11.5px;">Description (optional)</label>
            <input v-model="addDesc" class="input" placeholder="Short description" />
          </div>
          <div class="inline-actions" style="align-items:center;margin-top:4px;">
            <button class="btn light" :disabled="addLoading || !addName.trim() || !addPath.trim()" @click="doAdd">Create</button>
            <button class="icon-btn" title="Cancel" @click="showAdd = false"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg></button>
            <span v-if="addError" class="subtitle" style="margin:0;color:#fca5a5;">{{ addError }}</span>
          </div>
        </div>
      </div>

      <!-- Search -->
      <div style="margin-bottom:12px;">
        <input
          v-model="searchQuery"
          class="input"
          placeholder="Search..."
          style="width:100%;"
        />
      </div>

      <!-- Error -->
      <div v-if="error" class="subtitle" style="margin-bottom:12px;color:#fca5a5;">{{ error }}</div>

      <!-- Loading Skeleton -->
      <div v-if="loading" class="project-card-grid" style="margin-bottom:12px;">
        <div v-for="i in 6" :key="i" class="card" style="min-height:120px;">
          <div class="skeleton skeleton-title" style="width:50%;"></div>
          <div class="skeleton skeleton-text medium"></div>
          <div class="skeleton skeleton-text short"></div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="filteredProjects.length === 0" class="empty-state">
        <div class="empty-state-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></div>
        <div class="empty-state-title">No project records</div>
        <div class="empty-state-desc">Get started by adding your first project. Link a local repository to begin tracking tasks and ideas.</div>
        <button class="btn light small" @click="showAdd = true">+ Add Project</button>
      </div>

      <!-- Project Grid -->
      <div v-else class="project-card-grid" style="margin-bottom:12px;">
        <div v-for="row in pagedProjects" :key="row.project_id" class="card list-card project-card-item" @click="goDetail(row.project_id)">
          <div class="project-card-actions" @click.stop>
            <button
              class="icon-btn"
              :class="{ active: isPinned(row.project_id) }"
              :title="isPinned(row.project_id) ? 'Unpin' : 'Pin to top'"
              @click="togglePin(row.project_id)"
            >
              <svg v-if="isPinned(row.project_id)" width="14" height="14" viewBox="0 0 24 24" fill="#fbbf24" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
              <svg v-else width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/>
              </svg>
            </button>
            <button class="icon-btn danger" title="Delete" @click="doDelete(row.project_id)"><svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/></svg></button>
          </div>
          <div class="project-card-header">
            <div class="project-card-name">
              {{ displayName(row) }}
              <span v-if="hasUnread(row)" class="unread-badge" title="New timeline activity" />
            </div>
            <span class="chip project-card-status" :style="statusChipStyle(projectStatus(row))">{{ projectStatus(row) }}</span>
          </div>
          <div class="project-card-path" :title="row.path || ''">
            {{ row.project_id }}
            <span v-if="row.path" style="color:var(--text-tertiary);"> · {{ row.path }}</span>
          </div>
          <div v-if="row.description" class="project-card-desc">
            {{ row.description }}
          </div>
          <div class="project-card-footer">
            <div class="project-card-stats">
              <div class="project-card-stat">
                <span class="project-card-stat-label">T</span>
                <span class="project-card-stat-value">{{ row.counts?.total || 0 }}</span>
              </div>
              <div class="project-card-stat">
                <span class="project-card-stat-label" style="color:#38bdf8;">R</span>
                <span class="project-card-stat-value" style="color:#38bdf8;">{{ row.counts?.running || 0 }}</span>
              </div>
              <div class="project-card-stat">
                <span class="project-card-stat-label" style="color:#f87171;">F</span>
                <span class="project-card-stat-value" style="color:#f87171;">{{ row.counts?.failed || 0 }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div class="pagination-bar">
        <button class="icon-btn" :disabled="currentPage === 1" title="Previous page" @click="currentPage -= 1"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg></button>
        <span class="subtitle" style="margin:0;">Page {{ currentPage }} / {{ totalPages }}</span>
        <button class="icon-btn" :disabled="currentPage >= totalPages" title="Next page" @click="currentPage += 1"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></button>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getProjectState, deleteProject, addProject, getApiBase, getPinnedProjects, setProjectPinned } from '../api'

const router = useRouter()
const projects = ref([])
const loading = ref(false)
const error = ref('')
const pageSize = 20
const currentPage = ref(1)
const showAdd = ref(false)
const addName = ref('')
const addPath = ref('')
const addDesc = ref('')
const addLoading = ref(false)
const addError = ref('')
const searchQuery = ref('')

const pinnedSet = ref(new Set())

function isPinned(projectId) {
  return pinnedSet.value.has(projectId)
}

async function togglePin(projectId) {
  const next = new Set(pinnedSet.value)
  const willPin = !next.has(projectId)
  if (willPin) {
    next.add(projectId)
  } else {
    next.delete(projectId)
  }
  try {
    await setProjectPinned(projectId, willPin)
    pinnedSet.value = next
  } catch (err) {
    alert(err instanceof Error ? err.message : 'pin failed')
  }
}

async function loadPinned() {
  try {
    const data = await getPinnedProjects()
    pinnedSet.value = new Set(data.pinned || [])
  } catch {
    pinnedSet.value = new Set()
  }
}

const runningProjects = computed(() => projects.value.filter((x) => (x.counts?.running || 0) > 0).length)
const failedProjects = computed(() => projects.value.filter((x) => (x.counts?.failed || 0) > 0).length)
const autoResearchProjects = computed(() => projects.value.filter((x) => Boolean(x.autoresearch)).length)

function sortProjects(list) {
  return [...list].sort((a, b) => {
    const aPinned = pinnedSet.value.has(a.project_id)
    const bPinned = pinnedSet.value.has(b.project_id)
    if (aPinned && bPinned) return a.project_id.localeCompare(b.project_id)
    if (aPinned) return -1
    if (bPinned) return 1
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
}

const filteredProjects = computed(() => {
  const q = searchQuery.value.trim().toLowerCase()
  let list = projects.value
  if (q) {
    list = list.filter((p) => {
      const haystack = [
        p.project_id,
        p.path,
        p.description,
        p.aliases
      ].filter(Boolean).join(' ').toLowerCase()
      return haystack.includes(q)
    })
  }
  return sortProjects(list)
})

const totalPages = computed(() => Math.max(1, Math.ceil(filteredProjects.value.length / pageSize)))
const pagedProjects = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return filteredProjects.value.slice(start, start + pageSize)
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
    running: { background: 'rgba(56,189,248,0.1)', borderColor: 'rgba(56,189,248,0.15)', color: '#38bdf8' },
    pending: { background: 'rgba(251,191,36,0.1)', borderColor: 'rgba(251,191,36,0.15)', color: '#fbbf24' },
    failed:  { background: 'rgba(248,113,113,0.1)', borderColor: 'rgba(248,113,113,0.15)', color: '#f87171' },
    done:    { background: 'rgba(52,211,153,0.1)', borderColor: 'rgba(52,211,153,0.15)', color: '#34d399' },
    idle:    { background: 'var(--chip)', borderColor: 'rgba(255,255,255,0.04)', color: 'var(--text-secondary)' }
  }
  return map[status] || map.idle
}

function hasUnread(row) {
  const lastSeen = parseInt(localStorage.getItem(`project_last_seen_${row.project_id}`) || '0', 10)
  if (!lastSeen) return true
  const runTs = row.latest_run_updated_at ? new Date(row.latest_run_updated_at).getTime() : 0
  const memTs = row.latest_memory_updated_at ? new Date(row.latest_memory_updated_at).getTime() : 0
  const latestTs = Math.max(runTs, memTs)
  return latestTs > lastSeen
}

function displayName(row) {
  if (row.aliases) {
    const first = String(row.aliases).split(',')[0].trim()
    if (first && first !== row.project_id) return first
  }
  return row.project_id
}

function goDetail(projectId) {
  router.push(`/dashboard/project/${encodeURIComponent(projectId)}`)
}

async function doDelete(projectId) {
  if (!confirm(`Delete project "${projectId}"? This will remove all related tasks and runs.`)) return
  try {
    await deleteProject(projectId)
    await reload()
  } catch (err) {
    alert(err instanceof Error ? err.message : 'delete failed')
  }
}

async function doAdd() {
  addLoading.value = true
  addError.value = ''
  try {
    await addProject({
      project_name: addName.value.trim(),
      description: addDesc.value.trim(),
      repo_path: addPath.value.trim()
    })
    addName.value = ''
    addPath.value = ''
    addDesc.value = ''
    showAdd.value = false
    await reload()
  } catch (err) {
    addError.value = err instanceof Error ? err.message : 'add project failed'
  } finally {
    addLoading.value = false
  }
}

async function reload() {
  loading.value = true
  error.value = ''
  try {
    const data = await getProjectState()
    const raw = data.projects || []
    projects.value = sortProjects(raw)
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
    if (currentPage.value < 1) currentPage.value = 1
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'load projects failed'
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
}

onMounted(() => {
  reload()
  loadPinned()
})
</script>
