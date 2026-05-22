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
        <button class="icon-btn" title="Refresh" @click="reloadAll"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg></button>
      </div>
    </div>

    <div class="two-column-layout idea-page-layout">
      <!-- Left Column -->
      <div style="display:flex;flex-direction:column;gap:16px;">

        <!-- Audio Summaries Card -->
        <div class="card audio-summaries-card">
          <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:14px;">
            <div style="font-weight:700;font-size:14px;">Daily Audio Summaries</div>
            <button class="btn primary" :disabled="generating" @click="generateSummary">
              <span v-if="generating">Generating...</span>
              <span v-else>Generate Yesterday's Summary</span>
            </button>
          </div>

          <!-- Audio Player -->
          <div v-if="currentAudioUrl" class="audio-player-wrap">
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:8px;">
              <div class="audio-wave">
                <span></span><span></span><span></span><span></span><span></span>
              </div>
              <div style="font-size:12px;color:var(--text-secondary);">{{ currentAudioDate }}</div>
            </div>
            <audio :src="currentAudioUrl" controls style="width:100%;height:36px;border-radius:8px;" @ended="onAudioEnded" />
          </div>

          <!-- Summaries List -->
          <div v-if="audioSummaries.length === 0" class="empty-state" style="padding:20px 0;">
            <div class="empty-state-desc">No audio summaries yet. Generate one to hear your ideas.</div>
          </div>
          <div v-else class="audio-list">
            <div
              v-for="sum in audioSummaries"
              :key="sum.id"
              class="audio-list-item"
              :class="{ active: currentAudioId === sum.id }"
              @click="playSummary(sum)"
            >
              <div class="audio-list-icon">
                <svg v-if="sum.status === 'done'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"/></svg>
                <svg v-else-if="sum.status === 'generating'" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="spin"><polyline points="23 4 23 10 17 10"/><polyline points="1 20 1 14 7 14"/><path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"/></svg>
                <svg v-else width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              </div>
              <div class="audio-list-info">
                <div class="audio-list-date">{{ sum.summary_date }}</div>
                <div class="audio-list-meta">
                  <span v-if="sum.status === 'done'">{{ (sum.idea_ids ? JSON.parse(sum.idea_ids).length : 0) }} ideas</span>
                  <span v-else-if="sum.status === 'generating'">Generating...</span>
                  <span v-else-if="sum.status === 'error'">Error</span>
                  <span v-else>Pending</span>
                </div>
              </div>
              <div class="audio-list-actions" @click.stop>
                <button
                  v-if="sum.status === 'done'"
                  class="icon-btn small"
                  title="Play on phone"
                  @click="sendToMobile(sum)"
                >
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="2" width="14" height="20" rx="2" ry="2"/><line x1="12" y1="18" x2="12.01" y2="18"/></svg>
                </button>
              </div>
            </div>
          </div>
        </div>

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
import { createIdea, getIdeas, getApiBase, getAudioSummaries, generateDailySummary, playAudioOnMobile } from '../api'

const ideas = ref([])
const title = ref('')
const content = ref('')
const loading = ref(false)
const error = ref('')
const tip = ref('Use this panel to save ideas to backend.')
const pageSize = 20
const currentPage = ref(1)

const audioSummaries = ref([])
const generating = ref(false)
const currentAudioId = ref(null)
const currentAudioUrl = ref('')
const currentAudioDate = ref('')

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

async function reloadIdeas() {
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

async function reloadAudioSummaries() {
  try {
    const data = await getAudioSummaries(50)
    audioSummaries.value = data.audio_summaries || []
  } catch (err) {
    console.error('Failed to load audio summaries:', err)
  }
}

async function reloadAll() {
  await Promise.all([reloadIdeas(), reloadAudioSummaries()])
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
    await reloadIdeas()
    setTimeout(() => { tip.value = 'Use this panel to save ideas to backend.' }, 2000)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'save idea failed'
  }
}

async function generateSummary() {
  generating.value = true
  try {
    await generateDailySummary()
    await reloadAudioSummaries()
  } catch (err) {
    const msg = err instanceof Error ? err.message : 'generate summary failed'
    error.value = msg
  } finally {
    generating.value = false
  }
}

function playSummary(summary) {
  if (summary.status !== 'done') return
  const apiBase = getApiBase()
  currentAudioId.value = summary.id
  currentAudioDate.value = summary.summary_date
  currentAudioUrl.value = `${apiBase}/api/ideas/audio-summaries/${summary.id}/audio`
}

function onAudioEnded() {
  currentAudioUrl.value = ''
  currentAudioId.value = null
}

async function sendToMobile(summary) {
  try {
    await playAudioOnMobile(summary.id)
    tip.value = 'Sent to phone!'
    setTimeout(() => { tip.value = 'Use this panel to save ideas to backend.' }, 3000)
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'send to phone failed'
  }
}

onMounted(() => {
  reloadAll()
})
</script>

<style scoped>
.audio-summaries-card {
  padding: 16px;
}
.audio-player-wrap {
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 14px;
  margin-bottom: 14px;
}
.audio-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  height: 20px;
}
.audio-wave span {
  display: inline-block;
  width: 3px;
  background: var(--accent);
  border-radius: 2px;
  animation: wave 1.2s ease-in-out infinite;
}
.audio-wave span:nth-child(1) { height: 8px; animation-delay: 0s; }
.audio-wave span:nth-child(2) { height: 14px; animation-delay: 0.1s; }
.audio-wave span:nth-child(3) { height: 18px; animation-delay: 0.2s; }
.audio-wave span:nth-child(4) { height: 12px; animation-delay: 0.3s; }
.audio-wave span:nth-child(5) { height: 10px; animation-delay: 0.4s; }
@keyframes wave {
  0%, 100% { transform: scaleY(0.6); opacity: 0.6; }
  50% { transform: scaleY(1); opacity: 1; }
}
.audio-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.audio-list-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 12px;
  border-radius: 10px;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
  background: rgba(255,255,255,0.02);
}
.audio-list-item:hover {
  background: rgba(255,255,255,0.05);
  border-color: var(--line);
}
.audio-list-item.active {
  background: rgba(56, 189, 248, 0.08);
  border-color: rgba(56, 189, 248, 0.25);
}
.audio-list-icon {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: rgba(255,255,255,0.06);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
  flex-shrink: 0;
}
.audio-list-info {
  flex: 1;
  min-width: 0;
}
.audio-list-date {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
}
.audio-list-meta {
  font-size: 11px;
  color: var(--text-tertiary);
  margin-top: 2px;
}
.audio-list-actions {
  display: flex;
  gap: 4px;
  opacity: 0;
  transition: opacity 0.2s;
}
.audio-list-item:hover .audio-list-actions {
  opacity: 1;
}
.spin {
  animation: spin 1s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.btn.primary {
  background: var(--accent);
  color: #0f172a;
  font-weight: 600;
  font-size: 12px;
  padding: 6px 12px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.2s;
}
.btn.primary:hover {
  filter: brightness(1.1);
}
.btn.primary:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
.icon-btn.small {
  width: 28px;
  height: 28px;
}
audio::-webkit-media-controls-panel {
  background: rgba(15, 23, 42, 0.9);
}
audio::-webkit-media-controls-current-time-display,
audio::-webkit-media-controls-time-remaining-display {
  color: var(--text-secondary);
}
</style>
