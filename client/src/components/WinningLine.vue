<script setup>
import { computed } from 'vue'
import { cellCentres } from '@/utils/winningLines'

const props = defineProps({
  line: { type: Array, required: true },
  gap: { type: Number, default: 0 },
  symbol: { type: String, default: null },
})

const OVERSHOOT = 10

const style = computed(() => {
  const centres = cellCentres(props.gap)
  const [from] = props.line
  const to = props.line.at(-1)
  const dx = centres[to[1]] - centres[from[1]]
  const dy = centres[to[0]] - centres[from[0]]

  return {
    top: `${(centres[from[0]] + centres[to[0]]) / 2}%`,
    left: `${(centres[from[1]] + centres[to[1]]) / 2}%`,
    width: `${Math.hypot(dx, dy) + OVERSHOOT}%`,
    transform: `translate(-50%, -50%) rotate(${Math.atan2(dy, dx)}rad)`,
  }
})
</script>

<template>
  <div
    class="winning-line"
    :class="symbol?.toLowerCase()"
    :style="style"
    aria-hidden="true"
  >
    <div class="winning-line-fill" />
  </div>
</template>

<style scoped>
/* Boards set --strike-thickness to suit their own width. */
.winning-line {
  position: absolute;
  height: var(--strike-thickness, 3px);
  pointer-events: none;
  color: var(--symbol-x);
}

.winning-line.o {
  color: var(--symbol-o);
}

.winning-line-fill {
  width: 100%;
  height: 100%;
  border-radius: 999px;
  background: currentColor;
  box-shadow: 0 0 12px color-mix(in srgb, currentColor 60%, transparent);
  transform-origin: center;
  animation: draw 0.35s ease-out both;
}

@keyframes draw {
  from {
    opacity: 0;
    transform: scaleX(0);
  }

  to {
    opacity: 1;
    transform: scaleX(1);
  }
}

@media (prefers-reduced-motion: reduce) {
  .winning-line-fill {
    animation: none;
  }
}
</style>
