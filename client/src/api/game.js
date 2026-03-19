async function createGame() {
  const response = await fetch('http://localhost:8000/games', {
    method: 'POST',
  })

  return response.json()
}

export {
  createGame,
}
