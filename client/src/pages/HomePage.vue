<script setup>
import { RouterLink } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router/index.js'
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <img src="@/assets/cover.jpg">
    <div class="buttons-container">
      <RouterLink
        :to="{ name: ROUTES.CREATE }"
        class="action-button"
      >
        <button>Create Game</button>
      </RouterLink>
      <RouterLink
        :to="{ name: ROUTES.JOIN }"
        class="action-button"
      >
        <button>Join Game</button>
      </RouterLink>
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

.action-button {
  flex-grow: 1;

  & button {
    width: 100%;
  }
}
</style>
