<script setup>
import { ref } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { createGame } from '@/api/game'
import { GAME_MODES } from '@/constants'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const MODE_OPTIONS = [
  { value: GAME_MODES.CLASSIC, name: 'Classic', hint: 'One 3×3 board' },
  { value: GAME_MODES.ULTIMATE, name: 'Ultimate', hint: 'Nine boards in one' },
]

const mode = ref(GAME_MODES.CLASSIC)

const router = useRouter()

const username = ref('')
const error = ref()

async function create() {
  error.value = undefined
  try {
    const { id } = await createGame(mode.value)
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
      <fieldset class="modes">
        <legend>Game</legend>
        <div class="mode-options">
          <label
            v-for="option in MODE_OPTIONS"
            :key="option.value"
            class="mode"
          >
            <input
              v-model="mode"
              type="radio"
              name="mode"
              :value="option.value"
            >
            <span class="mode-label">
              <span class="mode-name">{{ option.name }}</span>
              <span class="mode-hint">{{ option.hint }}</span>
            </span>
          </label>
        </div>
      </fieldset>
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

.form > label,
.modes legend {
  font-size: 0.85rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  padding: 0;
}

.modes {
  border: none;
  padding: 0;
  margin: 0;
  /* Fieldsets size to min-content by default. */
  min-width: 0;
}

.mode-options {
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
}

.mode {
  flex: 1;
}

.mode input {
  position: absolute;
  width: 0;
  height: 0;
  opacity: 0;
}

.mode-label {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
  padding: 0.6rem 0.8rem;
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  cursor: pointer;
  transition:
    background-color 0.15s ease,
    border-color 0.15s ease;
}

.mode:hover .mode-label {
  background: rgba(244, 114, 182, 0.08);
}

.mode input:checked + .mode-label {
  background: rgba(244, 114, 182, 0.12);
  border-color: var(--pink);
}

.mode input:focus-visible + .mode-label {
  outline: 2px solid var(--pink);
  outline-offset: 2px;
}

.mode-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
}

.mode-hint {
  font-size: 0.75rem;
  color: var(--text-muted);
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
