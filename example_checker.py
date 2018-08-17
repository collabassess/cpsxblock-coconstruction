import json

def check(expect, answer):
    try:
        ans_dict = json.loads(answer)

        if not "provider_A" in ans_dict:
            # Not properly formatted
            return False

        ###
        # LOGIC HERE
        ###
        m = float(ans_dict["provider_A"])
		b = float(ans_dict["provider_B"])
		y = float(ans_dict["answer"])

  		return y == m*5. + b
    except (ValueError, TypeError) as err:
        # Not passed from server yet
        return False
