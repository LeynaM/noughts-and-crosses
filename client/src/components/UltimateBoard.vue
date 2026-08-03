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

const container = ref(null)
const focused = ref(null)
const zoomEnabled = ref(false)
let viewportQuery

const SCALE = computed(() => (zoomEnabled.value ? 2.2 : 2.7))

function onViewportChange(event) {
  zoomEnabled.value = event.matches
  if (!event.matches) {
    focused.value = null
  }
}

const drawn = computed(
  () => new Set(props.drawnBoards.map(([row, col]) => `${row},${col}`)),
)

const metaLines = computed(() => findWinningLines(props.metaBoard))

const activeKey = computed(() =>
  props.activeBoard ? props.activeBoard.join(',') : null,
)

watch([activeKey, () => props.myTurn], () => {
  focused.value = null
})

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

  return !props.activeBoard
    || (props.activeBoard[0] === row && props.activeBoard[1] === col)
}

function isFocused(row, col) {
  return !!focused.value && focused.value[0] === row && focused.value[1] === col
}

const canPick = computed(
  () => zoomEnabled.value && props.myTurn && !props.finished,
)

const zoomed = computed(
  () => zoomEnabled.value && !!focused.value && !props.finished,
)

function isLive(row, col) {
  if (!props.myTurn || !isPlayable(row, col)) {
    return false
  }
  return zoomEnabled.value ? isFocused(row, col) : true
}

function pick(row, col) {
  if (!canPick.value || !isPlayable(row, col)) {
    return
  }
  focused.value = [row, col]
}

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

  viewportQuery = window.matchMedia('(max-width: 700px)')
  zoomEnabled.value = viewportQuery.matches
  viewportQuery.addEventListener('change', onViewportChange)
})

onBeforeUnmount(() => {
  observer?.disconnect()
  viewportQuery?.removeEventListener('change', onViewportChange)
})

const zoomStyle = computed(() => {
  if (!zoomed.value) {
    return {}
  }
  const centres = cellCentres(gapPercent.value)
  const [row, col] = focused.value
  return {
    transform: `scale(${SCALE.value}) translate(${50 - centres[col]}%, ${50 - centres[row]}%)`,
  }
})
</script>

<template>
  <div class="viewport" :class="{ zoomed }">
    <button
      v-if="zoomed"
      type="button"
      class="chip"
      @click="focused = null"
    >
      See all boards
    </button>
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
        :symbol="metaBoard[line[0][0]][line[0][1]]"
        :gap="gapPercent"
      />
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
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 1;
  font-size: 0.75rem;
  padding: 0.35rem 0.75rem;
  /* Opaque enough to stay readable over the board behind it. */
  background: rgba(15, 15, 26, 0.85);
  border: 1px solid rgba(255, 255, 255, 0.15);
}

.chip:hover {
  background: rgba(244, 114, 182, 0.25);
}

.viewport {
  position: relative;
  width: 100%;
  overflow: hidden;
  border-radius: 12px;
  padding: 4px;
}

.ultimate-board {
  --strike-thickness: 12px;
  --meta-gap: clamp(0.25rem, 1.2vw, 0.5rem);

  --cell-gap: 0.15rem;
  --cell-radius: 4px;
  --cell-font: clamp(0.7rem, 2.6vw, 1.4rem);
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

.slot.claimed :deep(.board) {
  opacity: 0.2;
}
</style>
