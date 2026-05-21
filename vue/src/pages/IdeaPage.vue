<template>
  <DashboardLayout active="ideas">
    <div class="topbar">
      <div>
        <div class="eyebrow">Brainstorm</div>
        <div class="title">Ideas</div>
      </div>
      <div class="inline-actions">
        <RouterLink class="icon-btn" to="/dashboard/projects" title="Projects"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 19a2 2 0 0 1-2 2H4a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5l2 3h9a2 2 0 0 1 2 2z"/></svg></RouterLink>
        <button class="icon-btn" title="Save Idea" @click="saveIdea"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/></svg></button>
        <button class="icon-btn" title="Refresh" @click="reload"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
      </div>
    </div>

    <div class="two-column-layout idea-page-layout">
      <!-- Idea List -->
      <div class="card">

        <!-- Skeleton loading -->
        <div v-if="loading">
          <div v-for="i in 4" :key="i" class="card list-card" style="margin-bottom:8px;">
            <div class="skeleton skeleton-text short" style="margin-bottom:8px;"></div>
            <div class="skeleton skeleton-title" style="width:70%;"></div>
            <div class="skeleton skeleton-text medium"></div>
          </div>
        </div>

        <!-- Empty state -->
        <div v-else-if="ideas.length === 0" class="empty-state" style="padding:32px 16px;">
          <div class="empty-state-icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg></div>
          <div class="empty-state-title">No ideas yet</div>
          <div class="empty-state-desc">Use the draft panel on the right to capture your first idea before it slips away.</div>
        </div>

        <!-- Idea rows -->
        <div v-for="row in pagedIdeas" :key="row.id" class="card list-card" style="margin-bottom:8px;cursor:pointer;transition:all var(--duration-base) var(--ease-out-expo);" onmouseover="this.style.borderColor='#2a3240';this.style.transform='translateX(3px)'" onmouseout="this.style.borderColor='';this.style.transform=''">
          <div style="font-size:11px;color:var(--text-tertiary);font-family:var(--font-mono);display:flex;gap:8px;flex-wrap:wrap;align-items:center;">
            <span>#{{ row.id }}</span>
            <span style="color:var(--line);">|</span>
            <span>{{ row.source || 'manual' }}</span>
            <span style="color:var(--line);">|</span>
            <span>{{ formatTs(row.updated_at || row.created_at) }}</span>
          </div>
          <div style="font-size:14px;font-weight:700;margin-top:8px;letter-spacing:-0.01em;">{{ row.title }}</div>
          <div style="font-size:12.5px;color:var(--text-secondary);line-height:1.7;white-space:pre-wrap;margin-top:8px;">{{ row.content }}</div>
        </div>

        <div style="display:flex;justify-content:flex-end;align-items:center;gap:8px;margin-top:10px;">
          <button class="icon-btn" :disabled="currentPage === 1" title="Previous page" @click="currentPage -= 1"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15 18 9 12 15 6"/></svg></button>
          <span class="subtitle" style="margin:0;">Page {{ currentPage }} / {{ totalPages }}</span>
          <button class="icon-btn" :disabled="currentPage >= totalPages" title="Next page" @click="currentPage += 1"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg></button>
        </div>
      </div>

      <!-- Draft Panel -->
      <div class="card idea-draft-panel">
        <div style="font-weight:700;margin-bottom:14px;font-size:14px;">Draft</div>

        <div style="display:flex;flex-direction:column;gap:12px;">
          <div>
            <label class="idea-draft-label">Title</label>
            <input v-model="title" class="input" placeholder="e.g. Autonomous release quality gate" />
          </div>
          <div>
            <label class="idea-draft-label">Content</label>
            <textarea v-model="content" class="input idea-draft-textarea" placeholder="Describe the problem, possible solutions, and who might own it..." />
          </div>
          <div class="inline-actions" style="justify-content:space-between;align-items:center;">
            <button class="btn light" :disabled="!title.trim() || !content.trim()" @click="saveIdea">Save Idea</button>
            <div class="subtitle" style="margin:0;" :style="{ color: error ? '#fca5a5' : 'var(--text-tertiary)' }">{{ error || tip }}</div>
          </div>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { createIdea, getIdeas, getApiBase } from '../api'

const ideas = ref([])
const title = ref('')
const content = ref('')
const loading = ref(false)
const error = ref('')
const tip = ref('Use this panel to save ideas to backend.')
const pageSize = 20
const currentPage = ref(1)

const totalPages = computed(() => Math.max(1, Math.ceil(ideas.value.length / pageSize)))
const pagedIdeas = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  return ideas.value.slice(start, start + pageSize)
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
    const data = await getIdeas(100)
    ideas.value = data.ideas || []
    if (currentPage.value > totalPages.value) currentPage.value = totalPages.value
    if (currentPage.value < 1) currentPage.value = 1
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'load ideas failed'
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

async function saveIdea() {
  error.value = ''
  if (!title.value.trim() || !content.value.trim()) {
    error.value = 'title and content are required'
    return
  }
  try {
    await createIdea({ title: title.value, content: content.value, source: 'vue' })
    title.value = ''
    content.value = ''
    tip.value = 'Saved.'
    currentPage.value = 1
    await reload()
    setTimeout(() => { tip.value = 'Use this panel to save ideas to backend.' }, 2000)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'save idea failed'
  }
}

onMounted(reload)
</script>
