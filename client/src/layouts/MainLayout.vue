<script setup>
defineProps(['heading'])
</script>

<template>
  <div class="main-layout">
    <div class="content">
      <h1>{{ heading }} </h1>
      <slot />
    </div>
  </div>
</template>

<style scoped>
.main-layout {
  margin: 4rem;
  display: flex;
  justify-content: center;
}

.content {
  background-color: purple;
  display: flex;
  flex-direction: column;
  padding: 2rem;
  align-items: center;
  gap: 1rem;
  border-radius: 16px;
}
</style>
