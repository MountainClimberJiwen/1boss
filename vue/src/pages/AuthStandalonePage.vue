<template>
  <div class="auth-layout">
    <aside class="auth-left">
      <div>
        <div class="eyebrow">Authentication</div>
        <div style="font-size:32px;font-weight:800;letter-spacing:-0.03em;line-height:1.1;margin-top:12px;">1boss Account</div>
        <div class="subtitle" style="margin-top:10px;max-width:28ch;line-height:1.7;">One account to manage tasks, profile, and workflows across all your projects.</div>
      </div>
      <button class="btn" style="width:fit-content;" @click="router.push('/')">&larr; Back to home</button>
    </aside>

    <main class="auth-main">
      <div class="auth-card">
        <div style="font-size:28px;font-weight:800;margin-bottom:4px;letter-spacing:-0.02em;">Sign in</div>
        <div class="subtitle" style="margin-bottom:20px;">Welcome back. Enter your credentials to continue.</div>

        <div style="display:flex;flex-direction:column;gap:14px;">
          <div>
            <label style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-tertiary);display:block;margin-bottom:6px;">Username</label>
            <input v-model="username" class="input" placeholder="admin" @keyup.enter="submitLogin" />
          </div>
          <div>
            <label style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-tertiary);display:block;margin-bottom:6px;">Password</label>
            <input v-model="password" class="input" type="password" placeholder="" @keyup.enter="submitLogin" />
          </div>
        </div>

        <button class="btn light glow-border" style="width:100%;margin-top:20px;" :disabled="!username.trim() || !password.trim()" @click="submitLogin">
          Sign in to Dashboard
        </button>

        <div v-if="error" style="margin-top:12px;padding:10px 12px;background:rgba(248,113,113,0.08);border:1px solid rgba(248,113,113,0.2);border-radius:8px;color:#fca5a5;font-size:12.5px;">
          {{ error }}
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api'

const router = useRouter()
const username = ref('')
const password = ref('')
const error = ref('')

onMounted(() => {
  if (localStorage.getItem('auth_token')) {
    router.push('/dashboard/projects')
  }
})

async function submitLogin() {
  error.value = ''
  try {
    await login(username.value, password.value)
    await router.push('/dashboard/projects')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'login failed'
  }
}
</script>
