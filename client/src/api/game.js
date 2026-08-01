import { GAME_MODES } from '@/constants'

async function createGame(mode = GAME_MODES.CLASSIC) {
  const response = await fetch('/games', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ mode }),
  })

  if (!response.ok) {
    throw new Error('Could not create game')
  }

  return response.json()
}

export {
  createGame,
}
