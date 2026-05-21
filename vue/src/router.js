import { createRouter, createWebHistory } from 'vue-router'
import ProjectPage from './pages/ProjectPage.vue'
import ProjectDetailPage from './pages/ProjectDetailPage.vue'
import TaskPage from './pages/TaskPage.vue'
import IdeaPage from './pages/IdeaPage.vue'
import TaskDetailPage from './pages/TaskDetailPage.vue'
import WebsiteHomeEn from './pages/WebsiteHomeEn.vue'
import WebsiteHomeZh from './pages/WebsiteHomeZh.vue'
import ProfilePage from './pages/ProfilePage.vue'
import AuthStandalonePage from './pages/AuthStandalonePage.vue'

export default createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: WebsiteHomeEn },
    { path: '/dashboard/projects', component: ProjectPage },
    { path: '/dashboard/project/:id', component: ProjectDetailPage },
    { path: '/dashboard/tasks', component: TaskPage },
    { path: '/dashboard/ideas', component: IdeaPage },
    { path: '/dashboard/task/:id', component: TaskDetailPage },
    { path: '/website/en', component: WebsiteHomeEn },
    { path: '/website/zh', component: WebsiteHomeZh },
    { path: '/profile', component: ProfilePage },
    { path: '/auth', component: AuthStandalonePage }
  ]
})
