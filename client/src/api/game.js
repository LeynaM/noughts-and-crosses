async function createGame() {
  const response = await fetch('http://localhost:8000/games', {
    method: 'POST',
  })

  if (!response.ok) {
    throw new Error('Could not create game')
  }

  return response.json()
}

async function getGame(id) {
  const response = await fetch(`http://localhost:8000/games/${id}`)

  if (!response.ok) {
    throw new Error('Game not found')
  }

  return response.json()
}

async function joinGame(id) {
  const response = await fetch(`http://localhost:8000/games/${id}`)

  if (!response.ok) {
    throw new Error('Game not found')
  }

  return response.json()
}

export {
  createGame,
  getGame,
  joinGame,
}
