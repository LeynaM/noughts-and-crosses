// Every line that wins a game, as [row, col] triples ordered end to end.
const LINES = [
  [[0, 0], [0, 1], [0, 2]],
  [[1, 0], [1, 1], [1, 2]],
  [[2, 0], [2, 1], [2, 2]],
  [[0, 0], [1, 0], [2, 0]],
  [[0, 1], [1, 1], [2, 1]],
  [[0, 2], [1, 2], [2, 2]],
  [[0, 0], [1, 1], [2, 2]],
  [[0, 2], [1, 1], [2, 0]],
]

// A single move can complete two lines at once, so this returns every match.
export function findWinningLines(board) {
  return LINES.filter(([[r1, c1], [r2, c2], [r3, c3]]) => {
    const value = board[r1][c1]
    return value && value === board[r2][c2] && value === board[r3][c3]
  })
}

export function isInLines(lines, row, col) {
  return lines.some(line => line.some(([r, c]) => r === row && c === col))
}
