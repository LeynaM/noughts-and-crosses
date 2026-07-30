<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { findWinningLines, isInLines } from '@/utils/winningLines'
import WinningLine from './WinningLine.vue'

// A scripted game that loops as the home page cover: X takes the anti-diagonal
// on its third move.
const MOVES = [
  { row: 1, col: 1, value: 'X' },
  { row: 0, col: 0, value: 'O' },
  { row: 0, col: 2, value: 'X' },
  { row: 2, col: 2, value: 'O' },
  { row: 2, col: 0, value: 'X' },
]

const MOVE_DELAY = 650
const WIN_PAUSE = 2400

const played = ref(0)
let timer

const board = computed(() => {
  const grid = [[null, null, null], [null, null, null], [null, null, null]]
  for (const { row, col, value } of MOVES.slice(0, played.value))
    grid[row][col] = value
  return grid
})

const winningLines = computed(() => findWinningLines(board.value))
const won = computed(() => winningLines.value.length > 0)

function tick() {
  if (played.value < MOVES.length) {
    played.value++
    timer = setTimeout(tick, won.value ? WIN_PAUSE : MOVE_DELAY)
  }
  else {
    played.value = 0
    timer = setTimeout(tick, MOVE_DELAY)
  }
}

onMounted(() => {
  // Respect a reduced-motion preference by showing the finished game instead.
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    played.value = MOVES.length
    return
  }
  timer = setTimeout(tick, MOVE_DELAY)
})

onBeforeUnmount(() => clearTimeout(timer))
</script>

<template>
  <div class="demo-board" aria-hidden="true">
    <div
      v-for="(row, i) in board"
      :key="i"
      class="demo-row"
    >
      <div
        v-for="(value, j) in row"
        :key="j"
        class="demo-cell"
        :class="[value?.toLowerCase(), { winning: isInLines(winningLines, i, j) }]"
      >
        <span v-if="value" :key="value">{{ value }}</span>
      </div>
    </div>
    <WinningLine
      v-for="(line, i) in winningLines"
      :key="i"
      :line="line"
    />
  </div>
</template>

<style scoped>
.demo-board {
  position: relative;
  width: 100%;
  max-width: 240px;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.demo-row {
  display: flex;
  width: 100%;
  gap: 0.4rem;
}

.demo-cell {
  flex: 1;
  aspect-ratio: 1/1;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 10px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 2.2rem;
  font-weight: 700;
  line-height: 1;
  transition: background-color 0.25s ease;
}

.demo-cell.x {
  color: var(--pink);
}

.demo-cell.o {
  color: var(--text-muted);
}

.demo-cell.winning {
  background: rgba(244, 114, 182, 0.1);
}

@media (prefers-reduced-motion: no-preference) {
  .demo-cell span {
    animation: pop 0.28s ease-out;
  }
}

@keyframes pop {
  from {
    opacity: 0;
    transform: scale(0.4);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}
</style>
