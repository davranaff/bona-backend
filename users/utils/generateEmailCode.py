import random


def generateEmailCode(max_length=6):
    code = ""
    for _ in range(max_length):
        code += str(random.randint(0, 9))
    return int(code)
