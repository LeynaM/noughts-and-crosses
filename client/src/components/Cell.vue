<script setup>
defineProps(['value'])
</script>

<template>
  <button class="cell">
    {{ value }}
  </button>
</template>

<style scoped>
.cell {
  flex: 1;
  border: none;
  border-radius: 0;
  background-color: purple;
  padding: 0;
  aspect-ratio: 1/1;
}

.cell:hover {
  background-color: indigo;
}
</style>
