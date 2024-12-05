import std/sets
import std/strutils
import std/sequtils
import std/tables
import std/algorithm

var
  rules: HashSet[string]
  updates: seq[seq[int]]

proc processInput(input_file: string) =
  for line in lines input_file:
    var update: seq[int]
    if '|' in line:
      rules.incl(line.strip)
    elif ',' in line:
      for i in line.strip.split(","):
        update.add(i.parseInt)
      updates.add(update)

processInput("input.txt")

proc pageOrderCorrect(pages: seq[int]): bool =
  for idx, current in pages:
    var new_set: HashSet[string]
    for i in pages[idx + 1..^1]:
      new_set.incl("$1|$2" % [current.intToStr, i.intToStr])
    if len(new_set * rules) != pages.len - idx - 1:
      return false
  return true

proc fixPageOrder(pages: seq[int]): seq[int] =
  var result_table: CountTable[int]
  for page in pages:
    var new_set: HashSet[string]
    for i in pages:
      new_set.incl("$1|$2" % [page.intToStr, i.intToStr])
    result_table[page] = len(new_set * rules)
  result_table.sort(SortOrder.Descending)
  return result_table.keys.toSeq

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
