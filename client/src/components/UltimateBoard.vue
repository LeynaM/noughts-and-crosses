<script setup>
import { computed } from 'vue'
import { findWinningLines } from '@/utils/winningLines'
import Board from './Board.vue'
import ClaimMark from './ClaimMark.vue'
import WinningLine from './WinningLine.vue'

const props = defineProps({
  board: { type: Array, required: true },
  metaBoard: { type: Array, required: true },
  drawnBoards: { type: Array, default: () => [] },
  activeBoard: { type: Array, default: null },
})

defineEmits(['makeMove'])

// Drawn boards are claimed by nobody, so they are absent from metaBoard and
// have to be tracked separately.
const drawn = computed(
  () => new Set(props.drawnBoards.map(([row, col]) => `${row},${col}`)),
)

const metaLines = computed(() => findWinningLines(props.metaBoard))

function claimOf(row, col) {
  if (props.metaBoard[row][col]) {
    return props.metaBoard[row][col]
  }
  return drawn.value.has(`${row},${col}`) ? 'draw' : null
}

function isActive(row, col) {
  if (claimOf(row, col)) {
    return false
  }
  // A null active board means the next move may go anywhere still in play.
  return !props.activeBoard
    || (props.activeBoard[0] === row && props.activeBoard[1] === col)
}
</script>

<template>
  <div class="ultimate-board">
    <div
      v-for="(boards, i) in board"
      :key="i"
      class="meta-row"
    >
      <div
        v-for="(cells, j) in boards"
        :key="j"
        class="slot"
        :class="{ active: isActive(i, j), claimed: !!claimOf(i, j) }"
      >
        <Board
          :board="cells"
          @make-move="({ row, col }) => $emit('makeMove', { row, col, boardRow: i, boardCol: j })"
        />
        <ClaimMark v-if="claimOf(i, j)" :symbol="claimOf(i, j)" />
      </div>
    </div>
    <WinningLine
      v-for="(line, i) in metaLines"
      :key="i"
      :line="line"
    />
  </div>
</template>

<style scoped>
.ultimate-board {
  /* The meta strike reads this; nested .board overrides it with --board-strike. */
  --strike-thickness: 12px;
  --meta-gap: 0.5rem;

  /* Sizing for the nine boards nested inside. */
  --cell-gap: 0.15rem;
  --cell-radius: 4px;
  --cell-font: 1.4rem;
  --board-strike: 2px;

  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--meta-gap);
}

.meta-row {
  display: flex;
  width: 100%;
  gap: var(--meta-gap);
}

.slot {
  flex: 1;
  position: relative;
  padding: 0.25rem;
  border-radius: 8px;
  border: 1px solid transparent;
  transition:
    background-color 0.2s ease,
    border-color 0.2s ease;
}

.slot.active {
  background: rgba(244, 114, 182, 0.06);
  border-color: rgba(244, 114, 182, 0.45);
}

/* Claimed boards stay faintly visible under their mark. */
.slot.claimed :deep(.board) {
  opacity: 0.2;
}
</style>
