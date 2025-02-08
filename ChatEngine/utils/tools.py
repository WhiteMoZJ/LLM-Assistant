import json
import time

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