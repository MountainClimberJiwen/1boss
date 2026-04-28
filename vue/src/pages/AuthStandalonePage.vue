<template>
  <div class="auth-layout">
    <aside class="auth-left">
      <div>
        <div style="font-size:34px;font-weight:700;">1boss Account</div>
        <div class="subtitle" style="margin-top:8px;">一个账号，统一管理任务、个人主页和工作流。</div>
      </div>
      <button class="btn" style="width:fit-content;">返回主页</button>
    </aside>

    <main class="auth-main">
      <div class="auth-card">
        <div style="font-size:36px;font-weight:700;margin-bottom:8px;">登录或注册</div>
        <div class="subtitle">先使用后台账号登录：admin / admin123</div>
        <div class="subtitle" style="margin:12px 0 4px;">用户名</div>
        <input v-model="username" class="input" placeholder="admin" />
        <div class="subtitle" style="margin:12px 0 4px;">密码</div>
        <input v-model="password" class="input" type="password" placeholder="admin123" />
        <button class="btn light" style="width:100%;margin-top:14px;" @click="submitLogin">登录并进入 Dashboard</button>
        <div class="subtitle" style="margin-top:8px;" :style="{ color: error ? '#fca5a5' : 'var(--muted)' }">{{ error || '登录后即可查看 project/task/idea 数据' }}</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { login } from '../api'

const router = useRouter()
const username = ref('admin')
const password = ref('admin123')
const error = ref('')

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
