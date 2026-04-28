<template>
  <DashboardLayout active="ideas">
    <div class="topbar">
      <div>
        <div style="font-size:28px;font-weight:700;">Idea Page</div>
        <div class="subtitle">Capture raw ideas before they become tasks or projects.</div>
      </div>
      <div class="inline-actions"><button class="btn light" @click="saveIdea">+ Save Idea</button><button class="btn" @click="reload">+ Refresh</button></div>
    </div>

    <div class="two-column-layout">
      <div class="card">
        <div style="font-weight:600;margin-bottom:8px;">Idea List</div>
        <div v-if="loading" class="subtitle">Loading...</div>
        <div v-else-if="ideas.length === 0" class="subtitle">No ideas yet.</div>
        <div v-for="row in pagedIdeas" :key="row.id" class="card list-card">
          <div style="font-size:12px;color:var(--muted);">#{{ row.id }} · {{ row.source || 'manual' }} · {{ formatTs(row.updated_at || row.created_at) }}</div>
          <div style="font-size:14px;font-weight:600;margin-top:4px;">{{ row.title }}</div>
          <div style="font-size:12px;color:#cfd7e4;line-height:1.6;white-space:pre-wrap;margin-top:6px;">{{ row.content }}</div>
        </div>
        <div style="display:flex;justify-content:flex-end;align-items:center;gap:8px;margin-top:10px;">
          <button class="btn small" :disabled="currentPage === 1" @click="currentPage -= 1">Prev</button>
          <span class="subtitle" style="margin:0;">Page {{ currentPage }} / {{ totalPages }}</span>
          <button class="btn small" :disabled="currentPage >= totalPages" @click="currentPage += 1">Next</button>
        </div>
      </div>
      <div class="card">
        <div style="font-weight:600;">Rich Text Draft</div>
        <div class="subtitle">Title</div>
        <input v-model="title" class="input" placeholder="e.g. Autonomous release quality gate" />
        <div class="subtitle">Rich Text Content</div>
        <textarea v-model="content" class="input" style="min-height:120px;resize:vertical;" placeholder="Write hypotheses, context, constraints, and potential owners..." />
        <div class="subtitle" style="margin-top:8px;" :style="{ color: error ? '#fca5a5' : 'var(--muted)' }">{{ error || tip }}</div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { createIdea, getIdeas } from '../api'

const ideas = ref([])
const title = ref('')
const content = ref('')
const loading = ref(false)
const error = ref('')
const tip = ref('Use this panel to save ideas to backend.')
const pageSize = 10
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
    error.value = msg === 'unauthorized' ? '请先去 /auth 使用 admin/admin123 登录。' : msg
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
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'save idea failed'
  }
}

onMounted(reload)
</script>
