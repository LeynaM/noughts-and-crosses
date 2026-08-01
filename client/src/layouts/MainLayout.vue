<script setup>
defineProps(['heading', 'wide'])
</script>

<template>
  <div class="main-layout">
    <div class="content" :class="{ wide }">
      <h1>{{ heading }}</h1>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  box-sizing: border-box;
}

.content {
  background: linear-gradient(145deg, #1a0a2e, #2d1b4e);
  display: flex;
  flex-direction: column;
  padding: 2.5rem;
  align-items: center;
  gap: 1.5rem;
  border-radius: 20px;
  width: 100%;
  max-width: 480px;
  box-shadow:
    0 25px 50px rgba(0, 0, 0, 0.5),
    0 0 0 1px rgba(107, 33, 168, 0.3);
}

.content.wide {
  max-width: 640px;
}
</style>
