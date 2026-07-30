<script setup>
import { computed } from 'vue'

const props = defineProps({
  // The winning [row, col] triple, ordered end to end.
  line: { type: Array, required: true },
})

// Cell centres sit at 1/6, 1/2 and 5/6 across a square board, so one formula
// covers rows, columns and both diagonals.
const CENTRES = [50 / 3, 50, 250 / 3]

// Extra length, as a percentage of the board, so the strike clears the glyphs
// at each end rather than stopping dead on their centres.
const OVERSHOOT = 10

const style = computed(() => {
  const [from] = props.line
  const to = props.line.at(-1)
  const dx = CENTRES[to[1]] - CENTRES[from[1]]
  const dy = CENTRES[to[0]] - CENTRES[from[0]]

  return {
    top: `${(CENTRES[from[0]] + CENTRES[to[0]]) / 2}%`,
    left: `${(CENTRES[from[1]] + CENTRES[to[1]]) / 2}%`,
    width: `${Math.hypot(dx, dy) + OVERSHOOT}%`,
    transform: `translate(-50%, -50%) rotate(${Math.atan2(dy, dx)}rad)`,
  }
})
</script>

<template>
  <div class="winning-line" :style="style" aria-hidden="true">
    <div class="winning-line-fill" />
  </div>
</template>

<style scoped>
/* Boards set --strike-thickness to suit their own width. */
.winning-line {
  position: absolute;
  height: var(--strike-thickness, 3px);
  pointer-events: none;
}

.winning-line-fill {
  width: 100%;
  height: 100%;
  border-radius: 999px;
  background: var(--pink);
  box-shadow: 0 0 12px rgba(244, 114, 182, 0.6);
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
