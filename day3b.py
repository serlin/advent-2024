import string
import re
import copy
import aocd

data = aocd.get_data(day=3, year=2024)

sample = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"
rx = "(?:mul\\(\\d+,\\d+\\))|(?:don\'t\\(\\))|(?:do\\(\\))"

# data = sample

total = 0

res = re.findall(rx, data)

print(res)

enable = True
for match in res:
    print(match)
    if match == "don\'t()":
        print("turn off")
        enable = False
    elif match == "do()":
        print("turn on")
        enable = True
    else:
        if enable:
            nums = re.findall("\\d+", match)
            total += int(nums[0]) * int(nums[1])

print(total)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="b", day=3, year=2024)