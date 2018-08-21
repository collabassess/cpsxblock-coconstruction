import json

def check(expect, answer):
    ans_dict = {}

    try:
        ans_dict = json.loads(answer)
    except (TypeError, ValueError) as err:
        return False

    if "provider_A" not in ans_dict:
        # Not properly formatted
        return False
    
    try:
        ###
        # LOGIC HERE
        ###
        m = float(ans_dict["provider_A"])
        b = float(ans_dict["provider_B"])
        y = float(ans_dict["answer"])

        return y == m*5. + b
    except TypeError as err:
        # Not passed from server yet
        raise err
