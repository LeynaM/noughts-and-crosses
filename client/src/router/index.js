import { createRouter, createWebHistory } from 'vue-router'
import CreatePage from '@/pages/CreatePage.vue'
import GamePage from '@/pages/GamePage.vue'
import HomePage from '@/pages/HomePage.vue'
import JoinPage from '@/pages/JoinPage.vue'

const ROUTES = Object.freeze({
  HOME: 'HOME',
  GAME: 'GAME',
  CREATE: 'CREATE',
  JOIN: 'JOIN',
})

const routes = [
  {
    path: '/',
    name: ROUTES.HOME,
    component: HomePage,
  },
  {
    path: '/game/create',
    name: ROUTES.CREATE,
    component: CreatePage,
  },
  {
    path: '/game/:gameId',
    name: ROUTES.GAME,
    component: GamePage,
  },
  {
    path: '/game/join',
    name: ROUTES.JOIN,
    component: JoinPage,
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
