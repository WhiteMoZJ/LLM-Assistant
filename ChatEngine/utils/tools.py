import json
import time
import re

def messages_log(message:dict, response: str) -> dict:
    log_message = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
        "response": response,
        "message": message
    }

    log_file = f"ChatEngine/.log/log-{time.strftime('%Y-%m-%d', time.localtime())}.json"
    with open(log_file, "a") as f:
        json.dump(log_message, f, ensure_ascii=False, indent=4)
    return message

# def sovle_massage(message:str):
#     function_name = None
#     params = None
#     function_name_match = re.search(r'<\|tool▁call▁begin\|>(.*?)<\|tool▁call▁end\|>', message)
#     if function_name_match:
#         function_name = function_name_match.group(1)

#     json_match = re.search(r'(\{.*\})', message)
#     if json_match:
#         json_str = json_match.group(1)
#         params = json.loads(json_str)
    
#     return function_name, params