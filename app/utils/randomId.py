import random


def randomId(max_length=10):
    code = ""
    for _ in range(max_length):
        code += str(random.randint(0, 9))
    return int(code)
