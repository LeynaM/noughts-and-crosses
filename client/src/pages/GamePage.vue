<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import Board from '@/components/Board.vue'
import { useGame } from '@/composables/useGame'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const route = useRoute()
const router = useRouter()

const { game, joinGame, makeMove } = useGame()
joinGame(route.params.gameId, route.query.username)

const myPiece = computed(() => {
  if (!game.value)
    return null
  return game.value.player_x === route.query.username ? 'X' : 'O'
})

const inviteLink = computed(() => {
  const joinHref = router.resolve({ name: ROUTES.JOIN, query: { gameId: route.params.gameId } }).href

  return new URL(joinHref, window.location.origin).href
})

const statusMessage = computed(() => {
  if (!game.value)
    return 'Loading...'

  switch (game.value.status) {
    case 'waiting_for_opponent':
      return 'Waiting for opponent to join...'

    case 'in_progress':
      if (game.value.current_player === myPiece.value) {
        return 'It\'s your turn!'
      }
      else {
        return 'Opponent\'s turn...'
      }

    case 'player_x_won':
      return 'Player X won!'

    case 'player_o_won':
      return 'Player O won!'

    case 'draw':
      return 'It\'s a draw!'

    case 'abandoned':
      return 'Game abandoned'

    default:
      return game.value.status
  }
})
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <template v-if="!game">
      Loading...
    </template>
    <template v-else>
      <div class="info">
        <p>{{ route.query.username }}</p>
        <p>{{ statusMessage }}</p>
        <p>Opponent</p>
      </div>
      <Board
        :board="game.board"
        @make-move="makeMove"
      />
      <div class="game-link">
        Copy link to invite opponent: {{ inviteLink }}
      </div>
    </template>
  </MainLayout>
</template>

<style scoped>
.info {
  display: flex;
  justify-content: center;
  width: 100%;
  gap: 3rem;
}
</style>
