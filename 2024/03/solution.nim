import std/re
import std/strutils

let data: string = readFile("input.txt")
let regex: Regex = re"(?:(do|don't)\(\)|mul\((\d+),(\d+)\))"

proc processData(dampen: bool): int =
  var 
    match_array: array[3, string]
    bounds: (int, int) = (0, 0)
    enabled: bool = true
  while true:
    bounds = data.findBounds(regex, match_array, start = bounds[1])
    if bounds[0] == -1: return
    case match_array[0]:
      of "do":
        enabled = true
      of "don't":
        enabled = not dampen
      else:
        if enabled:
          result += match_array[1].parseInt * match_array[2].parseInt

proc solvePart1(): int =
  return processData(dampen = false)

proc solvePart2(): int = 
  return processData(dampen = true)

echo solvePart1()
echo solvePart2()