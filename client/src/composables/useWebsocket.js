export function useWebsocket(url, onMessage, onClose) {
  const websocket = new WebSocket(url)

  websocket.addEventListener('error', (e) => {
    console.error('Websocket error', e)
  })

  websocket.addEventListener('message', ({ data }) => {
    const message = JSON.parse(data)
    onMessage(message)
  })

  websocket.addEventListener('close', () => {
    onClose?.()
  })

  function sendMessage(message) {
    if (websocket.readyState !== WebSocket.OPEN) {
      return
    }
    websocket.send(JSON.stringify(message))
  }

  function close() {
    websocket.close()
  }

  return {
    sendMessage,
    close,
  }
}
