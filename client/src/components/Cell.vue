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
  border-radius: var(--cell-radius, 10px);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08) !important;
  padding: 0;
  aspect-ratio: 1/1;
  font-size: var(--cell-font, 3.5rem);
  font-weight: 700;
  color: transparent;
  transition:
    background-color 0.15s ease,
    transform 0.1s ease;
  cursor: pointer;
}

.cell.x {
  color: var(--symbol-x);
}

.cell.o {
  color: var(--symbol-o);
}

.cell.winning {
  background: color-mix(in srgb, currentColor 12%, transparent);
}

.cell:hover:not(.x):not(.o) {
  background: rgba(244, 114, 182, 0.08);
  transform: scale(1.03);
}

.cell:active {
  transform: scale(0.97);
}
</style>
