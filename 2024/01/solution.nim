import std/sugar
import std/strutils
import std/sequtils
import std/algorithm
import std/sets
import system/iterators

proc readInput(file: string): (seq[int], seq[int]) =
  var k = collect:
    for line in lines file:
      var values: seq[string] = line.splitWhitespace
      (values[0].parseInt, values[1].parseInt)
  return k.unzip

let data = readInput("input.txt")

proc solvePart1(): int =
  var 
    listA: seq[int] = data[0]
    listB: seq[int] = data[1]
  
  listA.sort
  listB.sort
  
  for a in 0..listA.maxIndex:
    result += abs(listA[a] - listB[a])

proc solvePart2(): int =
  let unique: HashSet[int] = data[0].toHashSet * data[1].toHashSet
  for i in unique:
    result += data[0].count(i) * data[1].count(i) * i

echo solvePart1()
echo solvePart2()
