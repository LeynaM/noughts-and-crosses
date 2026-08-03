<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { cellCentres, findWinningLines } from '@/utils/winningLines'
import Board from './Board.vue'
import ClaimMark from './ClaimMark.vue'
import WinningLine from './WinningLine.vue'

const props = defineProps({
  board: { type: Array, required: true },
  metaBoard: { type: Array, required: true },
  drawnBoards: { type: Array, default: () => [] },
  activeBoard: { type: Array, default: null },
  myTurn: { type: Boolean, default: false },
  finished: { type: Boolean, default: false },
})

defineEmits(['makeMove'])

// Enough to fill the frame while leaving a sliver of the neighbouring boards
// visible, which is most of what makes the position readable while zoomed.
const SCALE = 2.7

const container = ref(null)
const focused = ref(null)
const overview = ref(false)

// Drawn boards are claimed by nobody, so they are absent from metaBoard and
// have to be tracked separately.
const drawn = computed(
  () => new Set(props.drawnBoards.map(([row, col]) => `${row},${col}`)),
)

const metaLines = computed(() => findWinningLines(props.metaBoard))

// A stable key, so an unrelated update (a player reconnecting, say) does not
// re-fire the watcher and wipe a board the player has just chosen.
const activeKey = computed(() =>
  props.activeBoard ? props.activeBoard.join(',') : null,
)

watch(
  activeKey,
  (key) => {
    focused.value = key ? key.split(',').map(Number) : null
    overview.value = false
  },
  { immediate: true },
)

function claimOf(row, col) {
  if (props.metaBoard[row][col]) {
    return props.metaBoard[row][col]
  }
  return drawn.value.has(`${row},${col}`) ? 'draw' : null
}

function isPlayable(row, col) {
  if (props.finished || claimOf(row, col)) {
    return false
  }
  // A null active board means the next move may go anywhere still in play.
  return !props.activeBoard
    || (props.activeBoard[0] === row && props.activeBoard[1] === col)
}

function isFocused(row, col) {
  return !!focused.value && focused.value[0] === row && focused.value[1] === col
}

// The pick step: only on your turn, and only when the rules leave a choice.
const canPick = computed(
  () => props.myTurn && !props.activeBoard && !props.finished,
)

const zoomed = computed(() => !!focused.value && !overview.value && !props.finished)

// Cells accept clicks only in the board you are actually playing in.
function isLive(row, col) {
  return props.myTurn && isPlayable(row, col) && isFocused(row, col)
}

function pick(row, col) {
  if (!canPick.value || !isPlayable(row, col)) {
    return
  }
  focused.value = [row, col]
  overview.value = false
}

// The gutter is a length, but the zoom needs it as a percentage, and at 2.7x a
// one-percent error is plainly visible.
const gapPercent = ref(0)

function measure() {
  const element = container.value
  if (!element?.clientWidth) {
    return
  }
  const gap = Number.parseFloat(getComputedStyle(element).columnGap) || 0
  gapPercent.value = (gap / element.clientWidth) * 100
}

let observer

onMounted(() => {
  observer = new ResizeObserver(measure)
  observer.observe(container.value)
  measure()
})

onBeforeUnmount(() => observer?.disconnect())

const zoomStyle = computed(() => {
  if (!zoomed.value) {
    return {}
  }
  // Read right to left: bring the chosen board's centre to the middle of the
  // grid, then magnify about that middle.
  const centres = cellCentres(gapPercent.value)
  const [row, col] = focused.value
  return {
    transform: `scale(${SCALE}) translate(${50 - centres[col]}%, ${50 - centres[row]}%)`,
  }
})
</script>

<template>
  <div class="ultimate">
    <div class="controls">
      <button
        v-if="focused && !finished"
        type="button"
        class="chip"
        @click="overview = !overview"
      >
        {{ overview ? 'Zoom in' : 'See all boards' }}
      </button>
    </div>

    <div class="viewport" :class="{ zoomed }">
      <div
        ref="container"
        class="ultimate-board"
        :style="zoomStyle"
      >
        <div
          v-for="(boards, i) in board"
          :key="i"
          class="meta-row"
        >
          <div
            v-for="(cells, j) in boards"
            :key="j"
            class="slot"
            :class="{
              playable: isPlayable(i, j),
              pickable: canPick && isPlayable(i, j),
              focused: isFocused(i, j),
              live: isLive(i, j),
              claimed: !!claimOf(i, j),
            }"
            :role="canPick && isPlayable(i, j) ? 'button' : null"
            :tabindex="canPick && isPlayable(i, j) ? 0 : null"
            @click="pick(i, j)"
            @keydown.enter.prevent="pick(i, j)"
            @keydown.space.prevent="pick(i, j)"
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
          :gap="gapPercent"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.ultimate {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.controls {
  display: flex;
  justify-content: flex-end;
  min-height: 2rem;
}

.chip {
  font-size: 0.75rem;
  padding: 0.35rem 0.75rem;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
}

.chip:hover {
  background: rgba(244, 114, 182, 0.12);
}

.viewport {
  position: relative;
  width: 100%;
  overflow: hidden;
  border-radius: 12px;
  padding: 4px;
}

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
  transform-origin: center center;
  transition: transform 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  will-change: transform;
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
    border-color 0.2s ease,
    opacity 0.3s ease;
}

/* Gating both the click and the hover affordance in one rule. */
.slot :deep(.board) {
  pointer-events: none;
}

.slot.live :deep(.board) {
  pointer-events: auto;
}

.slot.playable {
  background: rgba(244, 114, 182, 0.06);
  border-color: rgba(244, 114, 182, 0.45);
}

.slot.pickable {
  cursor: pointer;
}

.slot.pickable:hover,
.slot.pickable:focus-visible {
  background: rgba(244, 114, 182, 0.14);
  border-color: var(--pink);
  outline: none;
}

.viewport.zoomed .slot:not(.focused) {
  opacity: 0.25;
  pointer-events: none;
}

/* Claimed boards stay faintly visible under their mark. */
.slot.claimed :deep(.board) {
  opacity: 0.2;
}

@media (prefers-reduced-motion: reduce) {
  .ultimate-board {
    transition: none;
  }
}
</style>
