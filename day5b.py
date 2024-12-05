import string
import re
import copy
import functools
import aocd

data = aocd.get_data(day=5, year=2024)

sample = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

# data = sample

lines = data.splitlines()
rules = []
checks = []

split = True

for line in lines:
    if line.strip() == "":
        split = False
    if split:
        rules.append(line)
    else:
        if line != "":
            checks.append(line)
        
after_dict = {}
before_dict = {}

for rule in rules:
    arr = rule.strip().split("|")
    if arr[0] not in after_dict:
        after_dict[arr[0]] = set()
    after_dict[arr[0]].add(arr[1])
    if arr[1] not in before_dict:
        before_dict[arr[1]] = set()
    before_dict[arr[1]].add(arr[0])

atotal = 0
btotal = 0

def compare(x, y):
    if x in after_dict and y in after_dict[x]:
        return -1
    elif x in before_dict and y in before_dict[x]:
        return 1
    elif y in after_dict and x in after_dict[y]:
        return 1
    elif y in before_dict and x in before_dict[y]:
        return -1
    else:
        return 0
    
def fix_broken(nums):
    fixed = sorted(nums, key=functools.cmp_to_key(compare))
    return fixed


for check in checks:
    print(check)
    nums = check.strip().split(",")
    worked = True
    for idx, num in enumerate(nums):
        if num in after_dict:
            if (set(nums[:idx]) & after_dict[num]) != set():
                worked = False

    if worked:
        atotal += int(nums[(len(nums) -1) // 2])
    else:
        print("fix this one: ", check)
        fixed = fix_broken(nums)
        print("fixed? ", fixed)
        btotal += int(fixed[(len(fixed) -1) // 2])

print(btotal)

print ("bTotal is: ", btotal, "submitting...")
# aocd.submit(btotal, part="b", day=5, year=2024)