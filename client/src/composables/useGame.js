import { ref, unref } from 'vue'
import { useWebsocket } from '@/composables/useWebsocket'

const MESSAGE_TYPES = {
  GAME_JOINED: 'game_joined',
  PLAYER_JOINED: 'player_joined',
  MOVE_MADE: 'move_made',
  GAME_ENDED: 'game_ended',
  PLAYER_DISCONNECTED: 'player_disconnected',
  PLAYER_RECONNECTED: 'player_reconnected',
  ERROR: 'error',
  CHAT_MESSAGE: 'chat_message',
  MAKE_MOVE: 'make_move',
}

let websocket
const game = ref()
const gameId = ref('')

function onMessage(message) {
  switch (message.type) {
    case MESSAGE_TYPES.GAME_JOINED:
      game.value = message.game
      break

    case MESSAGE_TYPES.PLAYER_JOINED:
      break

    case MESSAGE_TYPES.MOVE_MADE:
      game.value = message.game
      break

    default:
      console.error('Unknown message type', message)
      break
  }
}

export function useGame() {
  const joinGame = (gameId, username) => {
    const websocketUrl = `ws://localhost:8000/ws/game/${gameId}?username=${unref(username)}`
    websocket = useWebsocket(websocketUrl, onMessage)
  }

  const makeMove = (position) => {
    const message = {
      type: MESSAGE_TYPES.MAKE_MOVE,
      position,
    }
    websocket.sendMessage(message)
  }

  return {
    game,
    gameId,
    joinGame,
    makeMove,
  }
}
