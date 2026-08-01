<script setup>
defineProps({
  // 'X', 'O' or 'draw'.
  symbol: { type: String, required: true },
})
</script>

<template>
  <svg
    class="claim"
    :class="symbol.toLowerCase()"
    viewBox="0 0 100 100"
    aria-hidden="true"
  >
    <template v-if="symbol === 'X'">
      <line x1="22" y1="22" x2="78" y2="78" pathLength="100" />
      <line x1="78" y1="22" x2="22" y2="78" pathLength="100" />
    </template>
    <circle v-else-if="symbol === 'O'" cx="50" cy="50" r="28" pathLength="100" />
    <line v-else x1="26" y1="50" x2="74" y2="50" pathLength="100" />
  </svg>
</template>

<style scoped>
.claim {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
}

.claim :is(line, circle) {
  fill: none;
  stroke: currentColor;
  stroke-width: 8;
  stroke-linecap: round;
}

.claim.x {
  color: var(--pink);
}

.claim.o {
  color: var(--text-muted);
}

.claim.draw {
  color: var(--text-muted);
  opacity: 0.5;
}
</style>
