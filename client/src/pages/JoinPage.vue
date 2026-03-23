<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useGame } from '@/composables/useGame'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const router = useRouter()
const route = useRoute()

const { gameId } = useGame()
gameId.value = route.query.gameId

const username = ref('')

async function join() {
  router.push({
    name: ROUTES.GAME,
    params: { gameId: gameId.value },
    query: { username: username.value },
  })
}
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <form class="form" @submit.prevent="join">
      <label for="name">Name:</label>
      <input
        id="name"
        v-model="username"
        type="text"
        name="name"
        required
        minlength="1"
        placeholder="Enter a username"
      >
      <label for="gameId">Game ID:</label>
      <input
        id="gameId"
        v-model="gameId"
        type="text"
        name="name"
        required
        minlength="1"
        placeholder="Enter a game ID"
      >
      <button
        type="submit"
      >
        Join
      </button>
    </form>
  </MainLayout>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
}

input {
  margin-bottom: 1rem;
}
</style>
