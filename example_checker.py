"""
An example script to use as a check(expect, answer) function for the Custom Response problem type in the openedx CMS.
The `answer` field is a dictionary of the form:
{
    "provider_A": [The answer Partner A gave for a previous problem],
    "provider_B": [The answer Partner B gave for a previous problem],
    "answer": [The answer for the current problem]
}
"""

import json

def check(expect, answer):
    ans_dict = {}

    try:
        ans_dict = json.loads(answer)
    
        if not isinstance(ans_dict, dict) or "provider_A" not in ans_dict:
            # Not properly formatted or partner hasn't submitted
            raise Exception("Processing answer...")

        ###
        # LOGIC HERE
        ###
        m = float(ans_dict["provider_A"])
        b = float(ans_dict["provider_B"])
        y = float(ans_dict["answer"])

        return y == m*5. + b
    except (ValueError, TypeError) as err:
        # Not passed from server yet
        raise err
