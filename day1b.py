import string
import re
import aocd

data = aocd.get_data(day=1, year=2024)

sample = """3   4
4   3
2   5
1   3
3   9
3   3
"""

# data = sample

list1 = []
list2 = []

for idx, line in enumerate(data.splitlines()):
    list1.append(int(line.split(" ")[0]))
    list2.append(int(line.split(" ")[-1]))

list1.sort()
list2.sort()

total = 0

for idx, num in enumerate(list1):
    total += list1[idx] * list2.count(list1[idx])

print(total)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="b", day=1, year=2024)