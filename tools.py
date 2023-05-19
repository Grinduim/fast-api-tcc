import random

def format_result(result, data):
    if(result):
        var = random.randint(-2, 2)
        var = data["torque"] + var
        return var