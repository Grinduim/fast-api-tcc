import random

def format_result(result, data):
    if(result):
        var = random.randint(-10, 10)
        var = data["torque"] + var
        return var