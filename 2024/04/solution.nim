import std/strutils
import std/algorithm

let 
  grid: seq[string] = readFile("input.txt").splitWhitespace
  width: int = grid[0].len
  height: int = grid.len

proc transposeGrid(grid: seq[string]): seq[string] =
  for x in 0..<width:
    var new_row: string = ""
    for y in 0..<height:
      new_row.add(grid[y][x])
    result.add(new_row)

let grid_t: seq[string] = grid.transposeGrid

proc findDiagonal(x: int, y: int, word: string): int =
  let
    word_list: array[2, string] = [word, word.reversed.join]
  var
    diag_n: string
    diag_i: string
  
  for idx in 0..<word.len:
    diag_n.add(grid[idx + y][idx + x])
    diag_i.add(grid[idx + y][word.len + x - idx - 1])
  
  for w in word_list:
    if w == diag_n:
      result += 1
    if w == diag_i:
      result += 1

proc countWords(word: string): int =
  let reverse_word = word.reversed.join
  for w in [word, reverse_word]:
    for idx in 0..<height:
      result += grid[idx].count(w)
      result += grid_t[idx].count(w)

  for x in 0..width - word.len:
    for y in 0..height - word.len:
      result += findDiagonal(x, y, word)

proc countCrosses(word: string): int =
  for y in 0..height - word.len:
    for x in 0..width - word.len:
      if findDiagonal(x, y, word) == 2:
        result += 1

proc solvePart1(): int =
  return countWords("XMAS")

proc solvePart2(): int =
  return countCrosses("MAS")

echo solvePart1()
echo solvePart2()
