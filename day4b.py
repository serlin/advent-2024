import string
import re
import copy
import aocd

data = aocd.get_data(day=4, year=2024)

sample = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""
rx = 'mul\\(\\d+,\\d+\\)'

# data = sample

oldlines = data.splitlines()
str_len = len(oldlines[0]) + 6
cheatlines = []
pad = "+" * str_len

# Pad it so that I don't have to deal with edges.
for line in oldlines:
    out = "+++" + line + "+++"
    cheatlines.append(out)

cheatlines.append(pad)
cheatlines.append(pad)
cheatlines.append(pad)
cheatlines.insert(0, pad)
cheatlines.insert(0, pad)
cheatlines.insert(0, pad)

lines = cheatlines


def count_loc(m, n):
    built_str = ""
    count = 0
    if lines[m][n] != "A":
        return 0
    # What 4 surround.
    bs = lines[m-1][n-1] + lines[m-1][n+1] + lines[m+1][n+1] + lines[m+1][n-1]
    # Some iteration of MSSM works 
    if bs == "MSSM" or bs == "MMSS" or bs == "SMMS" or bs == "SSMM":
        count += 1
    return count

total = 0
for m in range(3, 3 + str_len - 6):
    for n in range(3, 3 + str_len - 6):
        total += count_loc(m, n)

print(total)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="b", day=4, year=2024)