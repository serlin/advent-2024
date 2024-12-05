import string
import re
import copy
import aocd

data = aocd.get_data(day=2, year=2024)

sample = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

# data = sample

reports = []
reportdiffs = []

def is_safe(arr):
    diffs = []
    for i in range(0, len(arr) - 1 ):
        diffs.append(arr[i+1] - arr[i])
    if 0 in diffs:
        print("unsafe")
        return(False)
    elif max(diffs) > 0 and min(diffs) < 0:
        print("unsafe")
        return(False)
    elif max(diffs) > 3 or min(diffs) < -3:
        print("unsafe")
        return(False)
    elif max(diffs) <= 3 and min(diffs) >= -3:
        print("safe")
        return(True)
    else:
        print("huh?")

def can_be_safe(arr):
    for i in range(0, len(arr)):
        check = copy.copy(arr)
        check.pop(i)
        if is_safe(check):
            return(True)
            

for idx, line in enumerate(data.splitlines()):
    levs = [int(x) for x in line.split(" ") if x]
    reports.append(levs)

total = 0
for rep in reports:
    if is_safe(rep):
        total += 1
    elif can_be_safe(rep):
        total +=1
    else:
        print("unsafe")


print(total)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="b", day=2, year=2024)