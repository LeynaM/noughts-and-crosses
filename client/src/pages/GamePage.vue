<script setup>
import confetti from 'canvas-confetti'
import { computed, watch } from 'vue'
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
    case 'waiting':
      return 'Waiting for opponent to join...'
    case 'in_progress':
      if (game.value.current_player === myPiece.value)
        return 'It\'s your turn!'
      else
        return 'Opponent\'s turn!'
    case 'over':
      if (!game.value.winner)
        return 'It\'s a draw!'
      return game.value.winner === myPiece.value ? 'You won!' : 'You lost!'
    case 'abandoned':
      return 'Game abandoned'
    default:
      return game.value.status
  }
})

function copyInviteLink() {
  navigator.clipboard.writeText(inviteLink.value)
}

watch(game, (val) => {
  if (val?.status === 'over' && val?.winner === myPiece.value) {
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
    })
  }
})
</script>

<template>
  <MainLayout heading="Noughts and Crosses">
    <template v-if="!game">
      <p class="loading">
        Connecting...
      </p>
    </template>
    <template v-else>
      <div class="players">
        <div class="player you">
          <span class="player-symbol">{{ myPiece }}</span>
          <span class="player-name">{{ route.query.username }}</span>
          <span class="player-label">You</span>
        </div>
        <div class="status-message">
          {{ statusMessage }}
        </div>
        <div class="player opponent">
          <span class="player-symbol">{{ myPiece === 'X' ? 'O' : 'X' }}</span>
          <span class="player-name">{{ myPiece === 'X' ? game.player_o : game.player_x }}</span>
          <span class="player-label">Opponent</span>
        </div>
      </div>

      <Board
        :board="game.board"
        @make-move="makeMove"
      />

      <div v-if="!(game.player_x && game.player_o)" class="game-link">
        <span class="game-link-label">Invite link</span>
        <div class="game-link-row">
          <span class="game-link-url">{{ inviteLink }}</span>
          <button @click="copyInviteLink">
            Copy
          </button>
        </div>
      </div>
    </template>
  </MainLayout>
</template>

<style scoped>
.loading {
  color: var(--text-muted);
  font-size: 0.95rem;
}

.players {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  align-items: center;
  width: 100%;
  gap: 1rem;
}

.player {
  display: flex;
  flex-direction: column;
  gap: 0.2rem;
}

.player-symbol {
  font-size: 2rem;
  font-weight: 700;
  color: var(--pink);
  line-height: 1;
}

.player-name {
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text);
}

.player-label {
  font-size: 0.75rem;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.player.you {
  align-items: flex-start;
}

.player.opponent {
  align-items: flex-end;
}

.status-message {
  flex: 1;
  text-align: center;
  white-space: nowrap;
  font-size: 0.95rem;
  font-weight: 600;
  color: var(--text-muted);
  padding: 0.5rem;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.08);
}

.game-link {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.game-link-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.game-link-row {
  display: flex;
  gap: 0.5rem;
  align-items: center;
}

.game-link-url {
  flex: 1;
  font-size: 0.75rem;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid rgba(255, 255, 255, 0.08);
  border-radius: 6px;
  padding: 0.4rem 0.6rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

button {
  white-space: nowrap;
}
</style>
