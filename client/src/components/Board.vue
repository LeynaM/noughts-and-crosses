<script setup>
import { computed } from 'vue'
import { findWinningLines, isInLines } from '@/utils/winningLines'
import Cell from './Cell.vue'
import WinningLine from './WinningLine.vue'

const props = defineProps(['board'])
const emit = defineEmits(['makeMove'])

const winningLines = computed(() => findWinningLines(props.board))
</script>

<template>
  <div class="board">
    <div
      v-for="(row, i) in board"
      :key="i"
      class="row"
    >
      <Cell
        v-for="(value, j) in row"
        :key="j"
        :value="value"
        :winning="isInLines(winningLines, i, j)"
        @click="emit('makeMove', { row: i, col: j })"
      />
    </div>
    <WinningLine
      v-for="(line, i) in winningLines"
      :key="i"
      :line="line"
    />
  </div>
</template>

<style scoped>
.board {
  --strike-thickness: var(--board-strike, 5px);

  position: relative;
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: var(--cell-gap, 0.4rem);
}

.row {
  display: flex;
  width: 100%;
  gap: var(--cell-gap, 0.4rem);
}
</style>
