<script setup>
defineProps(['value', 'winning'])
</script>

<template>
  <button class="cell" :class="[value?.toLowerCase(), { winning }]">
    {{ value }}
  </button>
</template>

<style scoped>
.cell {
  flex: 1;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding: 0;
  aspect-ratio: 1/1;
  font-size: 3.5rem;
  font-weight: 700;
  color: transparent;
  transition:
    background-color 0.15s ease,
    transform 0.1s ease;
  cursor: pointer;
}

.cell.x {
  color: var(--pink);
}

.cell.o {
  color: #a78bca;
}

.cell.winning {
  background: rgba(244, 114, 182, 0.1);
}

.cell:hover:not(.x):not(.o) {
  background: rgba(244, 114, 182, 0.08);
  transform: scale(1.03);
}

.cell:active {
  transform: scale(0.97);
}
</style>
