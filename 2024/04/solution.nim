import std/strutils
import std/algorithm

let 
  grid: seq[string] = readFile("input.txt").splitWhitespace
  height: int = grid.len

proc transposeGrid(grid: seq[string]): seq[string] =
  var new_row: string
  for x in 0..<height:
    new_row = ""
    for y in 0..<height:
      new_row.add(grid[y][x])
    result.add(new_row)

let grid_t: seq[string] = grid.transposeGrid

proc findDiagonal(x: int, y: int, word: string): int =
  var
    diag_n: string
    diag_i: string
  
  for idx in 0..<word.len:
    diag_n.add(grid[idx + y][idx + x])
    diag_i.add(grid[idx + y][word.len + x - idx - 1])
  
  for w in [word, word.reversed.join]:
    if w == diag_n:
      result += 1
    if w == diag_i:
      result += 1

proc countWords(word: string): int =
  for w in [word, word.reversed.join]:
    for idx in 0..<height:
      result += grid[idx].count(w)
      result += grid_t[idx].count(w)

  for x in 0..height - word.len:
    for y in 0..height - word.len:
      result += findDiagonal(x, y, word)

proc countCrosses(word: string): int =
  for y in 0..height - word.len:
    for x in 0..height - word.len:
      if findDiagonal(x, y, word) == 2:
        result += 1

proc solvePart1(): int =
  return countWords("XMAS")

proc solvePart2(): int =
  return countCrosses("MAS")

echo solvePart1()
echo solvePart2()
