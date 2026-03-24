<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { createGame } from '@/api/game'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const router = useRouter()

const username = ref('')

function back() {
  router.back()
}

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
    <form class="form" @submit.prevent="create" @back="back">
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
      <div class="buttons-container">
        <button
          class="action-button"
          type="submit"
        >
          Create
        </button>
        <button
          class="action-button"
          type="button" @click="router.back()"
        >
          Back
        </button>
      </div>
    </form>
  </MainLayout>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
}

.buttons-container {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.action-button {
  flex-grow: 1;

  & button {
    width: 100%;
  }
}

input {
  margin-bottom: 1rem;
}
</style>
