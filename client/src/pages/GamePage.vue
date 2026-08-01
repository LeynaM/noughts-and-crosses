<script setup>
import confetti from 'canvas-confetti'
import { computed, onBeforeUnmount, watch } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import { createGame } from '@/api/game'
import Board from '@/components/Board.vue'
import UltimateBoard from '@/components/UltimateBoard.vue'
import { useGame } from '@/composables/useGame'
import { GAME_MODES } from '@/constants'
import MainLayout from '@/layouts/MainLayout.vue'
import { ROUTES } from '@/router'

const route = useRoute()
const router = useRouter()

const { game, error, joinGame, leaveGame, makeMove, rematch } = useGame()
const isUltimate = computed(() => game.value?.mode === GAME_MODES.ULTIMATE)

// Starting a new game routes here with a different gameId, and vue-router
// reuses this component when only a param changes, so watch rather than
// joining once during setup.
watch(
  () => route.params.gameId,
  (id) => {
    leaveGame()
    joinGame(id, route.query.username)
  },
  { immediate: true },
)

onBeforeUnmount(leaveGame)

const myPiece = computed(() => {
  if (!game.value)
    return null
  return game.value.player_x?.username === route.query.username ? 'X' : 'O'
})

const opponent = computed(() => {
  if (!game.value)
    return null
  return myPiece.value === 'X' ? game.value.player_o : game.value.player_x
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
      if (game.value.current_player !== myPiece.value)
        return 'Opponent\'s turn!'
      if (isUltimate.value && !game.value.active_board)
        return 'Your turn — any board'
      return 'It\'s your turn!'
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

// A rematch needs someone to play, so it is offered only on a clean finish
// with the opponent still connected.
const canRematch = computed(() =>
  game.value?.status === 'over' && !!opponent.value?.connected,
)
const isFinished = computed(() =>
  ['over', 'abandoned'].includes(game.value?.status),
)

function copyInviteLink() {
  navigator.clipboard.writeText(inviteLink.value)
}

async function newGame() {
  // Reachable from the error view, where the server may be the thing at fault.
  try {
    const { id } = await createGame()
    router.push({
      name: ROUTES.GAME,
      params: { gameId: id },
      query: { username: route.query.username },
    })
  }
  catch {
    error.value = 'Could not reach the server.'
  }
}

// Only on the move that wins it. A finished game can be broadcast again when
// the opponent reconnects, which should not set the confetti off a second time.
watch(game, (val, previous) => {
  const won = val?.status === 'over' && val?.winner === myPiece.value
  if (won && previous?.status !== 'over') {
    confetti({
      particleCount: 150,
      spread: 70,
      origin: { y: 0.6 },
    })
  }
})
</script>

<template>
  <MainLayout heading="Noughts and Crosses" :wide="isUltimate">
    <template v-if="error">
      <p class="error-message">
        {{ error }}
      </p>
      <div class="buttons-container">
        <button class="action-button" @click="newGame">
          New Game
        </button>
        <RouterLink :to="{ name: ROUTES.HOME }" class="action-button">
          <button>Home</button>
        </RouterLink>
      </div>
    </template>
    <template v-else-if="!game">
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
        <div class="player opponent" :class="{ gone: opponent && !opponent.connected }">
          <span class="player-symbol">{{ myPiece === 'X' ? 'O' : 'X' }}</span>
          <span class="player-name">{{ opponent?.username }}</span>
          <span class="player-label">{{ opponent && !opponent.connected ? 'Left' : 'Opponent' }}</span>
        </div>
      </div>

      <Board
        v-if="!isUltimate"
        :board="game.board"
        @make-move="makeMove"
      />
      <UltimateBoard
        v-else
        :board="game.board"
        :meta-board="game.meta_board"
        :drawn-boards="game.drawn_boards"
        :active-board="game.active_board"
        @make-move="makeMove"
      />

      <div v-if="isFinished" class="buttons-container">
        <button
          v-if="canRematch"
          class="action-button"
          @click="rematch"
        >
          Rematch
        </button>
        <button
          class="action-button"
          @click="newGame"
        >
          New Game
        </button>
      </div>

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

.error-message {
  margin: 0;
  text-align: center;
  font-size: 1rem;
  font-weight: 600;
  color: var(--text);
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

.player.gone {
  opacity: 0.45;
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

.buttons-container {
  display: flex;
  gap: 1rem;
  width: 100%;
}

.action-button {
  flex-grow: 1;
  text-decoration: none;

  & button {
    width: 100%;
  }
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
