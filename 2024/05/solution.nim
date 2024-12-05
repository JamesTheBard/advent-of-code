import std/strutils
import std/sequtils
import std/tables
import std/algorithm

var
  rules: Table[int, seq[int]]
  updates: seq[seq[int]]

proc processInput(input_file: string) =
  for line in lines input_file:
    var update: seq[int]
    if '|' in line:
      let a: seq[string] = line.strip.split("|")
      if not rules.contains(a[0].parseInt):
        rules[a[0].parseInt] = @[a[1].parseInt]
      else:
        rules[a[0].parseInt].add(a[1].parseInt)
    elif ',' in line:
      for i in line.strip.split(","):
        update.add(i.parseInt)
      updates.add(update)

processInput("input.txt")

proc pageOrderCorrect(pages: seq[int]): bool =
  for idx, page in pages:
    for p in pages[idx + 1..^1]:
      if not rules[page].contains(p):
        return false
  return true 

proc fixPageOrder(pages: seq[int]): seq[int] =
  var total_count: CountTable[int]
  for page in pages:
    for p in pages:
      if rules[page].contains(p):
        total_count.inc(page)
        break
  total_count.sort(SortOrder.Descending)
  return total_count.keys.toSeq

proc solvePart1(): int =
  for update in updates:
    if pageOrderCorrect(update):
      result += update[update.len /% 2]

proc solvePart2(): int =
  for update in updates:
    if not pageOrderCorrect(update):
      result += update.fixPageOrder[update.len /% 2]

echo solvePart1()
echo solvePart2()
