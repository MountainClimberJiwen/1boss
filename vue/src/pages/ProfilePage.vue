<template>
  <DashboardLayout active="reports">
    <div class="topbar">
      <div>
        <div class="eyebrow">Account</div>
        <div class="title">Profile</div>
        <div class="subtitle">Manage your account info, preferences, and session status.</div>
      </div>
      <RouterLink class="btn" to="/dashboard/tasks">&larr; Back to Tasks</RouterLink>
    </div>

    <div class="profile-layout">
      <div class="card">
        <div style="font-weight:700;margin-bottom:16px;font-size:14px;">Personal Info</div>
        <div style="display:flex;flex-direction:column;gap:14px;">
          <div>
            <label style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-tertiary);display:block;margin-bottom:6px;">Name</label>
            <input class="input" value="Alex Chen" />
          </div>
          <div>
            <label style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-tertiary);display:block;margin-bottom:6px;">Email</label>
            <input class="input" value="alex@1boss.tech" />
          </div>
          <div>
            <label style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-tertiary);display:block;margin-bottom:6px;">Phone</label>
            <input class="input" value="+1 (312) 847-1928" />
          </div>
        </div>
        <button class="btn light" style="margin-top:16px;">Save Changes</button>
      </div>
      <div class="side-stack">
        <div class="card">
          <div style="font-weight:700;margin-bottom:12px;font-size:14px;">API Server</div>
          <div style="display:flex;flex-direction:column;gap:10px;">
            <div>
              <label style="font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:0.05em;color:var(--text-tertiary);display:block;margin-bottom:6px;">Backend URL</label>
              <input v-model="apiBase" class="input" placeholder="e.g. http://192.168.1.5:8080" />
            </div>
            <div style="font-size:11.5px;color:var(--text-secondary);line-height:1.5;">
              Required on mobile. Use your computer's LAN IP so the app can reach the backend.
            </div>
            <div class="inline-actions" style="gap:8px;">
              <button class="btn light small" @click="saveApiBase">Save</button>
              <button class="btn small" @click="clearApiBase">Reset</button>
            </div>
            <div v-if="apiMsg" style="font-size:12px;color:#34d399;">{{ apiMsg }}</div>
          </div>
        </div>
        <div class="card">
          <div style="font-weight:700;margin-bottom:12px;font-size:14px;">Actions</div>
          <button class="btn" style="width:100%;margin-bottom:8px;">Sign out</button>
          <button class="btn" style="width:100%;">Sign in / Register</button>
        </div>
      </div>
    </div>
  </DashboardLayout>
</template>

<script setup>
import { ref } from 'vue'
import { RouterLink } from 'vue-router'
import DashboardLayout from '../layouts/DashboardLayout.vue'
import { getApiBase, setApiBase } from '../api'

const apiBase = ref(getApiBase())
const apiMsg = ref('')

function saveApiBase() {
  setApiBase(apiBase.value)
  apiMsg.value = 'Saved. Pull-to-refresh or restart app to apply.'
  setTimeout(() => { apiMsg.value = '' }, 3000)
}

function clearApiBase() {
  setApiBase('')
  apiBase.value = ''
  apiMsg.value = 'Cleared. Using default relative URLs.'
  setTimeout(() => { apiMsg.value = '' }, 3000)
}
</script>
