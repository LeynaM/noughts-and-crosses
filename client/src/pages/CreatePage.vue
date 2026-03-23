<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createGame } from '@/api/game'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const router = useRouter()

const username = ref('')

async function create() {
  const { id } = await createGame()
  router.push({
    name: ROUTES.GAME,
    params: { gameId: id },
    query: { username: username.value },
  })
}
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <form class="form" @submit.prevent="create">
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
      <button
        type="submit"
      >
        Create
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
