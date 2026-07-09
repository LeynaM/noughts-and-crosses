import { ref, unref } from 'vue'
import { useWebsocket } from '@/composables/useWebsocket'

const MESSAGE_TYPES = {
  PLAYER_JOINED: 'player_joined',
  MOVE_MADE: 'move_made',
  GAME_UPDATE: 'game_update',
  GAME_ENDED: 'game_ended',
  PLAYER_DISCONNECTED: 'player_disconnected',
  PLAYER_RECONNECTED: 'player_reconnected',
  ERROR: 'error',
  MAKE_MOVE: 'make_move',
}

let websocket
const game = ref()
const gameId = ref('')

function onMessage(message) {
  switch (message.type) {
    case MESSAGE_TYPES.GAME_UPDATE:
      game.value = message.payload
      break
    case MESSAGE_TYPES.PLAYER_JOINED:
      break
    case MESSAGE_TYPES.PLAYER_RECONNECTED:
      break
    case MESSAGE_TYPES.PLAYER_DISCONNECTED:
      break
    case MESSAGE_TYPES.GAME_ENDED:
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
    websocket.sendMessage({
      type: MESSAGE_TYPES.MAKE_MOVE,
      payload: {
        row: position.row,
        col: position.col,
      },
    })
  }

  return {
    game,
    gameId,
    joinGame,
    makeMove,
  }
}
