import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'

const ROUTES = Object.freeze({
  HOME: 'HOME',
})

const routes = [
  {
    path: '/',
    name: 'ROUTES.HOME',
    component: HomePage,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export {
  router,
  ROUTES,
}
