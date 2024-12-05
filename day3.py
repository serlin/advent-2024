import string
import re
import copy
import aocd

data = aocd.get_data(day=3, year=2024)

sample = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
rx = 'mul\\(\\d+,\\d+\\)'

# data = sample

total = 0

res = re.findall(rx, data)

for match in res:
    nums = re.findall("\\d+", match)
    total += int(nums[0]) * int(nums[1])
    print(match)

print(total)

print ("Total is: ", total, "submitting...")
aocd.submit(total, part="a", day=3, year=2024)