import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './assets/styles.css'

const LAST_ROUTE_KEY = 'last_route_path'

const app = createApp(App)
app.use(router)

// Restore last visited route when app starts (mobile app relaunch)
const savedPath = localStorage.getItem(LAST_ROUTE_KEY)
if (savedPath && savedPath !== '/' && window.location.pathname === '/') {
  router.replace(savedPath)
}

// Persist route on every navigation so relaunch returns to the same page
router.afterEach((to) => {
  if (to.path !== '/auth') {
    localStorage.setItem(LAST_ROUTE_KEY, to.fullPath)
  }
})

router.isReady().then(() => {
  app.mount('#app')
})
