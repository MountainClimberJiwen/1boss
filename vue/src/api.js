const API_BASE = import.meta.env.VITE_API_BASE || ''

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    credentials: 'include',
    headers: {
      'Content-Type': 'application/json',
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
  const body = new URLSearchParams({
    username: String(username || ''),
    password: String(password || '')
  }).toString()
  const res = await fetch('/login', {
    method: 'POST',
    credentials: 'include',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body,
    redirect: 'follow'
  })
  if (!res.ok) {
    throw new Error('invalid username or password')
  }
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

export function getIdeas(limit = 100) {
  return request(`/api/ideas?limit=${limit}`)
}

export function createIdea(payload) {
  return request('/api/ideas', {
    method: 'POST',
    body: JSON.stringify(payload)
  })
}
