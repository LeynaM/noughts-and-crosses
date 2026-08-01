import { ref, unref } from 'vue'
import { useWebsocket } from '@/composables/useWebsocket'

const MESSAGE_TYPES = {
  GAME_UPDATE: 'game_update',
  ERROR: 'error',
  MAKE_MOVE: 'make_move',
  REMATCH: 'rematch',
}

// Errors that end the session: there is no game to show, so the page offers a
// way out instead of a board. Every other error is a rejected action whose
// outcome the board and status message already show, so it stays in the log
// rather than interrupting the game.
const FATAL_ERRORS = {
  game_not_found: 'That game no longer exists.',
  game_full: 'That game already has two players.',
}

let websocket
// Guards against a closing socket reporting failure after we moved on.
let connectionId = 0

const game = ref()
const error = ref()

function onMessage(message) {
  switch (message.type) {
    case MESSAGE_TYPES.GAME_UPDATE:
      game.value = message.payload
      break
    case MESSAGE_TYPES.ERROR: {
      const fatal = FATAL_ERRORS[message.payload?.kind]
      if (fatal)
        error.value = fatal
      else
        console.warn('Rejected by server', message.payload)
      break
    }
    default:
      console.error('Unknown message type', message)
      break
  }
}

export function useGame() {
  const joinGame = (id, username) => {
    const thisConnection = ++connectionId
    // Same origin as the page, so the deployed site talks to its own host over
    // wss and dev talks to the vite proxy over ws.
    const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:'
    const websocketUrl = `${protocol}//${window.location.host}/ws/game/${id}?username=${unref(username)}`

    websocket = useWebsocket(websocketUrl, onMessage, () => {
      // A close with nothing to show means we never got in, or lost the game
      // mid-play. Either way the board is dead and the user needs telling.
      if (thisConnection !== connectionId || error.value)
        return
      error.value = game.value
        ? 'Connection lost.'
        : 'Could not connect to the game.'
    })
  }

  // Closes the socket and drops the finished game, so the next board does not
  // render the previous one while its first update is in flight.
  const leaveGame = () => {
    connectionId++
    websocket?.close()
    websocket = undefined
    game.value = undefined
    error.value = undefined
  }

  const makeMove = (position) => {
    websocket.sendMessage({
      type: MESSAGE_TYPES.MAKE_MOVE,
      payload: {
        row: position.row,
        col: position.col,
        // Ultimate mode only: which large cell the move lands in.
        board_row: position.boardRow ?? null,
        board_col: position.boardCol ?? null,
      },
    })
  }

  const rematch = () => {
    websocket.sendMessage({
      type: MESSAGE_TYPES.REMATCH,
      payload: null,
    })
  }

  return {
    game,
    error,
    joinGame,
    leaveGame,
    makeMove,
    rematch,
  }
}
