<template>
  <div class="page-shell dashboard-layout">
    <aside class="sidebar">
      <div>
        <div class="brand">
          <img class="brand-logo" src="/logo.png" alt="1boss logo" />
          <span>1boss</span>
        </div>
        <div class="brand-sub">One App, Built for Solopreneurs.</div>
      </div>

      <div class="nav-group">
        <RouterLink class="nav-item" :class="{ active: active === 'projects' }" to="/dashboard/projects">Projects <span>›</span></RouterLink>
        <RouterLink class="nav-item" :class="{ active: active === 'tasks' }" to="/dashboard/tasks">Tasks <span>›</span></RouterLink>
        <RouterLink class="nav-item" :class="{ active: active === 'ideas' }" to="/dashboard/ideas">Ideas <span>›</span></RouterLink>
        <RouterLink class="nav-item" :class="{ active: active === 'reports' }" to="/profile">Reports <span>›</span></RouterLink>
      </div>

      <div class="account-wrap">
        <button class="account-btn" @click="toggleMenu">{{ email }}</button>
        <div v-if="menuOpen" class="account-menu">
          <RouterLink class="account-menu-item" to="/profile" @click="closeMenu">个人主页</RouterLink>
          <RouterLink class="account-menu-item" to="/auth" @click="closeMenu">登录 / 注册</RouterLink>
          <button class="account-menu-item danger" @click="logout">退出登录</button>
        </div>
      </div>
    </aside>

    <div class="mobile-dashboard-header">
      <div>
        <div class="brand">
          <img class="brand-logo" src="/logo.png" alt="1boss logo" />
          <span>1boss</span>
        </div>
        <div class="brand-sub">One App, Built for Solopreneurs.</div>
      </div>
      <button class="btn small mobile-menu-btn" @click="toggleMobileNav">
        {{ mobileNavOpen ? 'Close' : 'Menu' }}
      </button>
    </div>

    <div v-if="mobileNavOpen" class="mobile-nav-sheet">
      <div class="nav-group">
        <RouterLink class="nav-item" :class="{ active: active === 'projects' }" to="/dashboard/projects" @click="closeMobileNav">Projects <span>›</span></RouterLink>
        <RouterLink class="nav-item" :class="{ active: active === 'tasks' }" to="/dashboard/tasks" @click="closeMobileNav">Tasks <span>›</span></RouterLink>
        <RouterLink class="nav-item" :class="{ active: active === 'ideas' }" to="/dashboard/ideas" @click="closeMobileNav">Ideas <span>›</span></RouterLink>
        <RouterLink class="nav-item" :class="{ active: active === 'reports' }" to="/profile" @click="closeMobileNav">Reports <span>›</span></RouterLink>
      </div>

      <div class="account-wrap mobile-account-wrap">
        <button class="account-btn" @click="toggleMenu">{{ email }}</button>
        <div v-if="menuOpen" class="account-menu mobile-account-menu">
          <RouterLink class="account-menu-item" to="/profile" @click="closeMobileNavAndMenu">个人主页</RouterLink>
          <RouterLink class="account-menu-item" to="/auth" @click="closeMobileNavAndMenu">登录 / 注册</RouterLink>
          <button class="account-menu-item danger" @click="logout">退出登录</button>
        </div>
      </div>
    </div>

    <main class="main">
      <slot />
    </main>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'

defineProps({
  active: {
    type: String,
    default: 'projects'
  }
})

const router = useRouter()
const menuOpen = ref(false)
const email = ref('admin@local')
const mobileNavOpen = ref(false)

function closeMenu() {
  menuOpen.value = false
}

function closeMobileNav() {
  mobileNavOpen.value = false
}

function toggleMobileNav() {
  mobileNavOpen.value = !mobileNavOpen.value
  if (!mobileNavOpen.value) {
    closeMenu()
  }
}

function closeMobileNavAndMenu() {
  closeMenu()
  closeMobileNav()
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value
}

async function logout() {
  try {
    await fetch('/logout', {
      credentials: 'include'
    })
  } finally {
    closeMobileNavAndMenu()
    await router.push('/auth')
  }
}

function onWindowClick(event) {
  const target = event.target
  if (!(target instanceof Element)) return
  if (!target.closest('.account-wrap')) {
    closeMenu()
  }
}

onMounted(() => {
  window.addEventListener('click', onWindowClick)
})

onBeforeUnmount(() => {
  window.removeEventListener('click', onWindowClick)
})
</script>
