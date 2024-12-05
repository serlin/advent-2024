import string
import re
import copy
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

for rule in rules:
    arr = rule.strip().split("|")
    if arr[0] not in after_dict:
        after_dict[arr[0]] = set()
    after_dict[arr[0]].add(arr[1])

print(after_dict)

total = 0

for check in checks:
    print(check)
    nums = check.strip().split(",")
    worked = True
    for idx, num in enumerate(nums):
        # print(num)
        if num in after_dict:
            if (set(nums[:idx]) & after_dict[num]) != set():
                # print(check, "was broken")
                worked = False

    if worked:
        total += int(nums[(len(nums) -1) // 2])


print(total)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="a", day=5, year=2024)