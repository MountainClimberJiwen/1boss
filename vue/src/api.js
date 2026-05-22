import { Capacitor } from '@capacitor/core'

export function getApiBase() {
  // Priority: localStorage override > build-time env > Capacitor default > relative path
  const configured = localStorage.getItem('api_base')
  if (configured) return configured
  const envBase = import.meta.env?.VITE_API_BASE
  if (envBase) return envBase
  // Robust native platform detection: Capacitor API, then WKWebView bridge, then Android bridge.
  const isNative = Capacitor.isNativePlatform() || (
    typeof window !== 'undefined' && (
      window.webkit?.messageHandlers?.bridge !== undefined ||
      window.androidBridge !== undefined
    )
  )
  if (isNative) {
    // Public backend address (reverse proxy).
    return 'http://150.158.27.27:8080'
  }
  // Browser dev server with proxy, or same-origin deployment.
  return ''
}

export function setApiBase(url) {
  if (url && url.trim()) {
    localStorage.setItem('api_base', url.trim())
  } else {
    localStorage.removeItem('api_base')
  }
}

async function request(path, options = {}) {
  const API_BASE = getApiBase()
  const token = localStorage.getItem('auth_token')
  const res = await fetch(`${API_BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...(options.headers || {})
    },
    ...options
  })
  const data = await res.json().catch(() => ({}))
  if (!res.ok) {
    if (res.status === 401) {
      throw new Error('unauthorized')
    }
    const msg = data?.error || `request failed: ${res.status}`
    throw new Error(msg)
  }
  return data
}

export async function login(username, password) {
  const API_BASE = getApiBase()
  const body = new URLSearchParams({
    username: String(username || ''),
    password: String(password || '')
  }).toString()
  const res = await fetch(`${API_BASE}/login`, {
    method: 'POST',
    
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Accept': 'application/json'
    },
    body
  })
  if (!res.ok) {
    throw new Error('invalid username or password')
  }
  localStorage.setItem('auth_token', `${username}:${password}`)
}

export function logout() {
  localStorage.removeItem('auth_token')
}

export function getTasks(params = {}) {
  const query = new URLSearchParams()
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== '') {
      query.set(key, String(value))
    }
  })
  return request(`/api/tasks${query.toString() ? `?${query.toString()}` : ''}`)
}

export function getTaskById(taskId) {
  return request(`/api/tasks/${taskId}`)
}

export function getProjectState() {
  return request('/api/projects/state')
}

export function getProjectById(projectId) {
  return request(`/api/projects/${encodeURIComponent(projectId)}`)
}

export function deleteProject(projectId) {
  return request(`/api/projects/${encodeURIComponent(projectId)}`, { method: 'DELETE' })
}

export function sendHermesFollowup(projectId, instruction, sessionId, threadId, resumePreviousSession = false) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/hermes-followup`, {
    method: 'POST',
    body: JSON.stringify({
      instruction,
      session_id: sessionId || undefined,
      thread_id: threadId || undefined,
      resume_previous_session: resumePreviousSession || undefined
    })
  })
}

export function getProjectThreads(projectId, limit = 100) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/threads?limit=${limit}`)
}

export function getProjectThread(projectId, threadId) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/threads/${threadId}`)
}

export function getProjectAgents(projectId) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/agents`)
}

export function updateProjectConfig(projectId, payload) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/config`, {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function getResearchProposals(projectId, status = null, limit = 100) {
  const params = new URLSearchParams()
  if (status) params.set('status', status)
  params.set('limit', String(limit))
  return request(`/api/projects/${encodeURIComponent(projectId)}/research-proposals?${params.toString()}`)
}

export function approveResearchProposal(projectId, proposalId) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/research-proposals/${proposalId}/approve`, {
    method: 'POST'
  })
}

export function rejectResearchProposal(projectId, proposalId) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/research-proposals/${proposalId}/reject`, {
    method: 'POST'
  })
}

export function getIdeas(limit = 100) {
  return request(`/api/ideas?limit=${limit}`)
}

export function getBackendStats(projectId = null) {
  const params = new URLSearchParams()
  if (projectId) params.set('project_id', projectId)
  return request(`/api/backend-stats${params.toString() ? `?${params.toString()}` : ''}`)
}

export function getMemoryFeedback(limit = 20) {
  return request(`/api/memory-feedback?limit=${limit}`)
}

export function recordMemoryFeedback(query, memoryId, action, reward = 1.0) {
  return request('/api/memory-feedback', {
    method: 'POST',
    body: JSON.stringify({ query, memory_id: memoryId, action, reward })
  })
}

export function createIdea(payload) {
  return request('/api/ideas', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function getAudioSummaries(limit = 100) {
  return request(`/api/ideas/audio-summaries?limit=${limit}`)
}

export function generateDailySummary(date = null) {
  return request('/api/ideas/generate-daily-summary', {
    method: 'POST',
    body: JSON.stringify(date ? { date } : {})
  })
}

export function playAudioOnMobile(summaryId) {
  return request(`/api/ideas/audio-summaries/${summaryId}/play-on-mobile`, {
    method: 'POST'
  })
}

export function getMobilePlayQueue(deviceId = null) {
  const params = new URLSearchParams()
  if (deviceId) params.set('device_id', deviceId)
  return request(`/api/mobile/play-queue${params.toString() ? `?${params.toString()}` : ''}`)
}

export function ackMobilePlayRequest(requestId) {
  return request('/api/mobile/play-queue/ack', {
    method: 'POST',
    body: JSON.stringify({ request_id: requestId })
  })
}

export function addProject(payload) {
  return request('/api/project-intakes', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}

export function enqueueTask(projectId, payload) {
  return request('/api/tasks/enqueue', {
    method: 'POST',
    body: JSON.stringify({ project_id: projectId, payload })
  })
}

export function getPinnedProjects() {
  return request('/api/projects/pins')
}

export function setProjectPinned(projectId, pinned) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/pin`, {
    method: 'POST',
    body: JSON.stringify({ pinned })
  })
}

export function commitProjectToGit(projectId) {
  return request(`/api/projects/${encodeURIComponent(projectId)}/commit`, {
    method: 'POST'
  })
}
