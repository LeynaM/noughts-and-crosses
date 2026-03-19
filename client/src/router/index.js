import { createRouter, createWebHistory } from 'vue-router'
import GamePage from '@/pages/GamePage.vue'
import HomePage from '@/pages/HomePage.vue'

const ROUTES = Object.freeze({
  HOME: 'HOME',
  GAME: 'GAME',
})

const routes = [
  {
    path: '/',
    name: ROUTES.HOME,
    component: HomePage,
  },
  {
    path: '/game/:gameId',
    name: ROUTES.GAME,
    component: GamePage,
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
