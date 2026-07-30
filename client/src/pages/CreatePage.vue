<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { createGame } from '@/api/game'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const router = useRouter()

const username = ref('')
const error = ref()

async function create() {
  error.value = undefined
  try {
    const { id } = await createGame()
    router.push({
      name: ROUTES.GAME,
      params: { gameId: id },
      query: { username: username.value },
    })
  }
  catch {
    // Stay on the form so the name is kept and the button can be tried again.
    error.value = 'Could not reach the server. Please try again.'
  }
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
      <div class="buttons-container">
        <button
          class="action-button"
          type="submit"
        >
          Create
        </button>
        <RouterLink
          :to="{ name: ROUTES.HOME }"
          class="action-button"
        >
          <button type="button">
            Home
          </button>
        </RouterLink>
      </div>
      <p v-if="error" class="error-message">
        {{ error }}
      </p>
    </form>
  </MainLayout>
</template>

<style scoped>
.form {
  display: flex;
  flex-direction: column;
  width: 100%;
  gap: 0.5rem;
}

label {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.buttons-container {
  display: flex;
  gap: 1rem;
  width: 100%;
  margin-top: 0.5rem;
}

.action-button {
  flex-grow: 1;
  text-decoration: none;

  & button {
    width: 100%;
  }
}

.error-message {
  margin: 0;
  text-align: center;
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--error);
}
</style>
