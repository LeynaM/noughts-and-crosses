export function useWebsocket(url, onMessage) {
  const websocket = new WebSocket(url)

  websocket.addEventListener('error', (e) => {
    console.error('Websocket error', e)
  })

  websocket.addEventListener('message', ({ data }) => {
    const message = JSON.parse(data)
    onMessage(message)
  })

  function sendMessage(message) {
    websocket.send(JSON.stringify(message))
  }

  return {
    sendMessage,
  }
}
