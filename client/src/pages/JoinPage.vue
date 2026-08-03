<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const router = useRouter()
const route = useRoute()

const invited = !!route.query.gameId
const gameId = ref(route.query.gameId ?? '')
const username = ref('')

function join() {
  router.push({
    name: ROUTES.GAME,
    params: { gameId: gameId.value.trim() },
    query: { username: username.value },
  })
}
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <p class="intro">
      {{ invited ? 'You have been invited to a game.' : 'Enter the code you were sent.' }}
    </p>
    <form class="form" @submit.prevent="join">
      <template v-if="!invited">
        <label for="code">Game code:</label>
        <input
          id="code"
          v-model="gameId"
          type="text"
          name="code"
          required
          minlength="1"
          placeholder="Paste the game code"
        >
      </template>
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
          Join
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
    </form>
  </MainLayout>
</template>

<style scoped>
.intro {
  margin: 0;
  text-align: center;
  color: var(--text-muted);
  font-size: 0.95rem;
}

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
</style>
