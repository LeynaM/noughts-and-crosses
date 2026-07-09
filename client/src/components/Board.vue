<script setup>
import Cell from './Cell.vue'

defineProps(['board'])
const emit = defineEmits(['makeMove'])
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
        @click="emit('makeMove', { row: i, col: j })"
      />
    </div>
  </div>
</template>

<style scoped>
.board {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.row {
  display: flex;
  width: 100%;
  gap: 0.4rem;
}
</style>
