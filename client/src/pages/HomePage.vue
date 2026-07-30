<script setup>
import { RouterLink } from 'vue-router'
import DemoBoard from '@/components/DemoBoard.vue'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router/index.js'
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <DemoBoard />
    <div class="buttons-container">
      <RouterLink
        :to="{ name: ROUTES.CREATE }"
        class="action-button"
      >
        <button>Create Game</button>
      </RouterLink>
    </div>
  </MainLayout>
</template>

<style scoped>
.buttons-container {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.action-button {
  flex-grow: 1;
  text-decoration: none;

  & button {
    width: 100%;
  }
}
</style>
