import { createApp } from 'vue'
import { router } from '@/router/index.js'
import App from './App.vue'
import '@/assets/styles/main.css'

createApp(App).use(router).mount('#app')
