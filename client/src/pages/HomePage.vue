<script setup>
import { createGame } from '@/api/game.js'
import MainLayout from '@/layouts/MainLayout.vue'
import { router, ROUTES } from '@/router/index.js'

async function create() {
  const { id } = await createGame()
  router.push({ name: ROUTES.GAME, params: { gameId: id } })
}
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <img src="@/assets/cover.jpg">
    <div class="buttons-container">
      <button @click="create">
        Create game
      </button>
      <button> Join game </button>
    </div>
  </MainLayout>
</template>

<style scoped>
img {
  max-width: 100%;
}

.buttons-container {
  display: flex;
  gap: 1rem;
  width: 100%;
}

button {
  flex-grow: 1;
}
</style>
