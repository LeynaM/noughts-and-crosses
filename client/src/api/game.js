async function createGame() {
  const response = await fetch('/games', {
    method: 'POST',
  })

  if (!response.ok) {
    throw new Error('Could not create game')
  }

  return response.json()
}

export {
  createGame,
}
