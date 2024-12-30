import string
import re
import copy
import functools
import itertools
from functools import cache
import aocd
from math import isclose

data = aocd.get_data(day=17, year=2024)

sample = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

sample2 = """Register A: 729
Register B: 0
Register C: 9

Program: 2,6
"""

sample3 = """Register A: 10
Register B: 0
Register C: 0

Program: 5,0,5,1,5,4
"""

sample4 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

sample5 = """Register A: 2024
Register B: 29
Register C: 0

Program: 1,7
"""

sample6 = """Register A: 2024
Register B: 2024
Register C: 43690

Program: 4,0
"""

sample7 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

problem = """Register A: 23999685
Register B: 0
Register C: 0

Program: 2,4,1,1,7,5,1,5,0,3,4,4,5,5,3,0
"""

# 2,4 - A % 8 -> B
# 1,1 - B XOR 00000001 -> B
# 7,5 - A // 2^B > C
# 1,5 - B XOR 00000101 -> B
# 0,3 - A // 8 -> A
# 4,4 - B XOR C -> B
# 5,5 - B % 8 -> OUT
# 3,0 - JNZ -> 0



# data = sample7
lines = data.splitlines()
register_a = 0
register_b = 0
register_c = 0

instruction_pointer = 0

program_arr = []
output_buffer = []

for line in lines:
    nums = re.findall("\\d+", line)
    if line.startswith("Register A:"):
        register_a = int(nums[0])
    elif line.startswith("Register B:"):
        register_b = int(nums[0])
    elif line.startswith("Register C:"):
        register_c = int(nums[0])
    elif line.startswith("Program:"):
        for n in nums:
            program_arr.append(int(n))

orig_program_arr = program_arr

def print_computer_state():
    print("A: ", register_a, " B: ", register_b, " C: ", register_c)
    print("Program: ", program_arr)
    print("Output: ", output_buffer)

def translate_combo(oper):
    global register_a
    global register_b
    global register_c
    if oper <= 3:
        return oper
    elif oper == 4:
        return register_a
    elif oper == 5:
        return register_b
    elif oper == 6:
        return register_c

def adv(oper): # op-code 0
    global register_a
    global register_b
    global register_c

    register_a = register_a // pow(2, translate_combo(oper))

def bxl(oper): #opcode 1
    global register_b
    register_b = register_b ^ oper

def bst(oper): #opcode 2
    global register_b
    register_b = translate_combo(oper) % 8

def jnz(oper): #opcode 3
    global instruction_pointer

    if register_a == 0:
        instruction_pointer += 2
    else:
        instruction_pointer = oper
        # We'll need to prevent the IP from incrementing

def bxc(oper): #opcode 4
    global register_b
    register_b = register_b ^ register_c

def out(oper): #opcode 5
    global output_buffer
    output_buffer.append(translate_combo(oper) % 8)

def bdv(oper): #opcode 6
    global register_a
    global register_b
    global register_c

    register_b = register_a // pow(2, translate_combo(oper))
    
def cdv(oper): #opcode 6
    global register_a
    global register_b
    global register_c

    register_c = register_a // pow(2, translate_combo(oper))

print_computer_state()

adv(5)

print_computer_state()
# for n in range(1000000000, 2000000000):
#     register_a = n
#     output_buffer = []
#     instruction_pointer = 0
#     register_b = 0
#     register_c = 0
for i in range(0, 1000):
    # print("Step: ", i)
    if instruction_pointer >= len(program_arr):
        break
    opcode = program_arr[instruction_pointer]
    operand = program_arr[instruction_pointer + 1]
    # print("Opcode: ", opcode, " operand: ", operand)
    match opcode:
        case 0:
            adv(operand)
            instruction_pointer += 2
        case 1:
            bxl(operand)
            instruction_pointer += 2       
        case 2:
            bst(operand)
            instruction_pointer += 2       
        case 3:
            jnz(operand)
            # instruction_pointer += 2       
        case 4:
            bxc(operand)
            instruction_pointer += 2       
        case 5:
            out(operand)
            instruction_pointer += 2       
        case 6:
            bdv(operand)
            instruction_pointer += 2       
        case 7:
            cdv(operand)
            instruction_pointer += 2   
    # if output_buffer == orig_program_arr:
    #     print("Found it at: ", n)
    #     # print_computer_state()    

# print(",".join(output_buffer))

# total = 0
# print ("Total is: ", total, "submitting...")
# aocd.submit(total, part="a", day=17, year=2024)
