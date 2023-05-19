import random

def format_result(result, data):
    if(result):
        var = random.randint(-5, 5)
        var = data["torque"] + var
        return var